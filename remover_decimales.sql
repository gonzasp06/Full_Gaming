-- Script para remover decimales de toda la BD
-- Cambiar DECIMAL(10,2) a INT en todas las tablas de precios

ALTER TABLE `producto` MODIFY COLUMN `precio` INT NOT NULL DEFAULT 0;

ALTER TABLE `pedidos` MODIFY COLUMN `total` INT NOT NULL DEFAULT 0;

ALTER TABLE `pedido_items` MODIFY COLUMN `precio` INT NOT NULL DEFAULT 0;
ALTER TABLE `pedido_items` MODIFY COLUMN `subtotal` INT NOT NULL DEFAULT 0;

-- Actualizar datos existentes (quitar decimales)
UPDATE `producto` SET `precio` = ROUND(`precio`);
UPDATE `pedidos` SET `total` = ROUND(`total`);
UPDATE `pedido_items` SET `precio` = ROUND(`precio`);
UPDATE `pedido_items` SET `subtotal` = ROUND(`subtotal`);

-- Verificar que se aplicaron los cambios
SELECT 'Cambios completados' AS status;
