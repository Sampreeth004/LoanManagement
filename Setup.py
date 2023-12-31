import mysql.connector

# Replace these values with your MySQL server details
host = 'localhost'
user = 'root'
password = 'nanu2004'

# Connect to MySQL server
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password
)

# Create a cursor object to interact with the MySQL server
cursor = conn.cursor()

# Name of the database to be created
database_name = 'LoanManager'

try:
    # Create the database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database '{database_name}' created successfully")
    
    # Switch to the LoanManager database
    cursor.execute(f"USE {database_name}")

    # Create the 'Roles' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Roles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            role_name VARCHAR(255) NOT NULL
        )
    """)
    print("Table 'Roles' created successfully")

    # Check if the entry with id=1 already exists in the 'Roles' table
    cursor.execute("SELECT id FROM Roles WHERE id = 1")
    result = cursor.fetchone()

    # If the entry doesn't exist, insert it
    if result is None:
        # Insert an entry into the 'Roles' table
        cursor.execute("""
            INSERT INTO Roles (id, role_name) VALUES (%s, %s)
        """, (1, 'SuperAdmin'))
        print("Entry inserted into 'Roles' table successfully")
    else:
        print("Entry with id=1 already exists in 'Roles' table")


     # Create the 'Users' table with foreign key reference to 'Roles'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role_id INT,
            is_approved BOOLEAN,
            FOREIGN KEY (role_id) REFERENCES Roles(id)
        )
    """)
    print("Table 'Users' created successfully")
    
    # Check if the entry with id=1 already exists in the 'Users' table
    cursor.execute("SELECT id FROM Users WHERE id = 1")
    result = cursor.fetchone()

    # If the entry doesn't exist, insert it
    if result is None:
        # Insert an entry into the 'Users' table
        cursor.execute("""
            INSERT INTO Users (id, username, password, role_id, is_approved)
            VALUES (%s, %s, %s, %s, %s)
        """, (1, 'super', 'superadmin123', 0000, True))
        print("Entry inserted into 'Users' table successfully")
    else:
        print("Entry with id=1 already exists in 'Users' table")

    # Create the 'Borrowers' table with foreign key reference to 'Users'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Borrowers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            phone_number VARCHAR(20),
            address TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)
    print("Table 'Borrowers' created successfully")

    # Create the 'User_Activity_Log' table with foreign key reference to 'Users'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User_Activity_Log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            activity_type VARCHAR(255) NOT NULL,
            activity_description TEXT,
            activity_date DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)
    print("Table 'User_Activity_Log' created successfully")

    # Create the 'Loan_Applications' table with foreign key reference to 'Borrowers'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_Applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            borrower_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            purpose VARCHAR(255),
            application_date DATE NOT NULL,
            status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
            FOREIGN KEY (borrower_id) REFERENCES Borrowers(id)
        )
    """)
    print("Table 'Loan_Applications' created successfully")

    # Create the 'Loans' table with foreign key references to 'Borrowers' and 'Loan_Applications'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            borrower_id INT,
            loan_application_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            interest_rate DECIMAL(5, 2) NOT NULL,
            term_months INT NOT NULL,
            start_date DATE NOT NULL,
            status ENUM('active', 'closed') NOT NULL DEFAULT 'active',
            FOREIGN KEY (borrower_id) REFERENCES Borrowers(id),
            FOREIGN KEY (loan_application_id) REFERENCES Loan_Applications(id)
        )
    """)
    print("Table 'Loans' created successfully")

    # Create the 'Collaterals' table with foreign key reference to 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Collaterals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            description VARCHAR(255),
            estimated_value DECIMAL(10, 2),
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Collaterals' created successfully")

     # Create the 'Loan_History' table with foreign key reference to 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_History (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            event_date DATETIME NOT NULL,
            event_description TEXT,
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Loan_History' created successfully")

    # Create the 'Loan_Repayment_Schedule' table with foreign key reference to 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_Repayment_Schedule (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            installment_number INT NOT NULL,
            due_date DATE NOT NULL,
            amount_due DECIMAL(10, 2) NOT NULL,
            status ENUM('pending', 'paid') NOT NULL DEFAULT 'pending',
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Loan_Repayment_Schedule' created successfully")

    # Create the 'Loan_Approval_History' table with foreign key references to 'Loans' and 'Users'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_Approval_History (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            approval_date DATETIME NOT NULL,
            approved_by_user_id INT,
            status ENUM('approved', 'rejected') NOT NULL,
            comments TEXT,
            FOREIGN KEY (loan_id) REFERENCES Loans(id),
            FOREIGN KEY (approved_by_user_id) REFERENCES Users(id)
        )
    """)
    print("Table 'Loan_Approval_History' created successfully")

    # Create the 'Payments' table with foreign key reference to 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            amount DECIMAL(10, 2) NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Payments' created successfully")

    # Create the 'Loan_Documents' table with foreign key reference to 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_Documents (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            document_name VARCHAR(255) NOT NULL,
            document_path VARCHAR(255) NOT NULL,
            upload_date DATETIME NOT NULL,
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Loan_Documents' created successfully")

     # Create the 'Late_Payments' table with foreign key references to 'Loans' and 'Payments'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Late_Payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            payment_id INT,
            late_fee DECIMAL(10, 2) NOT NULL,
            late_fee_date DATETIME NOT NULL,
            FOREIGN KEY (loan_id) REFERENCES Loans(id),
            FOREIGN KEY (payment_id) REFERENCES Payments(id)
        )
    """)
    print("Table 'Late_Payments' created successfully")

    # Create the 'Loan_Audit_Trail' table with foreign key reference to 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_Audit_Trail (
            id INT AUTO_INCREMENT PRIMARY KEY,
            loan_id INT,
            event_type VARCHAR(255) NOT NULL,
            event_description TEXT,
            event_date DATETIME NOT NULL,
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Loan_Audit_Trail' created successfully")

     # Create the 'Loan_Comments' table with foreign key references to 'Users' and 'Loans'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Loan_Comments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            loan_id INT,
            comment_text TEXT NOT NULL,
            comment_date DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (loan_id) REFERENCES Loans(id)
        )
    """)
    print("Table 'Loan_Comments' created successfully")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()