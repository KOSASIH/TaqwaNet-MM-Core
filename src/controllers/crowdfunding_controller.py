from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from src.models.crowdfunding import CrowdfundingProject, User
from src.database import get_db
from src.auth import get_current_user

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str
    description: str
    target_amount: float
    end_date: str  # ISO format date string

class ProjectUpdate(BaseModel):
    title: str = None
    description: str = None
    target_amount: float = None
    end_date: str = None

@router.post("/projects/", response_model=CrowdfundingProject)
def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_project = CrowdfundingProject(
        id=str(uuid.uuid4()),
        title=project.title,
        description=project.description,
        target_amount=project.target_amount,
        end_date=datetime.fromisoformat(project.end_date),
        owner_id=current_user.id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/projects/", response_model=List[CrowdfundingProject])
def get_projects(db: Session = Depends(get_db)):
    return db.query(CrowdfundingProject).all()

@router.get("/projects/{project_id}", response_model=CrowdfundingProject)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(CrowdfundingProject).filter(CrowdfundingProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=CrowdfundingProject)
def update_project(project_id: str, project: ProjectUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(CrowdfundingProject).filter(CrowdfundingProject.id == project_id, CrowdfundingProject.owner_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
    
    if project.title is not None:
        db_project.title = project.title
    if project.description is not None:
        db_project.description = project.description
    if project.target_amount is not None:
        db_project.target_amount = project.target_amount
    if project.end_date is not None:
        db_project.end_date = datetime.fromisoformat(project.end_date)

    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/projects/{project_id}", response_model=dict)
def delete_project(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_project = db.query(CrowdfundingProject).filter(CrowdfundingProject.id == project_id, CrowdfundingProject.owner_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found or not authorized")
    
    db.delete(db_project)
    db.commit()
    return {"detail": "Project deleted successfully"}
