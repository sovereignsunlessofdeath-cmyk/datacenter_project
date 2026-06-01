from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    """Middleware Interceptor: Ensures a user session exists"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login_staff'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Middleware Interceptor: Ensures user has an active admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session.get('role') != 'admin':
            return redirect(url_for('auth.login_admin'))
        return f(*args, **kwargs)
    return decorated_function