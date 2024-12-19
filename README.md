# Poker Web Backend

A FastAPI-based backend service for the Poker Web application, providing API endpoints for poker game management and analysis.

![UI 1](https://pokerwebsite.s3.us-east-1.amazonaws.com/%E6%88%AA%E5%B1%8F2024-12-17+%E4%B8%8B%E5%8D%882.54.01.png)
![UI 2](https://pokerwebsite.s3.us-east-1.amazonaws.com/%E6%88%AA%E5%B1%8F2024-12-16+%E4%B8%8B%E5%8D%8811.44.34.png)
![UI 3](https://pokerwebsite.s3.us-east-1.amazonaws.com/%E6%88%AA%E5%B1%8F2024-12-18+%E4%B8%8B%E5%8D%887.14.38.png)



## 🚀 Features

- FastAPI-powered REST API
- AWS S3 integration for data storage
- OpenAI integration for advanced poker analysis
- Authentication and authorization
- Secure environment configuration
- Scalable architecture with modular design

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

## 🚀 Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload --port 8080
```

The API will be available at `http://localhost:8080`.

## 📁 Project Structure

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 
