<!--
  AdminLayout.vue
  Layout for admin dashboard. Restricts to admin role.
-->
<template>
  <div class="min-h-screen bg-zinc-50">
    <header class="bg-zinc-800 text-white px-6 py-4 flex items-center justify-between">
      <h1 class="text-xl font-semibold">Lab Evaluation Admin</h1>
    </header>
    <nav class="bg-zinc-100 px-6 py-2 flex gap-4">
      <RouterLink to="/admin/subjects" class="hover:underline">Subjects</RouterLink>
      <RouterLink to="/admin/questions" class="hover:underline">Questions</RouterLink>
      <RouterLink to="/admin/users" class="hover:underline">Users</RouterLink>
      <RouterLink to="/admin/enrollments" class="hover:underline">Enrollments</RouterLink>
      <RouterLink to="/admin/evaluations" class="hover:underline">Evaluations</RouterLink>
    </nav>
    <main class="p-6 max-w-5xl mx-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// No props; layout is slot-driven
</script>
