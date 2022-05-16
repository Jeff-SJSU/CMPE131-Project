from functools import wraps
from flask import redirect
from flask_login import current_user, login_required

# Wrapper to check if user is logged in and a seller
def seller_required(func):
    func = login_required(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        if not current_user.seller:
            return redirect('/account')
        return func(*args, **kwargs)
    return wrapper
