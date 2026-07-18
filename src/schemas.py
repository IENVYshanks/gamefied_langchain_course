from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class PasswordResetRequest(BaseModel):
    username: str
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    name: str
    role: str


class UsernameResponse(BaseModel):
    username: str | None


class ProgressRequest(BaseModel):
    progress: int = Field(ge=0, le=100)
    data: dict | None = None


class ProgressResponse(BaseModel):
    progress: int


class QuizAttemptRequest(BaseModel):
    score: int = Field(ge=0, le=10)
    total_questions: int = Field(default=10, ge=1, le=10)


class ModuleScore(BaseModel):
    module_key: str
    best_score: int
    attempts: int


class GamificationResponse(BaseModel):
    points: int
    modules: list[ModuleScore]
