from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import poker

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(poker.router, prefix="/chat", tags=["chat"])
app.include_router(poker.router, prefix="/poker", tags=["poker"]) 