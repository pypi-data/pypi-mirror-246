"""Simple selection and loc-style accessor which automatically translates PRIMAP2 short
column names to the actual long names including the categorization."""
import functools
import inspect
import typing

import xarray as xr

from . import _accessor_base
from ._types import DimOrDimsT, FunctionT, KeyT


class DimensionNotExistingError(ValueError):
    def __init__(self, dim):
        super().__init__(f"Dimension {dim!r} does not exist.")


def translate(item: KeyT, translations: typing.Mapping[typing.Hashable, str]) -> KeyT:
    if isinstance(item, str):
        if item in translations:
            return translations[item]
        else:
            return item
    else:
        sel: dict[typing.Hashable, typing.Hashable] = {}
        for key in item:
            if key in translations:
                sel[translations[key]] = item[key]
            else:
                sel[key] = item[key]
        return sel


def translations_from_attrs(
    attrs: dict[typing.Hashable, typing.Any], include_entity=False
) -> dict[typing.Hashable, str]:
    ret: dict[typing.Hashable, str] = {}
    for key, abbrev in [("category", "cat"), ("scenario", "scen"), ("area", "area")]:
        if abbrev in attrs:
            ret[key] = attrs[abbrev]
            ret[abbrev] = attrs[abbrev]
    if "sec_cats" in attrs:
        for full_name in attrs["sec_cats"]:
            key = full_name.split("(")[0][:-1]
            ret[key] = full_name

    if include_entity and "entity_terminology" in attrs:
        ret["entity"] = f"entity ({attrs['entity_terminology']})"
    return ret


def translations_from_dims(
    dims: typing.Iterable[typing.Hashable],
) -> dict[typing.Hashable, str]:
    ret: dict[typing.Hashable, str] = {}
    for dim in dims:
        if isinstance(dim, str) and " (" in dim:
            key: str = dim.split("(")[0][:-1]
            ret[key] = dim
    if "scenario" in ret:
        ret["scen"] = ret["scenario"]
    if "category" in ret:
        ret["cat"] = ret["category"]
    return ret


def alias(
    dim: DimOrDimsT,
    translations: dict[typing.Hashable, str],
    dims: typing.Iterable[typing.Hashable],
) -> DimOrDimsT:
    if isinstance(dim, str):
        dim = translations.get(dim, dim)
        if dim not in dims:
            raise DimensionNotExistingError(dim)
        return dim
    else:
        try:
            return [alias(idim, translations, dims) for idim in dim]
        except TypeError:  # not iterable, so some other hashable like int
            if dim not in dims:
                raise DimensionNotExistingError(dim) from None
            return dim


def alias_dims(
    args_to_alias: typing.Iterable[str],
    wraps: typing.Optional[typing.Callable] = None,
    additional_allowed_values: typing.Iterable[str] = (),
) -> typing.Callable[[FunctionT], FunctionT]:
    """Method decorator to automatically translate dimension aliases in parameters.

    Use like this:
    @alias_dims(["dim"])
    def sum(self, dim):
        return self._da.sum(dim)

    To copy the documentation etc. from an xarray function, use the wraps parameter:
    @alias_dims(["dim"], wraps=xr.DataArray.sum)
    def sum(self, *args, **kwargs):
        return self._da.sum(*args, **kwargs)
    """

    def decorator(func: FunctionT) -> FunctionT:
        if wraps is not None:
            wrap_func = wraps
        else:
            wrap_func = func

        # the parameters of the wrapped function without self
        func_args_list = list(inspect.signature(wrap_func).parameters.values())[1:]

        @functools.wraps(wrap_func)
        def wrapper(self, *args, **kwargs):
            try:
                obj = self._da
            except AttributeError:
                obj = self._ds
            translations = obj.pr.dim_alias_translations
            dims = set(obj.dims).union(set(additional_allowed_values))

            # translate kwargs
            for arg_to_alias in args_to_alias:
                if arg_to_alias in kwargs and kwargs[arg_to_alias] is not None:
                    kwargs[arg_to_alias] = alias(
                        kwargs[arg_to_alias], translations, dims
                    )

            # translate args
            args_translated = []
            for i, arg in enumerate(args):
                try:
                    translate_arg = func_args_list[i].name in args_to_alias
                except IndexError:  # more arguments given than function has
                    # translate if function has an *args-style parameter which should
                    # be translated
                    translate_arg = (
                        len(func_args_list) > 0
                        and func_args_list[-1].kind == inspect.Parameter.VAR_POSITIONAL
                        and func_args_list[-1].name in args_to_alias
                    )

                if translate_arg:
                    args_translated.append(alias(arg, translations, dims))
                else:
                    args_translated.append(arg)

            return func(self, *args_translated, **kwargs)

        return wrapper

    return decorator


class DataArrayAliasLocIndexer:
    """Provides loc-style selection with aliases. Needs to be a separate class for
    __getitem__ and __setitem__ functionality, which doesn't work directly on properties
    without an intermediate object."""

    __slots__ = ("_da",)

    def __init__(self, da: xr.DataArray):
        self._da = da

    def __getitem__(
        self, item: typing.Mapping[typing.Hashable, typing.Any]
    ) -> xr.DataArray:
        return self._da.loc[translate(item, self._da.pr.dim_alias_translations)]

    def __setitem__(self, key: typing.Mapping[typing.Hashable, typing.Any], value):
        self._da.loc.__setitem__(
            translate(key, self._da.pr.dim_alias_translations), value
        )


class DataArrayAliasSelectionAccessor(_accessor_base.BaseDataArrayAccessor):
    @property
    def dim_alias_translations(self) -> dict[typing.Hashable, str]:
        """Translate a shortened dimension alias to a full dimension name.

        For example, if the full dimension name is ``area (ISO3)``, the alias ``area``
        is mapped to ``area (ISO3)``.

        Returns
        -------
        translations : dict
            A mapping of all dimension aliases to full dimension names.
        """
        # we have to do string parsing because the Dataset's attrs are not available
        # in the DataArray context
        return translations_from_dims(self._da.dims)

    @property
    def loc(self):
        """Attribute for location-based indexing like xr.DataArray.loc, but also
        supports short aliases like ``area`` and translates them into the long
        names including the corresponding category-set."""
        return DataArrayAliasLocIndexer(self._da)

    def __getitem__(self, item: typing.Hashable) -> xr.DataArray:
        """Like da[], but translates short aliases like "area" into the long names
        including the corresponding category-set."""
        return self._da[self.dim_alias_translations.get(item, item)]


class DatasetAliasLocIndexer:
    """Provides loc-style selection with aliases. Needs to be a separate class for
    __getitem__ functionality, which doesn't work directly on properties without an
    intermediate object."""

    __slots__ = ("_ds",)

    def __init__(self, ds: xr.Dataset):
        self._ds = ds

    def __getitem__(
        self, item: typing.Mapping[typing.Hashable, typing.Any]
    ) -> xr.Dataset:
        return self._ds.loc[translate(item, self._ds.pr.dim_alias_translations)]


class DatasetAliasSelectionAccessor(_accessor_base.BaseDatasetAccessor):
    @property
    def dim_alias_translations(self) -> dict[typing.Hashable, str]:
        """Translate a shortened dimension alias to a full dimension name.

        For example, if the full dimension name is ``area (ISO3)``, the alias ``area``
        is mapped to ``area (ISO3)``.

        Returns
        -------
        translations : dict
            A mapping of all dimension aliases to full dimension names.
        """
        # First guess aliases from the names themselves. The meta data in attrs
        # is used to overwrite the guessed values where they are available
        ret = translations_from_dims(self._ds.dims)
        ret.update(translations_from_attrs(self._ds.attrs))
        return ret

    @typing.overload
    def __getitem__(self, item: str) -> xr.DataArray:
        ...

    @typing.overload
    def __getitem__(self, item: typing.Mapping[str, typing.Any]) -> xr.Dataset:
        ...

    def __getitem__(self, item):
        """Like ds[], but translates short aliases like "area" into the long names
        including the corresponding category-set."""
        return self._ds[translate(item, self.dim_alias_translations)]

    @property
    def loc(self):
        """Attribute for location-based indexing like xr.Dataset.loc, but also
        supports short aliases like ``area`` and translates them into the long
        names including the corresponding category-set."""
        return DatasetAliasLocIndexer(self._ds)
