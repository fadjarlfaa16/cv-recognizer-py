from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional, List
from pydantic import BaseModel

# Mongodb Connection
client = MongoClient("mongodb://localhost:27017")
db = client["job_vacancy"]
collection = db["vacancies"]

router = APIRouter()

class JobVacancy(BaseModel):
    job_title: str
    description: str
    similarity: Optional[float] = None

class CVText(BaseModel):
    cv_text: str

# def calculate_similarity(job_description: str, cv_text: str) -> float:
#     job_words = set(job_description.lower().split())
#     cv_words = set(cv_text.lower().split())
#     if not job_words:
#         return 0.0
#     common = job_words.intersection(cv_words)
#     similarity = (len(common) / len(job_words)) * 100
#     return similarity

# --- CRUD Endpoints ---

@router.post("/", response_model=dict)
def create_job(job: JobVacancy):
    job_dict = job.dict()
    result = collection.insert_one(job_dict)
    return {"_id": str(result.inserted_id), "message": "Job vacancy created successfully."}

@router.get("/", response_model=List[dict])
def get_jobs():
    jobs = []
    for job in collection.find():
        job["_id"] = str(job["_id"])
        jobs.append(job)
    return jobs

@router.get("/{job_id}", response_model=dict)
def get_job(job_id: str):
    job = collection.find_one({"_id": ObjectId(job_id)})
    if job:
        job["_id"] = str(job["_id"])
        return job
    else:
        raise HTTPException(status_code=404, detail="Job vacancy not found")

@router.put("/{job_id}", response_model=dict)
def update_job(job_id: str, job: JobVacancy):
    update_result = collection.update_one({"_id": ObjectId(job_id)}, {"$set": job.dict()})
    if update_result.modified_count == 1:
        return {"message": "Job vacancy updated successfully."}
    else:
        raise HTTPException(status_code=404, detail="Job vacancy not found")

@router.delete("/{job_id}", response_model=dict)
def delete_job(job_id: str):
    delete_result = collection.delete_one({"_id": ObjectId(job_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Job vacancy deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Job vacancy not found")

# --- Similarity Endpoint ---
@router.post("/update_similarity", response_model=dict)
def update_similarity(data: CVText):
    cv_text = data.cv_text
    updated_jobs = []
    for job in collection.find():
        similarity = calculate_similarity(job.get("description", ""), cv_text)
        collection.update_one({"_id": job["_id"]}, {"$set": {"similarity": similarity}})
        updated_jobs.append({"_id": str(job["_id"]), "similarity": similarity})
    return {"message": "Similarity updated for all job vacancies.", "updated_jobs": updated_jobs}

def calculate_similarity(job_description: str, cv_text: str) -> float:
    # split description into the list of words
    job_words = job_description.lower().split()
    cv_words = cv_text.lower().split()
    
    total_words = len(job_words)
    if total_words == 0:
        return 0.0

    # word counts of description
    common_count = sum(1 for word in job_words if word in cv_words)
    
    similarity = (common_count / total_words) * 100
    return similarity
