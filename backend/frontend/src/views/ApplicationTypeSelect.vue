<template>
  <div class="type-select-container">
    <h2>请选择业务类型</h2>
    <div class="type-cards">
      <div class="type-card" @click="selectType('leave_school')">
        <h3>离校申请</h3>
        <p>毕业生离校手续办理</p>
      </div>

      <div class="type-card" @click="selectType('stay_school')">
        <h3>留校申请</h3>
        <p>暑期留校住宿申请</p>
      </div>

      <div class="type-card disabled">
        <h3>请假申请</h3>
        <p>即将开放</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApplicationTypeSelect',
  methods: {
    selectType(type) {
      this.$router.push({
        name: 'ApplicationForm',
        query: { type }
      });
    }
  }
}
</script>

<style scoped>
.type-select-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 40px;
}

.type-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.type-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.type-card:hover:not(.disabled) {
  border-color: #409eff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
  transform: translateY(-2px);
}

.type-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #f5f5f5;
}

.type-card h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.type-card p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}
</style>
