from src.auth.models import User


def get_mock_user():
    return User(id=1, username='V', password='asdazxc')
    