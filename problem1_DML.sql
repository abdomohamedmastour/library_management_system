USE company;

INSERT INTO Department (Dnumber, Dname, mgr_start_date) VALUES (1, 'HR', '2022-01-01');
INSERT INTO Department (Dnumber, Dname, mgr_start_date) VALUES (2, 'IT', '2021-05-15');
INSERT INTO Department (Dnumber, Dname, mgr_start_date) VALUES (3, 'Finance', '2023-03-10');

INSERT INTO Employee (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES (101, 'Ahmed', 'Ali', '1990-05-12', 'Cairo', 'M', 8000.00, 2);
INSERT INTO Employee (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES (102, 'Sara', 'Mohamed', '1995-08-20', 'Alexandria', 'F', 6500.00, 1);
INSERT INTO Employee (ssn, fname, lname, bdate, address, gender, salary, Dno) VALUES (103, 'Omar', 'Khaled', '1988-12-05', 'Giza', 'M', 9500.00, 3);

UPDATE Department SET mgr_ssn = 102 WHERE Dnumber = 1;
UPDATE Department SET mgr_ssn = 101 WHERE Dnumber = 2;
UPDATE Department SET mgr_ssn = 103 WHERE Dnumber = 3;

INSERT INTO Project (Pnumber, Pname, Plocation, Dno) VALUES (10, 'Alpha', 'Cairo', 2);
INSERT INTO Project (Pnumber, Pname, Plocation, Dno) VALUES (20, 'Beta', 'Alexandria', 1);
INSERT INTO Project (Pnumber, Pname, Plocation, Dno) VALUES (30, 'Gamma', 'Aswan', 3);