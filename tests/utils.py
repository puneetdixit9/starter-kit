def get_user_role_login_credentials() -> dict:
    """
    This function is used to return user role login credentials
    :return:
    """
    return {
        "email": "testuser@xyz.com",
        "password": "testpassword",
    }


def get_user_role_signup_data() -> dict:
    """
    This function is used to return user role signup data
    :return:
    """
    return {"username": "testuser2", "email": "testuser2@xyz.com", "password": "testpassword", "role": "user"}


def get_admin_role_login_credentials() -> dict:
    """
    This function is used to return admin role login credentials
    :return:
    """
    return {
        "email": "testadmin@xyz.com",
        "password": "testpassword",
    }


def get_admin_role_signup_data() -> dict:
    """
    This function is used to return admin role signup data
    :return:
    """
    return {
        "email": "testadmin2@xyz.com",
        "password": "testpassword",
        "username": "testadmin2",
        "role": "admin",
    }


def get_update_password_data() -> dict:
    """
    This function is used to return update password data.
    :return:
    """
    return {"old_password": "testpassword", "new_password": "updatedtestpassword"}


def get_address_data() -> dict:
    """
    This function is used to get the address data.
    :return:
    """
    return {
        "type": "work",
        "house_no_and_street": "78, street 4",
        "country": "India",
        "pin_code": 121107,
    }


def get_updated_address_data() -> dict:
    """
    This function is used to get the updated address data.
    :return:
    """
    return {
        "type": "other",
        "house_no_and_street": "123, street 9",
        "country": "USA",
        "pin_code": 111111,
    }


def get_update_profile_data():
    return {
        "first_name": "Test",
        "last_name": "test last",
        "department": "test department",
        "function": "test function",
        "role": "test role",
    }
