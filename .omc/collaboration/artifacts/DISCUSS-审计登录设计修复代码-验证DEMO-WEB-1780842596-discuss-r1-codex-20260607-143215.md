= User.objects.create(user_id='D001', name='学工部', role=UserRole.DEAN)
./backend/apps/applications/tests/test_list_permissions.py:39:        self.dean.
set_password('D001')
./backend/apps/applications/serializers.py:7:    student_id = serializers.CharFi
eld(source='student.user_id', read_only=True)
./backend/apps/applications/serializers.py:18:    student_id = serializers.CharF
ield(source='student.user_id', read_only=True)
./backend/apps/approvals/tests/test_rejection_flow.py:17:            user_id='20
20001',
./backend/apps/approvals/tests/test_rejection_flow.py:18:            password='2
020001',
./backend/apps/approvals/tests/test_rejection_flow.py:29:            user_id='T0
01',
./backend/apps/approvals/tests/test_rejection_flow.py:30:            password='T
001',
./backend/apps/approvals/tests/test_rejection_flow.py:37:            user_id='M0
01',
./backend/apps/approvals/tests/test_rejection_flow.py:38:            password='M
001',
./backend/apps/approvals/tests/test_rejection_flow.py:55:        # Student login
 and submit
./backend/apps/approvals/tests/test_rejection_flow.py:56:        response = self
.client.post('/api/auth/login', {
./backend/apps/approvals/tests/test_rejection_flow.py:57:            'user_id':
'2020001',
./backend/apps/approvals/tests/test_rejection_flow.py:58:            'password':
 '2020001'
./backend/apps/approvals/tests/test_rejection_flow.py:60:        student_token =
 response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:72:        response = self
.client.post('/api/auth/login', {
./backend/apps/approvals/tests/test_rejection_flow.py:73:            'user_id':
'M001',
./backend/apps/approvals/tests/test_rejection_flow.py:74:            'password':
 'M001'
./backend/apps/approvals/tests/test_rejection_flow.py:76:        dorm_manager_to
ken = response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:90:        response = self
.client.post('/api/auth/login', {
./backend/apps/approvals/tests/test_rejection_flow.py:91:            'user_id':
'M001',
./backend/apps/approvals/tests/test_rejection_flow.py:92:            'password':
 'M001'
./backend/apps/approvals/tests/test_rejection_flow.py:94:        dorm_manager_to
ken = response.data['access_token']
./backend/apps/approvals/tests/test_rejection_flow.py:115:        # Counselor lo
gin and reject
./backend/apps/approvals/tests/test_rejection_flow.py:116:        response = sel
f.client.post('/api/auth/login', {
./backend/apps/approvals/tests/test_rejection_flow.py:117:            'user_id':
 'T001',
./backend/apps/approvals/tests/test_rejection_flow.py:118:            'password'
: 'T001'
./backend/apps/approvals/tests/test_rejection_flow.py:120:        counselor_toke
n = response.data['access_token']
./backend/apps/applications/tests/test_constraints.py:15:            user_id='20
20001',
./backend/apps/applications/tests/test_constraints.py:21:            password='2
020001',
./backend/apps/applications/tests/test_constraints.py:28:            user_id='T0
01',
./backend/apps/applications/tests/test_constraints.py:31:            password='T
001',
./backend/apps/applications/tests/test_constraints.py:35:            user_id='M0
01',
./backend/apps/applications/tests/test_constraints.py:38:            password='M
001',
./backend/apps/approvals/tests/test_list_permissions.py:13:        self.student
= User.objects.create(user_id='S001', name='学生', role=UserRole.STUDENT, class_
id='CS2020-01')
./backend/apps/approvals/tests/test_list_permissions.py:14:        self.student.
set_password('S001')
./backend/apps/approvals/tests/test_list_permissions.py:17:        self.counselo
r1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUNSELOR
)
./backend/apps/approvals/tests/test_list_permissions.py:18:        self.counselo
r1.set_password('T001')
./backend/apps/approvals/tests/test_list_permissions.py:21:        self.counselo
r2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUNSELOR
)
./backend/apps/approvals/tests/test_list_permissions.py:22:        self.counselo
r2.set_password('T002')
./backend/apps/approvals/tests/test_list_permissions.py:25:        self.dorm_man
ager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.DORM_M
ANAGER)
./backend/apps/approvals/tests/test_list_permissions.py:26:        self.dorm_man
ager1.set_password('M001')
./backend/apps/approvals/tests/test_list_permissions.py:29:        self.dorm_man
ager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.DORM_M
ANAGER)
./backend/apps/approvals/tests/test_list_permissions.py:30:        self.dorm_man
ager2.set_password('M002')
./backend/apps/approvals/tests/test_list_permissions.py:33:        self.dean1 =
User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
./backend/apps/approvals/tests/test_list_permissions.py:34:        self.dean1.se
t_password('D001')
./backend/apps/approvals/tests/test_list_permissions.py:37:        self.dean2 =
User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
./backend/apps/approvals/tests/test_list_permissions.py:38:        self.dean2.se
t_password('D002')
./backend/apps/users/serializers.py:9:        fields = ['user_id', 'name', 'role
', 'class_id', 'active', 'is_graduating', 'graduation_year']
./backend/apps/users/serializers.py:10:        read_only_fields = ['user_id']
./backend/apps/users/serializers.py:17:        fields = ['user_id', 'name', 'rol
e', 'class_id']
./backend/apps/users/serializers.py:20:class LoginSerializer(serializers.Seriali
zer):
./backend/apps/users/serializers.py:21:    user_id = serializers.CharField()
./backend/apps/users/serializers.py:22:    password = serializers.CharField(writ
e_only=True)
./backend/apps/users/serializers.py:25:        user_id = attrs.get('user_id')
./backend/apps/users/serializers.py:26:        password = attrs.get('password')
./backend/apps/users/serializers.py:29:            user = User.objects.get(user_
id=user_id)
./backend/apps/users/serializers.py:33:        if not user.check_password(passwo
rd):
./backend/apps/users/serializers.py:42:            'access_token': str(refresh.a
ccess_token),
./backend/apps/users/serializers.py:48:class LoginResponseSerializer(serializers
.Serializer):
./backend/apps/users/serializers.py:50:    access_token = serializers.CharField(
help_text="JWT access token")
./backend/apps/users/serializers.py:69:        user_id = self.DEMO_USERS.get(rol
e)
./backend/apps/users/serializers.py:72:            user = User.objects.get(user_
id=user_id)
./backend/apps/users/serializers.py:82:            'access_token': str(refresh.a
ccess_token),
./backend/apps/users/models.py:14:    def create_user(self, user_id, password=No
ne, **extra_fields):
./backend/apps/users/models.py:15:        if not user_id:
./backend/apps/users/models.py:16:            raise ValueError('user_id is requi
red')
./backend/apps/users/models.py:17:        user = self.model(user_id=user_id, **e
xtra_fields)
./backend/apps/users/models.py:18:        user.set_password(password)
./backend/apps/users/models.py:22:    def create_superuser(self, user_id, passwo
rd=None, **extra_fields):
./backend/apps/users/models.py:26:        return self.create_user(user_id, passw
ord, **extra_fields)
./backend/apps/users/models.py:30:    user_id = models.CharField(max_length=50,
unique=True, primary_key=True)
./backend/apps/users/models.py:50:    USERNAME_FIELD = 'user_id'
./backend/apps/users/models.py:57:        return f"{self.user_id} - {self.name}"
./backend/apps/applications/tests/test_application_flow.py:18:            user_i
d='2020001',
./backend/apps/applications/tests/test_application_flow.py:19:            passwo
rd='2020001',
./backend/apps/applications/tests/test_application_flow.py:30:            user_i
d='T001',
./backend/apps/applications/tests/test_application_flow.py:31:            passwo
rd='T001',
./backend/apps/applications/tests/test_application_flow.py:38:            user_i
d='M001',
./backend/apps/applications/tests/test_application_flow.py:39:            passwo
rd='M001',
./backend/apps/applications/tests/test_application_flow.py:46:            user_i
d='D001',
./backend/apps/applications/tests/test_application_flow.py:47:            passwo
rd='D001',
./backend/apps/applications/tests/test_application_flow.py:66:        response =
 self.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_application_flow.py:67:            'user_
id': '2020001',
./backend/apps/applications/tests/test_application_flow.py:68:            'passw
ord': '2020001'
./backend/apps/applications/tests/test_application_flow.py:71:        student_to
ken = response.data['access_token']
./backend/apps/applications/tests/test_application_flow.py:85:        response =
 self.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_application_flow.py:86:            'user_
id': 'M001',
./backend/apps/applications/tests/test_application_flow.py:87:            'passw
ord': 'M001'
./backend/apps/applications/tests/test_application_flow.py:89:        dorm_manag
er_token = response.data['access_token']
./backend/apps/applications/tests/test_application_flow.py:106:        response
= self.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_application_flow.py:107:            'user
_id': 'T001',
./backend/apps/applications/tests/test_application_flow.py:108:            'pass
word': 'T001'
./backend/apps/applications/tests/test_application_flow.py:110:        counselor
_token = response.data['access_token']
./backend/apps/approvals/tests/test_permissions.py:14:            user_id='20200
01',
./backend/apps/approvals/tests/test_permissions.py:18:            password='2020
001',
./backend/apps/approvals/tests/test_permissions.py:23:            user_id='20200
02',
./backend/apps/approvals/tests/test_permissions.py:27:            password='2020
002',
./backend/apps/approvals/tests/test_permissions.py:34:            user_id='T001'
,
./backend/apps/approvals/tests/test_permissions.py:37:            password='T001
',
./backend/apps/approvals/tests/test_permissions.py:41:            user_id='T002'
,
./backend/apps/approvals/tests/test_permissions.py:44:            password='T002
',
./backend/apps/approvals/tests/test_permissions.py:48:            user_id='M001'
,
./backend/apps/approvals/tests/test_permissions.py:51:            password='M001
',
./backend/apps/approvals/tests/test_permissions.py:55:            user_id='M002'
,
./backend/apps/approvals/tests/test_permissions.py:58:            password='M002
',
./backend/apps/approvals/tests/test_permissions.py:62:            user_id='D001'
,
./backend/apps/approvals/tests/test_permissions.py:65:            password='D001
'
./backend/apps/approvals/tests/test_permissions.py:68:            user_id='D002'
,
./backend/apps/approvals/tests/test_permissions.py:71:            password='D002
'
./backend/apps/applications/tests/test_p0_fixes.py:14:            user_id='S001'
,
./backend/apps/applications/tests/test_p0_fixes.py:20:            user_id='C001'
,
./backend/apps/applications/tests/test_p0_fixes.py:87:            user_id='S001'
,
./backend/apps/applications/tests/test_p0_fixes.py:93:            user_id='C001'
,
./backend/apps/approvals/views.py:112:    if user.role == UserRole.DEAN or appro
val.approver_id == user.user_id:
./backend/apps/approvals/views.py:154:    if approval.approver_id != user.user_i
d:
./backend/apps/approvals/views.py:196:                f"for application {applica
tion.application_id} after approval by {approval.approver.user_id}"
./backend/apps/approvals/views.py:216:        # Selection: order_by('user_id') p
icks lowest ID for deterministic routing.
./backend/apps/approvals/views.py:221:        ).order_by('user_id')
./backend/apps/approvals/views.py:226:                f"{counselors.count()} mat
ches. Selected {counselors.first().user_id} via order_by('user_id')"
./backend/apps/approvals/views.py:287:    if approval.approver_id != user.user_i
d:
./backend/apps/applications/tests/test_error_cases.py:17:            user_id='20
20001',
./backend/apps/applications/tests/test_error_cases.py:18:            password='2
020001',
./backend/apps/applications/tests/test_error_cases.py:29:            user_id='20
20002',
./backend/apps/applications/tests/test_error_cases.py:30:            password='2
020002',
./backend/apps/applications/tests/test_error_cases.py:41:            user_id='20
20003',
./backend/apps/applications/tests/test_error_cases.py:42:            password='2
020003',
./backend/apps/applications/tests/test_error_cases.py:53:            user_id='T0
01',
./backend/apps/applications/tests/test_error_cases.py:54:            password='T
001',
./backend/apps/applications/tests/test_error_cases.py:60:            user_id='M0
01',
./backend/apps/applications/tests/test_error_cases.py:61:            password='M
001',
./backend/apps/applications/tests/test_error_cases.py:68:            user_id='D0
01',
./backend/apps/applications/tests/test_error_cases.py:69:            password='D
001',
./backend/apps/applications/tests/test_error_cases.py:86:        response = self
.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_error_cases.py:87:            'user_id':
'2020003',
./backend/apps/applications/tests/test_error_cases.py:88:            'password':
 '2020003'
./backend/apps/applications/tests/test_error_cases.py:90:        token = respons
e.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:103:        response = sel
f.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_error_cases.py:104:            'user_id':
 '2020001',
./backend/apps/applications/tests/test_error_cases.py:105:            'password'
: '2020001'
./backend/apps/applications/tests/test_error_cases.py:107:        token = respon
se.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:131:        response = sel
f.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_error_cases.py:132:            'user_id':
 '2020001',
./backend/apps/applications/tests/test_error_cases.py:133:            'password'
: '2020001'
./backend/apps/applications/tests/test_error_cases.py:135:        token1 = respo
nse.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:147:        response = sel
f.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_error_cases.py:148:            'user_id':
 '2020002',
./backend/apps/applications/tests/test_error_cases.py:149:            'password'
: '2020002'
./backend/apps/applications/tests/test_error_cases.py:151:        token2 = respo
nse.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:160:        response = sel
f.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_error_cases.py:161:            'user_id':
 '2020001',
./backend/apps/applications/tests/test_error_cases.py:162:            'password'
: '2020001'
./backend/apps/applications/tests/test_error_cases.py:164:        token = respon
se.data['access_token']
./backend/apps/applications/tests/test_error_cases.py:173:        response = sel
f.client.post('/api/auth/login', {
./backend/apps/applications/tests/test_error_cases.py:174:            'user_id':
 '2020001',
./backend/apps/applications/tests/test_error_cases.py:175:            'password'
: '2020001'
./backend/apps/applications/tests/test_error_cases.py:177:        token = respon
se.data['access_token']
./backend/apps/applications/tests/test_detail_permissions.py:15:        self.stu
dent1 = User.objects.create(user_id='2020001', name='学生1', role=UserRole.STUDE
NT, class_id='CS2020-01', building='1号楼', department='计算机学院')
./backend/apps/applications/tests/test_detail_permissions.py:16:        self.stu
dent1.set_password('2020001')
./backend/apps/applications/tests/test_detail_permissions.py:19:        self.stu
dent2 = User.objects.create(user_id='2020002', name='学生2', role=UserRole.STUDE
NT, class_id='CS2020-02', building='2号楼', department='软件学院')
./backend/apps/applications/tests/test_detail_permissions.py:20:        self.stu
dent2.set_password('2020002')
./backend/apps/applications/tests/test_detail_permissions.py:24:        self.cou
nselor1 = User.objects.create(user_id='T001', name='辅导员1', role=UserRole.COUN
SELOR, department='计算机学院')
./backend/apps/applications/tests/test_detail_permissions.py:25:        self.cou
nselor1.set_password('T001')
./backend/apps/applications/tests/test_detail_permissions.py:28:        self.cou
nselor2 = User.objects.create(user_id='T002', name='辅导员2', role=UserRole.COUN
SELOR, department='软件学院')
./backend/apps/applications/tests/test_detail_permissions.py:29:        self.cou
nselor2.set_password('T002')
./backend/apps/applications/tests/test_detail_permissions.py:32:        self.dor
m_manager1 = User.objects.create(user_id='M001', name='宿管员1', role=UserRole.D
ORM_MANAGER, building='1号楼')
./backend/apps/applications/tests/test_detail_permissions.py:33:        self.dor
m_manager1.set_password('M001')
./backend/apps/applications/tests/test_detail_permissions.py:36:        self.dor
m_manager2 = User.objects.create(user_id='M002', name='宿管员2', role=UserRole.D
ORM_MANAGER, building='2号楼')
./backend/apps/applications/tests/test_detail_permissions.py:37:        self.dor
m_manager2.set_password('M002')
./backend/apps/applications/tests/test_detail_permissions.py:41:        self.dea
n1 = User.objects.create(user_id='D001', name='学工部1', role=UserRole.DEAN)
./backend/apps/applications/tests/test_detail_permissions.py:42:        self.dea
n1.set_password('D001')
./backend/apps/applications/tests/test_detail_permissions.py:45:        self.dea
n2 = User.objects.create(user_id='D002', name='学工部2', role=UserRole.DEAN)
./backend/apps/applications/tests/test_detail_permissions.py:46:        self.dea
n2.set_password('D002')
./backend/apps/users/management/commands/import_staff.py:65:        user_id = (r
ow.get('职工号') or row.get('user_id') or '').strip()
./backend/apps/users/management/commands/import_staff.py:72:        if not user_
id or not name or not role_str:
./backend/apps/users/management/commands/import_staff.py:74:            stats['e
rrors'].append(f'Missing required fields: user_id={user_id}, name={name}, role={
role_str}')
./backend/apps/users/management/commands/import_staff.py:90:            stats['e
rrors'].append(f'{user_id}: Unknown role "{role_str}"')
./backend/apps/users/management/commands/import_staff.py:100:
     f'{user_id} ({name}): {e} - keeping original value'
./backend/apps/users/management/commands/import_staff.py:109:            if user
_id != fallback_id:
./backend/apps/users/management/commands/import_staff.py:112:
     f'{user_id} ({name}): DORM_MANAGER without building (not fallback manager)'
./backend/apps/users/management/commands/import_staff.py:117:            exists
= User.objects.filter(user_id=user_id).exists()
./backend/apps/users/management/commands/import_staff.py:125:                use
r_id=user_id,
./backend/apps/users/integrations/xg_user_mapper.py:13:            'user_id': st
r | None,
./backend/apps/users/integrations/xg_user_mapper.py:26:        'user_id': None,
./backend/apps/users/integrations/xg_user_mapper.py:41:    user_identity = xg_us
er.get('user_identity')
./backend/apps/users/integrations/xg_user_mapper.py:61:        result['skip_reas
on'] = 'missing_user_id'
./backend/apps/users/integrations/xg_user_mapper.py:65:        result['user_id']
 = number
./backend/apps/users/integrations/xg_user_mapper.py:71:    if user_identity is n
ot None:
./backend/apps/users/integrations/xg_user_mapper.py:73:        if isinstance(use
r_identity, dict):
./backend/apps/users/integrations/xg_user_mapper.py:74:            identity_name
 = user_identity.get('name', '')
./backend/apps/users/integrations/xg_user_mapper.py:75:            identity_id =
 user_identity.get('id')
./backend/apps/users/integrations/xg_user_mapper.py:79:                result['u
ser_id'] = number
./backend/apps/users/integrations/xg_user_mapper.py:81:                result['s
kip_reason'] = f'unknown_user_identity: name={identity_name}, id={identity_id}'
./backend/apps/users/integrations/xg_user_mapper.py:85:            user_identity
_str = str(user_identity)
./backend/apps/users/integrations/xg_user_mapper.py:86:            if user_ident
ity_str == '1' or user_identity_str.lower() == 'student':
./backend/apps/users/integrations/xg_user_mapper.py:89:                result['u
ser_id'] = number
./backend/apps/users/integrations/xg_user_mapper.py:91:                result['s
kip_reason'] = f'unknown_user_identity: {user_identity_str}'
./backend/apps/users/integrations/xg_user_mapper.py:94:        result['user_id']
 = number
./backend/apps/users/integrations/xg_user_mapper.py:96:        result['skip_reas
on'] = 'missing_user_identity'
./backend/apps/users/integrations/xg_user_mapper.py:100:    result['user_id'] =
number
./backend/apps/users/management/commands/import_students.py:57:            requi
red = ['user_id', 'name', 'class_id']
./backend/apps/users/management/commands/import_students.py:82:        user_id =
 row['user_id'].strip()
./backend/apps/users/management/commands/import_students.py:92:        if user_i
d.startswith('TMP2026_'):
./backend/apps/users/management/commands/import_students.py:94:            stats
['errors'].append(f'{user_id}: TMP ID not allowed in import')
./backend/apps/users/management/commands/import_students.py:99:            exist
s = User.objects.filter(user_id=user_id).exists()
./backend/apps/users/management/commands/import_students.py:107:
user_id=user_id,
./backend/apps/users/management/commands/import_csv.py:87:
  exists = User.objects.filter(user_id=student_id).exists()
./backend/apps/users/management/commands/import_csv.py:94:
      user_id=student_id,
./backend/apps/users/management/commands/import_csv.py:104:
       user.set_password(row.get('password', student_id))
./backend/apps/users/management/commands/import_csv.py:110:
   self.stdout.write(f'{"Created" if created else "Updated"} student: {user.user
_id}')
./backend/apps/users/management/commands/import_csv.py:149:
   exists = User.objects.filter(user_id=employee_id).exists()
./backend/apps/users/management/commands/import_csv.py:156:
       user_id=employee_id,
./backend/apps/users/management/commands/import_csv.py:163:
       user.set_password(row.get('password', employee_id))
./backend/apps/users/management/commands/import_csv.py:169:
   self.stdout.write(f'{"Created" if created else "Updated"} counselor: {user.us
er_id}')
./backend/apps/users/management/commands/import_csv.py:211:
       counselor = User.objects.get(user_id=counselor_id, role=UserRole.COUNSELO
R)
./backend/apps/users/management/commands/import_csv.py:236:
   self.stdout.write(f'{"Created" if created else "Updated"} mapping: {mapping.c
lass_id} -> {counselor.user_id}')
./backend/apps/users/management/commands/seed_data.py:28:            {'user_id':
 '2020001', 'name': '张三', 'class_id': 'CS2020-01', 'building': '1号楼', 'depar
tment': '计算机学院'},
./backend/apps/users/management/commands/seed_data.py:29:            {'user_id':
 '2020002', 'name': '李四', 'class_id': 'CS2020-02', 'building': '2号楼', 'depar
tment': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:30:            {'user_id':
 '2020003', 'name': '王五', 'class_id': 'CS2020-01', 'building': '1号楼', 'depar
tment': '计算机学院'},
./backend/apps/users/management/commands/seed_data.py:31:            {'user_id':
 '2020004', 'name': '赵六', 'class_id': 'CS2020-01', 'building': '1号楼', 'depar
tment': '计算机学院'},
./backend/apps/users/management/commands/seed_data.py:32:            {'user_id':
 '2020005', 'name': '孙七', 'class_id': 'CS2020-01', 'building': '1号楼', 'depar
tment': '计算机学院'},
./backend/apps/users/management/commands/seed_data.py:33:            {'user_id':
 '2020006', 'name': '周八', 'class_id': 'CS2020-02', 'building': '2号楼', 'depar
tment': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:34:            {'user_id':
 '2020007', 'name': '吴九', 'class_id': 'CS2020-02', 'building': '2号楼', 'depar
tment': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:35:            {'user_id':
 '2020008', 'name': '郑十', 'class_id': 'CS2020-02', 'building': '2号楼', 'depar
tment': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:36:            {'user_id':
 '2020009', 'name': '王十一', 'class_id': 'CS2020-02', 'building': '2号楼', 'dep
artment': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:37:            {'user_id':
 '2020010', 'name': '王十二', 'class_id': 'CS2020-02', 'building': '2号楼', 'dep
artment': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:42:                user_id
=student_data['user_id'],
./backend/apps/users/management/commands/seed_data.py:55:                user.se
t_password(student_data['user_id'])
./backend/apps/users/management/commands/seed_data.py:57:            self.stdout
.write(f'{"Created" if created else "Updated"} student: {user.user_id}')
./backend/apps/users/management/commands/seed_data.py:61:            {'user_id':
 'T001', 'name': '李老师', 'department': '计算机学院'},
./backend/apps/users/management/commands/seed_data.py:62:            {'user_id':
 'T002', 'name': '王老师', 'department': '软件学院'},
./backend/apps/users/management/commands/seed_data.py:67:                user_id
=counselor_data['user_id'],
./backend/apps/users/management/commands/seed_data.py:76:                user.se
t_password(counselor_data['user_id'])
./backend/apps/users/management/commands/seed_data.py:78:                self.st
dout.write(f'Created counselor: {user.user_id}')
./backend/apps/users/management/commands/seed_data.py:82:            {'user_id':
 'M001', 'name': '宿管员1', 'building': '1号楼'},
./backend/apps/users/management/commands/seed_data.py:83:            {'user_id':
 'M002', 'name': '宿管员2', 'building': '2号楼'},
./backend/apps/users/management/commands/seed_data.py:84:            {'user_id':
 'M003', 'name': '宿管员3', 'building': '1号楼'},
./backend/apps/users/management/commands/seed_data.py:89:                user_id
=dm_data['user_id'],
./backend/apps/users/management/commands/seed_data.py:98:                user.se
t_password(dm_data['user_id'])
./backend/apps/users/management/commands/seed_data.py:100:                self.s
tdout.write(f'Created dorm_manager: {user.user_id}')
./backend/apps/users/management/commands/seed_data.py:104:            user_id='D
001',
./backend/apps/users/management/commands/seed_data.py:112:            user.set_p
assword('D001')
./backend/apps/users/management/commands/seed_data.py:114:            self.stdou
t.write(f'Created dean: {user.user_id}')
./backend/apps/users/urls.py:5:    path('login', views.login, name='login'),
./backend/apps/users/urls.py:6:    path('demo-login', views.demo_login, name='de
mo_login'),
./backend/apps/notifications/services.py:29:    message = f"学生{application.stu
dent_name}（{application.student.user_id}）提交了离校申请，请及时审批。"
./backend/apps/users/views.py:11:    operation_id='auth_login',
./backend/apps/users/views.py:28:def login(request):
./backend/apps/users/views.py:36:    operation_id='auth_demo_login',
./backend/apps/users/views.py:56:def demo_login(request):
./backend/apps/users/views.py:59:        return Response({'error': 'Demo login i
s disabled'}, status=status.HTTP_403_FORBIDDEN)
./backend/apps/users/services/xg_user_sync.py:52:        user_id = mapped['user_
id']
./backend/apps/users/services/xg_user_sync.py:55:        # user_id是主键，不会出
现MultipleObjectsReturned
./backend/apps/users/services/xg_user_sync.py:58:            local_user = User.o
bjects.get(user_id=user_id)
./backend/apps/users/services/xg_user_sync.py:64:                    'user_id':
user_id,
./backend/apps/users/services/xg_user_sync.py:77:            result['warnings'].
append(f"would_create_but_blocked: {user_id} (lacks class_id/is_graduating/gradu
ation_year)")
./backend/apps/users/services/xg_user_sync.py:132:        user_id = mapped['user
_id']
./backend/apps/users/services/xg_user_sync.py:135:            local_user = User.
objects.get(user_id=user_id)
./backend/apps/users/services/xg_user_sync.py:140:                    'user_id':
 user_id,
./backend/apps/users/services/xg_user_sync.py:157:            result['warnings']
.append(f"skip_missing_user: {user_id}")
./backend/apps/applications/views.py:141:
 'details': {'student_id': user.user_id, 'existing_application_id': existing.app
lication_id, 'status': existing.status}}},
./backend/apps/applications/views.py:145:        dorm_status = provider.check_st
atus(user.user_id)
./backend/apps/applications/views.py:149:
 'details': {'student_id': user.user_id, 'dorm_status': dorm_status.status,
./backend/apps/applications/views.py:162:            ).order_by('user_id'))
./backend/apps/applications/views.py:168:                fallback_manager = User
.objects.get(role=UserRole.DORM_MANAGER, user_id=fallback_id, active=True)
./backend/apps/notifications/serializers.py:22:    recipient_id = serializers.Ch
arField(source='recipient.user_id', read_only=True)
./backend/apps/notifications/serializers.py:23:    actor_id = serializers.CharFi
eld(source='actor.user_id', read_only=True, allow_null=True)
./backend/apps/users/admin.py:7:    list_display = ['user_id', 'name', 'role', '
class_id', 'active']
./backend/apps/users/admin.py:9:    search_fields = ['user_id', 'name', 'class_i
d']
./backend/apps/users/admin.py:10:    ordering = ['user_id']
./backend/apps/users/tests/test_xg_user_sync.py:16:            user_id='2021001'
,
./backend/apps/users/tests/test_xg_user_sync.py:27:            user_id='T001',
./backend/apps/users/tests/test_xg_user_sync.py:36:            {'number': None,
'name': '王五', 'user_identity': '1'},  # 缺number
./backend/apps/users/tests/test_xg_user_sync.py:37:            {'number': '20210
03', 'name': None, 'user_identity': '1'},  # 缺name
./backend/apps/users/tests/test_xg_user_sync.py:38:            {'number': '20210
04', 'name': '赵六', 'user_identity': '9'},  # 未知身份
./backend/apps/users/tests/test_xg_user_sync.py:48:        self.assertIn('missin
g_user_id', result['skipped_by_reason'])
./backend/apps/users/tests/test_xg_user_sync.py:57:                'user_identit
y': '1',
./backend/apps/users/tests/test_xg_user_sync.py:79:                'user_identit
y': '1',
./backend/apps/users/tests/test_xg_user_sync.py:92:        self.assertFalse(User
.objects.filter(user_id='2021999').exists())
./backend/apps/users/tests/test_xg_user_sync.py:105:                'user_identi
ty': '1',  # API认为是学生
./backend/apps/users/tests/test_xg_user_sync.py:118:        self.assertEqual(con
flict['user_id'], 'T001')
./backend/apps/users/tests/test_xg_user_sync.py:126:        original_user = User
.objects.get(user_id='2021001')
./backend/apps/users/tests/test_xg_user_sync.py:135:                'user_identi
ty': '1',
./backend/apps/users/tests/test_xg_user_sync.py:142:        user_after = User.ob
jects.get(user_id='2021001')
./backend/apps/users/tests/test_xg_user_sync.py:154:                'user_identi
ty': '1',
./backend/apps/users/tests/test_xg_user_sync.py:188:            {'number': None,
 'name': '测试1', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:191:            {'number': '2021
005', 'name': '测试2', 'user_identity': '9'},
./backend/apps/users/tests/test_xg_user_sync.py:194:            {'number': '2021
998', 'name': '测试3', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:197:            {'number': 'T001
', 'name': '李老师', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:200:            {'number': '2021
001', 'name': '张三', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:232:            user_id='2021001
',
./backend/apps/users/tests/test_xg_user_sync.py:244:            user_id='T001',
./backend/apps/users/tests/test_xg_user_sync.py:255:            'user_identity':
 '1',
./backend/apps/users/tests/test_xg_user_sync.py:264:        user = User.objects.
get(user_id='2021001')
./backend/apps/users/tests/test_xg_user_sync.py:272:            {'number': None,
 'name': '王五', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:273:            {'number': '2021
001', 'name': '张三', 'user_identity': '1', 'phone': '13800138000'}
./backend/apps/users/tests/test_xg_user_sync.py:280:        self.assertIn('missi
ng_user_id', result['skipped_by_reason'])
./backend/apps/users/tests/test_xg_user_sync.py:284:        xg_users = [{'number
': 'T001', 'name': '李老师', 'user_identity': '1'}]
./backend/apps/users/tests/test_xg_user_sync.py:294:        xg_users = [{'number
': '2021999', 'name': '新学生', 'user_identity': '1', 'phone': '13900139000'}]
./backend/apps/users/tests/test_xg_user_sync.py:300:        self.assertFalse(Use
r.objects.filter(user_id='2021999').exists())
./backend/apps/users/tests/test_xg_user_sync.py:307:            'user_identity':
 '1',
./backend/apps/users/tests/test_xg_user_sync.py:316:        user = User.objects.
get(user_id='2021001')
./backend/apps/users/tests/test_xg_user_sync.py:324:            user_id='2021002
',
./backend/apps/users/tests/test_xg_user_sync.py:334:            {'number': '2021
001', 'name': '张三', 'user_identity': '1', 'phone': '13800138000'},
./backend/apps/users/tests/test_xg_user_sync.py:335:            {'number': '2021
002', 'name': '李四', 'user_identity': '1', 'phone': '13800138001'}
./backend/apps/users/tests/test_xg_user_sync.py:341:        self.assertEqual(Use
r.objects.get(user_id='2021001').phone, '13800138000')
./backend/apps/users/tests/test_xg_user_sync.py:342:        self.assertEqual(Use
r.objects.get(user_id='2021002').phone, '13800138001')
./backend/apps/users/tests/test_xg_user_sync.py:347:            {'number': None,
 'name': '测试', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:348:            {'number': '2021
001', 'name': '张三', 'user_identity': '1', 'phone': '13800138000'},
./backend/apps/users/tests/test_xg_user_sync.py:349:            {'number': 'T001
', 'name': '李老师', 'user_identity': '1'},
./backend/apps/users/tests/test_xg_user_sync.py:350:            {'number': '2021
999', 'name': '新学生', 'user_identity': '1'}
./backend/apps/users/tests/test_xg_user_sync.py:368:            user_id='2021003
',
./backend/apps/users/tests/test_xg_user_sync.py:376:        xg_users = [{'number
': '2021001', 'name': '张三', 'user_identity': '1', 'phone': '13800138000'}]
./backend/apps/users/tests/test_xg_user_sync.py:380:        user_2021003 = User.
objects.get(user_id='2021003')
./backend/apps/users/tests/test_xg_user_sync.py:382:        counselor = User.obj
ects.get(user_id='T001')
./backend/apps/users/tests/test_import_csv.py:14:        User.objects.create_use
r(user_id='T001', name='李老师', role=UserRole.COUNSELOR, password='T001', depar
tment='计算机学院')
./backend/apps/users/tests/test_import_csv.py:15:        User.objects.create_use
r(user_id='T002', name='王老师', role=UserRole.COUNSELOR, password='T002', depar
tment='软件学院')
./backend/apps/users/tests/test_import_csv.py:34:            self.assertTrue(Use
r.objects.filter(user_id='T003', name='张老师').exists())
./backend/apps/users/tests/test_import_csv.py:77:            self.assertEqual(ma
pping.counselor.user_id, 'T001')
./backend/apps/users/tests/test_import_csv.py:99:        counselor = User.object
s.get(user_id='T001')
./backend/apps/users/tests/test_import_csv.py:110:            student = User.obj
ects.get(user_id='2020001')
./backend/apps/users/tests/test_import_csv.py:145:            self.assertFalse(U
ser.objects.filter(user_id='T005').exists())
./backend/apps/approvals/tests/test_state_machine.py:14:            user_id='202
0001',
./backend/apps/approvals/tests/test_state_machine.py:18:            password='20
20001',
./backend/apps/approvals/tests/test_state_machine.py:25:            user_id='T00
1',
./backend/apps/approvals/tests/test_state_machine.py:28:            password='T0
01',
./backend/apps/approvals/tests/test_state_machine.py:34:            user_id='M00
1',
./backend/apps/approvals/tests/test_state_machine.py:37:            password='M0
01',
./backend/apps/approvals/tests/test_state_machine.py:43:            user_id='D00
1',
./backend/apps/approvals/tests/test_state_machine.py:46:            password='D0
01'
./backend/apps/users/tests/test_xg_user_mapper.py:17:            'user_identity'
: '1'
./backend/apps/users/tests/test_xg_user_mapper.py:22:        self.assertEqual(re
sult['user_id'], '2022001')
./backend/apps/users/tests/test_xg_user_mapper.py:33:    def test_user_identity_
student_string(self):
./backend/apps/users/tests/test_xg_user_mapper.py:34:        """测试user_identit
y为'student'字符串"""
./backend/apps/users/tests/test_xg_user_mapper.py:38:            'user_identity'
: 'student'
./backend/apps/users/tests/test_xg_user_mapper.py:50:            'user_identity'
: '1'
./backend/apps/users/tests/test_xg_user_mapper.py:55:        self.assertIsNone(r
esult['user_id'])
./backend/apps/users/tests/test_xg_user_mapper.py:56:        self.assertEqual(re
sult['skip_reason'], 'missing_user_id')
./backend/apps/users/tests/test_xg_user_mapper.py:63:            'user_identity'
: '1'
./backend/apps/users/tests/test_xg_user_mapper.py:68:        self.assertEqual(re
sult['user_id'], '2022002')
./backend/apps/users/tests/test_xg_user_mapper.py:72:    def test_unknown_user_i
dentity_skip(self):
./backend/apps/users/tests/test_xg_user_mapper.py:73:        """测试user_identit
y未知值应跳过"""
./backend/apps/users/tests/test_xg_user_mapper.py:77:            'user_identity'
: '999'
./backend/apps/users/tests/test_xg_user_mapper.py:82:        self.assertEqual(re
sult['user_id'], '2022003')
./backend/apps/users/tests/test_xg_user_mapper.py:85:        self.assertEqual(re
sult['skip_reason'], 'unknown_user_identity: 999')
./backend/apps/users/tests/test_xg_user_mapper.py:87:    def test_missing_user_i
dentity_skip(self):
./backend/apps/users/tests/test_xg_user_mapper.py:88:        """测试user_identit
y缺失应跳过"""
./backend/apps/users/tests/test_xg_user_mapper.py:96:        self.assertEqual(re
sult['user_id'], '2022004')
./backend/apps/users/tests/test_xg_user_mapper.py:99:        self.assertEqual(re
sult['skip_reason'], 'missing_user_identity')
./backend/apps/users/tests/test_xg_user_mapper.py:106:            'user_identity
': '1'
./backend/apps/users/tests/test_xg_user_mapper.py:111:        self.assertEqual(r
esult['user_id'], '2022005')
./backend/apps/users/tests/test_xg_user_mapper.py:125:        self.assertEqual(r
esult['skip_reason'], 'missing_user_id')
./backend/apps/users/tests/test_xg_user_mapper.py:127:    def test_user_identity
_object_format(self):
./backend/apps/users/tests/test_xg_user_mapper.py:128:        """测试user_identi
ty对象格式（XG API实际返回格式）"""
./backend/apps/users/tests/test_xg_user_mapper.py:132:            'user_identity
': {'id': 4, 'name': '学生'},
./backend/apps/users/tests/test_xg_user_mapper.py:139:        self.assertEqual(r
esult['user_id'], '2025110140314')
./backend/apps/users/tests/test_xg_user_mapper.py:151:            'user_identity
': {'id': 4, 'name': '学生'},
./backend/apps/users/tests/test_xg_user_mapper.py:169:            'user_identity
': {'id': 4, 'name': '学生'},
./backend/apps/users/tests/test_xg_user_mapper.py:183:            'user_identity
': {'id': 4, 'name': '学生'},
./backend/apps/users/migrations/0001_initial.py:20:                ('password',
models.CharField(max_length=128, verbose_name='password')),
./backend/apps/users/migrations/0001_initial.py:21:                ('last_login'
, models.DateTimeField(blank=True, null=True, verbose_name='last login')),
./backend/apps/users/migrations/0001_initial.py:23:                ('user_id', m
odels.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
./backend/apps/attachments/tests/test_list.py:17:            user_id='2020001',
./backend/apps/attachments/tests/test_list.py:18:            password='2020001',
./backend/apps/attachments/tests/test_list.py:29:            user_id='2020002',
./backend/apps/attachments/tests/test_list.py:30:            password='2020002',
./backend/apps/attachments/tests/test_list.py:42:            user_id='T001',
./backend/apps/attachments/tests/test_list.py:43:            password='T001',
./backend/apps/attachments/tests/test_list.py:50:            user_id='T002',
./backend/apps/attachments/tests/test_list.py:51:            password='T002',
./backend/apps/attachments/tests/test_list.py:59:            user_id='D001',
./backend/apps/attachments/tests/test_list.py:60:            password='D001',
./backend/apps/attachments/tests/test_delete.py:17:            user_id='2020001'
,
./backend/apps/attachments/tests/test_delete.py:18:            password='2020001
',
./backend/apps/attachments/tests/test_delete.py:29:            user_id='2020002'
,
./backend/apps/attachments/tests/test_delete.py:30:            password='2020002
',
./backend/apps/attachments/tests/test_delete.py:42:            user_id='T001',
./backend/apps/attachments/tests/test_delete.py:43:            password='T001',
./backend/apps/attachments/views.py:67:    if user.role != UserRole.STUDENT or a
pplication.student_id != user.user_id:
./backend/apps/attachments/views.py:187:    if user.role != UserRole.STUDENT or
attachment.application.student_id != user.user_id:
./backend/apps/attachments/tests/test_upload.py:17:            user_id='2020001'
,
./backend/apps/attachments/tests/test_upload.py:18:            password='2020001
',
./backend/apps/attachments/tests/test_upload.py:30:            user_id='2020002'
,
./backend/apps/attachments/tests/test_upload.py:31:            password='2020002
',
./backend/apps/attachments/tests/test_upload.py:43:            user_id='T001',
./backend/apps/attachments/tests/test_upload.py:44:            password='T001',
./backend/apps/notifications/tests/test_auto_notifications_api.py:27:
 user_id='2020001',
./backend/apps/notifications/tests/test_auto_notifications_api.py:35:
 user_id='T001',
./backend/apps/notifications/tests/test_auto_notifications_api.py:41:
 user_id='M001',
./backend/apps/notifications/tests/test_auto_notifications_api.py:47:
 user_id='D001',
./backend/apps/notifications/tests/test_auto_notifications_api.py:167:
  user_id='2021002',
./backend/apps/notifications/tests/test_auto_notifications_api.py:247:
  user_id='2021999',
./backend/apps/notifications/tests/test_api.py:12:            user_id='2020001',
./backend/apps/notifications/tests/test_api.py:18:            user_id='2020002',
./backend/apps/notifications/tests/test_api.py:24:            user_id='T001',
./backend/apps/notifications/tests/test_timeout_warnings.py:16:            user_
id='2020001',
./backend/apps/notifications/tests/test_timeout_warnings.py:24:            user_
id='T001',
./backend/apps/notifications/tests/test_timeout_warnings.py:31:            user_
id='M001',
./backend/apps/notifications/tests/test_auto_notifications.py:28:            use
r_id='2021001',
./backend/apps/notifications/tests/test_auto_notifications.py:36:            use
r_id='T001',
./backend/apps/notifications/tests/test_auto_notifications.py:42:            use
r_id='M001',
./backend/apps/notifications/tests/test_models.py:10:            user_id='202000
1',
./backend/apps/notifications/tests/test_models.py:16:            user_id='T001',
./backend/apps/notifications/tests/test_models.py:81:            user_id='202000
2',
./backend/apps/notifications/admin.py:9:    search_fields = ['notification_id',
'title', 'message', 'recipient__user_id']
./backend/apps/attachments/tests/test_download.py:18:            user_id='202000
1',
./backend/apps/attachments/tests/test_download.py:19:            password='20200
01',
./backend/apps/attachments/tests/test_download.py:30:            user_id='202000
2',
./backend/apps/attachments/tests/test_download.py:31:            password='20200
02',
./backend/apps/attachments/tests/test_download.py:43:            user_id='T001',
./backend/apps/attachments/tests/test_download.py:44:            password='T001'
,

exec
/bin/bash -lc "rtk sed -n '300,640p' demo-web/index.html" in /home/caohui/projec
ts/graduation-leave-system
 succeeded in 0ms:
    .screen.active {
      display: block;
    }
  </style>
</head>
<body>
  <!-- 顶部导航 -->
  <div class="nav-tabs">
    <button class="nav-tab active" onclick="showScreen(0)">学生申请</button>
    <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approval-text"
>审批列表</span></button>
    <button class="nav-tab" onclick="showScreen(2)">申请详情</button>
  </div>

  <!-- 登录状态栏 -->
  <div id="userBar" style="background: white; padding: 8px 16px; border-bottom:
1px solid #f0f0f0; display: none; align-items: center; justify-content: space-be
tween;">
    <div>
      <span style="font-size: 14px; color: #666;">当前用户:</span>
      <span id="currentUserName" style="font-size: 14px; font-weight: 500; margi
n-left: 8px;"></span>
      <span id="currentUserRole" style="font-size: 12px; color: #999; margin-lef
t: 8px;"></span>
    </div>
    <button onclick="logout()" style="padding: 4px 12px; border: 1px solid #d9d9
d9; border-radius: 4px; background: white; cursor: pointer;">退出登录</button>
  </div>

  <!-- 登录屏幕 -->
  <div class="screen active" id="screen-login">
    <div style="padding: 40px 20px; max-width: 400px; margin: 0 auto;">
      <div class="card">
        <div style="text-align: center; margin-bottom: 30px;">
          <h2 style="color: var(--primary-color); margin-bottom: 8px;">毕业离校
申请系统</h2>
          <p style="color: #666; font-size: 14px;">请登录以继续</p>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">用户ID</label>
          <input id="loginUserId" type="text" style="width: 100%; padding: 12px;
 border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeholder="
请输入用户ID（如 2020001）" required>
        </div>
        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">密码</label>
          <input id="loginPassword" type="password" style="width: 100%; padding:
 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placehol
der="请输入密码" required>
        </div>
        <div id="loginError" style="display: none; padding: 10px; background: #f
ff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; font-size:
 14px; margin-bottom: 16px;"></div>
        <button class="btn-primary" onclick="doLogin()">登录</button>
        <div style="margin-top: 16px; padding: 12px; background: #f6f6f6; border
-radius: 4px;">
          <div style="font-size: 12px; color: #666; margin-bottom: 4px;">演示账
号：</div>
          <div style="font-size: 12px; color: #999;">学生: 2020001 / 2020001</di
v>
          <div style="font-size: 12px; color: #999;">宿管员: M001 / M001</div>
          <div style="font-size: 12px; color: #999;">辅导员: T001 / T001</div>
          <div style="font-size: 12px; color: #999;">学工部: D001 / D001</div>
        </div>
      </div>
    </div>
  </div>

  <div class="screen" id="screen-0">
    <div style="padding: 20px;">
      <!-- 用户信息卡片 -->
      <div class="card" style="margin-bottom: 20px;">
        <div style="font-size: 16px; font-weight: 600; color: var(--primary-colo
r); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #f0f0f0;
">
          申请人信息
        </div>
        <div style="display: flex; align-items: center; padding: 10px 0;">
          <span style="font-size: 14px; color: #666; width: 80px;">姓名</span>
          <span style="font-size: 14px; color: #333;">张三</span>
        </div>
        <div style="display: flex; align-items: center; padding: 10px 0;">
          <span style="font-size: 14px; color: #666; width: 80px;">学号</span>
          <span style="font-size: 14px; color: #333;">2020001</span>
        </div>
      </div>

      <!-- 表单卡片 -->
      <div class="card">
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">联系电话</label>
          <input id="contactPhone" type="tel" name="contact_phone" maxlength="20
" inputmode="numeric" style="width: 100%; padding: 12px; border: 1px solid #d9d9
d9; border-radius: 4px; font-size: 14px;" placeholder="请输入联系电话" required>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">离校原因</label>
          <textarea id="applicationReason" style="width: 100%; min-height: 120px
; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;
" placeholder="请输入离校原因"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color
: #999; margin-top: 4px;">0/500</span>
        </div>
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">离校日期</label>
          <input id="leaveDate" type="date" name="leave_date" style="width: 100%
; padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;
" required>
        </div>

        <!-- 附件上传区域 -->
        <div style="margin-bottom: 20px;">
          <label style="display: block; font-size: 14px; margin-bottom: 8px; fon
t-weight: 500;">附件材料（可选）</label>
          <div class="upload-zone">
            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.
pdf,.doc,.docx" style="display: none;">
            <div class="upload-area" onclick="document.getElementById('fileInput
').click()">
              <div style="font-size: 40px; color: #999; margin-bottom: 8px;">📎<
/div>
              <div style="font-size: 14px; color: #666;">点击或拖拽文件到此处上
传</div>
              <div style="font-size: 12px; color: #999; margin-top: 4px;">支持jp
g/png/pdf/doc/docx，单文件不超过10MB</div>
            </div>
          </div>
          <!-- 文件列表 -->
          <div id="fileList" style="margin-top: 12px;"></div>
        </div>

        <button class="btn-primary" onclick="doSubmitApplication()">提交申请</bu
tton>
      </div>
    </div>
  </div>

  <!-- 屏幕2: 审批列表页 -->
  <div class="screen" id="screen-1">
    <div style="background: white; padding: 16px; display: flex; justify-content
: space-between; align-items: center;">
      <div style="font-size: 18px; font-weight: bold;" id="list-title">审批列表<
/div>
      <div style="font-size: 12px; color: #999;" id="role-display">宿管员</div>
    </div>

    <!-- Tab切换 -->
    <div style="background: white; display: flex; border-bottom: 1px solid #f0f0
f0;">
      <div class="nav-tab active" style="flex: 1;">全部</div>
      <div class="nav-tab" style="flex: 1;">待审批</div>
      <div class="nav-tab" style="flex: 1;">已审批</div>
    </div>

    <div style="padding: 10px;">
      <!-- 列表项 -->
      <div class="card">
        <div class="flex-row justify-between align-center" style="margin-bottom:
 8px;">
          <span style="font-size: 16px; font-weight: bold;">申请 APP-001</span>
          <span class="tag tag-pending">待审批</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:
</span>
          <span style="font-size: 14px; color: #333;">APP-001</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步
骤:</span>
          <span style="font-size: 14px; color: #333;">宿管员审批</span>
        </div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0
f0f0;">
          <span style="font-size: 12px; color: #999;">2024-06-01 10:30</span>
        </div>
      </div>

      <div class="card">
        <div class="flex-row justify-between align-center" style="margin-bottom:
 8px;">
          <span style="font-size: 16px; font-weight: bold;">申请 APP-002</span>
          <span class="tag tag-approved">已通过</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">申请ID:
</span>
          <span style="font-size: 14px; color: #333;">APP-002</span>
        </div>
        <div style="margin-bottom: 4px;">
          <span style="font-size: 14px; color: #999; margin-right: 8px;">审批步
骤:</span>
          <span style="font-size: 14px; color: #333;">辅导员审批</span>
        </div>
        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid #f0
f0f0;">
          <span style="font-size: 12px; color: #999;">2024-05-30 14:20</span>
        </div>
      </div>
    </div>
  </div>

  <!-- 屏幕3: 申请详情页 -->
  <div class="screen" id="screen-2">
    <div style="background: white; padding: 16px;">
      <div style="font-size: 18px; font-weight: bold;">申请详情</div>
    </div>

    <div style="padding: 10px;">
      <!-- 基本信息 -->
      <div class="card">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">基
本信息</div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">申请ID:</span
>
          <span style="font-size: 14px; color: #333; flex: 1;">APP-001</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">学生:</span>
          <span style="font-size: 14px; color: #333; flex: 1;">张三 (2020001)</s
pan>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">离校日期:</sp
an>
          <span style="font-size: 14px; color: #333; flex: 1;">2024-06-15</span>
        </div>
        <div style="display: flex; margin-bottom: 8px;">
          <span style="font-size: 14px; color: #999; width: 80px;">申请原因:</sp
an>
          <span style="font-size: 14px; color: #333; flex: 1;">毕业实习，需要提
前离校</span>
        </div>
      </div>

      <!-- 审批记录时间轴 -->
      <div class="card">
        <div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">审
批记录</div>

        <!-- 时间轴项 -->
        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;
">
          <div style="position: absolute; left: 10px; top: 4px; width: 10px; hei
ght: 10px; border-radius: 50%; background: white; border: 2px solid var(--primar
y-color);"></div>
          <div style="position: absolute; left: 14px; top: 16px; bottom: -20px;
width: 1px; background: #e8e8e8;"></div>
          <div class="flex-row justify-between align-center" style="margin-botto
m: 6px;">
            <span style="font-size: 15px; font-weight: 600;">宿管员审批</span>
            <span class="tag tag-pending">待审批</span>
          </div>
          <div style="font-size: 13px; color: #666;">审批人: 李老师</div>
        </div>

        <div style="position: relative; padding-left: 30px; margin-bottom: 20px;
">
          <div style="position: absolute; left: 10px; top: 4px; width: 10px; hei
ght: 10px; border-radius: 50%; background: var(--status-success); border: 2px so
lid var(--status-success);"></div>
          <div class="flex-row justify-between align-center" style="margin-botto
m: 6px;">
            <span style="font-size: 15px; font-weight: 600;">提交申请</span>
            <span class="tag tag-approved">已完成</span>
          </div>
          <div style="font-size: 13px; color: #666;">提交时间: 2024-06-01 10:30<
/div>
        </div>
      </div>

      <!-- 审批操作 -->
      <div id="approval-section" style="padding: 10px;">
        <div class="card" style="margin-bottom: 10px;">
          <label style="display: block; font-size: 14px; color: #333; margin-bot
tom: 6px; font-weight: 500;">审批意见（可选）</label>
          <textarea id="approvalComment" style="width: 100%; min-height: 60px; p
adding: 8px; border: 1px solid #e8e8e8; border-radius: 4px; font-size: 14px;" pl
aceholder="请输入审批意见"></textarea>
          <span style="display: block; text-align: right; font-size: 12px; color
: #999; margin-top: 4px;">0/200</span>
        </div>
        <div style="display: flex; gap: 10px;" id="approval-actions">
          <button class="btn-primary" style="flex: 1;" onclick="doApprove()">通
过</button>
          <button class="btn-outline" style="flex: 1;" onclick="doReject()">拒绝
</button>
        </div>
      </div>
    </div>
  </div>

  <script>
    // Status mapping
    const statusMap = {
      'pending_dorm_manager': { text: '待宿管审批', class: 'tag-pending' },
      'pending_counselor': { text: '待辅导员审批', class: 'tag-pending' },
      'pending_dean': { text: '待学工部审批', class: 'tag-pending' },
      'approved': { text: '已通过', class: 'tag-approved' },
      'rejected': { text: '已拒绝', class: 'tag-rejected' }
    };

    function getStatusDisplay(status) {
      return statusMap[status] || { text: status, class: 'tag' };
    }

    function showScreen(index) {
      document.querySelectorAll('.screen').forEach((s, i) => {
        s.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) => {
        t.classList.toggle('active', i === index);
      });
    }

    async function doLogin() {
      const userId = document.getElementById('loginUserId').value.trim();
      const password = document.getElementById('loginPassword').value.trim();
      const errorEl = document.getElementById('loginError');

      if (!userId || !password) {
        errorEl.textContent = '请输入用户ID和密码';
        errorEl.style.display = 'block';
        return;
      }

      const result = await apiLogin(userId, password);

      if (result.success) {
        errorEl.style.display = 'none';
        document.getElementById('loginUserId').value = '';
        document.getElementById('loginPassword').value = '';

        // Show user bar
        document.getElementById('userBar').style.display = 'flex';
        document.getElementById('currentUserName').textContent = result.user.nam
e;
        const roleMap = {
          'student': '学生',
          'dorm_manager': '宿管员',
          'counselor': '辅导员',
          'dean': '学工部'
        };
        document.getElementById('currentUserRole').textContent = '(' + (roleMap[
result.user.role] || result.user.role) + ')';

        // Update UI based on role
        updateUIForRole(result.user.role);

        // Hide login screen, show appropriate screen
        document.getElementById('screen-login').classList.remove('active');
        if (result.user.role === 'student') {
          showScreen(0); // Student application screen
        } else {
          showScreen(1); // Approval list screen
          loadApprovals();
        }
      } else {
        errorEl.textContent = result.error.error || '登录失败，请检查用户ID和密
码';
        errorEl.style.display = 'block';
      }
    }

    function updateUIForRole(role) {
      const isStudent = role === 'student';
      const isDean = role === 'dean';

      // Update nav tab text
      document.getElementById('nav-approval-text').textContent = isStudent ? '我
的申请' : (isDean ? '备案查询' : '审批列表');

      // Update list page title and role display
      document.getElementById('list-title').textContent = isStudent ? '我的申请'
 : (isDean ? '备案查询' : '审批列表');
      document.getElementById('role-display').textContent = (isStudent ? '学生'
: isDean ? '学工部' : role === 'counselor' ? '辅导员' : '宿管员');

      // Show/hide approval section for student/dean
      const approvalSection = document.getElementById('approval-section');
      if (approvalSection) {
        approvalSection.style.display = (isStudent || isDean) ? 'none' : 'block'
;
      }
    }

    function logout() {
      currentToken = null;
      currentUser = null;
      document.getElementById('userBar').style.display = 'none';
      document.querySelectorAll('.screen').forEach(s => s.classList.remove('acti
ve'));
      document.getElementById('screen-login').classList.add('active');
    }

    // File upload management
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.docx'];
    let uploadedFiles = [];

    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const uploadArea = document.querySelector('.upload-area');

    // File selection handler
    fileInput.addEventListener('change', (e) => {
      handleFiles(e.target.files);
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.style.borderColor = 'var(--primary-color)';
      uploadArea.style.background = '#fafafa';

exec
/bin/bash -lc "rtk sed -n '1,120p' backend/apps/users/views.py" in /home/caohui/
projects/graduation-leave-system
 succeeded in 0ms:
import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import LoginSerializer, LoginResponseSerializer, DemoLoginSeri
alizer


@extend_schema(
    operation_id='auth_login',
    summary='用户登录',
    description='使用用户ID和密码登录，返回JWT access token',
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='登录成功，返回access token和用户信息'
        ),
        400: OpenApiResponse(
            description='登录失败：DRF默认ValidationError格式（非项目envelope）'
        ),
    },
    tags=['认证']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    operation_id='auth_demo_login',
    summary='演示登录（仅开发/演示环境）',
    description='按角色快速登录演示账号。生产环境必须禁用（DEMO_AUTH_ENABLED=fal
se）。',
    request=DemoLoginSerializer,
    responses={
        200: OpenApiResponse(
            response=LoginResponseSerializer,
            description='登录成功，返回access token和用户信息'
        ),
        403: OpenApiResponse(
            description='演示登录已禁用'
        ),
        400: OpenApiResponse(
            description='无效的角色或演示用户不存在'
        ),
    },
    tags=['认证']
)
@api_view(['POST'])
@permission_classes([AllowAny])
def demo_login(request):
    # 生产环境守卫
    if os.environ.get('DEMO_AUTH_ENABLED', 'false').lower() != 'true':
        return Response({'error': 'Demo login is disabled'}, status=status.HTTP_
403_FORBIDDEN)

    serializer = DemoLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

exec
/bin/bash -lc "rtk sed -n '1,180p' backend/apps/users/serializers.py" in /home/c
aohui/projects/graduation-leave-system
 succeeded in 0ms:
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id', 'active', 'is_graduatin
g', 'graduation_year']
        read_only_fields = ['user_id']


class AuthUserSerializer(serializers.ModelSerializer):
    """登录响应中的用户摘要（UserDTO子集）"""
    class Meta:
        model = User
        fields = ['user_id', 'name', 'role', 'class_id']


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        password = attrs.get('password')

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')

        if not user.active:
            raise serializers.ValidationError('Account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }


class LoginResponseSerializer(serializers.Serializer):
    """登录成功响应（schema-only，用于OpenAPI文档）"""
    access_token = serializers.CharField(help_text="JWT access token")
    token_type = serializers.CharField(default='Bearer', help_text="Token type")
    user = AuthUserSerializer(help_text="用户信息")


class DemoLoginSerializer(serializers.Serializer):
    """演示登录（仅在DEMO_AUTH_ENABLED=true时启用）"""
    role = serializers.ChoiceField(choices=['student', 'dorm_manager', 'counselo
r', 'dean'])

    # 角色到演示用户映射
    DEMO_USERS = {
        'student': '2020001',
        'dorm_manager': 'M001',
        'counselor': 'T001',
        'dean': 'D001',
    }

    def validate(self, attrs):
        role = attrs.get('role')
        user_id = self.DEMO_USERS.get(role)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'Demo user for role {role} not fo
und')

        if not user.active:
            raise serializers.ValidationError('Demo account is inactive')

        refresh = RefreshToken.for_user(user)

        return {
            'access_token': str(refresh.access_token),
            'token_type': 'Bearer',
            'user': AuthUserSerializer(user).data
        }

exec
/bin/bash -lc "rtk sed -n '1,80p' backend/apps/users/urls.py" in /home/caohui/pr
ojects/graduation-leave-system
 succeeded in 0ms:
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('demo-login', views.demo_login, name='demo_login'),
]

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '540,625p'" in /home/caoh
ui/projects/graduation-leave-system
exec
/bin/bash -lc 'rtk rg -n "switchRole|roleSelector|role-select|selectedRole|demo-
login|角色选择|select.*role|role.*select|onchange=.*role|data-role" demo-web' in
 /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba backend/apps/users/serializers.py | sed -n '20,45p'" i
n /home/caohui/projects/graduation-leave-system
exec
/bin/bash -lc "rtk nl -ba demo-web/js/api.js | sed -n '1,45p'" in /home/caohui/p
rojects/graduation-leave-system
 succeeded in 102ms:
 succeeded in 103ms:
    20  class LoginSerializer(serializers.Serializer):
    21      user_id = serializers.CharField()
    22      password = serializers.CharField(write_only=True)
    23
    24      def validate(self, attrs):
    25          user_id = attrs.get('user_id')
    26          password = attrs.get('password')
    27
    28          try:
    29              user = User.objects.get(user_id=user_id)
    30          except User.DoesNotExist:
    31              raise serializers.ValidationError('Invalid credentials')
    32
    33          if not user.check_password(password):
    34              raise serializers.ValidationError('Invalid credentials')
    35
    36          if not user.active:
    37              raise serializers.ValidationError('Account is inactive')
    38
    39          refresh = RefreshToken.for_user(user)
    40
    41          return {
    42              'access_token': str(refresh.access_token),
    43              'token_type': 'Bearer',
    44              'user': AuthUserSerializer(user).data
    45          }

 succeeded in 109ms:
   540
   541      function showScreen(index) {
   542        document.querySelectorAll('.screen').forEach((s, i) => {
   543          s.classList.toggle('active', i === index);
   544        });
   545        document.querySelectorAll('.nav-tabs .nav-tab').forEach((t, i) =>
{
   546          t.classList.toggle('active', i === index);
   547        });
   548      }
   549
   550      async function doLogin() {
   551        const userId = document.getElementById('loginUserId').value.trim()
;
   552        const password = document.getElementById('loginPassword').value.tr
im();
   553        const errorEl = document.getElementById('loginError');
   554
   555        if (!userId || !password) {
   556          errorEl.textContent = '请输入用户ID和密码';
   557          errorEl.style.display = 'block';
   558          return;
   559        }
   560
   561        const result = await apiLogin(userId, password);
   562
   563        if (result.success) {
   564          errorEl.style.display = 'none';
   565          document.getElementById('loginUserId').value = '';
   566          document.getElementById('loginPassword').value = '';
   567
   568          // Show user bar
   569          document.getElementById('userBar').style.display = 'flex';
   570          document.getElementById('currentUserName').textContent = result.
user.name;
   571          const roleMap = {
   572            'student': '学生',
   573            'dorm_manager': '宿管员',
   574            'counselor': '辅导员',
   575            'dean': '学工部'
   576          };
   577          document.getElementById('currentUserRole').textContent = '(' + (
roleMap[result.user.role] || result.user.role) + ')';
   578
   579          // Update UI based on role
   580          updateUIForRole(result.user.role);
   581
   582          // Hide login screen, show appropriate screen
   583          document.getElementById('screen-login').classList.remove('active
');
   584          if (result.user.role === 'student') {
   585            showScreen(0); // Student application screen
   586          } else {
   587            showScreen(1); // Approval list screen
   588            loadApprovals();
   589          }
   590        } else {
   591          errorEl.textContent = result.error.error || '登录失败，请检查用
户ID和密码';
   592          errorEl.style.display = 'block';
   593        }
   594      }
   595
   596      function updateUIForRole(role) {
   597        const isStudent = role === 'student';
   598        const isDean = role === 'dean';
   599
   600        // Update nav tab text
   601        document.getElementById('nav-approval-text').textContent = isStude
nt ? '我的申请' : (isDean ? '备案查询' : '审批列表');
   602
   603        // Update list page title and role display
   604        document.getElementById('list-title').textContent = isStudent ? '
我的申请' : (isDean ? '备案查询' : '审批列表');
   605        document.getElementById('role-display').textContent = (isStudent ?
 '学生' : isDean ? '学工部' : role === 'counselor' ? '辅导员' : '宿管员');
   606
   607        // Show/hide approval section for student/dean
   608        const approvalSection = document.getElementById('approval-section'
);
   609        if (approvalSection) {
   610          approvalSection.style.display = (isStudent || isDean) ? 'none' :
 'block';
   611        }
   612      }
   613
   614      function logout() {
   615        currentToken = null;
   616        currentUser = null;
   617        document.getElementById('userBar').style.display = 'none';
   618        document.querySelectorAll('.screen').forEach(s => s.classList.remo
ve('active'));
   619        document.getElementById('screen-login').classList.add('active');
   620      }
   621
   622      // File upload management
   623      const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
   624      const ALLOWED_TYPES = ['.jpg', '.jpeg', '.png', '.pdf', '.doc', '.do
cx'];
   625      let uploadedFiles = [];

 succeeded in 105ms:
exec
/bin/bash -lc 'rtk nl -ba backend/apps/users/urls.py' in /home/caohui/projects/g
raduation-leave-system
 succeeded in 0ms:
     1  from django.urls import path
     2  from . import views
     3
     4  urlpatterns = [
     5      path('login', views.login, name='login'),
     6      path('demo-login', views.demo_login, name='demo_login'),
     7  ]

exec
/bin/bash -lc "rtk rg -n \"include\\(.*users|api/auth|apps.users|users.urls\" ba
ckend config graduation_leave_system" in /home/caohui/projects/graduation-leave-
system
 exited 2 in 0ms:
rg: config: No such file or directory (os error 2)
rg: graduation_leave_system: No such file or directory (os error 2)
backend/scripts/verify_import_integrity.py:14:from apps.users.models import User
backend/scripts/comprehensive_db_analysis.py:16:from apps.users.models import Us
er
backend/scripts/diagnose_xg_api.py:14:from apps.users.integrations.xg_user_clien
t import generate_sign, XGUserAPIConfig, XGUserAPIClient
backend/scripts/xg_api_collection_test.py:27:from apps.users.integrations.xg_use
r_client import XGUserAPIClient, XGUserAPIConfig
backend/scripts/validate_import.py:16:from apps.users.models import User, UserRo
le
backend/scripts/import_graduates.py:16:from apps.users.models import User
backend/scripts/import_missing_counselors.py:13:from apps.users.models import Us
er
backend/config/settings/base.py:34:    'apps.users',
backend/scripts/analyze_department_values.py:14:from apps.users.models import Us
er
backend/scripts/normalize_department_names.py:13:from apps.users.models import U
ser
backend/scripts/verify_system_readiness.py:13:from apps.users.models import User
backend/scripts/export_blocked_students.py:14:from apps.users.models import User
backend/scripts/analyze_graduate_data.py:14:from apps.users.models import User
backend/scripts/normalize_building_null.py:13:from apps.users.models import User
backend/backend/apps/users/management/commands/cleanup_test_data.py:4:from apps.
users.models import User
backend/scripts/verify_db_status.py:14:from apps.users.models import User
backend/scripts/update_offcampus_graduates.py:14:from apps.users.models import U
ser
backend/apps/notifications/tests/test_auto_notifications_api.py:14:from apps.use
rs.class_mapping import ClassMapping
backend/apps/notifications/tests/test_models.py:3:from apps.users.models import
User
backend/apps/notifications/tests/test_api.py:4:from apps.users.models import Use
r
backend/docs/discussions/week3-day3-planning-2026-05-30/06-phase0-final-consensu
s.md:43:1. 添加import: `from apps.users.class_mapping import ClassMapping`
backend/apps/users/class_mapping.py:2:from apps.users.models import User
backend/apps/attachments/models.py:3:from apps.users.models import User
backend/apps/attachments/tests/test_upload.py:5:from apps.users.models import Us
er, UserRole
backend/apps/attachments/tests/test_upload.py:6:from apps.users.class_mapping im
port ClassMapping
backend/apps/attachments/tests/test_list.py:5:from apps.users.models import User
, UserRole
backend/apps/attachments/tests/test_list.py:6:from apps.users.class_mapping impo
rt ClassMapping
backend/apps/attachments/tests/test_download.py:5:from apps.users.models import
User, UserRole
backend/apps/attachments/tests/test_download.py:6:from apps.users.class_mapping
import ClassMapping
backend/apps/attachments/tests/test_delete.py:5:from apps.users.models import Us
er, UserRole
backend/apps/attachments/tests/test_delete.py:6:from apps.users.class_mapping im
port ClassMapping
backend/apps/users/tests/test_xg_user_mapper.py:3:from apps.users.integrations.x
g_user_mapper import map_xg_user_to_internal
backend/apps/attachments/views.py:9:from apps.users.models import UserRole
backend/apps/users/services/xg_user_sync.py:4:from apps.users.integrations.xg_us
er_mapper import map_xg_user_to_internal
backend/apps/users/tests/test_xg_user_client.py:4:from apps.users.integrations.x
g_user_client import generate_sign, XGUserAPIConfig, XGUserAPIClient
backend/apps/users/tests/test_import_csv.py:7:from apps.users.models import User
, UserRole
backend/apps/users/tests/test_import_csv.py:8:from apps.users.class_mapping impo
rt ClassMapping
backend/apps/users/tests/test_xg_user_sync.py:4:from apps.users.services.xg_user
_sync import plan_xg_user_sync, apply_xg_user_sync
backend/apps/users/apps.py:6:    name = 'apps.users'
backend/apps/notifications/management/commands/seed_notifications.py:3:from apps
.users.models import User
backend/apps/users/management/commands/import_students.py:9:from apps.users.mode
ls import User, UserRole
backend/apps/users/management/commands/import_csv.py:4:from apps.users.models im
port User, UserRole
backend/apps/users/management/commands/import_csv.py:5:from apps.users.class_map
ping import ClassMapping
backend/apps/users/management/commands/sync_xg_users.py:3:from apps.users.integr
ations.xg_user_client import XGUserAPIClient
backend/apps/users/management/commands/sync_xg_users.py:4:from apps.users.servic
es.xg_user_sync import apply_xg_user_sync
backend/apps/users/management/commands/cleanup_test_data.py:7:from apps.users.mo
dels import User
backend/apps/users/management/commands/import_staff.py:9:from apps.users.models
import User, UserRole
backend/config/urls.py:8:    path('api/auth/', include('apps.users.urls')),
backend/apps/users/management/commands/seed_data.py:2:from apps.users.models imp
ort User, UserRole
backend/apps/approvals/views.py:14:from apps.users.models import User, UserRole
backend/apps/applications/tests/test_p0_fixes.py:5:from apps.users.models import
 UserRole
backend/apps/applications/tests/test_p0_fixes.py:6:from apps.users.class_mapping
 import ClassMapping
backend/apps/approvals/models.py:2:from apps.users.models import User
backend/apps/applications/tests/test_error_cases.py:6:from apps.users.models imp
ort User, UserRole
backend/apps/applications/tests/test_error_cases.py:7:from apps.users.class_mapp
ing import ClassMapping
backend/apps/applications/tests/test_error_cases.py:86:        response = self.c
lient.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:103:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:131:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:147:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:160:        response = self.
client.post('/api/auth/login', {
backend/apps/applications/tests/test_error_cases.py:173:        response = self.
client.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:6:from apps.users.models imp
ort User, UserRole
backend/apps/approvals/tests/test_rejection_flow.py:7:from apps.users.class_mapp
ing import ClassMapping
backend/apps/approvals/tests/test_rejection_flow.py:56:        response = self.c
lient.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:72:        response = self.c
lient.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:90:        response = self.c
lient.post('/api/auth/login', {
backend/apps/approvals/tests/test_rejection_flow.py:116:        response = self.
client.post('/api/auth/login', {
backend/apps/approvals/tests/test_permissions.py:4:from apps.users.models import
 User, UserRole
backend/apps/approvals/tests/test_permissions.py:7:from apps.users.class_mapping
 import ClassMapping
backend/apps/applications/tests/test_detail_permissions.py:3:from apps.users.mod
els import User, UserRole
backend/apps/applications/tests/test_detail_permissions.py:4:from apps.users.cla
ss_mapping import ClassMapping
backend/apps/approvals/tests/test_state_machine.py:4:from apps.users.models impo
rt User, UserRole
backend/apps/approvals/tests/test_state_machine.py:7:from apps.users.class_mappi
ng import ClassMapping
backend/apps/approvals/tests/test_list_permissions.py:3:from apps.users.models i
mport User, UserRole
backend/apps/applications/models.py:3:from apps.users.models import User
backend/apps/applications/views.py:13:from apps.users.models import UserRole, Us
er
backend/apps/applications/tests/test_constraints.py:6:from apps.users.models imp
ort User, UserRole
backend/apps/applications/tests/test_constraints.py:8:from apps.users.class_mapp
ing import ClassMapping
backend/apps/applications/permissions.py:1:from apps.users.models import UserRol
e, User
backend/apps/applications/tests/test_application_flow.py:6:from apps.users.model
s import User, UserRole
backend/apps/applications/tests/test_application_flow.py:7:from apps.users.class
_mapping import ClassMapping
backend/apps/applications/tests/test_application_flow.py:66:        response = s
elf.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:85:        response = s
elf.client.post('/api/auth/login', {
backend/apps/applications/tests/test_application_flow.py:106:        response =
self.client.post('/api/auth/login', {
backend/apps/applications/tests/test_list_permissions.py:3:from apps.users.model
s import User, UserRole
backend/apps/applications/tests/test_list_permissions.py:4:from apps.users.class
_mapping import ClassMapping

exec
/bin/bash -lc "rtk nl -ba demo-web/index.html | sed -n '306,345p'" in /home/caoh
ui/projects/graduation-leave-system
 succeeded in 0ms:
   306    <!-- 顶部导航 -->
   307    <div class="nav-tabs">
   308      <button class="nav-tab active" onclick="showScreen(0)">学生申请</but
ton>
   309      <button class="nav-tab" onclick="showScreen(1)"><span id="nav-approv
al-text">审批列表</span></button>
   310      <button class="nav-tab" onclick="showScreen(2)">申请详情</button>
   311    </div>
   312
   313    <!-- 登录状态栏 -->
   314    <div id="userBar" style="background: white; padding: 8px 16px; border-
bottom: 1px solid #f0f0f0; display: none; align-items: center; justify-content:
space-between;">
   315      <div>
   316        <span style="font-size: 14px; color: #666;">当前用户:</span>
   317        <span id="currentUserName" style="font-size: 14px; font-weight: 50
0; margin-left: 8px;"></span>
   318        <span id="currentUserRole" style="font-size: 12px; color: #999; ma
rgin-left: 8px;"></span>
   319      </div>
   320      <button onclick="logout()" style="padding: 4px 12px; border: 1px sol
id #d9d9d9; border-radius: 4px; background: white; cursor: pointer;">退出登录</b
utton>
   321    </div>
   322
   323    <!-- 登录屏幕 -->
   324    <div class="screen active" id="screen-login">
   325      <div style="padding: 40px 20px; max-width: 400px; margin: 0 auto;">
   326        <div class="card">
   327          <div style="text-align: center; margin-bottom: 30px;">
   328            <h2 style="color: var(--primary-color); margin-bottom: 8px;">
毕业离校申请系统</h2>
   329            <p style="color: #666; font-size: 14px;">请登录以继续</p>
   330          </div>
   331          <div style="margin-bottom: 20px;">
   332            <label style="display: block; font-size: 14px; margin-bottom:
8px; font-weight: 500;">用户ID</label>
   333            <input id="loginUserId" type="text" style="width: 100%; paddin
g: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;" placeh
older="请输入用户ID（如 2020001）" required>
   334          </div>
   335          <div style="margin-bottom: 24px;">
   336            <label style="display: block; font-size: 14px; margin-bottom:
8px; font-weight: 500;">密码</label>
   337            <input id="loginPassword" type="password" style="width: 100%;
padding: 12px; border: 1px solid #d9d9d9; border-radius: 4px; font-size: 14px;"
placeholder="请输入密码" required>
   338          </div>
   339          <div id="loginError" style="display: none; padding: 10px; backgr
ound: #fff2f0; border: 1px solid #ffccc7; border-radius: 4px; color: #cf1322; fo
nt-size: 14px; margin-bottom: 16px;"></div>
   340          <button class="btn-primary" onclick="doLogin()">登录</button>
   341          <div style="margin-top: 16px; padding: 12px; background: #f6f6f6
; border-radius: 4px;">
   342            <div style="font-size: 12px; color: #666; margin-bottom: 4px;"
>演示账号：</div>
   343            <div style="font-size: 12px; color: #999;">学生: 2020001 / 202
0001</div>
   344            <div style="font-size: 12px; color: #999;">宿管员: M001 / M001
</div>
   345            <div style="font-size: 12px; color: #999;">辅导员: T001 / T001
</div>

exec
/bin/bash -lc "rtk nl -ba backend/config/urls.py | sed -n '1,25p'" in /home/caoh
ui/projects/graduation-leave-system
 succeeded in 0ms:
     1  """URL Configuration"""
     2  from django.contrib import admin
     3  from django.urls import path, include
     4  from drf_spectacular.views import SpectacularAPIView, SpectacularSwagger
View
     5
     6  urlpatterns = [
     7      path('admin/', admin.site.urls),
     8      path('api/auth/', include('apps.users.urls')),
     9      path('api/', include('apps.attachments.urls')),
    10      path('api/applications/', include('apps.applications.urls')),
    11      path('api/approvals/', include('apps.approvals.urls')),
    12      path('api/notifications/', include('apps.notifications.urls')),
    13
    14      # API Documentation
    15      path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    16      path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_na
me='schema'), name='swagger-ui'),
    17  ]

exec
/bin/bash -lc 'rtk rg -n "class UserRole|choices=|ADMIN|admin|dorm_manager|dean|
counselor" backend/apps/users/models.py backend/apps/approvals/views.py backend/
apps/applications/views.py' in /home/caohui/projects/graduation-leave-system
 succeeded in 0ms:
backend/apps/approvals/views.py:47:    # 宿管员: 只看自己的dorm_manager审批
backend/apps/approvals/views.py:54:    # 辅导员: 只看自己的counselor审批
backend/apps/approvals/views.py:111:    # Permission check: only the approver or
 dean can view this approval
backend/apps/approvals/views.py:199:        # Check for existing counselor appro
val to prevent duplicates
backend/apps/approvals/views.py:200:        existing_counselor_approval = Approv
al.objects.filter(
backend/apps/approvals/views.py:205:        if existing_counselor_approval:
backend/apps/approvals/views.py:212:        # Get counselor by department (Phase
 3 design: department-based routing)
backend/apps/approvals/views.py:215:        # Multiple counselors per department
 are allowed (different classes within department).
backend/apps/approvals/views.py:217:        counselors = User.objects.filter(
backend/apps/approvals/views.py:223:        if counselors.count() > 1:
backend/apps/approvals/views.py:225:                f"Multiple counselors found
for department {application.student.department}: "
backend/apps/approvals/views.py:226:                f"{counselors.count()} match
es. Selected {counselors.first().user_id} via order_by('user_id')"
backend/apps/approvals/views.py:229:        counselor = counselors.first()
backend/apps/approvals/views.py:231:        if not counselor:
backend/apps/approvals/views.py:240:            approver=counselor,
backend/apps/approvals/views.py:241:            approver_name=counselor.name,
backend/apps/users/models.py:5:class UserRole(models.TextChoices):
backend/apps/users/models.py:7:    DORM_MANAGER = 'dorm_manager', '宿管员'
backend/apps/users/models.py:8:    COUNSELOR = 'counselor', '辅导员'
backend/apps/users/models.py:9:    DEAN = 'dean', '学工部'
backend/apps/users/models.py:10:    ADMIN = 'admin', '学工管理员'
backend/apps/users/models.py:32:    role = models.CharField(max_length=20, choic
es=UserRole.choices)
backend/apps/applications/views.py:77:    # Counselor: applications with own pen
ding counselor approvals
backend/apps/applications/views.py:91:    elif user.role == UserRole.ADMIN:
backend/apps/applications/views.py:154:        dorm_managers = []
backend/apps/applications/views.py:158:            dorm_managers = list(User.obj
ects.filter(
backend/apps/applications/views.py:164:        if not dorm_managers:
backend/apps/applications/views.py:169:                dorm_managers = [fallback
_manager]
backend/apps/applications/views.py:202:        for dorm_manager in dorm_managers
:
backend/apps/applications/views.py:203:            dorm_manager_approval = Appro
val.objects.create(
backend/apps/applications/views.py:207:                approver=dorm_manager,
backend/apps/applications/views.py:208:                approver_name=dorm_manage
r.name,
backend/apps/applications/views.py:211:            notify_application_submitted(
application, dorm_manager_approval)

exec
/bin/bash -lc "rtk nl -ba backend/apps/users/models.py | sed -n '1,38p'" in /hom
e/caohui/projects/graduation-leave-system
 succeeded in 0ms:
     1  from django.contrib.auth.models import AbstractBaseUser, PermissionsMixi
n, BaseUserManager
     2  from django.db import models
     3
     4
     5  class UserRole(models.TextChoices):
     6      STUDENT = 'student', '学生'
     7      DORM_MANAGER = 'dorm_manager', '宿管员'
     8      COUNSELOR = 'counselor', '辅导员'
     9      DEAN = 'dean', '学工部'
    10      ADMIN = 'admin', '学工管理员'
    11
    12
    13  class UserManager(BaseUserManager):
    14      def create_user(self, user_id, password=None, **extra_fields):
    15          if not user_id:
    16              raise ValueError('user_id is required')
    17          user = self.model(user_id=user_id, **extra_fields)
    18          user.set_password(password)
    19          user.save(using=self._db)
    20          return user
    21
    22      def create_superuser(self, user_id, password=None, **extra_fields):
    23          extra_fields.setdefault('is_staff', True)
    24          extra_fields.setdefault('is_superuser', True)
    25          extra_fields.setdefault('active', True)
    26          return self.create_user(user_id, password, **extra_fields)
    27
    28
    29  class User(AbstractBaseUser, PermissionsMixin):
    30      user_id = models.CharField(max_length=50, unique=True, primary_key=T
rue)
    31      name = models.CharField(max_length=100)
    32      role = models.CharField(max_length=20, choices=UserRole.choices)
    33      active = models.BooleanField(default=True)
    34      class_id = models.CharField(max_length=50, null=True, blank=True)
    35      is_graduating = models.BooleanField(null=True, blank=True)
    36      graduation_year = models.IntegerField(null=True, blank=True)
    37
    38      # API补充字段（学工系统）

codex
[RESPONSE_START]
{
  "consensus": false,
  "decision": "当前实现不能判定为通过。POST /api/auth/login 的路径和成功响应契约
基本匹配，但 demo-web/index.html 的登录后页面切换存在阻塞级错误，角色映射也遗漏
后端合法的 admin 角色。",
  "blocking_issues": [
    "demo-web/index.html 的 showScreen(index) 遍历所有 .screen，包括 #screen-log
in；因此 doLogin 成功后调用 showScreen(0) 会重新激活登录页，showScreen(1) 会激活
学生申请页而不是审批列表页。",
    "后端 UserRole 包含 admin，但 updateUIForRole 仅显式处理 student/dean/counse
lor，其余角色被显示为宿管员并显示审批按钮，admin 登录会得到错误 UI 权限语义。"
  ],
  "reasoning": "我同意 DISCUSS-审计登录设计修复代码-验证DEMO-WEB-1780842596-r0-c
laude 要求先澄清兼容性和验证风险，但初始 framing 中最弱的假设是登录表单替换后页
面导航仍按原来的 0/1/2 索引工作。现在登录页也使用 .screen class，破坏了原 showSc
reen 的索引契约。apiLogin 对成功响应的字段使用与后端 LoginSerializer 返回的 acce
ss_token/user 匹配，/api/auth/login 无尾斜杠也与 urls.py 匹配；但错误响应未规范
化 DRF non_field_errors，且失败登录不会主动清理旧 token/user，建议修复。未发现上
下文中提供 Related Historical Consensus 或 Potential Consensus Conflicts。",
  "previous_responses": [
    "DISCUSS-审计登录设计修复代码-验证DEMO-WEB-1780842596-r0-claude"
  ],
  "targeted_challenges": [
    {
      "target_agent": "claude",
      "target_response_id": "DISCUSS-审计登录设计修复代码-验证DEMO-WEB-178084259
6-r0-claude",
      "question": "请确认本轮验收是否要求支持后端 UserRole.ADMIN；如果支持，admi
n 应映射到只读查询、学工管理员视图，还是禁止进入 demo-web？",
      "rationale": "后端模型声明 admin 为合法角色，当前前端把未知角色落到宿管员
UI，会造成权限语义错误和误导性操作入口。"
    }
  ],
  "dissent": "若 demo-web 明确只面向四个演示账号 student/dorm_manager/counselor/
dean，则 admin 映射可降级为非阻塞；但 showScreen 索引错误仍必须修复后才能通过。"
,
  "evidence": [
    "demo-web/index.html:541-547 showScreen 对所有 .screen 按 NodeList 索引切换
active。",
    "demo-web/index.html:324 登录页 #screen-login 也带有 class=\"screen active\"
，位于 #screen-0/#screen-1/#screen-2 之前。",
    "demo-web/index.html:583-588 登录成功后先移除 #screen-login active，又调用 s
howScreen(0) 或 showScreen(1)，会被 showScreen 重新按错误索引覆盖。",
    "demo-web/js/api.js:9-22 POST 到 /api/auth/login，并读取 access_token 与 use
r；backend/config/urls.py:8 和 backend/apps/users/urls.py:5 共同确认该路径存在。
",
    "backend/apps/users/serializers.py:41-44 登录成功返回 access_token、token_ty
pe、user，与 apiLogin 成功路径匹配。",
    "backend/apps/users/serializers.py:31-37 登录失败为 DRF ValidationError，常
见响应不是 {error: ...}；demo-web/index.html:591 只优先读取 result.error.error。
",
    "backend/apps/users/models.py:5-10 声明 student、dorm_manager、counselor、de
an、admin 五种角色；demo-web/index.html:596-610 未显式处理 admin。",
    "rg 在 demo-web 运行时文件中未发现 switchRole/roleSelector 等旧角色选择器引
用；仅 demo-web/IMPLEMENTATION_NOTES.md 仍有历史说明。"
  ],
  "action_items": [
    {
      "owner": "codex/implementer",
      "task": "修复 showScreen，使登录页不参与业务页索引，或改为按 screen id 切
换；同步修正 nav tab active 逻辑。",
      "due": "before pass",
      "verification": "学生登录后应显示 #screen-0；宿管员/辅导员/学工部登录后应
显示 #screen-1；登录页不再保持 active。"
    },
    {
      "owner": "codex/implementer",
      "task": "补全角色映射策略，至少显式处理 admin 或在登录成功后拒绝不支持角色
并清理会话。",
      "due": "before pass if admin is in scope",
      "verification": "使用 admin 用户登录时 UI 不再显示为宿管员，也不会暴露错误
审批操作。"
    },
    {
      "owner": "codex/implementer",
      "task": "规范化 apiLogin 错误对象，兼容 error/detail/non_field_errors/stri
ng，并在失败登录时避免保留旧 currentToken/currentUser。",
      "due": "recommended",
      "verification": "错误密码、禁用账号、非 JSON 错误、网络异常均显示稳定错误
信息，且 Authorization 不沿用旧 token。"
    },
    {
      "owner": "qa",
      "task": "做一次浏览器级 smoke test 覆盖四个演示账号登录、退出、再登录，以
及旧角色选择器引用扫描。",
      "due": "after fix",
      "verification": "记录每个角色登录后的 active screen、userBar、nav 文案、ap
proval-section 可见性和 logout 后 currentToken/currentUser 清空。"
    }
  ]
}
[RESPONSE_END]
tokens used
49,069

