from pydantic import BaseModel, Field
from typing import Optional
from datetime import date



class DeviceModelCreate(BaseModel):
    """Схема для создания новой модели устройства"""
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class FirmwareCreate(BaseModel):
    """Схема для создания новой прошивки"""
    model_name: str = Field(..., description="Название модели, для которой предназначена прошивка")
    version: str = Field(..., max_length=50)
    file_path: str = Field(..., max_length=255)

class PhysicalDeviceRegister(BaseModel):
    """Схема для регистрации физического устройства"""
    serial_number: str = Field(..., max_length=100)
    model_name: str = Field(..., description="Название модели, к которой относится устройство")

class FirmwareUpdate(BaseModel):
    """Схема для обновления прошивки на устройстве"""
    new_version: str = Field(..., description="Новая версия прошивки")



class FirmwareSchema(BaseModel):
    version: str
    release_date: date
   

    class Config:
        from_attributes = True 

class DeviceModelSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

class PhysicalDeviceSchema(BaseModel):
    serial_number: str
    is_active: bool
    
    
    model_type: DeviceModelSchema
    current_firmware: Optional[FirmwareSchema] = None

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str