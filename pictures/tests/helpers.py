from django.contrib.auth import get_user_model


def create_test_user(username, password):
    """Helper method to create users for testing"""
    user_model = get_user_model()
    user = user_model.objects.create_user(username)
    user.is_active = True
    user.set_password(password)
    user.save()
    return user
