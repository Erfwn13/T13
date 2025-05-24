import unittest
from T13_Engine.multiverse_core import ScenarioBuilder, MultiProjectSync, CreativityPulse, MultiverseCore, WorldBuilder

class TestMultiverseCore(unittest.TestCase):
    def test_scenario_builder(self):
        result = ScenarioBuilder("آینده هوش مصنوعی")
        self.assertIn("دنیاسازی", result)
        self.assertIn("آینده هوش مصنوعی", result)

    def test_multi_project_sync(self):
        projects = [
            {"title": "AI Core", "status": "در حال توسعه"},
            {"title": "Story Engine", "status": "تکمیل"}
        ]
        output = MultiProjectSync(projects)
        self.assertIn("AI Core", output)
        self.assertIn("Story Engine", output)

    def test_creativity_pulse(self):
        idea = CreativityPulse("AI")
        self.assertIn("ایده خلاقانه", idea)

    def test_multiverse_core_generate_idea(self):
        core = MultiverseCore()
        idea = core.generate_idea()
        self.assertIsInstance(idea, str)
        self.assertTrue(len(idea) > 0)

    def test_world_builder(self):
        builder = WorldBuilder()
        world = builder.create_world("علمی-تخیلی", 5)
        self.assertEqual(world["theme"], "علمی-تخیلی")
        self.assertEqual(world["complexity"], 5)
        self.assertIn("ایجاد شد", world["details"])
        worlds = builder.list_worlds()
        self.assertEqual(len(worlds), 1)
        self.assertEqual(worlds[0]["theme"], "علمی-تخیلی")

if __name__ == "__main__":
    unittest.main()
