# 前端设计规范

**项目**: 毕业生离校申请审批系统  
**版本**: v1.0  
**更新日期**: 2026-07-01

---

## 目录

1. [设计原则](#设计原则)
2. [颜色系统](#颜色系统)
3. [字体系统](#字体系统)
4. [组件库](#组件库)
5. [布局规范](#布局规范)
6. [响应式设计](#响应式设计)
7. [交互规范](#交互规范)

---

## 设计原则

### 核心理念

- **庄重严谨**: 使用深红主色调，体现正式教育场景
- **简洁高效**: 扁平化设计，减少视觉干扰
- **移动优先**: 适配手机、平板、桌面多端
- **无障碍访问**: 符合WCAG 2.1 AA标准

### 设计目标

1. 提供清晰的信息层次
2. 简化操作流程
3. 提升用户体验
4. 确保视觉一致性

---

## 颜色系统

### 主色调

```css
--primary-color: #971010;    /* 深红/庄重 */
--primary-hover: #781710;     /* 悬停态 */
```

**使用场景**:
- 主要按钮（提交、确认）
- 重要标题
- 强调信息

### 辅助色

```css
--secondary-color: #B56D18;   /* 金棕 */
--accent-color: #d99749;      /* 暖黄 */
```

**使用场景**:
- 次要按钮
- 辅助信息
- 装饰元素

### 背景色

```css
--bg-color: #f2f2f2;          /* 主背景 */
--bg-secondary: #f7f3eb;      /* 次要背景 */
--card-bg: #FFFFFF;           /* 卡片背景 */
```

### 边框色

```css
--border-color: #e4e4e4;      /* 常规边框 */
--border-accent: #edd9bd;     /* 强调边框 */
```

### 文本色

```css
--text-primary: #333333;      /* 主要文本 */
--text-secondary: #535353;    /* 次要文本 */
--text-tertiary: #787878;     /* 辅助文本 */
```

### 状态色

```css
--status-pending: #F59E0B;    /* 待审批/警告 */
--status-success: #2a7337;    /* 已通过/成功 */
--status-error: #C93939;      /* 已驳回/错误 */
--status-warning: #d99749;    /* 一般警告 */
```

**状态色应用**:
| 状态 | 颜色 | 背景色 | 使用场景 |
|------|------|--------|----------|
| 待审批 | #F59E0B | #FFF7E6 | 标签、提示 |
| 已通过 | #2a7337 | #F6FFED | 标签、提示 |
| 已驳回 | #C93939 | #FFF1F0 | 标签、提示 |

---

## 字体系统

### 字体族

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", 
             "Noto Sans", Helvetica, Arial, sans-serif, 
             "Apple Color Emoji", "Segoe UI Emoji";
```

**优先级**:
1. 系统字体（iOS/macOS）
2. Windows系统字体
3. 跨平台无衬线字体
4. Emoji支持

### 字号规范

```css
--font-xs: 12px;    /* 辅助信息 */
--font-sm: 14px;    /* 正文、标签 */
--font-base: 16px;  /* 主要正文 */
--font-lg: 18px;    /* 二级标题 */
--font-xl: 20px;    /* 一级标题 */
--font-2xl: 24px;   /* 页面标题 */
```

### 字重

```css
--font-normal: 400;
--font-medium: 500;
--font-bold: 600;
```

**使用场景**:
- **400**: 正文、描述
- **500**: 强调文本、标签
- **600**: 标题、按钮

---

## 组件库

### 按钮

#### 主按钮 (Primary)

```css
.btn-primary {
  background: var(--primary-color);
  color: white;
  padding: 10px 24px;
  border-radius: 6px;
  font-weight: 500;
}

.btn-primary:hover {
  background: var(--primary-hover);
}
```

**使用场景**: 提交、确认、主要操作

#### 次按钮 (Outline)

```css
.btn-outline {
  background: transparent;
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  padding: 10px 24px;
  border-radius: 6px;
}

.btn-outline:hover {
  background: var(--primary-color);
  color: white;
}
```

**使用场景**: 取消、返回、次要操作

### 卡片 (Card)

```css
.card {
  background: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border: 1px solid var(--border-color);
}
```

**使用场景**: 内容容器、列表项、信息展示

### 状态标签 (Tag)

```css
.tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

/* 待审批 */
.tag.pending {
  background: #FFF7E6;
  color: #F59E0B;
}

/* 已通过 */
.tag.approved {
  background: #F6FFED;
  color: #2a7337;
}

/* 已驳回 */
.tag.rejected {
  background: #FFF1F0;
  color: #C93939;
}
```

**使用场景**: 审批状态、申请类型标识

### Toast通知

```css
.toast {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9999;
}

.toast.success {
  background: #2a7337;
  color: white;
}

.toast.error {
  background: #C93939;
  color: white;
}
```

**使用场景**: 操作反馈、错误提示、成功消息

---

## 布局规范

### 间距系统

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 12px;
--spacing-lg: 16px;
--spacing-xl: 20px;
--spacing-2xl: 24px;
--spacing-3xl: 32px;
```

**使用规范**:
- 组件内边距: 16-20px (lg-xl)
- 元素间距: 12-16px (md-lg)
- 小元素间距: 8px (sm)
- 卡片间距: 16px (lg)

### 容器

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}
```

**桌面布局** (>1024px): 最大宽度1200px居中

### Flexbox工具类

```css
.flex-row { display: flex; }
.flex-column { display: flex; flex-direction: column; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.align-center { align-items: center; }
.gap-sm { gap: 8px; }
.gap-md { gap: 12px; }
```

---

## 响应式设计

### 断点系统

```css
/* 桌面 */
@media (max-width: 1024px) {
  .container { max-width: 100%; }
}

/* 平板 */
@media (max-width: 768px) {
  .card { padding: 16px; }
  .btn { padding: 8px 16px; }
}

/* 手机 */
@media (max-width: 480px) {
  .card { padding: 12px; }
  .font-base { font-size: 14px; }
}
```

### 响应式布局策略

**桌面 (>1024px)**:
- 容器最大宽度1200px
- 双列布局（表单+预览）
- 卡片网格展示

**平板 (768px-1024px)**:
- 全宽容器
- 单列布局
- 表单字段水平排列

**手机 (<768px)**:
- 全宽容器
- 垂直堆叠布局
- 表单字段垂直排列
- 减小间距和字号

### 触摸优化

```css
@media (max-width: 768px) {
  .btn {
    min-height: 44px;  /* iOS触摸目标推荐尺寸 */
    padding: 12px 20px;
  }
  
  input, textarea {
    font-size: 16px;   /* 防止iOS自动缩放 */
  }
}
```

---

## 交互规范

### 表单交互

**输入框样式**:
```css
input, textarea {
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 16px;
}

input:focus, textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 3px rgba(151, 16, 16, 0.1);
}
```

**错误状态**:
```css
input.error {
  border-color: var(--status-error);
}
```

### 按钮交互

- **悬停**: 背景色加深
- **点击**: 轻微缩放效果
- **禁用**: 50%透明度，禁用点击

```css
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### 加载状态

```css
.loading {
  cursor: wait;
  opacity: 0.6;
}
```

### Toast显示时长

- 成功消息: 2秒
- 错误消息: 3秒
- 警告消息: 2.5秒

---

## 最佳实践

### 颜色使用

✅ **正确**:
- 主按钮使用primary-color
- 状态标签使用对应status色
- 卡片背景使用card-bg

❌ **错误**:
- 不要直接使用硬编码颜色值
- 不要混用状态色和主题色

### 间距使用

✅ **正确**:
- 使用CSS变量定义的间距值
- 保持页面间距一致性

❌ **错误**:
- 不要使用奇数间距值（如13px, 17px）
- 避免过大或过小的间距

### 响应式开发

✅ **正确**:
- 移动优先，逐步增强
- 测试所有断点
- 使用相对单位（rem, em, %）

❌ **错误**:
- 不要只针对桌面设计
- 避免使用固定像素宽度

---

## 文件结构

```
demo-web/
├── css/
│   ├── global.css       # 全局样式和设计系统
│   └── components/      # （未来）组件样式
├── js/
│   ├── api.js          # API交互
│   └── utils.js        # 工具函数
└── index.html          # 主页面
```

---

## 设计演进

### 当前版本 (v1.0)

- 从微信小程序迁移到Web
- 建立基础设计系统
- 实现响应式布局

### 未来规划

- [ ] 暗色模式支持
- [ ] 更丰富的动画效果
- [ ] 组件样式模块化
- [ ] 无障碍访问增强

---

**维护者**: 开发团队  
**联系方式**: 见项目README

