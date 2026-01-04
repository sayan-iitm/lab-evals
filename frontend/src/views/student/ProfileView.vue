<!--
  ProfileView.vue (Student)
  Student can view their own profile info.
-->
<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">My Profile</h2>
    <div class="bg-white rounded shadow p-6 max-w-md">
      <div class="mb-2"><span class="font-semibold">Name:</span> {{ user?.name }}</div>
      <div class="mb-2"><span class="font-semibold">Email:</span> {{ user?.email }}</div>
      <div class="mb-2"><span class="font-semibold">Role:</span> {{ user?.role }}</div>
      <div class="mb-2"><span class="font-semibold">ID:</span> {{ user?.id }}</div>
      <div class="mb-2"><span class="font-semibold">Joined:</span> {{ user?.created_at }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Student profile view
import { ref, onMounted } from 'vue'
import { getMe } from '../../api/student'
import type { UserResponse } from '../../types/api'

const user = ref<UserResponse | null>(null)
async function load() {
  user.value = await getMe()
}
onMounted(load)
</script>
