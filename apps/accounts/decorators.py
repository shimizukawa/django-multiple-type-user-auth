from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def login_customer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    # FIXME: want to use psermission base testing: django.contrib.auth.decorators.permission_required
    actual_decorator = user_passes_test(
        lambda u: u.is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_supporter_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    # FIXME: want to use psermission base testing: django.contrib.auth.decorators.permission_required
    actual_decorator = user_passes_test(
        lambda u: u.is_supporter,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
