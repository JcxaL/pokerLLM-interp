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
        self.default_model = "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or"
        self.available_models = {
            "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or": "Fine-tuned Poker Model",
            "gpt-4o-mini": "Standard GPT-4o Mini"
        }
        self.system_prompt = """You are a GTO Strategy & Balancing Specialist with vision capabilities. 
        You can interpret game situations from text and images:
        - Provide unexploitable strategies for each betting round
        - Ideal action frequencies
        - Balanced ranges with value hands and bluffs
        - Consider board textures, stack sizes, pot sizes, player count
        - Use mixed strategy ratios when applicable"""

    async def get_response(
        self, 
        message: str, 
        game_state: Optional[Dict[str, Any]] = None,
        model_params: Optional[Dict[str, Any]] = None
    ) -> str:
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

            # 设置模型参数，只保留支持的参数
            model_params = model_params or {}
            completion_params = {
                "model": model_params.get('model_id', self.default_model),
                "messages": messages,
                "temperature": model_params.get('temperature', 0.7),
                "max_tokens": model_params.get('max_tokens', 512),
                "top_p": model_params.get('top_p', 1.0),
                "frequency_penalty": model_params.get('frequency_penalty', 0),
                "presence_penalty": model_params.get('presence_penalty', 0),
            }

            response = self.client.chat.completions.create(**completion_params)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in chat service: {e}")
            return f"Sorry, I encountered an error: {str(e)}" 