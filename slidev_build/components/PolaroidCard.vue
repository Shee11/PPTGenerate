<template>
  <div class="polaroid-card" :class="[variant, { tilted: tilt }]">
    <div class="polaroid-photo">
      <div class="photo-content">
        <slot />
      </div>
    </div>
    <div v-if="caption" class="polaroid-caption">
      {{ caption }}
    </div>
    <div class="polaroid-tape"></div>
  </div>
</template>

<script setup>
const props = defineProps({
  caption: String,
  variant: {
    type: String,
    default: 'classic', // classic, vintage, modern
  },
  tilt: {
    type: Boolean,
    default: true,
  },
})
</script>

<style scoped>
.polaroid-card {
  background: linear-gradient(145deg, #fafafa 0%, #ffffff 100%);
  padding: 1rem;
  padding-bottom: 3rem;
  border-radius: 4px;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.12),
    0 8px 32px rgba(0, 0, 0, 0.08),
    0 1px 3px rgba(0, 0, 0, 0.15);
  position: relative;
  max-width: 400px;
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
}

.polaroid-card.tilted {
  transform: rotate(-2deg);
}

.polaroid-card.tilted:nth-child(even) {
  transform: rotate(2deg);
}

.polaroid-photo {
  background: linear-gradient(145deg, #e8e8e8 0%, #f5f5f5 100%);
  padding: 0.75rem;
  border-radius: 2px;
  position: relative;
}

.photo-content {
  width: 100%;
  aspect-ratio: 4/3;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;
}

/* Film grain texture overlay */
.photo-content::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  pointer-events: none;
  opacity: 0.3;
}

.polaroid-caption {
  font-family: 'Shadows Into Light', 'Comic Sans MS', cursive;
  font-size: 1.1rem;
  text-align: center;
  margin-top: 1rem;
  color: #333;
  font-weight: 400;
}

/* Decorative tape */
.polaroid-tape {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 25px;
  background: linear-gradient(180deg, rgba(255, 255, 200, 0.7) 0%, rgba(255, 255, 180, 0.6) 100%);
  border-left: 1px solid rgba(0, 0, 0, 0.05);
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 
    0 2px 4px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  opacity: 0.8;
}

/* Vintage variant */
.polaroid-card.vintage {
  background: linear-gradient(145deg, #f4f1e8 0%, #faf8f3 100%);
}

.polaroid-card.vintage .photo-content::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(139, 90, 43, 0.15) 100%);
  pointer-events: none;
}

/* Modern variant */
.polaroid-card.modern {
  background: linear-gradient(145deg, #1a1a1a 0%, #2a2a2a 100%);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 4px 16px rgba(0, 0, 0, 0.2);
}

.polaroid-card.modern .polaroid-caption {
  color: #e0e0e0;
}

.polaroid-card.modern .polaroid-tape {
  background: linear-gradient(180deg, rgba(100, 100, 100, 0.4) 0%, rgba(80, 80, 80, 0.3) 100%);
}
</style>
