import streamlit as st
import openai
import time
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_openai():
    """Initialize OpenAI client with API key"""
    # Try to get API key from environment first
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not in environment, try to get from Streamlit secrets
    if not api_key:
        if 'openai_api_key' in st.secrets:
            api_key = st.secrets['openai_api_key']
    
    # If still no API key, ask user to input it
    if not api_key:
        api_key = st.sidebar.text_input('Enter OpenAI API Key:', type='password')
        if not api_key:
            st.error('Please enter your OpenAI API key to continue!')
            st.stop()
    
    return openai.OpenAI(api_key=api_key)

class PokerStrategyAdvisor:
    def __init__(self, model_id: str = "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or"):
        self.model_id = model_id
        self.client = initialize_openai()
        
        # Reference the system prompt from training
        self.system_prompt = """You are a GTO Strategy & Balancing Specialist tasked with providing theoretically sound poker strategies.
        Focus on:
        - Unexploitable strategies for each betting round
        - Ideal action frequencies
        - Balanced ranges with value hands and bluffs
        - Key factors like blockers, fold equity, and board textures
        - Mixed strategy ratios when applicable"""

    def get_advice(self, situation: Dict) -> Dict:
        try:
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self._format_situation(situation)}
                ],
                temperature=0.7
            )
            
            return {
                "advice": response.choices[0].message.content,
                "latency": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

    def _format_situation(self, situation: Dict) -> str:
        return f"""Analyze this poker situation:
        Position: {situation.get('position', 'N/A')}
        Stage: {situation.get('stage', 'N/A')}
        Hand: {situation.get('hand', 'N/A')}
        Board: {situation.get('board', '')}
        Stack Size: {situation.get('stack_size', '100BB')}
        Previous Action: {situation.get('previous_action', 'N/A')}
        """

def main():
    st.set_page_config(page_title="GTO Poker Advisor", layout="wide")
    
    # Set default API key if available
    if not os.getenv('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = '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' 
    # Initialize the advisor
    advisor = PokerStrategyAdvisor()
    
    # Sidebar for session settings
    st.sidebar.title("Session Settings")
    
    # API Key input in sidebar if not set
    if 'OPENAI_API_KEY' not in os.environ and 'openai_api_key' not in st.secrets:
        api_key = st.sidebar.text_input('OpenAI API Key', type='password')
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
        else:
            st.error('Please enter your OpenAI API key to continue!')
            st.stop()
    
    game_type = st.sidebar.selectbox("Game Type", ["Cash Game", "Tournament"])
    stack_size = st.sidebar.slider("Stack Size (BB)", 10, 200, 100)
    
    # Main content area
    st.title("GTO Poker Strategy Advisor")
    
    # Input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Situation")
        position = st.selectbox("Position", ["BTN", "SB", "BB", "UTG", "MP", "CO"])
        stage = st.selectbox("Stage", ["Preflop", "Flop", "Turn", "River"])
        hand = st.text_input("Your Hand (e.g., AKs, JTs)", "")
        board = st.text_input("Board (if post-flop, e.g., As Kh 2d)", "")
        previous_action = st.text_area("Previous Action", "")

    # Get advice button
    if st.button("Get Strategy Advice"):
        situation = {
            "position": position,
            "stage": stage,
            "hand": hand,
            "board": board,
            "stack_size": f"{stack_size}BB",
            "previous_action": previous_action,
            "game_type": game_type
        }
        
        with st.spinner("Analyzing situation..."):
            result = advisor.get_advice(situation)
            
        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            with col2:
                st.subheader("Strategic Advice")
                st.write(result["advice"])
                st.caption(f"Response time: {result['latency']:.2f}s")
                
                # Save to history
                if "session_history" not in st.session_state:
                    st.session_state.session_history = []
                st.session_state.session_history.append({
                    "situation": situation,
                    "advice": result["advice"],
                    "timestamp": result["timestamp"]
                })

    # History section
    if st.session_state.get("session_history"):
        st.subheader("Session History")
        for entry in reversed(st.session_state.session_history[-5:]):
            with st.expander(f"Situation at {entry['timestamp'][:19]}"):
                st.json(entry["situation"])
                st.write("Advice:", entry["advice"])

if __name__ == "__main__":
    main()