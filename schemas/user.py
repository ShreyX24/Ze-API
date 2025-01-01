# /schemas/user.py
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    """Container for a single user record."""
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
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

    model_config = ConfigDict(
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

class UserCollection(BaseModel):
    """Container for a list of UserModel instances."""
    users: List[UserModel]