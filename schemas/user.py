from typing import Optional, List, Union, Dict
from pydantic import BaseModel, ConfigDict, Field, EmailStr, HttpUrl
from typing_extensions import Annotated
from datetime import date
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class PhoneNumber(BaseModel):
    country_code: str
    number: str

class Address(BaseModel):
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    pincode: str

class Resume(BaseModel):
    resume_title: str
    resume_link: str

class Experience(BaseModel):
    job_title: str
    company_name: str
    yoe: str
    description: str

class Project(BaseModel):
    proj_name: str
    proj_link: HttpUrl
    proj_desc: str
    tech_stack: List[str]

class Portfolio(BaseModel):
    porfolio_name: str
    porfolio_link: HttpUrl

class Social(BaseModel):
    social_name: str
    social_link: HttpUrl

class Links(BaseModel):
    portfolio: List[Portfolio]
    socials: List[Social]

class FollowUpReminder(BaseModel):
    type: str
    value: str
    to_remind_on: str

class Application(BaseModel):
    company_name: str
    application_link: HttpUrl
    applied_on: str
    follow_up_reminder: FollowUpReminder
    additional_note: Optional[str] = None

class Metadata(BaseModel):
    skills: List[str]
    address: Address
    coverletter: str = ""
    resume: List[Resume]
    experience: List[Experience]
    projects: List[Project]
    links: List[Links]
    applications_filled: List[Application]

class UserModel(BaseModel):
    """Container for a single user record with expanded fields."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    profile_picture: str
    phone_number_details: Optional[PhoneNumber] = None
    bio: Optional[str] = None
    metadata: Optional[Metadata] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "profile_picture": "/aws/fs/image.jpg",
                "phone_number_details": {
                    "country_code": "+1",
                    "number": "1234567890"
                },
                "bio": "Full Stack Developer",
                "metadata": {
                    "skills": ["React.js", "Python"],
                    "address": {
                        "line1": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "pincode": "10001"
                    }
                }
            }
        }
    )

class UpdateUserModel(BaseModel):
    """Optional updates for a user document."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_picture: Optional[str] = None
    phone_number_details: Optional[PhoneNumber] = None
    bio: Optional[str] = None
    metadata: Optional[Metadata] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class UserCollection(BaseModel):
    """Container for a list of UserModel instances."""
    users: List[UserModel]