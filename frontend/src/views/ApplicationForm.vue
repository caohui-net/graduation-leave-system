<template>
  <div class="form-container">
    <h2>{{ typeTitle }}</h2>

    <form @submit.prevent="submitForm">
      <!-- 留校特有字段 -->
      <div v-if="applicationType === 'stay_school'" class="stay-fields">
        <div class="form-item">
          <label>留校时间 *</label>
          <input type="date" v-model="form.stay_start_date" required>
          <span>至</span>
          <input type="date" v-model="form.stay_end_date" required>
        </div>

        <div class="form-item">
          <label>留校原因 *</label>
          <select v-model="form.stay_reason" required>
            <option value="">请选择</option>
            <option value="exam_prep">考公考研</option>
            <option value="summer_practice">暑期实践</option>
            <option value="teacher_exam">考教师编</option>
            <option value="huangzhou_intern">黄州实习</option>
            <option value="sports_volunteer">体育比赛志愿服务</option>
            <option value="challenge_cup">挑战杯竞赛</option>
            <option value="college_competition">学院组织的比赛</option>
            <option value="mentor_guidance">导师指导</option>
            <option value="other">其它</option>
          </select>
        </div>
      </div>

      <!-- 通用字段 -->
      <div class="form-item">
        <label>联系电话 *</label>
        <input type="tel" v-model="form.contact_phone" required>
      </div>

      <div class="form-item">
        <label>申请原因</label>
        <textarea v-model="form.reason" rows="4"></textarea>
      </div>

      <div class="form-item" v-if="applicationType === 'leave_school'">
        <label>离校日期 *</label>
        <input type="date" v-model="form.leave_date" required>
      </div>

      <div class="form-actions">
        <button type="button" @click="goBack">返回</button>
        <button type="submit">提交申请</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ApplicationForm',
  data() {
    const validTypes = ['leave_school', 'stay_school', 'leave_request'];
    const type = this.$route.query.type;

    // 验证type参数，无效则重定向到选择页
    if (!type || !validTypes.includes(type)) {
      this.$router.replace({ name: 'ApplicationTypeSelect' });
      return { applicationType: 'leave_school', form: {} };
    }

    return {
      applicationType: type,
      form: {
        application_type: type,
        contact_phone: '',
        reason: '',
        leave_date: '',
        stay_start_date: '',
        stay_end_date: '',
        stay_reason: ''
      }
    }
  },
  computed: {
    typeTitle() {
      const titles = {
        'leave_school': '离校申请',
        'stay_school': '留校申请',
        'leave_request': '请假申请'
      };
      return titles[this.applicationType] || '申请表单';
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    async submitForm() {
      try {
        // TODO: API调用
        console.log('提交数据:', this.form);
        alert('提交成功');
        this.$router.push('/');
      } catch (error) {
        alert('提交失败: ' + error.message);
      }
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
}

h2 {
  margin-bottom: 30px;
  color: #333;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-item input,
.form-item select,
.form-item textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-item input[type="date"] {
  width: calc(50% - 20px);
}

.form-item span {
  margin: 0 10px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}

.form-actions button {
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.form-actions button[type="button"] {
  background: #f0f0f0;
  color: #333;
}

.form-actions button[type="submit"] {
  background: #1890ff;
  color: white;
}

.form-actions button:hover {
  opacity: 0.9;
}

.stay-fields {
  padding: 15px;
  background: #f9f9f9;
  border-radius: 4px;
  margin-bottom: 20px;
}
</style>
