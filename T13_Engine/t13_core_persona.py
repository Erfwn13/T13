# t13_core_persona.py

import random
import time

from echo_engine import echo_response


class T13Persona:
    def __init__(self, core_ai):
        self.core_ai = core_ai
        self.mood = "neutral"  # default mood
        self.energy_level = 5  # scale from 1 (low) to 10 (high)

    def set_mood(self, emotion_score):
        """Determine mood based on emotion score."""
        if emotion_score["joy"] > 7:
            self.mood = "happy"
        elif emotion_score["stress"] > 7:
            self.mood = "stressed"
        elif emotion_score["energy"] > 7:
            self.mood = "energized"
        else:
            self.mood = "neutral"

    def adapt_response(self):
        """Generate emotional echo response based on mood and energy."""
        message = "You’ve got this. Let’s move forward."
        return echo_response(self.mood_to_mode(), message, self.energy_level)

    def mood_to_mode(self):
        """Map mood to behavior mode."""
        mapping = {
            "happy": "ChillCompanion",
            "energized": "ShadowBoost",
            "stressed": "SafeSupport",
            "neutral": "SafeSupport",
        }
        return mapping.get(self.mood, "SafeSupport")

    def determine_auto_action(self, emotion_score):
        """Decide on the best course of action based on the emotional state."""
        self.set_mood(emotion_score)
        if self.mood == "stressed":
            return "SafeSupport"  # Choose calm, protective behavior
        elif self.mood == "energized":
            return "ShadowBoost"  # Choose energetic, motivating behavior
        elif self.mood == "happy":
            return "ChillCompanion"  # Choose friendly, relaxed behavior
        else:
            return "NeutralAction"  # Default to a balanced approach

    def update_energy(self, energy):
        """Update energy level and decide on the auto-action."""
        self.energy_level = energy
        if self.energy_level > 8:
            return "ChaosSpark"  # When highly energized, go for creativity
        elif self.energy_level < 4:
            return "SafeSupport"  # If low energy, protect and stabilize
        else:
            return self.determine_auto_action(self.core_ai.emotion_score)

    def execute_behavior(self):
        """Execute the behavior mode based on energy and mood."""
        return self.update_energy(self.core_ai.emotion_score["energy"])


# Example of how it works:
# ai_persona = T13Persona(ai)
# mood_message = ai_persona.adapt_response()
# action = ai_persona.execute_behavior()
# print(mood_message, action)
