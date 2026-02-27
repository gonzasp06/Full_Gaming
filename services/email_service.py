"""
Servicio de envío de emails para Full Gaming.
Utiliza SMTP para enviar correos (compatible con Gmail, Outlook, etc.)

CONFIGURACIÓN:
Para usar Gmail, necesitás habilitar "Contraseñas de aplicaciones" en tu cuenta:
1. Ir a https://myaccount.google.com/security
2. Activar verificación en 2 pasos
3. Generar una "Contraseña de aplicación" para "Correo"
4. Usar esa contraseña en EMAIL_PASSWORD

Las credenciales se configuran en config_email.py o mediante variables de entorno.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Intentar cargar configuración desde archivo
try:
    from config_email import EMAIL_USER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT
    _CONFIG_LOADED = True
except ImportError:
    _CONFIG_LOADED = False
    EMAIL_USER = ''
    EMAIL_PASSWORD = ''
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587


class EmailService:
    """Servicio para envío de emails transaccionales."""
    
    def __init__(self):
        # Configuración SMTP - Primero intenta config_email.py, luego variables de entorno
        if _CONFIG_LOADED:
            self.smtp_server = SMTP_SERVER
            self.smtp_port = SMTP_PORT
            self.email_user = EMAIL_USER
            self.email_password = EMAIL_PASSWORD
        else:
            self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
            self.email_user = os.environ.get('EMAIL_USER', '')
            self.email_password = os.environ.get('EMAIL_PASSWORD', '')
        self.nombre_sistema = "Full Gaming"
    
    def _crear_conexion(self):
        """Crea conexión SMTP con TLS."""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            return server
        except Exception as e:
            print(f"⚠ Error al conectar con servidor SMTP: {str(e)}")
            return None
    
    def enviar_codigo_recuperacion(self, email_destino, nombre_usuario, codigo):
        """
        Envía el código de recuperación de contraseña por email.
        
        Args:
            email_destino: Email del usuario
            nombre_usuario: Nombre del usuario para personalizar el mensaje
            codigo: Código de 6 dígitos generado
            
        Returns:
            dict: {"ok": True} si se envió, {"ok": False, "error": "mensaje"} si falló
        """
        if not self.email_user or not self.email_password:
            # Si no hay configuración de email, simular envío (modo desarrollo)
            print(f"📧 [DEV MODE] Código de recuperación para {email_destino}: {codigo}")
            return {"ok": True, "dev_mode": True}
        
        try:
            # Crear mensaje
            mensaje = MIMEMultipart('alternative')
            mensaje['Subject'] = f"🔐 {self.nombre_sistema} - Código de recuperación"
            mensaje['From'] = f"{self.nombre_sistema} <{self.email_user}>"
            mensaje['To'] = email_destino
            
            # Cuerpo del email en texto plano
            texto_plano = f"""
Hola {nombre_usuario},

Recibimos una solicitud para restablecer tu contraseña en {self.nombre_sistema}.

Tu código de verificación es:

    {codigo}

Este código expira en 10 minutos.

Si no solicitaste este cambio, podés ignorar este email.

Saludos,
El equipo de {self.nombre_sistema}
            """
            
            # Cuerpo del email en HTML (más visual)
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; background-color: #1a1a2e; color: #ffffff; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: linear-gradient(135deg, #252540 0%, #1a1a2e 100%); border-radius: 16px; padding: 30px; border: 1px solid #3C308C;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #6A44F2; margin: 0;">🎮 {self.nombre_sistema}</h1>
        </div>
        
        <p style="color: #bbb; font-size: 15px;">Hola <strong style="color: #fff;">{nombre_usuario}</strong>,</p>
        
        <p style="color: #bbb; font-size: 15px;">Recibimos una solicitud para restablecer tu contraseña.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <p style="color: #888; font-size: 13px; margin-bottom: 10px;">Tu código de verificación es:</p>
            <div style="background: linear-gradient(135deg, #6A44F2, #3C308C); display: inline-block; padding: 15px 40px; border-radius: 12px; font-size: 32px; letter-spacing: 8px; font-weight: bold; color: #fff;">
                {codigo}
            </div>
            <p style="color: #ff6b6b; font-size: 12px; margin-top: 15px;">⏱️ Este código expira en 10 minutos</p>
        </div>
        
        <p style="color: #666; font-size: 13px; text-align: center; margin-top: 30px;">
            Si no solicitaste este cambio, podés ignorar este email.
        </p>
        
        <hr style="border: none; border-top: 1px solid #3C308C; margin: 25px 0;">
        
        <p style="color: #555; font-size: 11px; text-align: center;">
            {self.nombre_sistema} - Tu tienda gamer de confianza
        </p>
    </div>
</body>
</html>
            """
            
            # Adjuntar ambas versiones
            parte_texto = MIMEText(texto_plano, 'plain', 'utf-8')
            parte_html = MIMEText(html, 'html', 'utf-8')
            mensaje.attach(parte_texto)
            mensaje.attach(parte_html)
            
            # Enviar
            server = self._crear_conexion()
            if not server:
                return {"ok": False, "error": "No se pudo conectar al servidor de email"}
            
            server.sendmail(self.email_user, email_destino, mensaje.as_string())
            server.quit()
            
            print(f"✓ Email de recuperación enviado a {email_destino}")
            return {"ok": True}
            
        except Exception as e:
            print(f"⚠ Error al enviar email: {str(e)}")
            return {"ok": False, "error": "Error al enviar el email. Intentá de nuevo."}
    
    def enviar_confirmacion_cambio(self, email_destino, nombre_usuario):
        """
        Envía confirmación de que la contraseña fue cambiada.
        Esto es una medida de seguridad para alertar al usuario.
        """
        if not self.email_user or not self.email_password:
            print(f"📧 [DEV MODE] Confirmación de cambio de contraseña para {email_destino}")
            return {"ok": True, "dev_mode": True}
        
        try:
            mensaje = MIMEMultipart('alternative')
            mensaje['Subject'] = f"✅ {self.nombre_sistema} - Contraseña actualizada"
            mensaje['From'] = f"{self.nombre_sistema} <{self.email_user}>"
            mensaje['To'] = email_destino
            
            texto = f"""
Hola {nombre_usuario},

Tu contraseña en {self.nombre_sistema} fue actualizada exitosamente.

Si no realizaste este cambio, contactanos inmediatamente.

Saludos,
El equipo de {self.nombre_sistema}
            """
            
            html = f"""
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color: #1a1a2e; color: #ffffff; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: #252540; border-radius: 16px; padding: 30px; border: 1px solid #3C308C;">
        <h2 style="color: #2ecc71; text-align: center;">✅ Contraseña Actualizada</h2>
        <p style="color: #bbb;">Hola <strong>{nombre_usuario}</strong>,</p>
        <p style="color: #bbb;">Tu contraseña en {self.nombre_sistema} fue actualizada exitosamente.</p>
        <p style="color: #ff6b6b; font-size: 13px;">Si no realizaste este cambio, contactanos inmediatamente.</p>
    </div>
</body>
</html>
            """
            
            mensaje.attach(MIMEText(texto, 'plain', 'utf-8'))
            mensaje.attach(MIMEText(html, 'html', 'utf-8'))
            
            server = self._crear_conexion()
            if server:
                server.sendmail(self.email_user, email_destino, mensaje.as_string())
                server.quit()
            
            return {"ok": True}
        except Exception as e:
            # No fallar si no se puede enviar confirmación
            print(f"⚠ Error al enviar confirmación: {str(e)}")
            return {"ok": True}  # No afecta el flujo principal

    def enviar_codigo_cambio_perfil(self, email_destino, nombre_usuario, codigo):
        """
        Envía código de verificación para cambiar contraseña desde el perfil.
        Similar a enviar_codigo_recuperacion pero con mensaje diferente.
        
        Args:
            email_destino: Email del usuario
            nombre_usuario: Nombre para personalizar
            codigo: Código de 6 dígitos
        """
        if not self.email_user or not self.email_password:
            print(f"📧 [DEV MODE] Código para cambio de contraseña desde perfil: {codigo}")
            return {"ok": True, "dev_mode": True}
        
        try:
            mensaje = MIMEMultipart('alternative')
            mensaje['Subject'] = f"🔐 {self.nombre_sistema} - Código para cambiar tu contraseña"
            mensaje['From'] = f"{self.nombre_sistema} <{self.email_user}>"
            mensaje['To'] = email_destino
            
            texto_plano = f"""
Hola {nombre_usuario},

Solicitaste cambiar tu contraseña desde tu perfil en {self.nombre_sistema}.

Tu código de verificación es:

    {codigo}

Este código expira en 10 minutos.

Si no solicitaste este cambio, ignorá este email.

Saludos,
El equipo de {self.nombre_sistema}
            """
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; background-color: #1a1a2e; color: #ffffff; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: linear-gradient(135deg, #252540 0%, #1a1a2e 100%); border-radius: 16px; padding: 30px; border: 1px solid #3C308C;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #6A44F2; margin: 0;">🎮 {self.nombre_sistema}</h1>
        </div>
        
        <p style="color: #bbb; font-size: 15px;">Hola <strong style="color: #fff;">{nombre_usuario}</strong>,</p>
        
        <p style="color: #bbb; font-size: 15px;">Solicitaste cambiar tu contraseña desde tu perfil.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <p style="color: #888; font-size: 13px; margin-bottom: 10px;">Tu código de verificación es:</p>
            <div style="background: linear-gradient(135deg, #6A44F2, #3C308C); display: inline-block; padding: 15px 40px; border-radius: 12px; font-size: 32px; letter-spacing: 8px; font-weight: bold; color: #fff;">
                {codigo}
            </div>
            <p style="color: #ff6b6b; font-size: 12px; margin-top: 15px;">⏱️ Este código expira en 10 minutos</p>
        </div>
        
        <p style="color: #666; font-size: 13px; text-align: center; margin-top: 30px;">
            Si no solicitaste este cambio, podés ignorar este email.
        </p>
        
        <hr style="border: none; border-top: 1px solid #3C308C; margin: 25px 0;">
        
        <p style="color: #555; font-size: 11px; text-align: center;">
            {self.nombre_sistema} - Tu tienda gamer de confianza
        </p>
    </div>
</body>
</html>
            """
            
            mensaje.attach(MIMEText(texto_plano, 'plain', 'utf-8'))
            mensaje.attach(MIMEText(html, 'html', 'utf-8'))
            
            server = self._crear_conexion()
            if not server:
                return {"ok": False, "error": "No se pudo conectar al servidor de email"}
            
            server.sendmail(self.email_user, email_destino, mensaje.as_string())
            server.quit()
            
            print(f"✓ Email de cambio de contraseña enviado a {email_destino}")
            return {"ok": True}
            
        except Exception as e:
            print(f"⚠ Error al enviar email: {str(e)}")
            return {"ok": False, "error": "Error al enviar el email"}
