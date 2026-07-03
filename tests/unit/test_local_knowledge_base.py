import unittest
import os
import tempfile
import json
import shutil
from shared.knowledge.local_knowledge_base import LocalKnowledgeBase


class TestKnowledgeAndRulesFoundation(unittest.TestCase):
    def setUp(self):
        # Create temp dirs for profiles and rules
        self.test_dir = tempfile.mkdtemp()
        self.profiles_dir = os.path.join(self.test_dir, "business_profiles")
        self.rules_dir = os.path.join(self.test_dir, "rules")

        os.makedirs(self.profiles_dir)
        os.makedirs(os.path.join(self.rules_dir, "finance"))

        # Write dummy profile
        with open(os.path.join(self.profiles_dir, "base.json"), "w") as f:
            json.dump({"id": "base", "name": "Base", "attributes": {"base_val": 1}}, f)

        with open(os.path.join(self.profiles_dir, "child.json"), "w") as f:
            json.dump(
                {
                    "id": "child",
                    "name": "Child",
                    "parent_id": "base",
                    "attributes": {"child_val": 2},
                },
                f,
            )

        # Write dummy rule
        with open(os.path.join(self.rules_dir, "finance", "global.json"), "w") as f:
            json.dump(
                {
                    "id": "global_finance",
                    "priority": "GLOBAL_DEFAULT",
                    "rules": {"margin": 0.2},
                },
                f,
            )

        with open(os.path.join(self.rules_dir, "finance", "industry.json"), "w") as f:
            json.dump(
                {
                    "id": "child",
                    "priority": "INDUSTRY_DEFAULT",
                    "rules": {"margin": 0.3},
                },
                f,
            )

        self.lkb = LocalKnowledgeBase(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_profile_inheritance(self):
        child = self.lkb.get_business_profile("child")
        self.assertIsNotNone(child)
        self.assertEqual(child.attributes.get("base_val"), 1)
        self.assertEqual(child.attributes.get("child_val"), 2)

    def test_rule_priority(self):
        # INDUSTRY_DEFAULT (4) should override GLOBAL_DEFAULT (5)
        # Wait, the enum sets User_Override to 1 and Global to 5.
        # But my logic in rule engine applies them from 5 down to 1.
        # So 4 is applied after 5, overriding it.
        rules = self.lkb.get_active_rules("child", None)
        self.assertEqual(rules.active_rules.get("margin"), 0.3)


if __name__ == "__main__":
    unittest.main()
