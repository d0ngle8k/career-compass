-- Create UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create auth_provider enum
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'auth_provider') THEN
        CREATE TYPE auth_provider AS ENUM ('email', 'google', 'github');
    END IF;
END $$;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    avatar_url TEXT,
    provider auth_provider NOT NULL DEFAULT 'email',
    provider_id VARCHAR(255),
    password_hash VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Constraints: email provider must have password, OAuth providers must have provider_id
    CONSTRAINT valid_email_provider CHECK (
        (provider = 'email' AND password_hash IS NOT NULL) OR
        (provider IN ('google', 'github') AND provider_id IS NOT NULL)
    ),
    
    -- Unique constraint for OAuth providers to prevent duplicates
    UNIQUE(provider, provider_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_provider_id ON users(provider, provider_id);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Insert default admin user (will be overridden by env var in production)
INSERT INTO users (email, password_hash, provider, name)
VALUES (
    'admin@careercompass.local',
    'admin123',  -- This should be hashed in production
    'email',
    'System Admin'
) ON CONFLICT (email) DO NOTHING;
