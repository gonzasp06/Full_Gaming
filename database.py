import mysql.connector

def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",  
        user="root",  
        password="constreseña_local",  
        database="nombre_base_datos" 
    )