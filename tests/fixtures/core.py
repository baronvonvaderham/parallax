import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(transactional_db):
    pass


@pytest.fixture
def create_user():
    """
    A function to create 'core.User' instances
    """
    from core.models import User

    def _create_user(**kwargs):
        return User.objects.create(**kwargs)
    return _create_user


@pytest.fixture
def user(create_user):
    """
    A 'core.User' instance for a generic default user.
    """
    return create_user(
        email='feynman@caltech.edu',
        username='Feynman'
    )
