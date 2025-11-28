CREATE TABLE IF NOT EXISTS usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120),
    role ENUM('admin', 'empleado') DEFAULT 'empleado',
    departamento VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_cliente VARCHAR(100),
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pedidos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    tipo VARCHAR(50),
    estatus VARCHAR(50) DEFAULT 'Generado',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    direccion_envio TEXT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS unidades(
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    placas VARCHAR(20),
    chofer_id INT,
    FOREIGN KEY (chofer_id) REFERENCES usuarios(id)
        ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS etiquetas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    color VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS pedido_etiqueta(
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    etiqueta_id INT NOT NULL,

    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        ON DELETE CASCADE,
    FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logs(
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(255),
    detalles TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE SET NULL
);