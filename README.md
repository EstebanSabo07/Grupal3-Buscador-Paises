# 🌍 Buscador de Países - Trabajo Grupal #3

**Conexión a API Externa y Creación de API Propia**

---

## 📋 Información del Proyecto

**Profesor:** Alejandro Zamora  
**Curso:** Programación Web  
**Universidad:** LEAD University  
**Fecha de Entrega:** 18 de julio, 7:00 PM  

### 👥 Equipo de Desarrollo

**Desarrollador Principal:** Esteban G. Saborío

Nota sobre el desarrollo del proyecto:
Cronología de coordinación grupal:

Sábado 12 de julio: Se estableció contacto inicial con los integrantes del grupo para coordinar el desarrollo colaborativo del proyecto.

Lunes 14 de julio: Se logró coordinar donde se acordó la distribución de tareas. Se asignó al suscrito el desarrollo del punto #1 del entregable, específicamente todos los procedimientos necesarios para la conexión a la API pública.

Miércoles 16 de julio: Se compartieron por WhatsApp los archivos correspondientes al trabajo desarrollado del punto #1 para que los otros integrantes lo revisaran y avanzar con los demás requirimientos, sin embargo, tampoco hubo respuesta. 

Viernes 18 de julio: Ante la falta de respuesta y colaboración de los demás integrantes (mensajes dejados en visto sin respuesta), se procedió a completar la totalidad del proyecto de forma individual.

Documentación de respaldo: Se adjuntan en el espacio de entrega las capturas de pantalla que respaldan la situación descrita anteriormente.
Resultado: El trabajo fue desarrollado en su totalidad por Esteban G. Saborío - esteban.gutierrez@ulead.ac.cr , cumpliendo con todos los requerimientos establecidos en las especificaciones del proyecto y manteniendo los estándares de calidad académica esperados.

---

##  Descripción del Proyecto

Una aplicación web completa que integra una **API externa pública** (RestCountries) para mostrar información de países del mundo, y una **API propia desarrollada con FastAPI** que permite a los usuarios guardar sus países favoritos con comentarios personales en una base de datos MySQL.

###  Características Principales

- **Búsqueda de países**: Conexión en tiempo real con la API de RestCountries
- **Países favoritos**: Sistema para guardar países con comentarios personales
- **Persistencia de datos**: Base de datos MySQL para almacenamiento local
- **Interfaz intuitiva**: Diseño responsive con navegación por pestañas
- **Experiencia de usuario**: Modales, confirmaciones y mensajes informativos

---

##  Tecnologías Utilizadas

### Frontend
- **HTML5**: Estructura semántica de la aplicación
- **CSS3**: Estilos modernos con diseño responsive
- **JavaScript (Vanilla)**: Lógica de interacción y consumo de APIs

### Backend
- **Python 3.8+**: Lenguaje de programación principal
- **FastAPI**: Framework web moderno para APIs REST
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pydantic**: Validación y serialización de datos

### Base de Datos
- **MySQL 8.0**: Sistema de gestión de base de datos relacional
- **mysql-connector-python**: Driver oficial para conectividad con MySQL

### Control de Versiones
- **Git**: Control de versiones distribuido
- **GitHub**: Repositorio remoto y colaboración

---

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- MySQL 8.0 o superior
- MySQL Workbench (recomendado)
- Navegador web moderno

### 1. Clonar el Repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd Grupal3Esteban
```

### 2. Configurar Base de Datos
Ejecutar en MySQL Workbench:
```sql
CREATE DATABASE IF NOT EXISTS paises_db;
USE paises_db;

CREATE TABLE IF NOT EXISTS paises_favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    capital VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    comentario TEXT,
    fecha_agregado DATETIME NOT NULL
);
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Conexión MySQL
Verificar en `app.py` las credenciales:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'paises_db'
}
```

### 5. Ejecutar la Aplicación
```bash
# Iniciar servidor backend
python app.py

# Abrir frontend
# Hacer doble clic en index.html o abrir en navegador
```

---

## 📖 Guía de Uso

### Búsqueda de Países
1. En la pestaña **"Buscar Países"**, ingresa el nombre del país deseado
2. Haz clic en **"Buscar"** para filtrar los resultados
3. Explora la información mostrada: nombre, capital, región y bandera

### Gestión de Favoritos
1. Desde cualquier país mostrado, haz clic en **"⭐ Agregar a Favoritos"**
2. En el modal que aparece, agrega un comentario personal (opcional)
3. Confirma con **"Agregar a Favoritos"**
4. Ve a la pestaña **"Mis Favoritos"** para ver tus países guardados
5. Usa **"🗑️ Eliminar"** para remover países de favoritos

---

## 🔌 Documentación de la API

### Base URL
```
http://localhost:8000
```

### Endpoints Disponibles

#### `GET /`
Verificación de estado del servidor
```json
{
  "message": "API de Países Favoritos - Funcionando correctamente"
}
```

#### `GET /paises-favoritos`
Obtener todos los países favoritos
```json
[
  {
    "id": 1,
    "nombre": "Colombia",
    "capital": "Bogotá",
    "region": "Americas",
    "comentario": "Excelente cultura",
    "fecha_agregado": "2025-07-18 10:56:21"
  }
]
```

#### `POST /paises-favoritos`
Agregar nuevo país a favoritos
```json
// Request Body
{
  "nombre": "Costa Rica",
  "capital": "San José",
  "region": "Americas",
  "comentario": "País muy verde y pacífico"
}

// Response
{
  "id": 2,
  "nombre": "Costa Rica",
  "capital": "San José",
  "region": "Americas",
  "comentario": "País muy verde y pacífico",
  "fecha_agregado": "2025-07-18 11:30:15"
}
```

#### `DELETE /paises-favoritos/{id}`
Eliminar país de favoritos
```json
{
  "message": "País eliminado de favoritos"
}
```

#### `GET /paises-favoritos/{id}`
Obtener país favorito específico
```json
{
  "id": 1,
  "nombre": "Colombia",
  "capital": "Bogotá",
  "region": "Americas",
  "comentario": "Excelente cultura",
  "fecha_agregado": "2025-07-18 10:56:21"
}
```

---

## 🌐 API Externa Utilizada

**RestCountries API**
- **URL:** https://restcountries.com/
- **Endpoint:** `https://restcountries.com/v3.1/all?fields=name,capital,region,flags`
- **Descripción:** Proporciona información completa sobre todos los países del mundo
- **Datos obtenidos:** Nombre, capital, región y bandera de cada país

---

## 📁 Estructura del Proyecto

```
Grupal3Esteban/
├── app.py                 # Servidor FastAPI con toda la lógica del backend
├── index.html             # Frontend completo (HTML + CSS + JavaScript)
├── requirements.txt       # Dependencias de Python
├── database_setup.sql     # Script opcional para configurar MySQL
└── README.md             # Documentación del proyecto
```

---

## ✅ Cumplimiento de Requerimientos

### Requerimientos Funcionales Completados

1. **✅ Conexión a API externa pública (GET)**
   - Integración con RestCountries API
   - Búsqueda y filtrado de países en tiempo real

2. **✅ Creación de API propia (CRUD mínimo)**
   - Endpoints POST y GET implementados
   - Operaciones CREATE y READ funcionalmente completas
   - Funcionalidad DELETE adicional para mejor UX

3. **✅ Visualización de datos**
   - Interfaz clara con separación entre datos externos e internos
   - Pestañas diferenciadas para cada fuente de datos

4. **✅ Formulario de ingreso**
   - Modal interactivo para captura de comentarios
   - Envío de datos a API propia via POST

### Tecnologías Obligatorias Implementadas

- **✅ Frontend:** HTML, CSS, JavaScript (Vanilla)
- **✅ Backend:** Python con FastAPI
- **✅ Base de datos:** MySQL
- **✅ ORM/Conexión:** mysql-connector-python
- **✅ Control de versiones:** Git y GitHub

---

## 🔧 Solución de Problemas

### Errores Comunes

**Error de conexión a MySQL**
```bash
# Verificar que MySQL esté ejecutándose
# Confirmar credenciales en app.py
# Asegurar que la base de datos 'paises_db' existe
```

**Frontend no conecta con backend**
```bash
# Verificar que el servidor esté corriendo en puerto 8000
python app.py
# Confirmar en http://localhost:8000
```

**Países no se guardan**
```bash
# Verificar conexión a base de datos
# Revisar logs en terminal del servidor
# Confirmar que la tabla 'paises_favoritos' existe
```

---

##  Valor Académico

Este proyecto demuestra competencias en:

- **Desarrollo Full-Stack**: Integración completa frontend-backend-database
- **Consumo de APIs REST**: Manejo de APIs externas y creación de APIs propias
- **Gestión de Bases de Datos**: Diseño, implementación y operaciones CRUD
- **Programación Asíncrona**: Manejo de requests HTTP asíncronos
- **Diseño de Interfaces**: UX/UI intuitivo y responsive
- **Documentación Técnica**: README completo y comentarios en código

---

##  Notas de Desarrollo

- **Arquitectura:** Separación clara entre capas de presentación, lógica de negocio y persistencia
- **Seguridad:** Configuración de CORS para desarrollo local
- **Escalabilidad:** Estructura preparada para extensiones futuras
- **Mantenibilidad:** Código bien documentado y organizado
- **Compatibilidad:** Funciona en navegadores modernos y sistemas operativos principales

---

##  Conclusión

El proyecto **Buscador de Países** cumple exitosamente con todos los requerimientos establecidos en las especificaciones del Trabajo Grupal #3. La aplicación demuestra una integración efectiva entre tecnologías frontend y backend, proporcionando una experiencia de usuario fluida y funcional.

A pesar de las dificultades de comunicación con el equipo asignado, el desarrollo se completó dentro del plazo establecido, manteniendo altos estándares de calidad en código, documentación y funcionalidad.

**Desarrollado  por:** Esteban G. Saborío  
**LEAD University - Julio 2025**