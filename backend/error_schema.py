from pydantic import BaseModel, ValidationError, Field

from flask import jsonify
from typing import List, Union

#declaração dos campos de erros
class FieldError(BaseModel):
    loc: List[Union[str, int]] = Field(..., description="Localização do campo com erro")
    msg: str = Field(..., description="Mensagem descritiva do erro")
    type: str = Field(..., description="Tipo do erro identificado")


class ValidationErrorResponse(BaseModel):
    detail: List[FieldError] = Field(..., description="Lista de erros de validação")


#requisição da mensagem de erro
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
