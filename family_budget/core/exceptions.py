from fastapi import HTTPException


class BaseServiceException(HTTPException):
    status_code = 500
    message = "Server error occured"

    def __init__(self):
        super(BaseException, self).__init__(self.status_code, self.message)


class HttpDefaultException(BaseServiceException):
    status_code = 400
    message = "Error"


class InteralServerException(BaseServiceException):
    status_code = 500
    message = "Server error occured"


class BudgetNotExistsException(BaseServiceException):
    status_code = 404
    message = "Following user does not have budget"


class DuplicateBudgetException(BaseServiceException):
    status_code = 400
    message = "User cannot have budget duplication"


class EmailDuplicateException(BaseServiceException):
    status_code = 400
    message = "User with this email already exists"


class NotFoundException(BaseServiceException):
    status_code = 404
    message = "Resource not found"
