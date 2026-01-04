<!--
  TALayout.vue
  Layout for TA dashboard. Restricts to TA role.
-->
<template>
  <div class="min-h-screen bg-zinc-50">
    <header class="bg-zinc-800 text-white px-6 py-4 flex items-center justify-between">
      <h1 class="text-xl font-semibold">Lab Evaluation TA</h1>
    </header>
    <nav class="bg-zinc-100 px-6 py-2 flex gap-4">
      <RouterLink to="/ta/evaluations" class="font-semibold hover:underline"
        >Evaluations</RouterLink
      >
      <RouterLink to="/ta/students" class="hover:underline">Students</RouterLink>
      <RouterLink to="/ta/subjects" class="hover:underline">Subjects</RouterLink>
      <RouterLink to="/ta/questions" class="hover:underline">Questions</RouterLink>
    </nav>
    <main class="p-6 max-w-7xl mx-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
// No props; layout is slot-driven
</script>
