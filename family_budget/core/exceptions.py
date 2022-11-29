from fastapi import HTTPException


class BaseException(HTTPException):
    status_code = 500
    message = "Server error occured"

    def __init__(self):
        super(BaseException, self).__init__(self.status_code, self.message)


class InteralServerException(BaseException):
    status_code = 500
    message = "Server error occured"


class BudgetNotExistsException(BaseException):
    status_code = 404
    message = "Following user does not have budget"


class DuplicateBudgetException(BaseException):
    status_code = 400
    message = "User cannot have budget duplication"
