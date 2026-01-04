<!--
  TableWidget.vue - Handdrawn Table Component
  
  Props:
    - headers: Table headers
    - rows: Table data rows
-->
<template>
  <div class="table-widget">
    <div class="table-paper">
      <!-- Paper clip -->
      <div class="table-clip">📎</div>
      
      <table class="hand-table">
        <thead v-if="headers.length">
          <tr>
            <th v-for="(header, i) in headers" :key="i">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in rows" :key="i" :class="`row-${i % 2 === 0 ? 'even' : 'odd'}`">
            <td v-for="(cell, j) in row" :key="j">{{ cell }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  headers?: string[]
  rows?: (string | number)[][]
}>(), {
  headers: () => [],
  rows: () => []
})
</script>

<style scoped>
.table-widget {
  width: 100%;
}

.table-paper {
  position: relative;
  background: var(--hand-bg-cream);
  border: 2px solid var(--hand-text-light);
  border-radius: 8px;
  padding: 1.5rem;
  padding-top: 2rem;
  box-shadow: 4px 4px 0 var(--hand-shadow-color);
  transform: rotate(-0.5deg);
}

.table-clip {
  position: absolute;
  top: -10px;
  left: 20px;
  font-size: 1.5rem;
  transform: rotate(-15deg);
}

.hand-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.hand-table th {
  font-family: var(--hand-font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--hand-bg-cream);
  background: var(--hand-pink);
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 3px solid var(--hand-text-dark);
}

.hand-table th:first-child {
  border-radius: 8px 0 0 0;
}

.hand-table th:last-child {
  border-radius: 0 8px 0 0;
}

.hand-table td {
  font-family: var(--hand-font-body);
  font-size: 0.95rem;
  color: var(--hand-text);
  padding: 0.65rem 1rem;
  border-bottom: 1px dashed var(--hand-text-light);
}

.row-even {
  background: var(--hand-pink-light);
}

.row-odd {
  background: transparent;
}

.hand-table tr:last-child td {
  border-bottom: none;
}

.hand-table tr:last-child td:first-child {
  border-radius: 0 0 0 8px;
}

.hand-table tr:last-child td:last-child {
  border-radius: 0 0 8px 0;
}
</style>
