import unittest

from backend.services.engines.simulation.models import ScenarioContext
from backend.services.engines.simulation.context_cloner import ContextCloner


class TestContextCloner(unittest.TestCase):
    def test_clone_isolation(self):
        base_ctx = ScenarioContext()
        base_ctx.variables["nested"] = {"a": 1}

        cloned_ctx = ContextCloner.clone(base_ctx)

        # Modify clone
        cloned_ctx.variables["nested"]["a"] = 2
        cloned_ctx.variables["new_key"] = "test"

        # Ensure base is unchanged
        self.assertEqual(base_ctx.variables["nested"]["a"], 1)
        self.assertNotIn("new_key", base_ctx.variables)

    def test_merge_contexts(self):
        base_ctx = ScenarioContext()
        base_ctx.variables = {"shared": 1, "nested": {"keep": True, "override": False}}

        override_ctx = ScenarioContext()
        override_ctx.variables = {
            "shared": 2,
            "new_var": True,
            "nested": {"override": True},
        }

        merged_ctx = ContextCloner.merge(base_ctx, override_ctx)

        self.assertEqual(merged_ctx.variables["shared"], 2)
        self.assertEqual(merged_ctx.variables["new_var"], True)
        self.assertEqual(merged_ctx.variables["nested"]["keep"], True)
        self.assertEqual(merged_ctx.variables["nested"]["override"], True)

        # Ensure originals are unchanged
        self.assertEqual(base_ctx.variables["shared"], 1)
        self.assertEqual(base_ctx.variables["nested"]["override"], False)
