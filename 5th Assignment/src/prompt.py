class Prompts:
    @staticmethod
    def prompt(user_story: str, story_genre: str, art_style: str, previous_story: str = ""):
        story_context = previous_story or "This is the opening scene."
        prompt = f"""
            You are the director and writer of an interactive choose-your-own-adventure visual novel.
            Continue the story based on the player's latest action.

            Latest player action:
            "{user_story}"

            Story so far:
            "{story_context}"

            Genre:
            "{story_genre}"

            Art style:
            "{art_style}"

            Generate a STRICT JSON object in exactly this format:

            {{
                "story_text": "<one vivid narrative paragraph, 80 to 130 words>",
                "image_prompt": "<detailed cinematic image prompt for Pollinations in the '{art_style}' art style>",
                "options": [
                    "<option-1>",
                    "<option-2>",
                    "<option-3>"
                ]
            }}

            Rules:
            - Return 2 or 3 distinct options.
            - Do not include markdown fences.
            - Do not include text before or after the JSON.
            - Use double quotes for every JSON key and string.
            - Escape any quotes inside string values.

            Return ONLY the JSON object. Do not include markdown, explanations, or any extra text.
            """
        return prompt