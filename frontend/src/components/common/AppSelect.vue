<!--
  AppSelect.vue
  Reusable select component styled with Tailwind. Used for dropdowns.
-->
<template>
  <select
    class="w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-400 disabled:opacity-50 disabled:bg-zinc-100"
    v-bind="$attrs"
    :value="modelValue"
    @change="handleChange"
  >
    <slot />
  </select>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string | number | null
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
}>()

function handleChange(event: Event) {
  const target = event.target as HTMLSelectElement
  const value = target.value

  // Handle empty string or "null" string as null
  if (value === '' || value === 'null') {
    emit('update:modelValue', null)
    return
  }

  // Try to convert to number if it looks like a number and the modelValue expects a number type
  const numValue = Number(value)
  if (!isNaN(numValue) && value !== '') {
    // If modelValue is currently a number or null (indicating it could be a number)
    // and we're dealing with a numeric string, emit as number
    if (typeof props.modelValue === 'number' || props.modelValue === null) {
      emit('update:modelValue', numValue)
      return
    }
  }

  // Otherwise emit as string
  emit('update:modelValue', value)
}
</script>

<style scoped lang="scss">
select:disabled {
  cursor: not-allowed;
}
</style>
