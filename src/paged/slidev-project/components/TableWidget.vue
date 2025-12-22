<template>
  <div class="table-widget" :class="variant">
    <div v-if="title" class="table-title">{{ title }}</div>
    <div class="table-container">
      <table>
        <thead v-if="showHeader">
          <tr>
            <th v-for="(col, index) in columns" :key="index" :class="col.align">
              {{ col.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in rows" :key="rowIndex" :class="{ highlight: row.highlight }">
            <td v-for="(col, colIndex) in columns" :key="colIndex" :class="col.align">
              <span v-if="col.format === 'badge'" class="badge" :class="row[col.key + '_variant']">
                {{ row[col.key] }}
              </span>
              <span v-else-if="col.format === 'number'" class="number">
                {{ formatNumber(row[col.key]) }}
              </span>
              <span v-else-if="col.format === 'percent'" class="percent">
                {{ row[col.key] }}%
              </span>
              <span v-else-if="col.format === 'change'" class="change" :class="getChangeClass(row[col.key])">
                {{ row[col.key] > 0 ? '↑' : '↓' }} {{ Math.abs(row[col.key]) }}%
              </span>
              <span v-else>{{ row[col.key] }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  variant: {
    type: String,
    default: 'default', // default, striped, bordered, minimal
  },
  showHeader: {
    type: Boolean,
    default: true,
  },
  columns: {
    type: Array,
    required: true,
    // Format: [{ key: 'name', label: 'Name', align: 'left', format: 'text' }, ...]
    // Formats: text, badge, number, percent, change
  },
  rows: {
    type: Array,
    required: true,
    // Format: [{ name: 'Product A', value: 1234, change: 12.5, highlight: false }, ...]
  },
})

const formatNumber = (num) => {
  if (typeof num !== 'number') return num
  return num.toLocaleString()
}

const getChangeClass = (value) => {
  return value > 0 ? 'positive' : 'negative'
}
</script>

<style scoped>
.table-widget {
  padding: 2rem;
  background: linear-gradient(145deg,
    color-mix(in srgb, var(--c-bg-base) 98%, white) 0%,
    color-mix(in srgb, var(--c-bg-base) 95%, white) 100%);
  border-radius: 12px;
  height: 100%;
  overflow: auto;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.06),
    0 1px 3px rgba(0, 0, 0, 0.08);
  border: 1px solid color-mix(in srgb, white 10%, transparent);
  position: relative;
}

/* Top accent */
.table-widget::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, 
    var(--slidev-theme-primary, #3b82f6) 0%, 
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 70%, #8b5cf6) 100%);
  border-radius: 12px 12px 0 0;
}

.table-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--slidev-theme-text, #1f2937);
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

thead th {
  padding: 1rem 1.25rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 3px solid var(--slidev-theme-primary, #3b82f6);
  color: var(--slidev-theme-text, #1f2937);
  background: linear-gradient(180deg,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 8%, transparent) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 3%, transparent) 100%);
  position: relative;
}

/* Gradient underline on headers */
thead th::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg,
    transparent 0%,
    var(--slidev-theme-primary, #3b82f6) 50%,
    transparent 100%);
  opacity: 0.3;
}

tbody td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr.highlight {
  background: linear-gradient(90deg,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 12%, transparent) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 8%, transparent) 100%);
  font-weight: 600;
  box-shadow: inset 3px 0 0 var(--slidev-theme-primary, #3b82f6);
}

tbody tr:hover {
  background: linear-gradient(90deg,
    rgba(0, 0, 0, 0.02) 0%,
    rgba(0, 0, 0, 0.01) 100%);
}

/* Alignment */
.left {
  text-align: left;
}

.center {
  text-align: center;
}

.right {
  text-align: right;
}

/* Variants */
.striped tbody tr:nth-child(even) {
  background: linear-gradient(90deg,
    rgba(0, 0, 0, 0.02) 0%,
    rgba(0, 0, 0, 0.01) 50%,
    rgba(0, 0, 0, 0.02) 100%);
}

.striped tbody tr:nth-child(odd):hover,
.striped tbody tr:nth-child(even):hover {
  background: linear-gradient(90deg,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 6%, transparent) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 3%, transparent) 50%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 6%, transparent) 100%);
}

.bordered table {
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.bordered td,
.bordered th {
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.minimal thead th {
  background: transparent;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}

.minimal tbody td {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

/* Formatters */
.badge {
  display: inline-block;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  background: linear-gradient(135deg,
    var(--slidev-theme-primary, #3b82f6) 0%,
    color-mix(in srgb, var(--slidev-theme-primary, #3b82f6) 80%, #8b5cf6) 100%);
  color: white;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
}

.badge.success {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
}

.badge.warning {
  background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
  box-shadow: 0 2px 6px rgba(245, 158, 11, 0.3);
}

.badge.error {
  background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
}

.badge.info {
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
}

.number {
  font-variant-numeric: tabular-nums;
  font-weight: 500;
}

.percent {
  font-variant-numeric: tabular-nums;
  color: var(--slidev-theme-primary, #3b82f6);
  font-weight: 600;
}

.change {
  font-variant-numeric: tabular-nums;
  font-weight: 600;
}

.change.positive {
  color: #10b981;
}

.change.negative {
  color: #ef4444;
}
</style>
