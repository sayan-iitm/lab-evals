<!--
  AppInput.vue
  Reusable input component styled with Tailwind. Used for all text fields.
-->
<template>
  <input
    class="w-full px-3 py-2 border border-zinc-300 rounded-md focus:outline-none focus:ring-2 focus:ring-zinc-400"
    v-bind="$attrs"
    :type="type"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string | number
  type?: string
}>()
</script>
