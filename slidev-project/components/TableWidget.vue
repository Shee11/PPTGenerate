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
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  height: 100%;
  overflow: auto;
}

.table-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
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
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid var(--slidev-theme-primary, #3b82f6);
  color: var(--slidev-theme-text, #1f2937);
  background: rgba(0, 0, 0, 0.02);
}

tbody td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr.highlight {
  background: rgba(59, 130, 246, 0.1);
  font-weight: 600;
}

tbody tr:hover {
  background: rgba(0, 0, 0, 0.02);
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
  background: rgba(0, 0, 0, 0.02);
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
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  background: var(--slidev-theme-primary, #3b82f6);
  color: white;
}

.badge.success {
  background: #10b981;
}

.badge.warning {
  background: #f59e0b;
}

.badge.error {
  background: #ef4444;
}

.badge.info {
  background: #3b82f6;
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
