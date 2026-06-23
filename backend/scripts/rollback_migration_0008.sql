-- Rollback script for migration 0008: application_type and stay_* fields
-- WARNING: This will drop columns and lose data. Only use in emergency.
-- Execute with: psql -U postgres -d graduation_prod < rollback_migration_0008.sql

BEGIN;

-- Drop indexes first
DROP INDEX IF EXISTS applications_application_type_idx;

-- Drop new columns
ALTER TABLE applications_application DROP COLUMN IF EXISTS stay_reason;
ALTER TABLE applications_application DROP COLUMN IF EXISTS stay_end_date;
ALTER TABLE applications_application DROP COLUMN IF EXISTS stay_start_date;
ALTER TABLE applications_application DROP COLUMN IF EXISTS application_type;

-- Record rollback
INSERT INTO django_migrations (app, name, applied)
VALUES ('applications', '0008_rollback', NOW())
ON CONFLICT DO NOTHING;

COMMIT;
