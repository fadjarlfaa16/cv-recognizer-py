from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import cv, job

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv.router, prefix="/cv")
app.include_router(job.router, prefix="/job")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
