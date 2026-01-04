<!--
  AppBadge.vue
  Reusable badge component for status indicators, roles, and tags.
-->
<template>
  <span :class="badgeClasses">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info' | 'purple'
  size?: 'sm' | 'md' | 'lg'
}>()

const badgeClasses = computed(() => {
  const base = 'inline-flex items-center justify-center font-medium rounded-full'

  // Size classes
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-xs',
    lg: 'px-3 py-1 text-sm',
  }
  const size = sizeClasses[props.size || 'md']

  // Variant classes
  const variantClasses = {
    default: 'bg-zinc-100 text-zinc-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800',
    purple: 'bg-purple-100 text-purple-800',
  }
  const variant = variantClasses[props.variant || 'default']

  return `${base} ${size} ${variant}`
})
</script>
