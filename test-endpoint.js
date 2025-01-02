/*
* POST: Create new user
* POST http://localhost:8000/user/create

{
  "name": "John Doe",
  "email": "john@example.com",
  "profile_picture": "/aws/fs/profile.jpg",
  "phone_number_details": {
    "country_code": "+1",
    "number": "1234567890"
  },
  "bio": "Full Stack Developer",
  "metadata": {
    "skills": ["React", "Python", "MongoDB"],
    "address": {
      "line1": "123 Main St",
      "line2": "Apt 4B",
      "city": "New York",
      "state": "NY",
      "pincode": "10001"
    },
    "coverletter": "",
    "resume": [
      {
        "resume_title": "Full Stack Resume",
        "resume_link": "/aws/fs/resume1.pdf"
      }
    ],
    "experience": [
      {
        "job_title": "Senior Developer",
        "company_name": "Tech Corp",
        "yoe": "3",
        "description": "Lead developer for web applications"
      }
    ],
    "projects": [],
    "links": [
      {
        "portfolio": [
          {
            "porfolio_name": "main",
            "porfolio_link": "https://portfolio.com"
          }
        ],
        "socials": [
          {
            "social_name": "LinkedIn",
            "social_link": "https://linkedin.com/in/johndoe"
          }
        ]
      }
    ],
    "applications_filled": []
  }
}

* GET: Fetch all users
GET http://localhost:8000/user/get/all

* GET: Fetch specific user
GET http://localhost:8000/user/get/6772367fe4f1b0ac7a291212

* PATCH: Update skills
PATCH http://localhost:8000/user/update/6772367fe4f1b0ac7a291212/skills
["React", "Node.js", "MongoDB", "AWS"]

* PATCH: Add resume
PATCH http://localhost:8000/user/update/6772367fe4f1b0ac7a291212/resume/add
{
  "resume_title": "Backend Developer Resume",
  "resume_link": "/aws/fs/backend_resume.pdf"
}

* PUT: Update user profile
PUT http://localhost:8000/user/update/6772367fe4f1b0ac7a291212
{
  "name": "John Smith",
  "bio": "Senior Full Stack Developer",
  "phone_number_details": {
    "country_code": "+1",
    "number": "9876543210"
  }
}

* DELETE: Remove application
DELETE http://localhost:8000/user/update/6772367fe4f1b0ac7a291212/applications/Netflix

* DELETE: Delete user
DELETE http://localhost:8000/user/delete/6772367fe4f1b0ac7a291212

*/