"""审批模块常量配置"""

# Excel导出表头配置
EXPORT_HEADERS = {
    'stay_school': [
        '姓名', '学号', '学院', '专业', '班级', '手机号',
        '留校开始', '留校结束', '留校原因',
        '楼栋', '房间',
        '提交时间', '状态',
        '辅导员', '审批时间', '审批结果'
    ],
    'leave_school': [
        '姓名', '学号', '学院', '专业', '班级', '手机号',
        '离校日期',
        '楼栋', '房间',
        '提交时间', '状态',
        '宿管员', '审批时间', '审批结果',
        '辅导员', '审批时间', '审批结果'
    ]
}

# 序列化器字段映射（用于前端预览）
SERIALIZER_FIELDS = [
    'id', 'status',
    'student_name', 'student_id', 'department', 'major', 'class_id',
    'contact_phone',
    'leave_date', 'stay_start_date', 'stay_end_date', 'stay_reason',
    'building', 'room_number',
    'created_at'
]
