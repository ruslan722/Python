from fastapi import FastAPI, HTTPException
from peewee import IntegrityError, DoesNotExist
from typing import List


from models import DeviceModel, Firmware, PhysicalDevice, db, create_tables
from schemas import (
    DeviceModelCreate, DeviceModelSchema, 
    FirmwareCreate, FirmwareSchema, 
    PhysicalDeviceRegister, PhysicalDeviceSchema, 
    FirmwareUpdate, MessageResponse
)

app = FastAPI(
    title="Система Управления Прошивками",
    description="",
    version="1.0.0"
)




@app.middleware("http")
async def db_connection_middleware(request, call_next):
    """Открывает соединение с БД перед запросом и закрывает после."""
    try:
        db.connect(reuse_if_open=True)
        response = await call_next(request)
    finally:
        if not db.is_closed():
            db.close()
    return response


@app.on_event("startup")
def startup_event():
    try:
        db.connect()
        create_tables() 
        print("База данных готова и таблицы созданы.")
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")
       
    finally:
        if not db.is_closed():
            db.close()



@app.post("/models/", response_model=DeviceModelSchema, status_code=201, tags=["Модели Устройств"])
def create_model(model_data: DeviceModelCreate):
    """Создание новой модели устройства"""
    try:
        new_model = DeviceModel.create(
            name=model_data.name,
            description=model_data.description
        )
        return new_model
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Модель с таким именем уже существует.")

@app.get("/models/{model_id}", response_model=DeviceModelSchema, tags=["Модели Устройств"])
def get_model(model_id: int):
    """Получение информации о модели по ID"""
    try:
        model = DeviceModel.get_by_id(model_id)
        return model
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Модель не найдена.")
    

@app.get('/models/', response_model=list[DeviceModelSchema], tags= ["Модели Устройств"])
async def list_midel():
    models = DeviceModel.select()
    return list(models)




@app.post("/firmwares/", response_model=FirmwareSchema, status_code=201, tags=["Прошивки"])
def create_firmware(firmware_data: FirmwareCreate):
    """Добавление новой версии прошивки для модели"""
    try:
        model = DeviceModel.get(DeviceModel.name == firmware_data.model_name)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Модель '{firmware_data.model_name}' не найдена.")

    try:
        new_firmware = Firmware.create(
            device_model=model,
            version=firmware_data.version,
            file_path=firmware_data.file_path
        )
        return new_firmware
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"Прошивка версии '{firmware_data.version}' для этой модели уже существует.")

@app.get("/firmwares/by_model/{model_name}", response_model=List[FirmwareSchema], tags=["Прошивки"])
def get_firmwares_by_model(model_name: str):
    """Получение всех прошивок для указанной модели"""
    try:
        model = DeviceModel.get(DeviceModel.name == model_name)
     
        firmwares = list(model.firmwares.order_by(Firmware.release_date.desc())) 
        return firmwares
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Модель '{model_name}' не найдена.")
@app.get('/filtrames/', response_model=list[FirmwareSchema], tags= ["Прошивки"])
async def list_frames():
    try:
        firmaries =  Firmware.select()
        return List(firmaries)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail='Прошивки не найдены.')
    

@app.post("/devices/register", response_model=PhysicalDeviceSchema, status_code=201, tags=["Устройства (SN)"])
def register_device(device_data: PhysicalDeviceRegister):
    """Регистрация нового физического устройства по серийному номеру"""
    try:
        model = DeviceModel.get(DeviceModel.name == device_data.model_name)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Модель '{device_data.model_name}' не найдена. Сначала создайте модель.")
    
    try:
       
        new_device = PhysicalDevice.create(
            serial_number=device_data.serial_number,
            model_type=model
        )
        return new_device
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Устройство с таким серийным номером уже зарегистрировано.")

@app.get("/devices/{sn}", response_model=PhysicalDeviceSchema, tags=["Устройства (SN)"])
def get_device_info(sn: str):
    """Получение полной информации об устройстве по серийному номеру"""
    try:
        device = PhysicalDevice.get(PhysicalDevice.serial_number == sn)
        return device
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Устройство с SN: {sn} не найдено.")
    
@app.get("/devices/", response_model=list[PhysicalDeviceSchema], tags=["Устройства"])
async def get_device_info():
    devices = PhysicalDevice.select()
    
    return list(devices)



    

    
    
@app.put("/devices/{sn}/update_firmware", response_model=PhysicalDeviceSchema, tags=["Устройства (SN)"])
def update_firmware_on_device(sn: str, update_data: FirmwareUpdate):
    """Обновление прошивки на зарегистрированном устройстве"""
    try:
       
        device = PhysicalDevice.get(PhysicalDevice.serial_number == sn)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Устройство с SN: {sn} не найдено.")

    try:
       
        new_firmware = Firmware.get(
            (Firmware.device_model == device.model_type) & 
            (Firmware.version == update_data.new_version)
        )
        
        
        device.current_firmware = new_firmware
        device.save()
        
        
        return device
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Прошивка версии '{update_data.new_version}' не найдена или несовместима с моделью {device.model_type.name}.")

@app.delete("/devices/{sn}", response_model=MessageResponse, tags=["Устройства (SN)"])
def delete_device(sn: str):
    """Удаление устройства из системы по серийному номеру"""
    query = PhysicalDevice.delete().where(PhysicalDevice.serial_number == sn)
    rows_deleted = query.execute()
    
    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail=f"Устройство с SN: {sn} не найдено.")
    
    return {"message": f"Устройство с SN: {sn} успешно удалено."}

