<template>
  <div class="table-widget" :class="variant">
    <div v-if="title" class="table-title">
      <span class="title-icon">📋</span>
      {{ title }}
    </div>
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
          <tr 
            v-for="(row, rowIndex) in rows" 
            :key="rowIndex" 
            :class="{ highlight: row.highlight }"
            :style="{ '--row-index': rowIndex }"
          >
            <td v-for="(col, colIndex) in columns" :key="colIndex" :class="col.align">
              <span v-if="col.format === 'badge'" class="badge" :class="row[col.key + '_variant'] || 'default'">
                {{ row[col.key] }}
              </span>
              <span v-else-if="col.format === 'number'" class="number">
                {{ formatNumber(row[col.key]) }}
              </span>
              <span v-else-if="col.format === 'percent'" class="percent">
                <span class="percent-bar" :style="{ width: `${row[col.key]}%` }"></span>
                <span class="percent-value">{{ row[col.key] }}%</span>
              </span>
              <span v-else-if="col.format === 'change'" class="change" :class="getChangeClass(row[col.key])">
                {{ row[col.key] > 0 ? '📈' : '📉' }} {{ Math.abs(row[col.key]) }}%
              </span>
              <span v-else-if="col.format === 'streak'" class="streak">
                🔥 {{ row[col.key] }}
              </span>
              <span v-else-if="col.format === 'xp'" class="xp">
                ⚡ {{ formatNumber(row[col.key]) }} XP
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
    // Formats: text, badge, number, percent, change, streak, xp
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
  padding: 1.5rem;
  background: white;
  border-radius: 20px;
  height: 100%;
  overflow: auto;
  box-shadow: 
    0 4px 0 var(--duo-green-dark, #46a302),
    0 8px 20px rgba(88, 204, 2, 0.15);
  border: 3px solid var(--duo-green, #58CC02);
  position: relative;
}

.table-title {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-size: 1.25rem;
  font-weight: 800;
  margin-bottom: 1.25rem;
  color: var(--duo-text, #4B4B4B);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.title-icon {
  font-size: 1.5rem;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 0.5rem;
  font-family: var(--duo-font, 'Nunito', sans-serif);
}

thead th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 800;
  color: var(--duo-gray-dark, #777);
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  border-bottom: 3px solid var(--duo-green, #58CC02);
}

th.center { text-align: center; }
th.right { text-align: right; }

tbody tr {
  background: var(--duo-gray-light, #F7F7F7);
  border-radius: 12px;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
  animation: row-enter 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
  animation-delay: calc(var(--row-index) * 0.05s);
}

@keyframes row-enter {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
}

tbody tr:hover {
  transform: scale(1.01);
  background: white;
  box-shadow: 0 4px 12px rgba(88, 204, 2, 0.2);
}

tbody tr.highlight {
  background: rgba(88, 204, 2, 0.15);
}

tbody tr.highlight:hover {
  background: rgba(88, 204, 2, 0.25);
}

tbody td {
  padding: 1rem;
  font-weight: 600;
  color: var(--duo-text, #4B4B4B);
}

tbody td:first-child {
  border-radius: 12px 0 0 12px;
}

tbody td:last-child {
  border-radius: 0 12px 12px 0;
}

td.center { text-align: center; }
td.right { text-align: right; }

/* Badge styling */
.badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 800;
}

.badge.default {
  background: var(--duo-gray-light, #E5E5E5);
  color: var(--duo-gray-dark, #777);
}

.badge.success {
  background: rgba(88, 204, 2, 0.2);
  color: var(--duo-green-dark, #46a302);
}

.badge.warning {
  background: rgba(255, 150, 0, 0.2);
  color: #E68600;
}

.badge.error {
  background: rgba(255, 75, 75, 0.2);
  color: var(--duo-red, #FF4B4B);
}

.badge.info {
  background: rgba(28, 176, 246, 0.2);
  color: var(--duo-blue-dark, #1899D6);
}

/* Number styling */
.number {
  font-family: var(--duo-font-display, 'Nunito', sans-serif);
  font-weight: 800;
}

/* Percent with bar */
.percent {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  position: relative;
}

.percent-bar {
  height: 8px;
  background: linear-gradient(90deg, var(--duo-green, #58CC02) 0%, var(--duo-blue, #1CB0F6) 100%);
  border-radius: 4px;
  min-width: 20px;
  max-width: 100px;
}

.percent-value {
  font-weight: 800;
  color: var(--duo-text, #4B4B4B);
}

/* Change indicator */
.change {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-weight: 800;
}

.change.positive {
  color: var(--duo-green-dark, #46a302);
}

.change.negative {
  color: var(--duo-red, #FF4B4B);
}

/* Streak styling */
.streak {
  font-weight: 800;
  color: var(--duo-orange, #FF9600);
}

/* XP styling */
.xp {
  font-weight: 800;
  color: var(--duo-blue, #1CB0F6);
}

/* Variant: striped */
.table-widget.striped tbody tr:nth-child(odd) {
  background: white;
}

.table-widget.striped tbody tr:nth-child(even) {
  background: var(--duo-gray-light, #F7F7F7);
}

/* Variant: bordered */
.table-widget.bordered {
  border-color: var(--duo-blue, #1CB0F6);
  box-shadow: 
    0 4px 0 var(--duo-blue-dark, #1899D6),
    0 8px 20px rgba(28, 176, 246, 0.15);
}

.table-widget.bordered thead th {
  border-bottom-color: var(--duo-blue, #1CB0F6);
}

/* Variant: minimal */
.table-widget.minimal {
  border: none;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.table-widget.minimal thead th {
  border-bottom-width: 2px;
  border-color: var(--duo-gray-light, #E5E5E5);
}
</style>
