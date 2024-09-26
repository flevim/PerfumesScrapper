import mysql.connector
from db_connection import get_db_connection

def exist_rut(rut):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM entidad WHERE rut = %s"
        cursor.execute(query, (rut,))
        
        result = cursor.fetchone()
        
        if result[0] > 0:
            return True
        
        return False
    
    except mysql.connector.Error as error: 
        print(f"Error: {error}")
        return False
    
    finally:
        if cursor:
            cursor.close()
            
        if conn.is_connected():
            conn.close()
            

def query_get_data(rut):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """SELECT 
                        a.nombre, a.codigo, a.categoria, a.afecta_iva, a.fecha, e.nombre, e.rut 
                    FROM actividad a 
                    JOIN entidad e ON a.entidad_id = e.id 
                    WHERE e.rut = %s
                """
        cursor.execute(query, (rut,))
        
        result = cursor.fetchall()
        return result
        
        
    
    except mysql.connector.Error as error: 
        print(f"Error: {error}")
        return None
    
    finally:
        if cursor:
            cursor.close()
            
        if conn.is_connected():
            conn.close()
            

def query_post_data(rut, name, activities):
    try:
        
        conn = get_db_connection()
        
        cursor = conn.cursor()
        
        # Se inicia una transacción para atomizar consultas de inserción 
        conn.start_transaction()
        
        insert_entity_query = """
                INSERT INTO entidad 
                    (nombre, rut) 
                VALUES (%s, %s)
        """ 
        
        cursor.execute(insert_entity_query, (name, rut))
        
        #se obtiene id de entidad insertada 
        entity_id = cursor.lastrowid
        
        insert_activity_query = """
                INSERT INTO actividad 
                    (nombre, codigo, categoria, afecta_iva, fecha, entidad_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
        
        for activity in activities: 
            cursor.execute(insert_activity_query, (activity['nombre'], activity['codigo'], activity['categoria'], activity['afecta IVA'], activity['fecha'], entity_id))
        
        conn.commit()
        print("Inserción realizada.")
        
        
    
    except mysql.connector.Error as error: 
        print(f"Error: {error}")
        conn.rollback()
    
    finally:
        if cursor:
            cursor.close()
            
        if conn.is_connected():
            conn.close()