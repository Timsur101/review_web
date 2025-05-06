CREATE DATABASE IF NOT EXISTS review_web;
USE review_web;

CREATE TABLE IF NOT EXISTS users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'reviewer', 'admin') NOT NULL DEFAULT 'student'
)

CREATE TABLE IF NOT EXISTS projects (
    id_project INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    author_id INT NOT NULL,
    repository_url VARCHAR(255)
)

CREATE TABLE reviews (
    id_review INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    rating TINYINT CHECK (rating BETWEEN 1 AND 10),
    comment TEXT
)