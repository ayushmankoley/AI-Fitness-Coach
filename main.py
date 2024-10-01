from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import Column, Integer, String, Float, Enum, create_engine, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from ollama import Client
from datetime import datetime
from enum import Enum as PyEnum
from fastapi.responses import JSONResponse
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./fitness_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enum for body types and activity levels
class BodyType(PyEnum):
    ectomorph = "Ectomorph"
    mesomorph = "Mesomorph"
    endomorph = "Endomorph"

class ActivityLevel(PyEnum):
    sedentary = "Sedentary"
    light = "Light"
    moderate = "Moderate"
    active = "Active"
    athlete = "Athlete"

# Database Models
class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    body_type = Column(Enum(BodyType))
    activity_level = Column(Enum(ActivityLevel))

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    date = Column(String)
    calories_burned = Column(Float)

class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    plan = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class UserProfileCreate(BaseModel):
    name: str
    age: int
    height_cm: float
    weight_kg: float
    body_type: BodyType
    activity_level: ActivityLevel

class UserProfileResponse(BaseModel):
    id: int
    name: str
    age: int
    height_cm: float
    weight_kg: float
    body_type: BodyType
    activity_level: ActivityLevel

class WorkoutLogCreate(BaseModel):
    user_id: int
    date: str
    calories_burned: float

# Create DB tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ollama Setup
ollama_client = Client()

def format_plan(plan):
    plan = re.sub(r'\.(?=\s|$)', '.\n', plan)
    plan = re.sub(r'\n([A-Z]{2,})', r'\n\n\1', plan)
    plan = re.sub(r'(\d+\..*?)\n(?=\d+\.)', r'\1\n\n', plan)
    plan = re.sub(r'\n{3,}', '\n\n', plan)
    return plan.strip()

def generate_workout_plan(profile: UserProfile):
    prompt = f"""
    Create a personalized 30-day workout plan for a {profile.age} year-old {profile.body_type.value} body type person. 
    Activity level: {profile.activity_level.value}. 
    Weight: {profile.weight_kg}kg, Height: {profile.height_cm}cm.
    Structure the plan with clear headers and numbered exercises.
    """
    
    try:
        logger.info(f"Sending prompt to Ollama: {prompt}")
        response = ollama_client.generate(model="llama3.2:latest", prompt=prompt)
        workout_plan = response['response'].strip()
        formatted_plan = format_plan(workout_plan)
        return formatted_plan
    except Exception as e:
        logger.error(f"Error generating workout plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating workout plan: {str(e)}")

def generate_nutrition_plan(profile: UserProfile):
    prompt = f"""
    Create a personalized nutrition plan for a {profile.age} year-old {profile.body_type.value} body type person.
    Activity level: {profile.activity_level.value}.
    Weight: {profile.weight_kg}kg, Height: {profile.height_cm}cm.
    Structure the plan with clear headers and bullet points for meals and snacks.
    """
    
    try:
        logger.info(f"Sending prompt to Ollama: {prompt}")
        response = ollama_client.generate(model="llama3.2:latest", prompt=prompt)
        nutrition_plan = response['response'].strip()
        formatted_plan = format_plan(nutrition_plan)
        return formatted_plan
    except Exception as e:
        logger.error(f"Error generating nutrition plan: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating nutrition plan: {str(e)}")

# API Endpoints
@app.post("/signup", response_model=UserProfileResponse)
def signup(user: UserProfileCreate, db: Session = Depends(get_db)):
    db_user = UserProfile(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Created user with ID: {db_user.id}")
    return db_user

@app.get("/generate_workout/{user_id}")
def get_workout_plan(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    
    workout_plan = generate_workout_plan(profile)
    return {"workout_plan": workout_plan}

@app.get("/generate_nutrition_plan/{user_id}")
def get_nutrition_plan(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="User not found")
    
    nutrition_plan = generate_nutrition_plan(profile)
    
    try:
        db_nutrition_plan = NutritionPlan(user_id=user_id, plan=nutrition_plan)
        db.add(db_nutrition_plan)
        db.commit()
    except Exception as e:
        logger.error(f"Error saving nutrition plan: {str(e)}")
    
    return {"nutrition_plan": nutrition_plan}

@app.post("/log_workout/", response_model=WorkoutLogCreate)
def log_workout(log: WorkoutLogCreate, db: Session = Depends(get_db)):
    db_log = WorkoutLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# to start backend
# uvicorn main:app --reload 