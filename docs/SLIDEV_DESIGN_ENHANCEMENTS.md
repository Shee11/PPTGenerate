# Slidev 设计增强系统

本文档说明三层设计增强机制，用于提升组件的"设计含金量"。

## 概览

我们通过三个层面的增强，让 Slidev 组件从 boring 变得 stunning：

1. **Layout 层**：nth-child 变换打破网格单调
2. **Shell 层**：vibe 参数注入背景光效
3. **Widget 层**：强风格组件库

---

## 1. Layout 层 - 动态网格变换

### 原理

使用 CSS `nth-child` 选择器对网格元素施加不同的变换，打破横平竖直的单调感。

### 实现效果

#### Smart Grid Layout
```css
.grid-cell:nth-child(2) {
  transform: rotate(-1deg);  /* 微旋转 */
}

.grid-cell:nth-child(3) {
  transform: rotate(1deg) translateY(-5px);  /* 旋转+偏移 */
}

.grid-cell:nth-child(4) {
  border-radius: 16px 4px 16px 4px;  /* 不对称圆角 */
}
```

#### Feature Grid Layout
```css
.feature-box:nth-child(odd) {
  transform: translateY(-8px) rotate(-0.5deg);
}

.feature-box:nth-child(even) {
  transform: translateY(8px) rotate(0.5deg);
}
```

#### Timeline Layout
```css
.timeline-step:nth-child(odd) .step-content {
  transform: translateX(5px);
  border-radius: 12px 20px 12px 4px;  /* 交替不对称 */
}
```

### 设计原则

- **微妙为主**：旋转角度控制在 -2° ~ 2° 范围
- **位置变化**：translateX/Y 控制在 -10px ~ 10px
- **不对称美学**：使用不规则 border-radius
- **自然节奏**：通过 odd/even 或 3n+1 创造视觉律动

---

## 2. Shell 层 - Vibe 背景光效系统

### 使用方法

在 slide frontmatter 中添加 `vibe` 参数：

```yaml
---
layout: smart-grid
vibe: particles
---
```

### 可用 Vibe 类型

#### `particles` - 漂浮粒子
```vue
<div class="vibe-particles">
  <div class="particle" v-for="i in 20" :key="i"></div>
</div>
```

**效果**：20 个粒子从下往上漂浮，不同速度和延迟，营造动态能量感

**适用场景**：
- 科技主题演示
- 创新、未来感内容
- 需要活力的页面

#### `waves` - 波浪运动
**效果**：3 层渐变波浪缓慢起伏

**适用场景**：
- 冥想、放松主题
- 海洋、流体相关
- 需要平静氛围

#### `noise` - 胶片颗粒
**效果**：SVG fractalNoise 纹理叠加

**适用场景**：
- 复古、怀旧风格
- 电影感呈现
- 增加质感和深度

#### `bokeh` - 散景光斑
**效果**：12 个模糊光球随机漂浮

**适用场景**：
- 梦幻、浪漫主题
- 高端产品展示
- 柔和优雅氛围

#### `mesh` - 渐变网格
**效果**：多点径向渐变动态变换

**适用场景**：
- 现代商务演示
- 抽象背景
- 专业精致感

### 技术实现

```vue
<!-- SlideShell.vue -->
<template>
  <div class="slidev-slide-shell" :class="vibeClass">
    <div v-if="vibe === 'particles'" class="vibe-particles">
      <!-- Particles rendered here -->
    </div>
    <slot />
  </div>
</template>
```

**性能优化**：
- 使用 CSS 动画代替 JS
- `pointer-events: none` 避免交互干扰
- 控制元素数量（粒子 20 个，散景 12 个）
- 使用 `transform` 而非 `left/top` 提升性能

---

## 3. Widget 层 - 强风格组件库

### 组件清单

| 组件 | 风格 | 使用场景 |
|------|------|----------|
| `<PolaroidCard>` | 拍立得相框 | 照片墙、创意展示、作品集 |
| `<NeonFrame>` | 赛博霓虹 | 科技主题、未来感、突出强调 |
| `<GlassCard>` | 毛玻璃 | 现代 UI、iOS 风格、叠层设计 |
| `<RetroTerminal>` | 复古终端 | 代码展示、极客美学、命令行演示 |
| `<HolographicCard>` | 全息投影 | 科幻主题、高端产品、视觉冲击 |

---

### 组件详解

#### 1. PolaroidCard - 拍立得相框

**特点**：
- 真实物理效果（阴影、纸张纹理）
- 手写体 caption
- 胶片颗粒叠加
- 随机倾斜角度
- 透明胶带装饰

**用法**：
```vue
<PolaroidCard caption="Team Retreat 2024" variant="vintage" :tilt="true">
  <img src="photo.jpg" />
</PolaroidCard>
```

**Variants**：
- `classic` - 经典白框
- `vintage` - 复古泛黄 + 暗角
- `modern` - 黑色极简风

---

#### 2. NeonFrame - 赛博霓虹框

**特点**：
- 4 边 + 4 角霓虹灯管
- 多重 box-shadow 辉光
- 网格背景纹理
- 扫描线效果
- 可选脉冲动画

**用法**：
```vue
<NeonFrame color="cyan" :pulse="true">
  # Cyberpunk 2077
  Welcome to Night City
</NeonFrame>
```

**Colors**：
- `cyan` - 青色（赛博朋克经典）
- `magenta` - 洋红
- `lime` - 荧光绿
- `orange` - 橙色

---

#### 3. GlassCard - 毛玻璃卡片

**特点**：
- `backdrop-filter: blur()` 背景模糊
- 半透明渐变背景
- 高光反射模拟
- 噪点纹理
- 边缘辉光

**用法**：
```vue
<GlassCard variant="tinted" blur="heavy">
  Premium content with iOS-style glass effect
</GlassCard>
```

**Variants**：
- `light` - 亮色玻璃（白底）
- `dark` - 暗色玻璃（黑底）
- `tinted` - 彩色玻璃（蓝紫渐变）

---

#### 4. RetroTerminal - 复古终端

**特点**：
- 窗口标题栏 + 三色按钮
- CRT 扫描线效果
- 屏幕暗角模拟
- 磷光体辉光
- 闪烁光标
- 单色显示（绿/琥珀/青）

**用法**：
```vue
<RetroTerminal title="SYSTEM.EXE" color="green">
> npm run deploy
> Deployment successful ✓
> Server running at http://localhost:3000
</RetroTerminal>
```

**Colors**：
- `green` - 绿色磷光（IBM 5151 风格）
- `amber` - 琥珀色（Apple II 风格）
- `cyan` - 青色（Commodore 64 风格）

---

#### 5. HolographicCard - 全息卡片

**特点**：
- 彩虹渐变扫光
- 色相旋转动画
- 扫描线纹理
- 边缘辉光
- 科幻感十足

**用法**：
```vue
<HolographicCard :shimmer="true">
  **PREMIUM TIER**
  
  Unlock all features
  $99/month
</HolographicCard>
```

**效果**：
- `shimmer: true` - 启用色彩流动动画
- 自动 hue-rotate 360° 循环

---

## 组合使用示例

### 示例 1：科技产品发布会

```yaml
---
layout: hero-split
vibe: particles
ratio: "60-40"
---

::left::
<NeonFrame color="cyan" :pulse="true">
# Next-Gen AI Chip

**10x Performance**  
**50% Less Power**

Available Q2 2024
</NeonFrame>

::right::
<HolographicCard>
  <img src="chip-render.png" />
</HolographicCard>
```

---

### 示例 2：创意作品集展示

```yaml
---
layout: smart-grid
vibe: bokeh
cols: 3
---

::header::
# My Photography

::col1::
<PolaroidCard caption="Street Life" variant="vintage">
  <img src="street.jpg" />
</PolaroidCard>

::col2::
<PolaroidCard caption="Nature" variant="classic">
  <img src="forest.jpg" />
</PolaroidCard>

::col3::
<PolaroidCard caption="Urban Nights" variant="modern">
  <img src="city.jpg" />
</PolaroidCard>
```

---

### 示例 3：开发者技术分享

```yaml
---
layout: full-bleed
vibe: noise
align: center
---

<RetroTerminal title="DEPLOY.SH" color="green">
> git push origin main
> Building Docker image...
> ✓ Image built successfully
> Deploying to production...
> ✓ Deployment complete
> 
> https://app.example.com is live!
</RetroTerminal>
```

---

### 示例 4：高端产品宣传

```yaml
---
layout: comparison
vibe: mesh
---

::beforeLabel::
Standard Plan

::before::
<GlassCard variant="light">
- Basic features
- Email support
- 10 GB storage

$29/mo
</GlassCard>

::afterLabel::
Premium Plan

::after::
<HolographicCard>
- All features
- Priority support
- Unlimited storage
- Advanced analytics

$99/mo
</HolographicCard>
```

---

## LLM 调用指南

### 推荐使用场景映射

| 主题/场景 | 推荐 Vibe | 推荐组件 |
|----------|----------|---------|
| 科技/未来 | particles | NeonFrame, HolographicCard |
| 商务/专业 | mesh | GlassCard, MetricWidget |
| 创意/艺术 | bokeh | PolaroidCard |
| 代码/技术 | noise | RetroTerminal |
| 产品/营销 | waves | HolographicCard, GlassCard |
| 复古/怀旧 | noise | PolaroidCard, RetroTerminal |

### 自动选择逻辑

LLM 在生成 slide 时可按以下逻辑选择：

1. **检测关键词**
   - "tech", "AI", "future" → `vibe: particles` + `NeonFrame`
   - "photo", "gallery", "portfolio" → `vibe: bokeh` + `PolaroidCard`
   - "code", "terminal", "command" → `vibe: noise` + `RetroTerminal`
   - "premium", "pro", "exclusive" → `vibe: mesh` + `HolographicCard`

2. **匹配 layout**
   - `smart-grid` + 图片内容 → 考虑 `PolaroidCard`
   - `full-bleed` + 代码内容 → 考虑 `RetroTerminal`
   - `comparison` + 定价 → 考虑 `HolographicCard`

3. **氛围感知**
   - 需要动感 → `particles`
   - 需要平静 → `waves`
   - 需要质感 → `noise`
   - 需要梦幻 → `bokeh`
   - 需要高级 → `mesh`

---

## 性能优化

### CSS 优先原则
- 所有动画使用 CSS `@keyframes`
- 避免 JavaScript 操作 DOM
- 使用 `transform` 和 `opacity` 触发硬件加速

### 元素数量控制
- particles: 20 个（足够视觉效果）
- bokeh: 12 个（平衡性能和美观）
- 使用 `will-change` 提示浏览器优化

### 条件渲染
```vue
<div v-if="vibe === 'particles'">
  <!-- 只在需要时渲染 -->
</div>
```

---

## 设计原则总结

1. **微妙优先**：变换角度小（-2° ~ 2°），不喧宾夺主
2. **性能第一**：CSS 动画 > JS 动画
3. **主题一致**：组件风格与内容主题匹配
4. **层次清晰**：vibe 在背景，内容在前景
5. **可访问性**：`pointer-events: none` 确保交互不受影响

---

## 开发者备注

### 新增文件
- `slidev-project/components/PolaroidCard.vue`
- `slidev-project/components/NeonFrame.vue`
- `slidev-project/components/GlassCard.vue`
- `slidev-project/components/RetroTerminal.vue`
- `slidev-project/components/HolographicCard.vue`

### 修改文件
- `slidev-project/components/SlideShell.vue` - 添加 vibe 系统
- `slidev-project/layouts/smart-grid.vue` - 添加 nth-child 变换
- `slidev-project/layouts/feature-grid.vue` - 添加 nth-child 变换
- `slidev-project/layouts/timeline.vue` - 添加 nth-child 变换
- `src/layout/slidev/layout_engine.py` - 更新文档

### 测试建议
```bash
# 生成测试演示
python -m cli.uce_render \
  --source data/test/design_showcase.txt \
  --user-instruction "Create a presentation showcasing all new design components" \
  --layout-engine slidev \
  --output output/design_showcase.html \
  --verbose
```

---

**版本**: 1.0.0  
**更新日期**: 2025-12-18  
**作者**: UCE Render Team
