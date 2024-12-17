# **Poker GTO Interpreter using Large Language Models (LLMs)**

## **Project Overview**
This project bridges the gap between quantitative **Game Theory Optimal (GTO)** strategies and interpretability in **No-Limit Texas Hold'em poker**. By fine-tuning a language model, we transform raw GTO outputs and poker data into **actionable strategic insights**, enabling players to understand and apply optimal poker strategies effectively.

---

## **Features**
- 🚀 **Advanced Data Processing**: Parse poker books, GTO solver outputs, and strategic content seamlessly.  
- 🧠 **Fine-Tuned LLM Pipeline**: Specialized model trained on poker strategy and GTO concepts.  
- 🖥️ **Interactive UI**: Streamlit-based interface for real-time strategy consultation.  
- 🔍 **Validation Framework**: Robust testing suite for model performance evaluation.  
- 🖼️ **Multi-Modal Support**: Supports text, images, and structured poker data for broader applicability.  

---

## **Project Structure**
```plaintext
poker-LLM/
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies list
├── poker_app.py              # Streamlit-based interactive interface
├── data/
│   ├── raw/                  # Original training data
│   ├── processed/            # Preprocessed datasets
│   └── final/                # Analysis outputs and model results
└── notebooks/
    ├── part1a.ipynb          # General data preparation and cleaning
    ├── part1b.ipynb          # Cleaning image data from poker books
    ├── part1c.ipynb          # Transcript cleaning for YouTube videos
    ├── part1d.ipynb          # NLP-based YouTube transcript pair extraction
    ├── part1e.ipynb          # Supplemental GTO solver data preparation
    ├── part2_classifier.ipynb # Feature engineering for model input
    ├── part3_augmentation.ipynb # Context-based data augmentation for scarce sources
    ├── part4_finetune.ipynb  # Fine-tuning the LLM for poker reasoning
    ├── part5_validation.ipynb # Performance validation and benchmarks
    └── part6_serving.ipynb   # Deployment testing and utilities
```

---

## **Notebook Details**
1. **Data Preparation**: Cleans and processes raw poker strategy content and GTO solver outputs.  
2. **Preprocessing**: Implements tokenization and feature engineering tailored for poker terminology.  
3. **Augmentation**: Generates scenario variations to expand training data for underrepresented cases.  
4. **Fine-Tuning**: Customizes LLMs to reason effectively about GTO strategy and poker play.  
5. **Validation**: Evaluates model performance through a robust testing suite.  
6. **Serving**: Tests deployment pipelines and API integration.  

---

## **Running the Application**

### **1. Prerequisites**
Install the required dependencies:
```bash
pip install -r requirements.txt
```

---

### **2. Starting the Streamlit Interface**
Navigate to the project directory:
```bash
ls
```

Run the Streamlit application:
```bash
streamlit run poker_app.py
```

---

### **3. Using the Interface**
- **Mode Selection**: Choose between "Beginner" and "Pro" modes.  
- **Input Options**:  
   - Text-based strategy questions  
   - Board state visualization  
   - Hand range selection  
   - Position and stack size parameters  
- **Advanced Settings (Pro Mode)**:  
   - Temperature adjustment  
   - Response length control  
   - Sampling parameters  

---

### UI Explanation and Usage

#### Session Settings Panel (Left Sidebar)
The **Session Settings Panel** allows users to configure session parameters efficiently:

1. **Select Mode**:
   - **Beginner**: Simplified explanations for new players.
   - **Pro**: Advanced strategy breakdowns and deeper GTO analysis.

2. **Stack Size**:
   - Adjust the current stack size in **big blinds** using the slider (10–200).
   - Real-time updates reflect user input.

3. **Game Type**:
   - Dropdown to select the poker game type and format:
     - **Cash Game**
     - **Tournament Play** *(future feature)*

4. **Documentation Reference**:
   - Expandable dropdown providing access to:
     - Poker terms
     - Position explanations
     - GTO concepts

---

#### Current Situation Panel (Main Section)
The **Current Situation Panel** enables interactive poker hand scenario descriptions.

##### Voice Input
- **Start New Recording**: Record a voice description of the poker scenario (e.g., position, stack size, hole cards).
- **Submit Recording**: Convert audio into a structured format.
- Real-time audio visualization appears during recording.

**Example Voice Input**:  
*"I’m on the button with Ace-King suited, and it’s preflop."*

**Voice Input Format**:
- **Position**: Specify your position (e.g., BTN, SB, BB, UTG).
- **Stage**: Select the round of betting (e.g., Preflop, Flop, Turn, River).
- **Your Hand**: Use standard poker notation for hole cards (e.g., `AhKs` for Ace of Hearts and King of Spades).

---

#### Optional Image Input
- Upload an image file for **complex hand visualizations** or **solver output screenshots**.
- **Usage**: Drag and drop a file or browse for an image.
- **File Size Limit**: 200MB (Although the model can handle larger files, it's recommended to keep it under 2MB for optimal performance)
- **Supported Formats**: PNG, JPG, JPEG

---

#### Example Scenario Walkthrough
1. **Set Stack Size**: 100 big blinds.
2. **Select Game Type**: Cash Game.
3. **Input Details** (manually or via voice input):
   - **Position**: BTN (Button).
   - **Stage**: Preflop.
   - **Hole Cards**: AhKs (Ace of Hearts, King of Spades).
4. **(Optional)** Upload a solver result screenshot.

---

This interface simplifies poker scenario inputs, offering seamless transitions from **raw descriptions** to **interpretable insights**. Players can choose between **text** or **voice inputs** while enhancing accuracy through optional **visual uploads**.


---

## **API Key Configuration**
To use the fine-tuned model, configure your OpenAI API key through one of the following methods:
- Set as an environment variable:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
- Add to Streamlit secrets:
   - Path: `streamlit/secrets.toml`
   - Example:
     ```toml
     OPENAI_API_KEY = "your_api_key_here"
     ```
- Secure input via the UI.

---

## **Model Performance**
The fine-tuned LLM demonstrates significant improvements in:
- 📊 **Strategic Depth**: Enhanced interpretation of GTO solver outputs.  
- 🃏 **GTO Concept Understanding**: Clear explanations of complex optimal plays.  
- 🎯 **Actionable Insights**: Generates strategies tailored to specific board states.  
- 💬 **Response Coherence**: Ensures relevance and consistency in strategy outputs.  

---

## **Future Work**
- Optimize the methodology for more GTO tasks
- Integrate with real-time APIs to help with games
- Expand datasets with expert players for better performance

---

Enjoy using the **Poker GTO Interpreter** to elevate your poker game! ♠️♥️♣️♦️  