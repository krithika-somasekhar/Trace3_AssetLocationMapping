-- Create Database and Use It
CREATE DATABASE IF NOT EXISTS AssetManagement;
USE AssetManagement;

-- Drop Tables if They Exist (Reverse Dependency Order for Foreign Keys)
DROP TABLE IF EXISTS Contract;
DROP TABLE IF EXISTS Asset;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS Department;
DROP TABLE IF EXISTS Map;
DROP TABLE IF EXISTS AssetThumbnail;

-- Create Tables with Relationships

-- Asset Thumbnail Table
CREATE TABLE AssetThumbnail (
    asset_thumb_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_thumb_name VARCHAR(255) NOT NULL,
    asset_thumb_url VARCHAR(500) NOT NULL
);

-- Map Table (without map_company)
CREATE TABLE Map (
    map_id INT PRIMARY KEY AUTO_INCREMENT,
    map_building VARCHAR(255) NOT NULL,
    map_floor INT NOT NULL,
    map_url VARCHAR(500) NOT NULL
);

-- Room Table
CREATE TABLE Room (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_name VARCHAR(255) NOT NULL,
    room_floor_no INT NOT NULL,
    room_shape ENUM('rectangle', 'semicircle', 'square') NOT NULL,
    r_coordinates VARCHAR(255) NOT NULL,
    map_id INT,
    FOREIGN KEY (map_id) REFERENCES Map(map_id) ON DELETE SET NULL
);

-- Department Table
CREATE TABLE Department (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(255) NOT NULL,
    map_id INT,
    d_coordinates VARCHAR(255) NOT NULL,
    FOREIGN KEY (map_id) REFERENCES Map(map_id) ON DELETE SET NULL
);

-- Asset Table
CREATE TABLE Asset (
    asset_id INT PRIMARY KEY AUTO_INCREMENT,
    asset_name VARCHAR(255) NOT NULL,
    asset_type VARCHAR(100) NOT NULL,
    asset_thumb_id INT,
    room_id INT,
    FOREIGN KEY (asset_thumb_id) REFERENCES AssetThumbnail(asset_thumb_id) ON DELETE SET NULL,
    FOREIGN KEY (room_id) REFERENCES Room(room_id) ON DELETE SET NULL
);

-- Contract Table
CREATE TABLE Contract (
    contract_id INT PRIMARY KEY AUTO_INCREMENT,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_expired_flag BOOLEAN DEFAULT FALSE,
    asset_id INT,
    FOREIGN KEY (asset_id) REFERENCES Asset(asset_id) ON DELETE CASCADE
);
