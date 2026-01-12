"""
Excepciones lanzadas para fallos en las reglas de negocio.
"""


class DomainException(Exception):
    """ Excepción base para errores de la lógica de negocio. """
    pass


class InvalidEntityData(DomainException):
    """ Excepción lanzada cuando los datos de una entidad son inválidos. """

    def __init__(self, message: str):
        super().__init__(f'Datos de entidad inválidos: {message}')


class DepartmentNotFound(DomainException):
    """ Excepción lanzada cuando no se encuentra un departamento. """

    def __init__(self, dep_id: int = None, dep_name: str = None, dep_code: str = None):
        if dep_id:
            message = f'El departamento con ID {dep_id} no fue encontrado.'
        elif dep_name:
            message = f'El {dep_name} no fue encontrado.'
        elif dep_name:
            message = f'El departamento de siglas {dep_code} no fue encontrado.'
        else:
            message = "Departamento no encontrado."
        super().__init__(message)


class DepartmentAlreadyExists(DomainException):
    """ Excepción lanzada al intentar crear un departamento que ya existe. """

    def __init__(self, dep_code: str = None, dep_name: str = None):
        if dep_code:
            message = f'El departamento con código {dep_code} ya existe.'
        elif dep_name:
            message = f'El {dep_name} ya existe.'
        else:
            message = f'El departamento ya existe.'
        super().__init__(message)


class CannotDeleteDepartment(DomainException):
    """ Excepción lanzada cuando un departamento no puede ser eliminado. """

    def __init__(self, dep_id: int, reason: str):
        super().__init__(f'No se puede eliminar el departamento con ID {dep_id}: {reason}')
