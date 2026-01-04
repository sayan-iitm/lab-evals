<!--
  EnrollmentsView.vue (Admin)
  Admin can view, create, and delete enrollments.
-->
<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Enrollments</h2>
      <div class="flex gap-2 items-center">
        <AppSelect v-model="filterSubjectId" class="w-64">
          <option value="">All Subjects</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </AppSelect>
        <AppButton @click="showCreate = true" class="whitespace-nowrap">Add Enrollment</AppButton>
      </div>
    </div>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>User Email</th>
        <th>User Name</th>
        <th>Subject</th>
        <th>Actions</th>
      </template>
      <tr v-for="enrollment in filteredEnrollments" :key="enrollment.id">
        <td>{{ enrollment.id }}</td>
        <td>{{ getUser(enrollment.user_id)?.email }}</td>
        <td>{{ getUser(enrollment.user_id)?.name }}</td>
        <td>{{ getSubjectName(enrollment.subject_id) }}</td>
        <td>
          <AppButton
            class="bg-red-600 hover:bg-red-500"
            @click="deleteEnrollmentHandler(enrollment.id)"
            >Delete</AppButton
          >
        </td>
      </tr>
    </AppTable>
    <!-- Create Modal -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/30 flex items-center justify-center z-10">
      <div class="bg-white p-6 rounded shadow w-96">
        <h3 class="font-semibold mb-4">Add Enrollment</h3>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Student</label>
          <AppSelect v-model="newUserId">
            <option :value="null" disabled>Select a student</option>
            <option v-for="user in students" :key="user.id" :value="user.id">
              {{ user.name }} ({{ user.email }})
            </option>
          </AppSelect>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Subject</label>
          <AppSelect v-model="newSubjectId" :disabled="!newUserId">
            <option :value="null" disabled>Select a subject</option>
            <option v-for="subject in availableSubjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </AppSelect>
        </div>
        <div class="flex gap-2">
          <AppButton @click="createEnrollmentHandler">Create</AppButton>
          <AppButton @click="showCreate = false">Cancel</AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admin Enrollments CRUD view
import { ref, onMounted, computed } from 'vue'
import AppButton from '../../components/common/AppButton.vue'
import AppSelect from '../../components/common/AppSelect.vue'
import AppTable from '../../components/common/AppTable.vue'
import {
  getEnrollments,
  createEnrollment,
  deleteEnrollment,
  getUsers,
  getSubjects,
} from '../../api/admin'
import type { EnrollmentResponse, UserResponse, SubjectResponse } from '../../types/api'

const enrollments = ref<EnrollmentResponse[]>([])
const users = ref<UserResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const showCreate = ref(false)
const newUserId = ref<number | null>(null)
const newSubjectId = ref<number | null>(null)
const filterSubjectId = ref<number | string>('')

const filteredEnrollments = computed(() => {
  if (!filterSubjectId.value) return enrollments.value
  return enrollments.value.filter((e) => e.subject_id === Number(filterSubjectId.value))
})

const students = computed(() => {
  return users.value.filter((u) => u.role === 'student')
})

const availableSubjects = computed(() => {
  if (!newUserId.value) return []
  const studentEnrollments = enrollments.value.filter((e) => e.user_id === newUserId.value)
  const enrolledSubjectIds = studentEnrollments.map((e) => e.subject_id)
  return subjects.value.filter((s) => !enrolledSubjectIds.includes(s.id))
})

async function load() {
  ;[enrollments.value, users.value, subjects.value] = await Promise.all([
    getEnrollments(),
    getUsers(),
    getSubjects(),
  ])
}
onMounted(load)

function getUser(id: number) {
  return users.value.find((u) => u.id === id)
}
function getSubjectName(id: number) {
  return subjects.value.find((s) => s.id === id)?.name || ''
}

async function createEnrollmentHandler() {
  if (!newUserId.value || !newSubjectId.value) return
  await createEnrollment({ user_id: newUserId.value, subject_id: newSubjectId.value })
  newUserId.value = null
  newSubjectId.value = null
  showCreate.value = false
  await load()
}

async function deleteEnrollmentHandler(id: number) {
  await deleteEnrollment(id)
  await load()
}
</script>
