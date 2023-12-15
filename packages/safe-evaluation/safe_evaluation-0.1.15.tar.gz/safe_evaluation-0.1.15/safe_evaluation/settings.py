from safe_evaluation.constants import ALLOWED_FUNCS, NUMPY_ALLOWED_FUNCS


class Settings:
    def __init__(
            self, *,
            allowed_funcs: list = ALLOWED_FUNCS.keys(),
            numpy_allowed_funcs: list = NUMPY_ALLOWED_FUNCS,
            forbidden_funcs: list = [],
            df_startswith: str = '$',
            df_regex: str = r'\${[^\{\}]+}',
            df_name: str = '__df'
    ):
        self.numpy_allowed_funcs = numpy_allowed_funcs
        self.allowed_funcs = allowed_funcs
        self.forbidden_funcs = forbidden_funcs
        self.df_startswith = df_startswith
        self.df_regex = df_regex
        self.df_name = df_name

    def _check_allowed_func(self, func_name: str):
        is_numpy_pandas = func_name.startswith(tuple(self.numpy_allowed_funcs))
        return func_name in self.allowed_funcs or is_numpy_pandas

    def _check_forbidden_func(self, func_name: str):
        return func_name not in self.forbidden_funcs

    def is_available(self, func_name: str):
        return self._check_allowed_func(func_name=func_name) and \
               self._check_forbidden_func(func_name=func_name)
