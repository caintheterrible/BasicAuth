from sqlalchemy import Column, String
from app_config.settings.database import Base


class ClientUser(Base):

    first_name= Column(
        String(40),
        nullable=False,
    )
    last_name= Column(
        String(40),
        nullable=False,
    )
    email= Column(
        String(100),
        nullable=False,
        unique=True,
    )
    password_hash= Column(
        String(255),
        nullable=False,
    )

    def __init__(self, first_name:str, last_name:str, email:str, password_hash:str):
        self.first_name= first_name
        self.last_name= last_name
        self.email= email
        self.password_hash= password_hash

    def __repr__(self):
        return f'<ClientUser: (id={self.id} | name={self.first_name} {self.last_name} | email={self.email})'