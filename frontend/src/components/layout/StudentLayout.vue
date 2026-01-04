<!--
  StudentLayout.vue
  Layout for student dashboard. Restricts to student role.
-->
<template>
  <div class="min-h-screen bg-zinc-50">
    <header class="bg-zinc-800 text-white px-6 py-4 flex items-center justify-between">
      <h1 class="text-xl font-semibold">Lab Evaluation Student</h1>
    </header>
    <nav class="bg-zinc-100 px-6 py-2 flex gap-4">
      <RouterLink to="/student/questions" class="hover:underline">Questions</RouterLink>
      <RouterLink to="/student/profile" class="hover:underline">Profile</RouterLink>
    </nav>
    <main class="p-6 max-w-5xl mx-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
// No props; layout is slot-driven
</script>
