import unittest
from interaction_module import TextInteraction

class TestTextInteraction(unittest.TestCase):
    def setUp(self):
        self.interaction = TextInteraction()

    def test_auto_learn(self):
        response = self.interaction.auto_learn("Python is awesome")
        self.assertIn("یاد گرفتم", response)
        self.assertEqual(self.interaction.memory.get("python"), "awesome")

    def test_auto_learn_no_pattern(self):
        response = self.interaction.auto_learn("سلام خوبی؟")
        self.assertIsNone(response)

    def test_learn_and_memory(self):
        self.interaction.learn("ai", "هوش مصنوعی")
        self.assertEqual(self.interaction.memory["ai"], "هوش مصنوعی")

if __name__ == "__main__":
    unittest.main()
