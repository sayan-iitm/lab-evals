<!--
  AppSelect.vue
  Reusable select component styled with Tailwind. Used for dropdowns.
-->
<template>
  <div class="w-full">
    <div v-if="label" class="flex items-center gap-1 mb-1">
      <label class="block text-sm font-medium text-zinc-700">{{ label }}</label>
      <span v-if="required" class="text-red-500 text-sm">*</span>
    </div>
    <select :class="selectClasses" v-bind="$attrs" :value="modelValue" @change="handleChange">
      <slot />
    </select>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    <p v-if="hint && !error" class="mt-1 text-sm text-zinc-500">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: string | number | null
  label?: string
  error?: string
  hint?: string
  required?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
}>()

const selectClasses = computed(() => {
  const base =
    'w-full px-3 py-2 border rounded-md text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:bg-zinc-100 disabled:cursor-not-allowed'

  if (props.error) {
    return `${base} border-red-300 focus:border-red-500 focus:ring-red-500`
  }

  return `${base} border-zinc-300 focus:border-zinc-400 focus:ring-zinc-400`
})

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
