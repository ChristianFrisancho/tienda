from fastapi import FastAPI
import mysql.connector
import schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define object-related classes
class Tienda:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

class ObjetoEnTienda:
    def __init__(self, id, nombre_tienda, nombre_objeto, id_tienda, id_objeto, precio, stock):
        self.id = id
        self.nombre_tienda = nombre_tienda
        self.nombre_objeto = nombre_objeto
        self.id_tienda = id_tienda
        self.id_objeto = id_objeto
        self.precio = precio
        self.stock = stock
        
ALLOWED_ORIGINS = '*'    # or 'foo.com', etc.

# Function to build Tienda and ObjetoEnTienda objects
def build_tienda_object(data):
    if data:
        return Tienda(id=data[0], nombre=data[1])
    return None

def build_objeto_en_tienda_object(data):
    if data:
        return ObjetoEnTienda(id=data[0], nombre_tienda=data[1], nombre_objeto=data[2], id_tienda=data[3], id_objeto=data[4], precio=data[5], stock=data[6])
    return None

# Database connection parameters
host_name = "database-1.cofb7quhpsqh.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "tienda"

@app.get("/")
def get_success():
    return { "message": "success" }

# Obtener todas las tiendas
@app.get("/tiendas")
def get_tiendas():
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM tienda")
    results = cursor.fetchall()
    mydb.close()

    tiendas = [build_tienda_object(data) for data in results]
    return {"tiendas": tiendas}

# Post
@app.post("/tiendas")
def add_tienda(tienda: schemas.Tienda):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    nombre = tienda.nombre
    cursor = mydb.cursor()
    sql = "INSERT INTO tienda (nombre) VALUES (%s)"
    val = (nombre,)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Tienda añadida exitosamente"} 

# Obtener los objetos de una tienda por ID
@app.get("/tiendas/{id}/objetos")
def get_objetos_en_tienda(id: int):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM objetos_en_tienda WHERE id_tienda = {id}")
    results = cursor.fetchall()
    mydb.close()

    objetos_en_tienda = [build_objeto_en_tienda_object(data) for data in results]
    return {"objetos": objetos_en_tienda}

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
    id_objeto = item.id_objeto
    cursor = mydb.cursor()
    sql = "INSERT INTO objetos_en_tienda (nombre_tienda, nombre_objeto, precio, stock, id_tienda, id_objeto) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (nombre_tienda, nombre_objeto, precio, stock, id, id_objeto)
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
    sql = "UPDATE objetos_en_tienda SET stock=%s WHERE id_tienda=%s AND id_objeto=%s"
    val = (stock, id_tienda, id_objeto)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Objeto modificado exitosamente"}
    
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)
