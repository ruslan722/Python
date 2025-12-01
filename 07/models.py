from peewee import *
import datetime
import sys 

# --- КОНФИГУРАЦИЯ БАЗЫ ДАННЫХ ---
DB_NAME = 'firmware_system'
DB_USER = 'root'
DB_PASS = 'root'        
DB_HOST = 'localhost'
DB_PORT = 3306

db = MySQLDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

# --- БАЗОВАЯ МОДЕЛЬ ---
class BaseModel(Model):
    """Базовый класс, который определяет подключение к БД для всех моделей."""
    class Meta:
        database = db

# --- МОДЕЛИ СУЩНОСТЕЙ ---
class DeviceModel(BaseModel):
    name = CharField(unique=True, verbose_name="Название модели", max_length=100)
    description = TextField(null=True, verbose_name="Описание")
    created_at = DateTimeField(default=datetime.datetime.now)


class Firmware(BaseModel):
    version = CharField(verbose_name="Версия прошивки", max_length=50)
    file_path = CharField(verbose_name="Путь к файлу", max_length=255)
    release_date = DateField(default=datetime.date.today)
    
    # Внешний ключ: Прошивка принадлежит одной модели
    device_model = ForeignKeyField(DeviceModel, backref='firmwares', on_delete='CASCADE')

    class Meta:
        # Уникальный индекс: Одна модель не может иметь две одинаковые версии
        indexes = (
            (('device_model', 'version'), True),
        )


class PhysicalDevice(BaseModel):
    serial_number = CharField(unique=True, verbose_name="Серийный номер", max_length=100)
    is_active = BooleanField(default=True, verbose_name="Активен")
    
    # Внешний ключ: Устройство имеет определенную модель
    model_type = ForeignKeyField(DeviceModel, backref='devices')
    
    # Внешний ключ: Устройство имеет определенную прошивку (может быть NULL)
    current_firmware = ForeignKeyField(Firmware, backref='installed_on', null=True)


def create_tables():
    """Создает все таблицы в базе данных."""
    with db:
        db.create_tables([DeviceModel, Firmware, PhysicalDevice])

if __name__ == "__main__":
    print(f"Попытка подключения к БД '{DB_NAME}'...")
    try:
        db.connect()
        print("✅ Подключение к MySQL успешно!")
        create_tables()
        print("✅ Таблицы созданы/проверены.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        if not db.is_closed():
            db.close()