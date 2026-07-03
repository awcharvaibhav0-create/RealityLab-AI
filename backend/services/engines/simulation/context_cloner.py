import copy
from .models import ScenarioContext


class ContextCloner:
    @staticmethod
    def clone(base_ctx):
        new_ctx = ScenarioContext()
        new_ctx.variables = copy.deepcopy(base_ctx.variables)
        return new_ctx

    @staticmethod
    def merge(base_ctx, override_ctx):
        def deep_merge(d1, d2):
            res = copy.deepcopy(d1)
            for k, v in d2.items():
                if k in res and isinstance(res[k], dict) and isinstance(v, dict):
                    res[k] = deep_merge(res[k], v)
                else:
                    res[k] = copy.deepcopy(v)
            return res

        merged_ctx = ScenarioContext()
        merged_ctx.variables = deep_merge(base_ctx.variables, override_ctx.variables)
        return merged_ctx
