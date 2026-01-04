<!--
  TableWidget.vue - Editorial Table Widget
  
  Props:
    - headers: Table headers array
    - rows: Table data rows
    - caption: Optional table caption
-->
<template>
  <div class="table-widget">
    <table>
      <thead>
        <tr>
          <th v-for="(header, i) in headers" :key="i">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in rows" :key="i">
          <td v-for="(cell, j) in row" :key="j">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="caption" class="table-caption">{{ caption }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  headers: string[]
  rows: string[][]
  caption?: string
}>(), {})
</script>

<style scoped>
.table-widget {
  width: 100%;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  border-bottom: 2px solid var(--edit-gold);
}

th {
  font-family: var(--edit-font-accent);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--edit-text-dark);
  text-align: left;
  padding: 0.75rem 1rem;
}

td {
  font-family: var(--edit-font-body);
  font-size: 0.95rem;
  color: var(--edit-text);
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--edit-border);
}

tbody tr:hover {
  background: rgba(201, 169, 98, 0.05);
}

.table-caption {
  font-family: var(--edit-font-accent);
  font-size: 0.8rem;
  font-style: italic;
  color: var(--edit-text-light);
  margin-top: 0.75rem;
  text-align: right;
}
</style>
