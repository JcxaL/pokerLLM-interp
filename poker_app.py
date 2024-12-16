import os
import time
from datetime import datetime
from typing import Dict
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------- CUSTOM CSS & PAGE SETUP --------------
st.set_page_config(page_title="GTO Poker Advisor", page_icon="♠", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #ddd;
    }
    .header-img {
        display: block;
        margin: 0 auto;
        width: 60%;
    }
    .title {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 2.5em;
        font-weight: 700;
        color: #333;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 1.2em;
        font-weight: 400;
        color: #555;
        text-align: center;
        margin-bottom: 2em;
    }
    h2, h3 {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #333;
    }
    p, div, span, label {
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        color: #333;
    }
    div.stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 4px !important;
        border: none !important;
        font-size: 1em !important;
        padding: 0.6em 1.2em !important;
        cursor: pointer !important;
    }
    div.stButton > button:hover {
        background-color: #45a049 !important;
    }
    .streamlit-expanderHeader {
        font-size: 1.1em;
        font-weight: 600;
        color: #333;
    }
    .advice-box {
        background-color: #ffffff;
        padding: 1.5em;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-top: 1em;
    }
    .time-caption {
        text-align: right;
        color: #888;
        font-size: 0.9em;
    }
    
    /* New Tooltip Styles */
    .tooltip-container {
        position: relative;
        display: inline-block;
        margin-bottom: 0.5em;
    }
    
    .tooltip-label {
        font-weight: 500;
        color: #333;
    }
    
    .tooltip-text {
        visibility: hidden;
        width: 220px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.9em;
        line-height: 1.4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .tooltip-text::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }
    
    .tooltip-container:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def create_tooltip(label: str, tooltip_text: str) -> str:
    """Create a tooltip with hover effect."""
    return f"""
        <div class="tooltip-container">
            <span class="tooltip-label">{label}</span>
            <span class="tooltip-text">{tooltip_text}</span>
        </div>
    """

# ---------------- INITIALIZATION FUNCTIONS ----------------
def initialize_openai():
    """Initialize OpenAI client with API key."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key and 'openai_api_key' in st.secrets:
        api_key = st.secrets['openai_api_key']

    if not api_key:
        api_key = st.sidebar.text_input('🔑 Enter OpenAI API Key:', type='password')
        if not api_key:
            st.error('Please enter your OpenAI API key to continue!')
            st.stop()

    return openai.OpenAI(api_key=api_key)


class PokerStrategyAdvisor:
    def __init__(self, model_id: str = "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or"):
        self.model_id = model_id
        self.client = initialize_openai()
        self.system_prompt = """You are a GTO Strategy & Balancing Specialist with vision capabilities. 
        You can interpret game situations from text and images:
        - Provide unexploitable strategies for each betting round
        - Ideal action frequencies
        - Balanced ranges with value hands and bluffs
        - Consider board textures, stack sizes, pot sizes, player count
        - Use mixed strategy ratios when applicable"""

    def get_advice(self, situation: Dict) -> Dict:
        try:
            start_time = time.time()
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self._format_situation(situation)}
            ]

            # If image content is available and the model supports it
            # This is placeholder logic. In a real scenario, you'd format as required:
            if situation.get("image_content"):
                image_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": situation["image_content"],
                                "detail": "low"
                            }
                        }
                    ]
                }
                messages.append(image_message)

            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=situation.get("temperature", 0.7),
                max_tokens=situation.get("max_tokens", 512),
                top_p=situation.get("top_p", 1),
                frequency_penalty=situation.get("frequency_penalty", 0),
                presence_penalty=situation.get("presence_penalty", 0)
            )

            return {
                "advice": response.choices[0].message.content.strip(),
                "latency": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    def _format_situation(self, situation: Dict) -> str:
        # Construct a textual scenario description
        desc = f"""Analyze this poker situation:
        Position: {situation.get('position', 'N/A')}
        Stage: {situation.get('stage', 'N/A')}
        Hand: {situation.get('hand', 'N/A')}
        Board: {situation.get('board', 'N/A')}
        Stack Size: {situation.get('stack_size', '100BB')}
        Game Type: {situation.get('game_type', 'N/A')}
        Previous Action: {situation.get('previous_action', 'N/A')}
        """
        # Add Pro mode details if available
        if situation.get('pro_mode', False):
            desc += f"Pot Size: {situation.get('pot_size','N/A')}\n"
            desc += f"Number of Players: {situation.get('num_players','N/A')}\n"
            if situation.get('custom_cards'):
                desc += f"Specific Cards in Play: {situation.get('custom_cards')}\n"
        return desc

def main():
    st.markdown("<div class='title'>Poker Strategy Advisor</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Interpreting Game Theory Optimal strategies for Texas Hold'em (with Vision)</div>", unsafe_allow_html=True)

    # SIDEBAR
    st.sidebar.title("Session Settings")

    # API Key input if needed
    if 'OPENAI_API_KEY' not in os.environ and 'openai_api_key' not in st.secrets:
        api_key = st.sidebar.text_input('OpenAI API Key', type='password')
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
        else:
            st.error('Please enter your OpenAI API key to continue!')
            st.stop()

    # Mode selection
    mode = st.sidebar.radio("Select Mode", ["Beginner", "Pro"], index=0)

    # Advanced parameters in Pro Mode
    if mode == "Pro":
        st.sidebar.markdown("### Advanced Model Parameters")
        temperature = st.sidebar.slider("Temperature (Creativity)", 0.0, 1.0, 0.7)
        max_tokens = st.sidebar.number_input("Max Tokens", min_value=100, max_value=2048, value=512)
        top_p = st.sidebar.slider("Top-p (Nucleus Sampling)", 0.0, 1.0, 1.0)
        frequency_penalty = st.sidebar.slider("Frequency Penalty", 0.0, 2.0, 0.0)
        presence_penalty = st.sidebar.slider("Presence Penalty", 0.0, 2.0, 0.0)
    else:
        # Default values for beginner mode
        temperature = 0.7
        max_tokens = 512
        top_p = 1
        frequency_penalty = 0
        presence_penalty = 0

    # Documentation Reference
    with st.sidebar.expander("🔎 Documentation Reference"):
        st.markdown("""
**From the Docs:**
- Vision fine-tuning allows you to provide images as input.
- You can fine-tune GPT-4o to improve performance on image-based tasks.
- Dataset formatting and JSONL structure is crucial.
- See OpenAI docs for more details on parameters and use cases.

[OpenAI Fine-tuning Docs](https://platform.openai.com/docs/guides/fine-tuning)
        """)

    advisor = PokerStrategyAdvisor()

    # MAIN CONTENT
    st.markdown("## Current Situation")

    # Define tooltips dictionary for both modes
    tooltips = {
        "position": "Your position at the poker table relative to the dealer button. BTN (Button) is the best position, followed by CO (Cutoff), etc.",
        "stage": "The current betting round in the hand: Preflop (before community cards), Flop (first 3 cards), Turn (4th card), or River (5th card)",
        "hand": "Your two hole cards. Use 's' for suited and 'o' for offsuit (e.g., AKs = Ace-King suited, JTo = Jack-Ten offsuit)",
        "board": "The community cards on the table. Format using card value and suit (e.g., As Kh 2d = Ace of spades, King of hearts, 2 of diamonds)",
        "previous_action": "What has happened in the hand so far? Include any raises, calls, or other significant actions by players",
        "pot_size": "The total amount of chips in the pot at this point in the hand",
        "num_players": "Number of players still active in the hand",
        "custom_cards": "Known cards held by other players or removed from deck",
        "stack_size": "Your stack size in big blinds (BB). 100BB is standard for cash games",
        "game_type": "Cash Game: Playing with real money chips. Tournament: Playing in a competition format with elimination",
        "speech_input": "Record and transcribe verbal descriptions of the poker situation"
    }

    # Beginner vs Pro input forms
    if mode == "Beginner":
        col1, col2 = st.columns([1,1])
        
        with col1:
            st.markdown(create_tooltip("🔎 Position", tooltips["position"]), unsafe_allow_html=True)
            position = st.selectbox("", ["BTN", "SB", "BB", "UTG", "MP", "CO"], key="pos")
            
            st.markdown(create_tooltip("🃏 Stage", tooltips["stage"]), unsafe_allow_html=True)
            stage = st.selectbox("", ["Preflop", "Flop", "Turn", "River"], key="stage")
            
            st.markdown(create_tooltip("📝 Your Hand", tooltips["hand"]), unsafe_allow_html=True)
            hand = st.text_input("", "", key="hand")
            
            st.markdown(create_tooltip("🌍 Board", tooltips["board"]), unsafe_allow_html=True)
            board = st.text_input("", "", key="board")
            
            st.markdown(create_tooltip("💬 Previous Action", tooltips["previous_action"]), unsafe_allow_html=True)
            previous_action = st.text_area("", "e.g. UTG raised 3BB, MP called...", key="prev_action")

        with col2:
            st.markdown("### Optional Image Input")
            uploaded_image = st.file_uploader("Upload image (optional)", type=["png", "jpg", "jpeg"])
            image_content = None
            if uploaded_image is not None:
                st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
                image_content = "https://example.com/path/to/image.jpg"

        pot_size = None
        num_players = None
        custom_cards = None
        pro_mode_flag = False

    else:  # Pro Mode
        col1, col2 = st.columns([1,1])
        
        with col1:
            st.markdown(create_tooltip("🔎 Position", tooltips["position"]), unsafe_allow_html=True)
            position = st.selectbox("", ["BTN", "SB", "BB", "UTG", "MP", "CO"], key="pro_pos")
            
            st.markdown(create_tooltip("🃏 Stage", tooltips["stage"]), unsafe_allow_html=True)
            stage = st.selectbox("", ["Preflop", "Flop", "Turn", "River"], key="pro_stage")
            
            st.markdown(create_tooltip("📝 Your Hand", tooltips["hand"]), unsafe_allow_html=True)
            hand = st.text_input("", "", key="pro_hand")
            
            st.markdown(create_tooltip("🌍 Board", tooltips["board"]), unsafe_allow_html=True)
            board = st.text_input("", "", key="pro_board")
            
            st.markdown(create_tooltip("💬 Previous Action", tooltips["previous_action"]), unsafe_allow_html=True)
            previous_action = st.text_area("", "Describe last betting actions", key="pro_prev_action")

            st.markdown(create_tooltip("💲 Pot Size", tooltips["pot_size"]), unsafe_allow_html=True)
            pot_size = st.number_input("", min_value=0, value=100, key="pro_pot_size")
            
            st.markdown(create_tooltip("👥 Number of Players", tooltips["num_players"]), unsafe_allow_html=True)
            num_players = st.slider("", 2, 10, 6, key="pro_num_players")
            
            st.markdown(create_tooltip("🗃 Custom Cards", tooltips["custom_cards"]), unsafe_allow_html=True)
            custom_cards = st.text_area("", "List specific cards dealt to players, if needed.", key="pro_custom_cards")

        with col2:
            st.markdown("### Optional Image Input")
            uploaded_image = st.file_uploader("Upload reference image", type=["png", "jpg", "jpeg"], key="pro_image")
            image_content = None
            if uploaded_image is not None:
                st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
                image_content = "https://example.com/path/to/image.jpg"

            st.markdown("#### Speech Input (Experimental)")
            st.markdown(create_tooltip("🎤 Speech Input", tooltips["speech_input"]), unsafe_allow_html=True)
            if st.button("Record Speech", key="pro_speech"):
                st.info("Simulating speech capture... (In a real implementation, speech-to-text would occur here)")
                previous_action += "\n[Speech Input: Player said 'Let's gamble big!']"

        pro_mode_flag = True

    # Sidebar elements with tooltips
    st.sidebar.markdown(create_tooltip("💰 Stack Size", tooltips["stack_size"]), unsafe_allow_html=True)
    stack_size = st.sidebar.slider("", 10, 200, 100)

    st.sidebar.markdown(create_tooltip("🎮 Game Type", tooltips["game_type"]), unsafe_allow_html=True)
    game_type = st.sidebar.selectbox("", ["Cash Game", "Tournament"])

    st.markdown("---")
    st.markdown("## Get Strategic Advice")
    st.markdown("When ready, click the button to retrieve the GTO-based advice.")

    if st.button("Get Strategy Advice"):
        situation = {
            "position": position,
            "stage": stage,
            "hand": hand,
            "board": board,
            "stack_size": f"{stack_size}BB",
            "previous_action": previous_action,
            "game_type": game_type,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "pro_mode": pro_mode_flag,
            "pot_size": pot_size if pro_mode_flag else None,
            "num_players": num_players if pro_mode_flag else None,
            "custom_cards": custom_cards if pro_mode_flag else None,
            "image_content": image_content
        }

        with st.spinner("Analyzing situation..."):
            result = advisor.get_advice(situation)

        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.markdown("### Strategic Advice")
            st.markdown("The following guidance is derived from a Game Theory Optimal perspective (Enhanced by Vision):")
            st.markdown(f"<div class='advice-box'>{result['advice']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='time-caption'>Response time: {result['latency']:.2f}s</div>", unsafe_allow_html=True)

            # Save to history
            if "session_history" not in st.session_state:
                st.session_state.session_history = []
            st.session_state.session_history.append({
                "situation": situation,
                "advice": result["advice"],
                "timestamp": result["timestamp"]
            })

    # History Section
    if st.session_state.get("session_history"):
        st.markdown("---")
        st.markdown("## Session History")
        st.markdown("Review your recent queries and the advice provided:")
        for entry in reversed(st.session_state.session_history[-5:]):
            with st.expander(f"Situation at {entry['timestamp'][:19]}"):
                st.json(entry["situation"])
                st.markdown("**Advice:**")
                st.markdown(f"<div class='advice-box'>{entry['advice']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
