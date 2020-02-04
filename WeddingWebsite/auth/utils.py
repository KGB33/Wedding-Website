from functools import wraps

from flask_login import current_user
from flask import redirect, url_for

from WeddingWebsite import login_manager
from WeddingWebsite.auth.exceptions import NoRolesProvided


def requires_roles(*roles):
    """
    Implements role biased authentication over Flask-login

    :param roles: Required Roles for authentication
    """

    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            if not roles:
                raise NoRolesProvided(
                    "No Roles provided, Please use @login_required instead"
                )

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if current_user.roles is None:
                return redirect(url_for("auth.unauthorized_role"))

            for role in roles:
                if role not in current_user.roles:
                    return redirect(url_for("auth.unauthorized_role"))
            return func(*args, **kwargs)

        return decorated_view

    return wrapper


def roles_cannot_access(*roles):
    """
    Implements role biased authentication over Flask-login

    Users with the provided roles CANNOT access the route.

    :param roles: Required Roles for authentication
    """

    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            if not roles:
                raise NoRolesProvided(
                    "No Roles provided, Please use @login_required instead"
                )

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            if current_user.roles is None:
                return func(*args, **kwargs)

            for role in roles:
                if role in current_user.roles:
                    return redirect(url_for("auth.unauthorized_role"))
            return func(*args, **kwargs)

        return decorated_view

    return wrapper
