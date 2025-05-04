-- File: backend/db/schema.sql

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enable Row-Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create the RLS policy
CREATE POLICY user_rls_policy ON users
    USING (id = current_setting('app.current_user_id', true)::INT);

-- Optional: future admin-only view
-- CREATE POLICY admin_read_all ON users FOR SELECT TO admin_role USING (true);
