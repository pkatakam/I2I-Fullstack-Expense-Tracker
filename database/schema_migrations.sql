-- schema_migrations.sql

-- This file will contain necessary migrations scripts to ensure the schema is up to date.

-- Applied migrations table
CREATE TABLE IF NOT EXISTS schema_migrations (
    migration_id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Function to check if a migration has been applied
CREATE OR REPLACE FUNCTION has_migration_been_applied(migration_name VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    migration_count INT;
BEGIN
    SELECT COUNT(*)
    INTO migration_count
    FROM schema_migrations
    WHERE migration_name = migration_name;

    IF migration_count > 0 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Example migration script execution

-- Replace 'migration_name_example' with the unique name for your migration
DO $$
BEGIN
    IF NOT has_migration_been_applied('create_users_table') THEN
        -- Users table creation script
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );

        -- Record migration as applied
        INSERT INTO schema_migrations (migration_name)
        VALUES ('create_users_table');
    END IF;
END;
$$;

DO $$
BEGIN
    IF NOT has_migration_been_applied('create_roles_table') THEN
        -- Roles table creation script
        CREATE TABLE IF NOT EXISTS roles (
            role_id SERIAL PRIMARY KEY,
            role_name VARCHAR(255) NOT NULL UNIQUE
        );

        -- Record migration as applied
        INSERT INTO schema_migrations (migration_name)
        VALUES ('create_roles_table');
    END IF;
END;
$$;

DO $$
BEGIN
    IF NOT has_migration_been_applied('create_user_roles_table') THEN
        -- User roles table creation script
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INT NOT NULL,
            role_id INT NOT NULL,
            PRIMARY KEY (user_id, role_id),
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (role_id) REFERENCES roles (role_id)
        );

        -- Record migration as applied
        INSERT INTO schema_migrations (migration_name)
        VALUES ('create_user_roles_table');
    END IF;
END;
$$;

-- Add any additional migrations as separate DO blocks following the above pattern.
