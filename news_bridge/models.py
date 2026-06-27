from pydantic import BaseModel, Field, field_validator

# ==================== JOB SCHEMA ====================

class JobCreate(BaseModel):
    """
    Pydantic schema representing the data required to create a new job post.
    Includes custom field validators to ensure inputs are non-empty, stripped,
    and meet minimum length requirements.
    """
    title: str = Field(..., description="Job title, minimum 3 characters")
    company: str = Field(..., description="Company name, minimum 2 characters")
    salary: str = Field(..., description="Salary format, non-empty")
    location: str = Field(..., description="Location, minimum 2 characters")
    description: str = Field(..., description="Job description, minimum 10 characters")
    posted_by: str = Field("", description="Email of user who posted the job")
    logo: str = Field("", description="Base64 encoded logo image")
    gpa: str = Field("", description="Minimum GPA requirement")
    languages: str = Field("", description="Language requirements")
    other_reqs: str = Field("", description="Other requirements")

    @field_validator('title', 'company', 'salary', 'location', 'description', mode='before')
    @classmethod
    def strip_and_check_empty(cls, value: str) -> str:
        """
        Pydantic validator to clean string fields by stripping whitespace
        and ensuring they are not empty.
        """
        if not isinstance(value, str):
            raise ValueError("Field must be a valid string")
        
        stripped = value.strip()
        if not stripped:
            raise ValueError("Field cannot be empty or contain only whitespace")
            
        return stripped

    @field_validator('title')
    @classmethod
    def validate_title_length(cls, value: str) -> str:
        """Enforces minimum length of 3 for job title."""
        if len(value) < 3:
            raise ValueError("Job title must be at least 3 characters long")
        return value

    @field_validator('company')
    @classmethod
    def validate_company_length(cls, value: str) -> str:
        """Enforces minimum length of 2 for company name."""
        if len(value) < 2:
            raise ValueError("Company name must be at least 2 characters long")
        return value

    @field_validator('location')
    @classmethod
    def validate_location_length(cls, value: str) -> str:
        """Enforces minimum length of 2 for location name."""
        if len(value) < 2:
            raise ValueError("Location must be at least 2 characters long")
        return value

    @field_validator('description')
    @classmethod
    def validate_description_length(cls, value: str) -> str:
        """Enforces minimum length of 10 for job description."""
        if len(value) < 10:
            raise ValueError("Job description must be at least 10 characters long")
        return value


# ==================== USER SCHEMAS ====================

class UserRegister(BaseModel):
    """Schema for validating user registration input."""
    name: str = Field(..., description="Full name of the user, min 2 chars")
    title: str = Field(..., description="Recruiter/Professional title, min 2 chars")
    email: str = Field(..., description="Email address, non-empty")
    password: str = Field(..., description="Password, min 4 chars")

    @field_validator('name', 'title', 'email', 'password', mode='before')
    @classmethod
    def strip_and_check_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Field must be a valid string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Field cannot be empty")
        return stripped

    @field_validator('name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return value

    @field_validator('title')
    @classmethod
    def validate_title(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError("Professional title must be at least 2 characters long")
        return value

    @field_validator('email')
    @classmethod
    def validate_email(cls, value: str) -> str:
        if '@' not in value or '.' not in value:
            raise ValueError("Invalid email format")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 4:
            raise ValueError("Password must be at least 4 characters long")
        return value


class UserLogin(BaseModel):
    """Schema for validating login requests."""
    email: str = Field(..., description="Email address")
    password: str = Field(..., description="Password")

    @field_validator('email', 'password', mode='before')
    @classmethod
    def strip_and_check_empty(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Field must be a valid string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Field cannot be empty")
        return stripped


class UserProfileUpdate(BaseModel):
    """Schema for updating user profiles."""
    email: str = Field(..., description="Email key to identify user")
    name: str = Field(..., description="Updated display name")
    title: str = Field(..., description="Updated title")
    bio: str = Field("", description="Updated professional bio description")
    skills: str = Field("", description="Updated skills, comma-separated")

    @field_validator('email', 'name', 'title', mode='before')
    @classmethod
    def check_required_fields(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Field must be a valid string")
        stripped = value.strip()
        if not stripped:
            raise ValueError("Field cannot be empty")
        return stripped

    @field_validator('bio', 'skills', mode='before')
    @classmethod
    def clean_optional_fields(cls, value: str) -> str:
        if value is None:
            return ""
        return str(value).strip()


# ==================== CV SCHEMA ====================

class CVCreate(BaseModel):
    name: str = Field(..., description="Full name of student")
    email: str = Field(..., description="Email of student")
    major: str = Field(..., description="Student's major")
    university: str = Field(..., description="Student's university")
    gpa: float = Field(..., description="Student's GPA")
    skills: str = Field(..., description="Student's skills")
    languages: str = Field("", description="Languages spoken")
    bio: str = Field("", description="Student's bio/intro")
    avatar: str = Field("", description="Base64 encoded avatar image")
    certificates: str = Field("", description="JSON list of certificates")
