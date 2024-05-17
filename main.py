from fastapi import FastAPI
import mysql.connector
import schemas

app = FastAPI()

host_name = "database-1.cpxnwinne8ao.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "tienda"  

# Obtener todas las tiendas
@app.get("/tiendas")
def get_tiendas():
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM tienda")
    result = cursor.fetchall()
    mydb.close()
    return {"tiendas": result}

# Obtener los objetos de una tienda por ID
@app.get("/tiendas/{id}/objetos")
def get_objetos_en_tienda(id: int):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM objetos_en_tienda WHERE id = {id}")
    result = cursor.fetchall()
    mydb.close()
    return {"objetos": result}

# Añadir un nuevo objeto a una tienda
@app.post("/tiendas/{id}/objetos")
def add_objeto_en_tienda(id: int, item: schemas.Item):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    nombre_tienda = item.nombre_tienda
    nombre_objeto = item.nombre_objeto
    precio = item.precio
    stock = item.stock
    cursor = mydb.cursor()
    sql = "INSERT INTO objetos_en_tienda (nombre_tienda, nombre_objeto, precio, stock) VALUES (%s, %s, %s, %s)"
    val = (nombre_tienda, nombre_objeto, precio, stock)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Objeto añadido exitosamente"}

# Modificar un objeto en una tienda
@app.put("/tiendas/{id_tienda}/objetos/{id_objeto}")
def update_objeto_en_tienda(id_tienda: int, id_objeto: int, item: schemas.Item):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    nombre_objeto = item.nombre_objeto
    precio = item.precio
    stock = item.stock
    cursor = mydb.cursor()
    sql = "UPDATE objetos_en_tienda SET nombre_objeto=%s, precio=%s, stock=%s WHERE id=%s"
    val = (nombre_objeto, precio, stock, id_objeto)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Objeto modificado exitosamente"}

# Eliminar un objeto de una tienda por ID
@app.delete("/tiendas/{id_tienda}/objetos/{id_objeto}")
def delete_objeto_en_tienda(id_tienda: int, id_objeto: int):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM objetos_en_tienda WHERE id = {id_objeto}")
    mydb.commit()
    mydb.close()
    return {"message": "Objeto eliminado exitosamente"}

# Eliminar una tienda por ID
@app.delete("/tiendas/{id}")
def delete_tienda(id: int):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM tienda WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Tienda eliminada exitosamente"}
