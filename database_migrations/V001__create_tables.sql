-- V001__create_tables.sql
-- Flyway migration: creates the `seashells` and `users` tables

CREATE TABLE seashells (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  species TEXT,
  description TEXT,
  personal_notes TEXT,
  date_found DATE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
);
