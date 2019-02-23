
def check_user_staff_superuser(user_obj):
    """
    Helps to find user is staff and superuser and
    returns True for positive and False for negative
    :param user_obj: user queryset of User model
    :return: boolean value True or False
    """
    if user_obj.is_staff and user_obj.is_superuser:
        return True
    return False

def is_user_active(user_obj):
    """
    Helps to find user is active or not.
    Returns boolean value True or False
    :param user_obj: user queryset of User model
    :return: boolean value
    """
    if user_obj.is_active:
        return True
    return False