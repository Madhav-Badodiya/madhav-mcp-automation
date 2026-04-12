-- =============================================
-- Project  : madhav-mcp-automation
-- Author   : Person 2 (Madhav Badodiya)
-- Branch   : feature/sql-integration
-- Purpose  : Full database schema + seed data
-- Run on   : localhost\SQLEXPRESS via SSMS
-- =============================================

-- ─────────────────────────────────────────
-- STEP 1: Create Database on D Drive
-- ─────────────────────────────────────────
CREATE DATABASE madhav_test_data
ON PRIMARY (
    NAME = madhav_test_data,
    FILENAME = 'D:\madhav-mcp-database-Integration\db\madhav_test_data.mdf'
)
LOG ON (
    NAME = madhav_test_data_log,
    FILENAME = 'D:\madhav-mcp-database-Integration\db\madhav_test_data_log.ldf'
);
GO

USE madhav_test_data;
GO

-- ─────────────────────────────────────────
-- STEP 2: Create Tables
-- ─────────────────────────────────────────

-- Table 1: Login credentials for automation tests
CREATE TABLE test_users (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    email       VARCHAR(100) NOT NULL,
    password    VARCHAR(100) NOT NULL,
    role        VARCHAR(50)  NOT NULL
);
GO

-- Table 2: Products for cart and checkout tests
CREATE TABLE test_products (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    category    VARCHAR(50)   NOT NULL,
    price       DECIMAL(10,2) NOT NULL
);
GO

-- ─────────────────────────────────────────
-- STEP 3: Seed Data
-- ─────────────────────────────────────────

INSERT INTO test_users (email, password, role) VALUES
    ('rahulshetty@gmail.com', 'Iamking@000', 'admin');
GO

INSERT INTO test_products (name, category, price) VALUES
    ('ZARA COAT 3',     'fashion',     31500.00),
    ('iphone 13 pro',   'electronics', 231500.00),
    ('ADIDAS ORIGINAL', 'fashion',     31500.00);
GO

-- ─────────────────────────────────────────
-- STEP 4: Verify
-- ─────────────────────────────────────────
SELECT * FROM test_users;
SELECT * FROM test_products;