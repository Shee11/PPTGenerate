# Slidev 风格组件速查表

## 强风格组件（5个）

### 1. PolaroidCard 📸
**风格**: 拍立得相框  
**关键词**: photo, vintage, creative, portfolio  
```vue
<PolaroidCard caption="Summer 2023" variant="vintage">
  <img src="photo.jpg" />
</PolaroidCard>
```

### 2. NeonFrame ⚡
**风格**: 赛博霓虹  
**关键词**: cyber, tech, futuristic, neon  
```vue
<NeonFrame color="cyan" :pulse="true">
  Your content
</NeonFrame>
```

### 3. GlassCard 🪟
**风格**: 毛玻璃  
**关键词**: modern, iOS, glass, premium  
```vue
<GlassCard variant="tinted" blur="heavy">
  Your content
</GlassCard>
```

### 4. RetroTerminal 🖥️
**风格**: 复古终端  
**关键词**: code, retro, terminal, hacker  
```vue
<RetroTerminal title="SYSTEM" color="green">
  > Your commands
</RetroTerminal>
```

### 5. HolographicCard 🌈
**风格**: 全息投影  
**关键词**: holographic, sci-fi, premium, rainbow  
```vue
<HolographicCard :shimmer="true">
  Your content
</HolographicCard>
```

---

## Vibe 背景效果（6种）

| Vibe | 效果 | 场景 |
|------|------|------|
| `particles` | 漂浮粒子 | 科技、动感 |
| `waves` | 波浪运动 | 平静、流动 |
| `noise` | 胶片颗粒 | 复古、质感 |
| `bokeh` | 散景光斑 | 梦幻、高端 |
| `mesh` | 渐变网格 | 商务、现代 |
| `none` | 无效果 | 默认 |

**用法**:
```yaml
---
layout: smart-grid
vibe: particles
---
```

---

## 快速选择矩阵

| 如果内容是... | 推荐组件 | 推荐 Vibe |
|-------------|---------|----------|
| 产品照片 | PolaroidCard | bokeh |
| AI/科技发布 | NeonFrame | particles |
| 高端服务 | HolographicCard | mesh |
| 代码演示 | RetroTerminal | noise |
| 现代 UI 展示 | GlassCard | waves |
| 创意作品集 | PolaroidCard | bokeh |
| 极客主题 | RetroTerminal | noise |
| 未来概念 | HolographicCard | particles |

---

## 组合示例

### 科技风
```yaml
vibe: particles
```
```vue
<NeonFrame color="cyan">
  <HolographicCard>
    Tech content
  </HolographicCard>
</NeonFrame>
```

### 复古风
```yaml
vibe: noise
```
```vue
<PolaroidCard variant="vintage">
  <RetroTerminal color="amber">
    Retro content
  </RetroTerminal>
</PolaroidCard>
```

### 高端风
```yaml
vibe: mesh
```
```vue
<GlassCard variant="tinted">
  <HolographicCard>
    Premium content
  </HolographicCard>
</GlassCard>
```
