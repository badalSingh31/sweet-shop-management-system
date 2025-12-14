from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, sweets

app = FastAPI(
    title="Sweet Shop Management System",
    description="A comprehensive API for managing a sweet shop with inventory and purchases",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sweets.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Sweet Shop Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
