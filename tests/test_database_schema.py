import unittest
import sqlite3

class TestDatabaseSchema(unittest.TestCase):

    def setUp(self):
        # This will run before each test
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.create_schemas()

    def tearDown(self):
        # This will run after each test
        self.connection.close()

    def create_schemas(self):
        # Create the users table
        self.cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create the roles table
        self.cursor.execute('''
            CREATE TABLE roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT NOT NULL UNIQUE
            )
        ''')
        # Create the user_roles table with foreign keys
        self.cursor.execute('''
            CREATE TABLE user_roles (
                user_id INTEGER,
                role_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (role_id) REFERENCES roles(role_id),
                PRIMARY KEY (user_id, role_id)
            )
        ''')

    def test_create_users_table(self):
        # Verify the users table has been created correctly
        self.cursor.execute("PRAGMA table_info(users);")
        columns = self.cursor.fetchall()
        expected_columns = [
            (0, 'user_id', 'INTEGER', 0, None, 1),
            (1, 'username', 'TEXT', 1, None, 0),
            (2, 'email', 'TEXT', 1, None, 0),
            (3, 'password_hash', 'TEXT', 1, None, 0),
            (4, 'created_at', 'TIMESTAMP', 0, "CURRENT_TIMESTAMP", 0),
            (5, 'updated_at', 'TIMESTAMP', 0, "CURRENT_TIMESTAMP", 0),
        ]
        self.assertEqual(columns, expected_columns)

    def test_create_roles_table(self):
        # Verify the roles table has been created correctly
        self.cursor.execute("PRAGMA table_info(roles);")
        columns = self.cursor.fetchall()
        expected_columns = [
            (0, 'role_id', 'INTEGER', 0, None, 1),
            (1, 'role_name', 'TEXT', 1, None, 0),
        ]
        self.assertEqual(columns, expected_columns)

    def test_create_user_roles_table(self):
        # Verify the user_roles table has been created correctly with foreign key linkages
        self.cursor.execute("PRAGMA table_info(user_roles);")
        columns = self.cursor.fetchall()
        expected_columns = [
            (0, 'user_id', 'INTEGER', 1, None, 0),
            (1, 'role_id', 'INTEGER', 1, None, 0),
        ]
        self.assertEqual(columns, expected_columns)

        # Verify the foreign keys
        self.cursor.execute("PRAGMA foreign_key_list(user_roles);")
        foreign_keys = self.cursor.fetchall()
        expected_foreign_keys = [
            (0, 'users', 'user_id', 'user_id', 0, 'NO ACTION', 'NO ACTION'),
            (1, 'roles', 'role_id', 'role_id', 0, 'NO ACTION', 'NO ACTION'),
        ]
        self.assertEqual(foreign_keys, expected_foreign_keys)

    def test_apply_schema_changes(self):
        # For this, we would typically ensure that any schema changes are applied without errors
        # In this case, we are verifying that the tables created successfully
        try:
            self.create_schemas()
            success = True
        except Exception as e:
            success = False
            print("An error occurred: ", e)
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()
