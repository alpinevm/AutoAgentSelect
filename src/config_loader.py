import json

from pydantic import BaseModel

class Config(BaseModel):
    monitor_number: int
    state_delay_ms: int
    switch_key: str

def load() -> Config:
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    return Config(**data)