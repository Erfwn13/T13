import unittest
from datetime import datetime
from T13_Engine.emotion_stack import EmotionStack, analyze_emotion, adaptive_reaction

class TestEmotionStack(unittest.TestCase):
    def test_add_and_get_recent_emotions(self):
        stack = EmotionStack(max_size=3)
        stack.add_emotion('joy', 8)
        stack.add_emotion('stress', 2)
        stack.add_emotion('hope', 7)
        stack.add_emotion('fear', 4)
        recent = stack.get_recent_emotions(2)
        self.assertEqual(len(recent), 2)
        self.assertEqual(recent[-1]['emotion'], 'fear')
        self.assertEqual(recent[-2]['emotion'], 'hope')

    def test_analyze_emotion(self):
        input_data = {'joy': 9, 'stress': 3, 'hope': 8, 'fear': 2, 'energy': 7}
        result = analyze_emotion(input_data)
        self.assertEqual(result['joy'], 9)
        self.assertEqual(result['stress'], 3)
        self.assertIn('timestamp', result)

    def test_adaptive_reaction(self):
        high_stress = {'joy': 5, 'stress': 8, 'hope': 5, 'fear': 5, 'energy': 5}
        self.assertIn('پرتنش', adaptive_reaction(high_stress))
        high_joy = {'joy': 9, 'stress': 2, 'hope': 7, 'fear': 2, 'energy': 9}
        self.assertIn('اوجه', adaptive_reaction(high_joy))
        low_hope = {'joy': 5, 'stress': 5, 'hope': 3, 'fear': 5, 'energy': 5}
        self.assertIn('امید پایین', adaptive_reaction(low_hope))
        stable = {'joy': 5, 'stress': 5, 'hope': 5, 'fear': 5, 'energy': 5}
        self.assertIn('پایدار', adaptive_reaction(stable))

if __name__ == '__main__':
    unittest.main()
