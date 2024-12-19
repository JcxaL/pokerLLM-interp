[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0+-blue.svg)](https://fastapi.tiangolo.com/)
# **♠️♥️ Fine-Tuning LLMs for Interpreting Game Theory Optimal Strategies in Poker ♣️♦️**
*ReadMe and Tutorial by Jiangchen Li & Ren De*

## 📑 Table of Contents

### 🌟 Core Sections
- [**Project Overview**](#project-overview)
- [**Main Features**](#main-features)
- [**Model Performance**](#model-performance)

### 📚 Documentation
- [Repo Structure](#repo-structure)
- [Notebook Details](#notebook-details)

### 💻 Application Guide
- [**Running Our Poker Web Backend Application**](#running-our-poker-web-backend-application)
  - [UI App Features](#-ui-app-features)
  - [**UI Elements Guide**](#-ui-elements-guide)
  - [Prerequisites](#-prerequisites)
  - [**Installation**](#-installation)
  - [**Running the Application**](#-running-the-application)
  - [UI App Sub-Structure](#-ui-app-sub-structure)

### 🔒 Security & API
  - [API Authentication](#-api-authentication)
  - [API Documentation](#-api-documentation)
  - [Dependencies](#-dependencies)
  - [Security](#-security)
  - [Deployment](#-deployment)
  - [Error Handling](#-error-handling)

### ℹ️ Additional Information
- [Future Work](#-future-work)
- [Contributing](#-contributing)
- [License](#-license)

<br>

## **Project Overview**
This project bridges the gap between quantitative **Game Theory Optimal (GTO)** strategies and interpretability in **No-Limit Texas Hold'em poker**. By fine-tuning a pretrained LLM model, we transform a diverse set of GTO/poker resources,otherwise unused, into **actionable strategic insights**, enabling players to understand and apply optimal poker strategies effectively in game and post-game. This can also encourage new players to self-study and improve their skills.


## **Main Features**
- 🚀 **Advanced Data Processing**: Parse poker books, GTO solver outputs, and strategic content seamlessly.  
- 🧠 **Fine-Tuned LLM Pipeline**: Specialized model trained on poker strategy and GTO concepts.  
- 🖥️ **Interactive UI**: React-based interface for real-time strategy consultation.  
- 🔍 **Validation Framework**: Robust testing suite for model performance evaluation.  
- 🖼️ **Multi-Modal Support**: Supports text, images, and structured poker data for broader applicability. Voice chat can also be added (capable) if future budget allows.


## **Model Performance**
The fine-tuned LLM demonstrates significant improvements in:
- 📊 **Strategic Depth**: Enhanced interpretation of GTO solver outputs.  
- 🃏 **GTO Concept Understanding**: Clear explanations of complex optimal plays.  
- 🎯 **Actionable Insights**: Generates strategies tailored to specific board states.  
- 💬 **Response Coherence**: Ensures relevance and consistency in strategy outputs.  

## **Repo Structure**
```plaintext
poker-LLM/
├── README.md                 # Project documentation
├── requirements.txt          # Dependencies list
├── poker_app.py              # React-based interactive UI interface
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
    ├── part5_validation.ipynb # Performance validation and benchmarks Trial
    └── part5a_summarization_plots.ipynb # Performance validation and benchmarks Final
```


```plaintext
pokerLLM-interp-web-interface/  
    ├── README.md              # Web interface documentation
    ├── requirements.txt       # Web app dependencies
    ├── app/                   # Backend application
    │   ├── main.py            # FastAPI application entry point
    │   ├── models/            # Data models and schemas
    │   ├── routers/           # API route handlers
    │   └── services/          # Business logic services
    └── frontend/              # React frontend application
        ├── src/
        │   ├── components/     # React components
        │   │   ├── CardSelector.tsx
        │   │   ├── ChatInterface.tsx
        │   │   ├── PlayerCardSelector.tsx
        │   │   └── PositionSelector.tsx
        │   ├── assets/         # Static assets
        │   └── App.tsx         # Main application component
        └── public/             # Public assets
```


## **Notebook Details**
1. **Data Preparation**: Cleans and processes raw poker strategy content and GTO solver outputs.  
2. **Preprocessing**: Implements tokenization and feature engineering tailored for poker terminology.  
3. **Augmentation**: Generates scenario variations to expand training data for underrepresented cases.  
4. **Fine-Tuning**: Customizes LLMs to reason effectively about GTO strategy and poker play.  
5. **Validation**: Evaluates model performance through a robust testing suite.  
6. **Serving**: Tests deployment pipelines and API integration.  
   
<br>
<br>

# Running Our Poker Web Backend Application

A FastAPI-based backend service for the Poker Web application, providing API endpoints for poker game management and analysis.

## [Watch our demo video on YouTube](https://youtu.be/CQW_0K7iGeQ)

<div align="center">

![UI 1](https://pokerwebsite.s3.us-east-1.amazonaws.com/%E6%88%AA%E5%B1%8F2024-12-17+%E4%B8%8B%E5%8D%882.54.01.png)
![UI 2](https://pokerwebsite.s3.us-east-1.amazonaws.com/%E6%88%AA%E5%B1%8F2024-12-16+%E4%B8%8B%E5%8D%8811.44.34.png)
![UI 3](https://pokerwebsite.s3.us-east-1.amazonaws.com/%E6%88%AA%E5%B1%8F2024-12-18+%E4%B8%8B%E5%8D%887.14.38.png)

</div>


## ⭐ UI App Features

- FastAPI-powered REST API
- AWS S3 integration for data storage
- OpenAI integration for advanced poker analysis
- Authentication and authorization
- Secure environment configuration
- Scalable architecture with modular design

## 🎮 UI Elements Guide

If you have any doubts regarding the use of the web app, refer to the youtube video above.

### 🎴 Card Selection Interface
- **Player Cards**: Select your hole cards using the intuitive card picker
  - Click on card values (2-A) and suits (♠♥♣♦) to select your cards
  - Visual representation matches standard poker notation
  - Quick clear and reset options available

### 🎯 Position and Stack Size Controls
- **Position Selector**: Dropdown menu for selecting your table position (CO, BTN, BB, etc.)
- **Stack Size Slider**: Adjust your stack size from 10BB to 200BB
  - Input field for precise stack size entry
  - Visual slider for quick adjustments

### 🃏 Board State Interface
- **Board Cards Selection**: Similar to player cards interface
  - Select up to 5 community cards
  - Cards are displayed in standard poker layout
  - Automatic validation prevents invalid card combinations

### 📊 Game State Display
- **Current Game State Banner**: Shows complete game information
  - Position, Stage, Stack Size, and Board Cards
  - Updates in real-time as you modify selections
  - Clear formatting for easy reading

### 🔧 Analysis Tools
- **💬 Chat Interface**: Interactive advice system
  - Automatically populates the game state and player cards based on your selections
  - Natural language input for poker questions
  - Detailed strategic responses
  - Hand history and previous advice accessible
- **📸 Image Analysis**: Upload hand history or current board images
  - Automatic game state detection
  - Strategic advice based on detected situation

<br>

## 📋 Prerequisites

- Python 3.8 or later
- pip (Python package installer)
- AWS Account with S3 access
- OpenAI API key

## 🛠️ Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd poker_web
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:
```
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=your_aws_region
AWS_BUCKET_NAME=your_s3_bucket_name

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# App Configuration
ENVIRONMENT=development
```

## ▶️ Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload --port 8080
```

The API will be available at `http://localhost:8080`.

## 📁 UI App Sub-Structure

```
app/
├── main.py           # Application entry point
├── models/          # Data models and schemas
├── routers/         # API route handlers
├── services/        # Business logic and external service integrations
└── static/          # Static files
```

## 🔑 API Authentication

The API uses token-based authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## 🔧 Dependencies

Key dependencies include:
- FastAPI: Modern web framework for building APIs
- Uvicorn: ASGI server implementation
- Python-multipart: Multipart form data parsing
- Python-dotenv: Environment variable management
- Boto3: AWS SDK for Python
- OpenAI: OpenAI API client
- Pydantic: Data validation
- Python-jose: JWT token handling
- Passlib & Bcrypt: Password hashing

## 🔐 Security

- Environment variables are used for sensitive configuration
- Authentication is required for protected endpoints
- Password hashing is implemented using bcrypt
- CORS middleware is configured for security

## 🐳 Deployment

The application is configured for deployment on AWS Elastic Beanstalk. Key deployment files:
- `Procfile`: Defines process types for deployment
- `.ebignore`: Specifies files to ignore in deployment
- `.ebextensions/`: Contains AWS Elastic Beanstalk configuration

## ⚠️ Error Handling

The API implements comprehensive error handling:
- Validation errors return 422 status code
- Authentication errors return 401 status code
- Authorization errors return 403 status code
- Not found errors return 404 status code


## 🚀 Future Work
- Optimize the methodology for more GTO strategies
- Integrate with real-time APIs to help with games live
- Expand datasets with expert players for better performance and reliability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 

---

Enjoy using the **Poker GTO Interpreter** to elevate your poker game! ♠️♥️♣️♦️  