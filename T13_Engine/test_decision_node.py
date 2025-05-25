import unittest
from decision_node import rank_options

class TestDecisionNode(unittest.TestCase):
    def test_rank_options_energy_continue(self):
        options = ["ادامه پروژه", "استراحت", "تعویق"]
        emo_score = {"stress": 3, "energy": 8, "hope": 6}
        best, ranked = rank_options(options, emo_score, goal="پیشرفت")
        self.assertEqual(best["option"], "ادامه پروژه")
        self.assertGreaterEqual(best["score"], 25)
        self.assertIn("انرژی بالاست", " ".join(best["why"]))

    def test_rank_options_stress_rest(self):
        options = ["ادامه پروژه", "استراحت", "تعویق"]
        emo_score = {"stress": 8, "energy": 5, "hope": 7}
        best, ranked = rank_options(options, emo_score, goal="پیشرفت")
        self.assertEqual(best["option"], "استراحت")
        self.assertIn("استرس بالا", " ".join(best["why"]))

    def test_rank_options_hope_delay(self):
        options = ["ادامه پروژه", "استراحت", "تعویق"]
        emo_score = {"stress": 2, "energy": 4, "hope": 3}
        best, ranked = rank_options(options, emo_score, goal="پیشرفت")
        self.assertEqual(best["option"], "تعویق")
        self.assertIn("امید کم", " ".join(best["why"]))

    def test_no_options(self):
        best, ranked = rank_options([], {"stress": 5, "energy": 5, "hope": 5}, goal="پیشرفت")
        self.assertIsNone(best["option"])
        self.assertIn("هیچ گزینه‌ای یافت نشد", " ".join(best["why"]))

if __name__ == "__main__":
    unittest.main()
