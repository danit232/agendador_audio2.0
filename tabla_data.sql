
-- Crear la database clientes`
CREATE DATABASE IF NOT EXISTS `crud_clientes`;
USE `crud_clientes`;

-- Crear la tabla `clientes`
CREATE TABLE `clientes` (
  `nombreCompleto` varchar(225),
  `celular` varchar(10) NOT NULL,  -- Llave primaria
  `cedula` varchar(10) NOT NULL,  -- Llave primaria
  `email` varchar(255),
  `fecha_hora` DATETIME NOT NULL,
  PRIMARY KEY (`celular`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;