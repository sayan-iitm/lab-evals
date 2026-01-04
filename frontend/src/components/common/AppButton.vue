<!--
  AppButton.vue
  Reusable button component styled with Tailwind. Used for all actions.
-->
<template>
  <button :type="type" :class="buttonClasses" :disabled="disabled" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}>()

const buttonClasses = computed(() => {
  const base =
    'inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

  // Size classes
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  }
  const size = sizeClasses[props.size || 'md']

  // Variant classes
  const variantClasses = {
    primary: 'bg-zinc-800 text-white hover:bg-zinc-700 focus:ring-zinc-400',
    secondary: 'bg-zinc-200 text-zinc-900 hover:bg-zinc-300 focus:ring-zinc-400',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-400',
    success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-400',
    ghost: 'bg-transparent text-zinc-700 hover:bg-zinc-100 focus:ring-zinc-400',
  }
  const variant = variantClasses[props.variant || 'primary']

  return `${base} ${size} ${variant}`
})
</script>
