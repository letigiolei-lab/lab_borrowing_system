-- Laboratory Equipment Borrowing Management System Database
CREATE DATABASE IF NOT EXISTS lab_borrowing_db;
USE lab_borrowing_db;

-- Users / Authentication table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('Administrator', 'Staff') NOT NULL DEFAULT 'Staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 1: Equipment / Items
CREATE TABLE IF NOT EXISTS equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_code VARCHAR(20) NOT NULL UNIQUE,
    item_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    total_qty INT NOT NULL DEFAULT 1,
    available_qty INT NOT NULL DEFAULT 1,
    condition_status ENUM('Good', 'Fair', 'Damaged') DEFAULT 'Good'
);

-- Table 2: Borrowers (Students / Faculty)
CREATE TABLE IF NOT EXISTS borrowers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_number VARCHAR(30) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    contact_number VARCHAR(20) NOT NULL
);

-- Table 3: Borrow Transactions / Loans
CREATE TABLE IF NOT EXISTS borrow_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    borrower_id INT NOT NULL,
    equipment_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    expected_return_date DATE NOT NULL,
    actual_return_date DATETIME NULL,
    status ENUM('Borrowed', 'Returned', 'Overdue') DEFAULT 'Borrowed',
    issued_by_user_id INT NOT NULL,
    remarks VARCHAR(255) DEFAULT '',
    FOREIGN KEY (borrower_id) REFERENCES borrowers(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE,
    FOREIGN KEY (issued_by_user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Seed Data (Default passwords hashed with SHA-256: 'admin123' and 'staff123')
-- admin123 hash: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9
-- staff123 hash: 24e393a5c2d3a3f5a5e363673c683b27b9c6f2430030580971a8f6834b68427f
INSERT IGNORE INTO users (username, password_hash, full_name, role) VALUES 
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Lab Head Administrator', 'Administrator'),
('staff', '24e393a5c2d3a3f5a5e363673c683b27b9c6f2430030580971a8f6834b68427f', 'Lab Assistant Staff', 'Staff');

INSERT IGNORE INTO equipment (item_code, item_name, category, total_qty, available_qty, condition_status) VALUES
('EQ-MIC-01', 'Binocular Microscope', 'Biology', 10, 8, 'Good'),
('EQ-OSC-01', 'Digital Oscilloscope 100MHz', 'Electronics', 6, 6, 'Good'),
('EQ-MUL-01', 'Digital Multimeter', 'Electronics', 15, 14, 'Good'),
('EQ-BUN-01', 'Bunsen Burner Kit', 'Chemistry', 12, 12, 'Good'),
('EQ-CAL-01', 'Vernier Caliper', 'Physics', 20, 19, 'Good');

INSERT IGNORE INTO borrowers (id_number, full_name, department, contact_number) VALUES
('STU-2024-001', 'Juan Dela Cruz', 'Computer Engineering', '09171234567'),
('STU-2024-002', 'Maria Santos', 'Chemical Engineering', '09187654321'),
('FAC-2022-005', 'Engr. Roberto Reyes', 'Electronics Department', '09223334444');

INSERT IGNORE INTO borrow_records (borrower_id, equipment_id, quantity, borrow_date, expected_return_date, status, issued_by_user_id, remarks) VALUES
(1, 1, 2, NOW(), DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'Borrowed', 1, 'For BioLab experiment'),
(2, 3, 1, NOW(), DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'Borrowed', 2, 'Field circuit testing');
