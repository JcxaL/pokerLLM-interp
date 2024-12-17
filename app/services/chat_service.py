import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

def format_card(card: Dict[str, str]) -> str:
    """Format a card dictionary into a string representation."""
    return f"{card['rank']}{card['suit']}"

class ChatService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or"  # 您的fine-tuned模型
        self.system_prompt = """You are a GTO Strategy & Balancing Specialist with vision capabilities. 
        You can interpret game situations from text and images:
        - Provide unexploitable strategies for each betting round
        - Ideal action frequencies
        - Balanced ranges with value hands and bluffs
        - Consider board textures, stack sizes, pot sizes, player count
        - Use mixed strategy ratios when applicable"""

    async def get_response(self, message: str, game_state: Optional[Dict[str, Any]] = None) -> str:
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ]

            if game_state:
                board_cards = game_state.get('board_cards', [])
                player_cards = game_state.get('player_cards', [])
                
                context = f"""Current game state:
                Position: {game_state.get('position', 'N/A')}
                Stage: {game_state.get('stage', 'N/A')}
                Stack Size: {game_state.get('stack_size', '100')}BB
                Board Cards: {' '.join(format_card(card) for card in board_cards) if board_cards else 'N/A'}
                Player Cards: {' '.join(format_card(card) for card in player_cards) if player_cards else 'N/A'}
                """
                messages.append({"role": "system", "content": context})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=512
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in chat service: {e}")
            return f"Sorry, I encountered an error: {str(e)}" 