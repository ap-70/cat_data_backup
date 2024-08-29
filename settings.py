from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field, field_validator

def validate_threshold(value):
    if value <= 0:
        return False
    return True

class MySettings(BaseModel):
    max_num_backup: int = 3

    @field_validator("max_num_backup")
    @classmethod
    def max_num_backup_validator(cls, threshold):
        if not validate_threshold(threshold):
            raise ValueError("Max Num Backup must be greater than 0")

@plugin
def settings_model():
    return MySettings
