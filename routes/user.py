# /routes/user.py
from typing import List
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response
from bson import ObjectId
from pymongo import ReturnDocument

from database import user_collection
from schemas.user import Resume, UserModel, UpdateUserModel, UserCollection

router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/create",
    response_description="Add new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    """Create a new user record."""
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.get(
    "/get/all",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_users(skip: int = 0, limit: int = 100):
    """List users with pagination."""
    return UserCollection(
        users=await user_collection.find().skip(skip).limit(limit).to_list(limit)
    )

@router.get(
    "/get/{user_id}",
    response_description="Get user by ID",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def get_user(user_id: str):
    """Retrieve a user by their ID."""
    try:
        user_obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
        
    if (user := await user_collection.find_one({"_id": user_obj_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@router.put(
    "/update/{user_id}",
    response_description="Update user",
    response_model=UserModel,
    response_model_by_alias=False,
)
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    """Update a user's information."""
    try:
        user_obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    update_data = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }
    
    if len(update_data) < 1:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be updated"
        )

    updated_user = await user_collection.find_one_and_update(
        {"_id": user_obj_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    
    if updated_user is not None:
        return updated_user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@router.patch("/update/{user_id}/resume/add", response_model=UserModel)
async def add_resume(user_id: str, resume: Resume):
    """Add a new resume to user's metadata."""
    try:
        user_obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    updated_user = await user_collection.find_one_and_update(
        {"_id": user_obj_id},
        {"$push": {"metadata.resume": resume.model_dump()}},
        return_document=ReturnDocument.AFTER
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/update/{user_id}/applications/{company_name}", response_model=UserModel)
async def remove_application(user_id: str, company_name: str):
    """Remove a specific application by company name."""
    try:
        user_obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    updated_user = await user_collection.find_one_and_update(
        {"_id": user_obj_id},
        {"$pull": {"metadata.applications_filled": {"company_name": company_name}}},
        return_document=ReturnDocument.AFTER
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.patch("/update/{user_id}/skills", response_model=UserModel)
async def update_skills(user_id: str, skills: List[str]):
    """Update user's skills list."""
    try:
        user_obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    updated_user = await user_collection.find_one_and_update(
        {"_id": user_obj_id},
        {"$set": {"metadata.skills": skills}},
        return_document=ReturnDocument.AFTER
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/detele/{user_id}", response_description="Delete user")
async def delete_user(user_id: str):
    """Delete a user by their ID."""
    try:
        user_obj_id = ObjectId(user_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
        
    delete_result = await user_collection.delete_one({"_id": user_obj_id})
    
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")