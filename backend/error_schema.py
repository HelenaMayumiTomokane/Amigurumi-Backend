from pydantic import BaseModel, ValidationError
from flask import jsonify
from typing import List, Union

class FieldError(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str

class ValidationErrorResponse(BaseModel):
    detail: List[FieldError]

def register_validation_error_handler(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        errors = []

        if hasattr(e, 'errors'):
            for err in e.errors():
                error_type = err.get("type", "erro_desconhecido")
                message = err.get("msg", "Erro de validação")

                errors.append({
                    "loc": err.get("loc", []),
                    "msg": message,
                    "type": error_type
                })
