<!--
  AppTable.vue
  Reusable table component styled with Tailwind. Used for all data tables.
-->
<template>
  <div class="overflow-x-auto rounded-lg border border-zinc-200 bg-white shadow-sm">
    <table class="min-w-full divide-y divide-zinc-200">
      <thead class="bg-zinc-50">
        <tr>
          <slot name="head" />
        </tr>
      </thead>
      <tbody class="divide-y divide-zinc-200 bg-white">
        <slot />
      </tbody>
    </table>
    <div v-if="isEmpty" class="px-6 py-12 text-center">
      <svg
        class="mx-auto h-12 w-12 text-zinc-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        aria-hidden="true"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
        />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-zinc-900">No data</h3>
      <p class="mt-1 text-sm text-zinc-500">{{ emptyMessage || 'No records found.' }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isEmpty?: boolean
  emptyMessage?: string
}>()
</script>

<style scoped>
table :deep(td),
table :deep(th) {
  padding: 0.875rem 1rem;
  text-align: left;
  font-size: 0.875rem;
}

table :deep(th) {
  font-weight: 600;
  color: #3f3f46; /* zinc-700 */
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.75rem;
}

table :deep(tbody tr) {
  transition: background-color 0.15s ease;
}

table :deep(tbody tr:hover) {
  background-color: #fafafa; /* zinc-50 */
}

table :deep(td) {
  color: #18181b; /* zinc-900 */
}
</style>
