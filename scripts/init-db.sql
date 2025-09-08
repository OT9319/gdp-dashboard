-- Initialize database for GDP Dashboard Constitutional APIs
-- This script sets up the basic database structure

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schema for constitutional APIs
CREATE SCHEMA IF NOT EXISTS constitutional;

-- Grant permissions
GRANT USAGE ON SCHEMA constitutional TO gdp_user;
GRANT CREATE ON SCHEMA constitutional TO gdp_user;
GRANT USAGE ON SCHEMA public TO gdp_user;
GRANT CREATE ON SCHEMA public TO gdp_user;

-- Set search path
ALTER USER gdp_user SET search_path TO constitutional, public;

-- Create initial tables will be handled by SQLAlchemy migrations