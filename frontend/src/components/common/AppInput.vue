<!--
  AppInput.vue
  Reusable input component styled with Tailwind. Used for all text fields.
-->
<template>
  <div class="w-full">
    <div v-if="label" class="flex items-center gap-1 mb-1">
      <label class="block text-sm font-medium text-zinc-700">{{ label }}</label>
      <span v-if="required" class="text-red-500 text-sm">*</span>
    </div>
    <input
      :class="inputClasses"
      v-bind="$attrs"
      :type="type"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    <p v-if="hint && !error" class="mt-1 text-sm text-zinc-500">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  modelValue: string | number
  type?: string
  label?: string
  error?: string
  hint?: string
  required?: boolean
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()

const inputClasses = computed(() => {
  const base =
    'w-full px-3 py-2 border rounded-md text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1'

  if (props.error) {
    return `${base} border-red-300 focus:border-red-500 focus:ring-red-500`
  }

  return `${base} border-zinc-300 focus:border-zinc-400 focus:ring-zinc-400`
})
</script>
