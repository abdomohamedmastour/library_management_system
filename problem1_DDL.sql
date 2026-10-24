CREATE DATABASE IF NOT EXISTS company;
USE company;

CREATE TABLE Department (
    Dnumber INT PRIMARY KEY,
    Dname VARCHAR(50) NOT NULL,
    mgr_ssn INT,
    mgr_start_date DATE
);

CREATE TABLE Employee (
    ssn INT PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    bdate DATE,
    address VARCHAR(100),
    gender CHAR(1),
    salary DECIMAL(10,2),
    Dno INT,
    FOREIGN KEY (Dno) REFERENCES Department(Dnumber) ON DELETE SET NULL ON UPDATE CASCADE
);

ALTER TABLE Department
ADD CONSTRAINT fk_dept_mgr
FOREIGN KEY (mgr_ssn) REFERENCES Employee(ssn) ON DELETE SET NULL ON UPDATE CASCADE;

CREATE TABLE Project (
    Pnumber INT PRIMARY KEY,
    Pname VARCHAR(50) NOT NULL,
    Plocation VARCHAR(100),
    Dno INT,
    FOREIGN KEY (Dno) REFERENCES Department(Dnumber) ON DELETE CASCADE ON UPDATE CASCADE
);