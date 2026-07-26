-- ================================================================
-- Atharva Digital & Photo Studio - Database Schema
-- ================================================================
-- Requires MySQL 8.0.16+ for CHECK constraint enforcement.
-- Run: SELECT VERSION();  to confirm before executing.
-- ================================================================

CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

-- ---------------- CUSTOMERS TABLE ----------------
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    phone       VARCHAR(10)  NOT NULL,
    address     VARCHAR(200),
    CONSTRAINT chk_phone_10digit CHECK (phone REGEXP '^[0-9]{10}$')
);

-- ---------------- ORDERS TABLE ----------------
CREATE TABLE orders (
    order_id    INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    service     VARCHAR(100),
    amount      INT,
    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);
