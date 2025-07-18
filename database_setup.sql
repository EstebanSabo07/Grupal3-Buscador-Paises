-- ========================================
-- SCRIPT SQL PARA TRABAJO GRUPAL #3
-- Buscador de Países - LEAD University
-- Desarrollado por: Esteban G. Saborío
-- ========================================

-- 1. CREAR BASE DE DATOS
CREATE DATABASE IF NOT EXISTS paises_db;

-- 2. SELECCIONAR LA BASE DE DATOS
USE paises_db;

-- 3. CREAR TABLA DE PAÍSES FAVORITOS
CREATE TABLE IF NOT EXISTS paises_favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único del país favorito',
    nombre VARCHAR(255) NOT NULL COMMENT 'Nombre del país',
    capital VARCHAR(255) NOT NULL COMMENT 'Capital del país',
    region VARCHAR(255) NOT NULL COMMENT 'Región geográfica del país',
    comentario TEXT COMMENT 'Comentario personal del usuario sobre el país',
    fecha_agregado DATETIME NOT NULL COMMENT 'Fecha y hora cuando se agregó a favoritos',
    INDEX idx_nombre (nombre) COMMENT 'Índice para búsquedas por nombre',
    INDEX idx_fecha (fecha_agregado) COMMENT 'Índice para ordenar por fecha'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabla para almacenar países favoritos de los usuarios';

-- 4. VERIFICAR ESTRUCTURA DE LA TABLA
DESCRIBE paises_favoritos;

-- 5. CONSULTAS DE VERIFICACIÓN
-- Ver todos los países favoritos
SELECT * FROM paises_favoritos ORDER BY fecha_agregado DESC;

-- Contar total de países favoritos
SELECT COUNT(*) as total_favoritos FROM paises_favoritos;

-- Ver países favoritos por región
SELECT region, COUNT(*) as cantidad 
FROM paises_favoritos 
GROUP BY region 
ORDER BY cantidad DESC;

-- 6. DATOS DE PRUEBA (OPCIONAL)
-- Insertar algunos países de ejemplo para pruebas
INSERT INTO paises_favoritos (nombre, capital, region, comentario, fecha_agregado) VALUES
('Costa Rica', 'San José', 'Americas', 'País hermoso con mucha biodiversidad', NOW()),
('España', 'Madrid', 'Europe', 'Rica cultura e historia', NOW()),
('Japón', 'Tokyo', 'Asia', 'Tecnología avanzada y tradiciones únicas', NOW());

-- 7. CONSULTAS ÚTILES PARA DESARROLLO
-- Buscar países por nombre (similar a la funcionalidad del frontend)
SELECT * FROM paises_favoritos WHERE nombre LIKE '%costa%';

-- Obtener países agregados en los últimos 7 días
SELECT * FROM paises_favoritos 
WHERE fecha_agregado >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY fecha_agregado DESC;

-- Limpiar tabla para empezar de nuevo (usar con cuidado)
-- DELETE FROM paises_favoritos;

-- 8. PROCEDIMIENTOS ALMACENADOS (AVANZADO)
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS AgregarPaisFavorito(
    IN p_nombre VARCHAR(255),
    IN p_capital VARCHAR(255),
    IN p_region VARCHAR(255),
    IN p_comentario TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    -- Verificar si el país ya existe
    IF EXISTS (SELECT 1 FROM paises_favoritos WHERE nombre = p_nombre) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Este país ya está en favoritos';
    END IF;
    
    -- Insertar el nuevo país
    INSERT INTO paises_favoritos (nombre, capital, region, comentario, fecha_agregado)
    VALUES (p_nombre, p_capital, p_region, p_comentario, NOW());
    
    COMMIT;
END //

DELIMITER ;

-- 9. FUNCIÓN PARA OBTENER ESTADÍSTICAS
DELIMITER //

CREATE FUNCTION IF NOT EXISTS ObtenerTotalFavoritos() 
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE total INT DEFAULT 0;
    SELECT COUNT(*) INTO total FROM paises_favoritos;
    RETURN total;
END //

DELIMITER ;

-- ========================================
-- FIN DEL SCRIPT
-- ========================================

-- NOTAS DE USO:
-- 1. Este script debe ejecutarse en MySQL Workbench o línea de comandos MySQL
-- 2. Verificar los permisos para crear bases de datos
-- 3. Los datos de prueba son opcionales, puedes comentar esa sección
-- 4. Los procedimientos almacenados y funciones son características avanzadas