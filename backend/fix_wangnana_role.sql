-- 修正王娜娜用户角色
UPDATE users_user 
SET role = 'counselor' 
WHERE name = '王娜娜' AND role = 'teacher';

-- 验证修改
SELECT user_id, name, role FROM users_user WHERE name = '王娜娜';
