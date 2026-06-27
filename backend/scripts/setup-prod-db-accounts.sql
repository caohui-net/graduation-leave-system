-- 生产环境数据库账号隔离设置
-- 执行前提：使用超级用户或具有CREATEDB/CREATEROLE权限的账号

-- ============================================
-- 1. 创建应用账号（受限权限）
-- ============================================
CREATE USER app_prod_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';

-- 授予连接权限
GRANT CONNECT ON DATABASE graduation_prod TO app_prod_user;

-- 授予schema使用权限
GRANT USAGE ON SCHEMA public TO app_prod_user;

-- 授予表级DML权限（SELECT/INSERT/UPDATE/DELETE）
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_prod_user;

-- 授予序列使用权限（用于自增ID）
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_prod_user;

-- 设置默认权限（新建表自动授权）
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_prod_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_prod_user;

-- ============================================
-- 2. 创建迁移账号（DDL权限）
-- ============================================
CREATE USER migration_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';

-- 授予完整权限（仅发布时使用）
GRANT CONNECT ON DATABASE graduation_prod TO migration_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO migration_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO migration_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO migration_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO migration_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO migration_user;

-- ============================================
-- 3. 创建只读账号（监控/报表）
-- ============================================
CREATE USER readonly_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';

GRANT CONNECT ON DATABASE graduation_prod TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO readonly_user;

-- ============================================
-- 4. 验证权限设置
-- ============================================

-- 验证应用账号无DDL权限
-- SELECT has_table_privilege('app_prod_user', 'users', 'CREATE');
-- 应返回 false

-- 验证迁移账号有DDL权限
-- SELECT has_table_privilege('migration_user', 'users', 'CREATE');
-- 应返回 true

-- 验证只读账号仅有SELECT权限
-- SELECT has_table_privilege('readonly_user', 'users', 'INSERT');
-- 应返回 false

-- ============================================
-- 5. 安全建议
-- ============================================

-- 修改密码（执行后立即执行）
-- ALTER USER app_prod_user PASSWORD 'STRONG_PASSWORD_HERE';
-- ALTER USER migration_user PASSWORD 'STRONG_PASSWORD_HERE';
-- ALTER USER readonly_user PASSWORD 'STRONG_PASSWORD_HERE';

-- 限制连接来源（可选）
-- ALTER USER app_prod_user CONNECTION LIMIT 50;
-- ALTER USER migration_user CONNECTION LIMIT 2;
-- ALTER USER readonly_user CONNECTION LIMIT 10;
