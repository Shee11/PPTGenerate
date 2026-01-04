<!--
  TableWidget.vue - Business Table Component
  
  Professional data table for business presentations.
  
  Props:
    - title: Table title
    - variant: Table style (default, striped, bordered, minimal)
    - columns: Column definitions
    - rows: Table data
-->
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
                {{ row[col.key] > 0 ? '▲' : '▼' }} {{ Math.abs(row[col.key]) }}%
              </span>
              <span v-else-if="col.format === 'currency'" class="currency">
                ${{ formatNumber(row[col.key]) }}
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
    default: 'default',
  },
  showHeader: {
    type: Boolean,
    default: true,
  },
  columns: {
    type: Array,
    required: true,
  },
  rows: {
    type: Array,
    required: true,
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
  background: var(--c-bg-surface, #ffffff);
  border-radius: var(--radius-card, 8px);
  padding: 1.5rem;
  border: 1px solid var(--c-border, #e5e7eb);
  height: 100%;
  overflow: auto;
}

.table-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--c-text-primary, #1a1a1a);
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-weight: 600;
  color: var(--c-text-secondary, #6b7280);
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  border-bottom: 2px solid var(--c-primary, #0F4C81);
}

td {
  padding: 0.75rem 1rem;
  color: var(--c-text-primary, #1a1a1a);
  border-bottom: 1px solid var(--c-border, #e5e7eb);
}

tr:last-child td {
  border-bottom: none;
}

tr.highlight {
  background: color-mix(in srgb, var(--c-primary, #0F4C81) 5%, transparent);
}

tr:hover {
  background: var(--c-bg-muted, #f9fafb);
}

/* Alignment */
.left { text-align: left; }
.center { text-align: center; }
.right { text-align: right; }

/* Variants */
.striped tbody tr:nth-child(even) {
  background: var(--c-bg-muted, #f9fafb);
}

.bordered table {
  border: 1px solid var(--c-border, #e5e7eb);
}

.bordered th,
.bordered td {
  border: 1px solid var(--c-border, #e5e7eb);
}

.minimal {
  background: transparent;
  border: none;
  padding: 0;
}

.minimal th {
  border-bottom: 1px solid var(--c-border, #e5e7eb);
}

/* Badge */
.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--c-bg-muted, #f3f4f6);
  color: var(--c-text-secondary, #6b7280);
}

.badge.success {
  background: rgba(22, 163, 74, 0.1);
  color: #16a34a;
}

.badge.warning {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.badge.danger {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.badge.info {
  background: rgba(15, 76, 129, 0.1);
  color: #0F4C81;
}

/* Number formatting */
.number {
  font-family: 'Inter', system-ui, sans-serif;
  font-variant-numeric: tabular-nums;
}

.currency {
  font-family: 'Inter', system-ui, sans-serif;
  font-variant-numeric: tabular-nums;
  font-weight: 500;
}

/* Change indicator */
.change {
  font-weight: 600;
  font-size: 0.85rem;
}

.change.positive {
  color: #16a34a;
}

.change.negative {
  color: #dc2626;
}
</style>
