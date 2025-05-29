import unittest
import os
from T13_Engine import self_upgrade_engine

class TestSelfUpgradeEngine(unittest.TestCase):
    def test_self_read_and_suggest_rule_based(self):
        # حالت rule-based باید همیشه لیست پیشنهاد برگرداند (حتی اگر خالی باشد)
        suggestions = self_upgrade_engine.self_read_and_suggest(smart_mode=False)
        self.assertIsInstance(suggestions, list)

    def test_self_read_and_suggest_smart_mode_api_fail(self):
        # اگر API فعال نباشد، باید graceful fail کند و لیست پیشنهاد برگرداند
        suggestions = self_upgrade_engine.self_read_and_suggest(smart_mode=True, ai_api_url="http://localhost:8000/ai/analyze")
        self.assertIsInstance(suggestions, list)

    def test_auto_apply_suggestions_no_crash(self):
        # تابع باید حتی با ورودی خالی crash نکند
        result = self_upgrade_engine.auto_apply_suggestions([])
        self.assertIsInstance(result, list)

if __name__ == "__main__":
    unittest.main()
