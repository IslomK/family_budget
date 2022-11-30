from sqlalchemy import Column, String

from family_budget.core.utils import get_hashed_password, verify_password
from family_budget.models.base import Base


class User(Base):
    first_name = Column(String(32), index=True)
    last_name = Column(String(32), index=True)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String(16))
    hashed_password = Column(String(128))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, value):
        self.hashed_password = get_hashed_password(value)

    def check_password(self, password):
        return verify_password(self.hashed_password, password)
