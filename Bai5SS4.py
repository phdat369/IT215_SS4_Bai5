from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
import re
import uuid

app = FastAPI()

class StudentRegister(BaseModel):
    full_name: str = Field(..., min_length=3)
    email: EmailStr
    age: int = Field(..., ge=15, le=60)
    phone: str = Field(..., min_length=10, max_length=11)
    course: str
    note: Optional[str] = Field(default=None, max_length=200)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Họ tên không được để trống")
        return value.title()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa chữ số")
        return value

    @field_validator("course")
    @classmethod
    def normalize_course(cls, value):
        return value.lower()

    @field_validator("note")
    @classmethod
    def normalize_note(cls, value):
        if value:
            return value.strip().lower()
        return value


@app.post("/students/register")
def register_student(student: StudentRegister):
    register_id = "STU-" + uuid.uuid4().hex[:8].upper()

    return {
        "message": "Đăng ký học viên thành công",
        "register_id": register_id,
        "data": student.model_dump()
    }