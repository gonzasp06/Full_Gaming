from flask import session, abort, redirect, url_for
from functools import wraps


class AdminManager:
    """Gestiona permisos y autorizaciones del sistema"""
    
    def __init__(self):
        pass
    
    def es_admin(self):
        """Verifica si el usuario actual es admin"""
        return session.get('es_admin') == 1
    
    def es_logueado(self):
        """Verifica si el usuario está logueado"""
        return 'usuario_id' in session
    
    def requerir_admin(self, f):
        """Decorador: Solo admin puede acceder"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.es_admin():
                return abort(403)  # Acceso denegado
            return f(*args, **kwargs)
        return decorated_function
    
    def requerir_login(self, f):
        """Decorador: Solo usuarios logueados pueden acceder"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not self.es_logueado():
                return redirect(url_for('render_acceso'))
            return f(*args, **kwargs)
        return decorated_function
