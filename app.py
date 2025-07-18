from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = FastAPI(title="API de Países Favoritos", version="1.0.0")

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Tu contraseña de MySQL
    'database': 'paises_db'
}

# Función para obtener conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

# Inicializar la base de datos
def init_db():
    try:
        # Crear la tabla si no existe
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paises_favoritos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(255) NOT NULL,
                    capital VARCHAR(255) NOT NULL,
                    region VARCHAR(255) NOT NULL,
                    comentario TEXT,
                    fecha_agregado DATETIME NOT NULL
                )
            ''')
            
            connection.commit()
            cursor.close()
            connection.close()
            print("✅ Tabla paises_favoritos verificada/creada exitosamente")
        
    except Error as e:
        print(f"❌ Error al inicializar la base de datos: {e}")

# Modelo de datos para países favoritos
class PaisFavorito(BaseModel):
    nombre: str
    capital: str
    region: str
    comentario: Optional[str] = None
    fecha_agregado: Optional[str] = None

class PaisFavoritoResponse(PaisFavorito):
    id: int

# Inicializar la base de datos al iniciar la aplicación
init_db()

@app.get("/")
async def root():
    return {"message": "API de Países Favoritos - Funcionando correctamente"}

@app.get("/paises-favoritos", response_model=List[PaisFavoritoResponse])
async def obtener_paises_favoritos():
    """Obtener todos los países favoritos guardados"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id, nombre, capital, region, comentario, fecha_agregado
            FROM paises_favoritos
            ORDER BY fecha_agregado DESC
        ''')
        
        paises = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return [
            PaisFavoritoResponse(
                id=pais[0],
                nombre=pais[1],
                capital=pais[2],
                region=pais[3],
                comentario=pais[4],
                fecha_agregado=pais[5].strftime("%Y-%m-%d %H:%M:%S") if pais[5] else None
            )
            for pais in paises
        ]
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener países: {e}")

@app.post("/paises-favoritos", response_model=PaisFavoritoResponse)
async def agregar_pais_favorito(pais: PaisFavorito):
    """Agregar un nuevo país a favoritos"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = connection.cursor()
        
        # Verificar si el país ya existe
        cursor.execute('SELECT id FROM paises_favoritos WHERE nombre = %s', (pais.nombre,))
        existe = cursor.fetchone()
        
        if existe:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=400, detail="Este país ya está en favoritos")
        
        # Agregar fecha actual si no se proporciona
        fecha_agregado = datetime.now() if not pais.fecha_agregado else datetime.fromisoformat(pais.fecha_agregado.replace('Z', '+00:00'))
        
        cursor.execute('''
            INSERT INTO paises_favoritos (nombre, capital, region, comentario, fecha_agregado)
            VALUES (%s, %s, %s, %s, %s)
        ''', (pais.nombre, pais.capital, pais.region, pais.comentario, fecha_agregado))
        
        pais_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        
        return PaisFavoritoResponse(
            id=pais_id,
            nombre=pais.nombre,
            capital=pais.capital,
            region=pais.region,
            comentario=pais.comentario,
            fecha_agregado=fecha_agregado.strftime("%Y-%m-%d %H:%M:%S")
        )
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar país: {e}")

@app.delete("/paises-favoritos/{pais_id}")
async def eliminar_pais_favorito(pais_id: int):
    """Eliminar un país de favoritos"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM paises_favoritos WHERE id = %s', (pais_id,))
        
        if cursor.rowcount == 0:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail="País no encontrado")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": "País eliminado de favoritos"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar país: {e}")

@app.get("/paises-favoritos/{pais_id}", response_model=PaisFavoritoResponse)
async def obtener_pais_favorito(pais_id: int):
    """Obtener un país favorito específico"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
    
    try:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT id, nombre, capital, region, comentario, fecha_agregado
            FROM paises_favoritos
            WHERE id = %s
        ''', (pais_id,))
        
        pais = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not pais:
            raise HTTPException(status_code=404, detail="País no encontrado")
        
        return PaisFavoritoResponse(
            id=pais[0],
            nombre=pais[1],
            capital=pais[2],
            region=pais[3],
            comentario=pais[4],
            fecha_agregado=pais[5].strftime("%Y-%m-%d %H:%M:%S") if pais[5] else None
        )
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener país: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)