<!--
  AppTable.vue
  Reusable table component styled with Tailwind. Used for all data tables.
-->
<template>
  <table class="min-w-full border border-zinc-200 rounded-md">
    <thead class="bg-zinc-100 text-left">
      <tr>
        <slot name="head" />
      </tr>
    </thead>
    <tbody>
      <slot />
    </tbody>
  </table>
</template>

<script setup lang="ts">
// No props; table is slot-driven
</script>

<style scoped>
table :deep(td),
table :deep(th) {
  padding: 0.75rem; /* px-3 py-2 */
  border-bottom: 1px solid #e4e4e7; /* zinc-200 */
}

table :deep(th) {
  font-weight: 600;
}
</style>
