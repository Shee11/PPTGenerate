<!--
  TableWidget.vue - Cyberpunk Data Table Widget
  
  Props:
    - headers: Array of column headers
    - rows: 2D array of table data
    - highlight: Optional row index to highlight
-->
<template>
  <div class="table-widget">
    <div class="table-frame">
      <div class="frame-corner frame-tl"></div>
      <div class="frame-corner frame-tr"></div>
      <div class="frame-corner frame-bl"></div>
      <div class="frame-corner frame-br"></div>
    </div>
    <table class="cyber-table">
      <thead>
        <tr>
          <th v-for="(header, i) in headers" :key="i">
            {{ header }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(row, rowIndex) in rows" 
          :key="rowIndex"
          :class="{ highlighted: rowIndex === highlight }"
        >
          <td v-for="(cell, cellIndex) in row" :key="cellIndex">
            {{ cell }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  headers: string[]
  rows: (string | number)[][]
  highlight?: number
}>()
</script>

<style scoped>
.table-widget {
  position: relative;
  background: rgba(18, 18, 26, 0.9);
  padding: 0.5rem;
}

.table-frame {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.frame-corner {
  position: absolute;
  width: 12px;
  height: 12px;
}

.frame-tl {
  top: 0; left: 0;
  border-top: 2px solid var(--cyber-cyan, #00FFFF);
  border-left: 2px solid var(--cyber-cyan, #00FFFF);
}

.frame-tr {
  top: 0; right: 0;
  border-top: 2px solid var(--cyber-cyan, #00FFFF);
  border-right: 2px solid var(--cyber-cyan, #00FFFF);
}

.frame-bl {
  bottom: 0; left: 0;
  border-bottom: 2px solid var(--cyber-magenta, #FF00FF);
  border-left: 2px solid var(--cyber-magenta, #FF00FF);
}

.frame-br {
  bottom: 0; right: 0;
  border-bottom: 2px solid var(--cyber-magenta, #FF00FF);
  border-right: 2px solid var(--cyber-magenta, #FF00FF);
}

.cyber-table {
  width: 100%;
  border-collapse: collapse;
}

.cyber-table th {
  font-family: var(--cyber-font-display);
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--cyber-cyan, #00FFFF);
  text-transform: uppercase;
  letter-spacing: 1px;
  text-align: left;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(0, 255, 255, 0.3);
  background: rgba(0, 255, 255, 0.05);
}

.cyber-table td {
  font-family: var(--cyber-font-mono);
  font-size: 0.9rem;
  color: var(--cyber-text, #e0e0e0);
  padding: 0.6rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.cyber-table tr:hover {
  background: rgba(0, 255, 255, 0.03);
}

.cyber-table tr.highlighted {
  background: rgba(255, 0, 255, 0.1);
  border-left: 3px solid var(--cyber-magenta, #FF00FF);
}

.cyber-table tr.highlighted td {
  color: var(--cyber-magenta, #FF00FF);
}
</style>
