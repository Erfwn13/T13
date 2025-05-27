import unittest

from behavior_manager import generate_response, get_behavior_mode


class TestBehaviorManager(unittest.TestCase):
    def test_get_behavior_mode(self):
        self.assertEqual(
            get_behavior_mode({"joy": 5, "stress": 9, "energy": 5}), "SafeSupport"
        )
        self.assertEqual(
            get_behavior_mode({"joy": 8, "stress": 3, "energy": 8}), "ShadowBoost"
        )
        self.assertEqual(
            get_behavior_mode({"joy": 4, "stress": 2, "energy": 3}), "ChillCompanion"
        )
        self.assertEqual(
            get_behavior_mode({"joy": 5, "stress": 5, "energy": 5}), "ChaosSpark"
        )

    def test_generate_response(self):
        msg = "پیشرفت خوبی داشتی!"
        self.assertIn("محافظ", generate_response("SafeSupport", msg))
        self.assertIn("مضاعف", generate_response("ShadowBoost", msg))
        self.assertIn("آروم", generate_response("ChillCompanion", msg))
        self.assertIn("خلاقیت", generate_response("ChaosSpark", msg))
        self.assertIn("پیش‌فرض", generate_response("OtherMode", msg))


if __name__ == "__main__":
    unittest.main()
