class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message


class NotFoundException(BaseException):
    message = "Not Found"

class InsertError(Exception):
    def __init__(self, detail: str = "Erro ao inserir os dados"):
        self.detail = detail
        
class NotFoundError(Exception):
    def __init__(self, detail: str = "Recurso não encontrado"):
        self.detail = detail
