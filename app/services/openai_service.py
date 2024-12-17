import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

prompt = """
I am uploading an image of a poker situation. Please analyze the image and return the following structured JSON data:

1. Actions Until Now:
   • Extract all the player actions listed at the top of the image.
   • For each action, capture:
     - The player’s position (e.g., UTG, HJ, BTN, BB, etc.).
     - The action taken (e.g., Fold, Call, Raise).
     - The bet size, if applicable. If no bet size is present, set the value to null.

2. Board Cards:
   • Extract the visible board cards from the center of the image.
   • For each card, capture:
     - The rank of the card (e.g., J, 6, 5).
     - The suit of the card (e.g., spades, hearts, diamonds, clubs).

3. Player’s Hand:
   • Extract the player’s hole cards visible at the bottom right of the image.
   • For each card, capture:
     - The rank of the card (e.g., K, K).
     - The suit of the card (e.g., clubs, spades).

4. Current User's Position:
   • Identify the current user’s position as shown near their hand cards (e.g., BB, BTN, CO, etc.).
   • Capture this position as a string.

5. Current Action Options:
   • Extract all the action options available to the player at this point in the game (visible at the bottom of the image).
   • For each option, capture:
     - The action (e.g., Check, Bet 6.2, All-in).
     - The frequency percentage of the action as shown in the image.

6. Output:
   • Format the extracted information into the following JSON schema:
{
  "actions_until_now": [
    {
      "position": "string",           // Position of the player (e.g., UTG, HJ, BTN, BB).
      "action": "string",            // Action taken (e.g., Fold, Call, Raise).
      "bet_size": "number|null"      // Bet size, if applicable (null if no bet).
    }
  ],
  "board_cards": [
    {
      "rank": "string",              // Rank of the card (e.g., J, 6, 5).
      "suit": "string"               // Suit of the card (e.g., spades, hearts, diamonds, clubs).
    }
  ],
  "player_hand": [
    {
      "rank": "string",              // Rank of the player's card (e.g., K, K).
      "suit": "string"               // Suit of the player's card (e.g., clubs, spades).
    }
  ],
  "current_user_position": "string", // The current user’s position (e.g., BB, BTN, CO).
  "current_action_options": [
    {
      "action": "string",            // Action option (e.g., Check, Bet 6.2).
      "frequency": "number"          // Frequency percentage for the action (e.g., 63.3).
    }
  ]
}
"""

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def analyze_poker_image(self, image_url: str) -> dict:
        try:
            response = self.client.chat.completions.create(model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            }
                        },
                    ],
            
                }
            ],
            response_format={
                "type": "json_object"
            })
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error analyzing image with OpenAI: {e}")
            raise 