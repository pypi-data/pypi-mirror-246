import json
from pydantic import BaseModel, create_model, ConfigDict
from typing import Type, get_type_hints

class Validator(object):
    @classmethod
    def generate_schema(cls, model_class: Type[BaseModel], allow_additional: bool = False) -> str:
        if allow_additional:
            model_class.model_config = ConfigDict(extra="allow")
        schema = model_class.model_json_schema()
        return json.dumps(schema, indent=2)
