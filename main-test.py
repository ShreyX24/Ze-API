import os
from dotenv import load_dotenv
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status, Response
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

app = FastAPI(
    title="User Management API",
    description="API for managing user profiles with MongoDB backend",
    version="1.0.0"
)

# Load .env file
load_dotenv()

# Initialize MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("job-app")
user_collection = db.get_collection("user")

# Custom type for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    """Container for a single user record."""
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # name: str = Field(..., min_length=1, max_length=100)
    # username: str = Field(..., min_length=3, max_length=50)
    # email: EmailStr
    # profile_picture: Optional[str] = None
    # bio: str = Field(..., max_length=500)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "janedoe",
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "profile_picture": "image.jpg",
                "bio": "This is my bio",
            }
        },
    )

class UpdateUserModel(BaseModel):
    """Optional updates for a user document."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "username": "janedoe",
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "profile_picture": "image.jpg",
                "bio": "This is my bio",
            }
        },
    )

class UserCollection(BaseModel):
    """Container for a list of UserModel instances."""
    users: List[UserModel]

@app.get("/", response_description="API Health Check")
def read_root():
    return {"status": "healthy", "message": "User Management API is running"}

@app.post(
    "/user/create",
    response_description="Add new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: UserModel = Body(...)):
    """Create a new user record."""
    # Check if email or username already exists
    existing_user = await user_collection.find_one(
        {"$or": [{"email": user.email}, {"username": user.username}]}
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )
    
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@app.get(
    "/user/get/all",
    response_description="List all users",
    response_model=UserCollection,
    response_model_by_alias=False,
)
async def list_users(skip: int = 0, limit: int = 100):
    """List users with pagination."""
    return UserCollection(
        users=await user_collection.find().skip(skip).limit(limit).to_list(limit)
    )

@app.get(
    "/user/get/{user_id}",
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

@app.put(
    "/user/update/{user_id}",
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

    # Filter out None values
    update_data = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }
    
    if len(update_data) < 1:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be updated"
        )

    # Check if new username/email conflicts with existing users
    if "username" in update_data or "email" in update_data:
        query = {"_id": {"$ne": user_obj_id}}
        if "username" in update_data:
            query["username"] = update_data["username"]
        if "email" in update_data:
            query["email"] = update_data["email"]
        if await user_collection.find_one(query):
            raise HTTPException(
                status_code=400,
                detail="Username or email already taken"
            )

    updated_user = await user_collection.find_one_and_update(
        {"_id": user_obj_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    
    if updated_user is not None:
        return updated_user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@app.delete("/user/delete/{user_id}", response_description="Delete user")
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