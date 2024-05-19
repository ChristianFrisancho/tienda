from pydantic import BaseModel

class Item(BaseModel):
    nombre_tienda: str
    nombre_objeto: str
    precio: int
    stock: int

class Tienda(BaseModel):
    nombre: str
    
