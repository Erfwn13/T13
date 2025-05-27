import unittest

from memory_core import MemoryManager


class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = MemoryManager()

    def test_add_and_get_fact(self):
        self.manager.add_fact("test_key", "test_value")
        self.assertEqual(self.manager.get_fact("test_key"), "test_value")

    def test_get_fact_not_found(self):
        self.assertEqual(self.manager.get_fact("unknown"), "اطلاعاتی یافت نشد.")

    def test_clean_memory(self):
        self.manager.add_fact("a", "old_data")
        self.manager.add_fact("b", "new_data")
        self.manager.clean_memory()
        self.assertNotIn("a", self.manager.memory)
        self.assertIn("b", self.manager.memory)


if __name__ == "__main__":
    unittest.main()
