from sqlalchemy import Column, String
from werkzeug.security import check_password_hash, generate_password_hash

from family_budget.models.base import Base


class User(Base):
    first_name = Column(String(32), index=True)
    last_name = Column(String(32), index=True)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String(16))
    hashed_password = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
