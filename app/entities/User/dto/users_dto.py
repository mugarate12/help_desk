from app.core.database.models.users import UsersModel


class UserDTO():
    model = None

    def __init__(self, user: UsersModel):
        self.model = user

        self.id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name

        self.username = user.username
        self.email = user.email
        self.password = user.password
        
        self.address = user.address
        self.city = user.city
        self.state = user.state
        self.zip = user.zip
        self.country = user.country
        self.phone = user.phone

        self.created_at = user.created_at
        self.updated_at = user.updated_at

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'country': self.country,
            'phone': self.phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def to_model(self) -> UsersModel:
        return self.model
