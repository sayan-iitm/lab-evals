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
        <AppButton
          @click="showBulkUpload = true"
          class="bg-blue-600 hover:bg-blue-500 whitespace-nowrap"
          >Bulk Upload CSV</AppButton
        >
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

    <!-- Bulk Upload Modal -->
    <div
      v-if="showBulkUpload"
      class="fixed inset-0 bg-black/30 flex items-center justify-center z-10"
    >
      <div class="bg-white p-6 rounded shadow w-[700px] max-h-[80vh] overflow-auto">
        <h3 class="font-semibold mb-4">Bulk Upload Enrollments</h3>

        <!-- Subject Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2"
            >Select Subject to Enroll Students In:</label
          >
          <AppSelect v-model="bulkUploadSubjectId" class="w-full">
            <option :value="null" disabled>Choose a subject</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </AppSelect>
        </div>

        <div
          v-if="bulkUploadSubjectId"
          class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm"
        >
          <p class="font-semibold mb-1">CSV Format:</p>
          <p>Your CSV file should have a single column with student emails (one per row):</p>
          <ul class="list-disc list-inside mt-1">
            <li><strong>email</strong> (required): Email address of the student</li>
          </ul>
          <p class="mt-2">Available Students:</p>
          <div class="ml-4 text-xs mt-1 max-h-24 overflow-auto bg-white p-2 rounded">
            <div v-for="student in students" :key="student.id" class="py-0.5">
              {{ student.email }} - {{ student.name }}
            </div>
          </div>
          <p class="mt-2">Example:</p>
          <code class="block mt-1 p-2 bg-white rounded">
            email<br />
            alice.johnson@university.edu<br />
            bob.smith@university.edu<br />
            carol.williams@university.edu
          </code>
        </div>

        <input
          v-if="bulkUploadSubjectId"
          ref="fileInput"
          type="file"
          accept=".csv"
          @change="handleFileSelect"
          class="mb-4 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />

        <!-- Validation Errors -->
        <div
          v-if="validationErrors.length > 0"
          class="mb-4 p-3 bg-red-50 border border-red-200 rounded"
        >
          <p class="font-semibold text-red-800 mb-2">Validation Errors:</p>
          <ul class="text-sm text-red-700 list-disc list-inside max-h-40 overflow-auto">
            <li v-for="(error, idx) in validationErrors" :key="idx">{{ error }}</li>
          </ul>
        </div>

        <!-- Preview Table -->
        <div v-if="csvData.length > 0 && validationErrors.length === 0" class="mb-4">
          <p class="font-semibold mb-2">
            Preview ({{ csvData.length }} students enrolling in
            {{ getSubjectName(bulkUploadSubjectId!) }}):
          </p>
          <div class="border rounded max-h-60 overflow-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-50 sticky top-0">
                <tr>
                  <th class="px-3 py-2 text-left">Student Email</th>
                  <th class="px-3 py-2 text-left">Student Name</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, idx) in csvData" :key="idx" class="border-t">
                  <td class="px-3 py-2">{{ getUser(row.user_id)?.email }}</td>
                  <td class="px-3 py-2">{{ getUser(row.user_id)?.name }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Progress Bar -->
        <div v-if="isUploading" class="mb-4">
          <div class="flex justify-between text-sm mb-1">
            <span>Uploading...</span>
            <span>{{ uploadProgress.current }} / {{ uploadProgress.total }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              class="bg-blue-600 h-full transition-all duration-300"
              :style="{ width: `${(uploadProgress.current / uploadProgress.total) * 100}%` }"
            ></div>
          </div>
        </div>

        <!-- Upload Results -->
        <div
          v-if="uploadResults.success.length > 0 || uploadResults.errors.length > 0"
          class="mb-4"
        >
          <div
            v-if="uploadResults.success.length > 0"
            class="mb-2 p-3 bg-green-50 border border-green-200 rounded"
          >
            <p class="text-green-800 font-semibold">
              ✓ Successfully uploaded {{ uploadResults.success.length }} enrollments
            </p>
          </div>
          <div
            v-if="uploadResults.errors.length > 0"
            class="p-3 bg-red-50 border border-red-200 rounded"
          >
            <p class="font-semibold text-red-800 mb-2">Failed uploads:</p>
            <ul class="text-sm text-red-700 list-disc list-inside max-h-40 overflow-auto">
              <li v-for="(error, idx) in uploadResults.errors" :key="idx">{{ error }}</li>
            </ul>
          </div>
        </div>

        <div class="flex gap-2">
          <AppButton
            v-if="
              csvData.length > 0 &&
              validationErrors.length === 0 &&
              !isUploading &&
              uploadResults.success.length === 0 &&
              uploadResults.errors.length === 0
            "
            @click="startUpload"
            :disabled="isUploading"
          >
            Upload {{ csvData.length }} Enrollments
          </AppButton>
          <AppButton @click="closeBulkUpload" :disabled="isUploading">
            {{ isUploading ? 'Uploading...' : 'Close' }}
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admin Enrollments CRUD view
import { ref, onMounted, computed } from 'vue'
import Papa from 'papaparse'
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
import type {
  EnrollmentResponse,
  UserResponse,
  SubjectResponse,
  EnrollmentCreate,
} from '../../types/api'

const enrollments = ref<EnrollmentResponse[]>([])
const users = ref<UserResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const showCreate = ref(false)
const newUserId = ref<number | null>(null)
const newSubjectId = ref<number | null>(null)
const filterSubjectId = ref<number | string>('')

// Bulk upload state
const showBulkUpload = ref(false)
const bulkUploadSubjectId = ref<number | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const csvData = ref<EnrollmentCreate[]>([])
const validationErrors = ref<string[]>([])
const isUploading = ref(false)
const uploadProgress = ref({ current: 0, total: 0 })
const uploadResults = ref<{ success: string[]; errors: string[] }>({ success: [], errors: [] })

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
  const enrollment = enrollments.value.find((e) => e.id === id)
  if (enrollment) {
    const user = getUser(enrollment.user_id)
    const subjectName = getSubjectName(enrollment.subject_id)
    const userName = user?.name || 'this student'
    if (
      !confirm(
        `Are you sure you want to remove ${userName} from ${subjectName}? This action cannot be undone.`,
      )
    ) {
      return
    }
  } else {
    if (
      !confirm('Are you sure you want to delete this enrollment? This action cannot be undone.')
    ) {
      return
    }
  }
  await deleteEnrollment(id)
  await load()
}

// Bulk upload functions
function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file) return

  // Reset state
  csvData.value = []
  validationErrors.value = []
  uploadResults.value = { success: [], errors: [] }

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      validateAndLoadCSV(results.data as Record<string, string>[])
    },
    error: (error) => {
      validationErrors.value = [`CSV parsing error: ${error.message}`]
    },
  })
}

function validateAndLoadCSV(data: Record<string, string>[]) {
  const errors: string[] = []
  const validData: EnrollmentCreate[] = []
  const csvEmails = new Set<string>()

  if (!bulkUploadSubjectId.value) {
    errors.push('Please select a subject first')
    validationErrors.value = errors
    return
  }

  const subjectId = bulkUploadSubjectId.value
  const subject = subjects.value.find((s) => s.id === subjectId)

  if (data.length === 0) {
    errors.push('CSV file is empty')
    validationErrors.value = errors
    return
  }

  data.forEach((row, index) => {
    const rowNum = index + 2 // +2 because of header row and 0-based index

    // Validate email
    if (!row.email || !row.email.trim()) {
      errors.push(`Row ${rowNum}: 'email' is required`)
      return
    }

    const email = row.email.trim().toLowerCase()

    // Basic email format validation
    if (!email.includes('@') || !email.includes('.')) {
      errors.push(`Row ${rowNum}: 'email' must be a valid email address`)
      return
    }

    // Check for duplicate emails within the CSV
    if (csvEmails.has(email)) {
      errors.push(`Row ${rowNum}: duplicate email '${row.email.trim()}' found in CSV`)
      return
    }
    csvEmails.add(email)

    // Find user by email
    const user = users.value.find((u) => u.email.toLowerCase() === email)
    if (!user) {
      errors.push(`Row ${rowNum}: student with email '${row.email.trim()}' does not exist`)
      return
    }

    // Check if user is a student
    if (user.role !== 'student') {
      errors.push(`Row ${rowNum}: user '${row.email.trim()}' is not a student (role: ${user.role})`)
      return
    }

    const userId = user.id

    // Check if enrollment already exists in database
    const existingEnrollment = enrollments.value.find(
      (e) => e.user_id === userId && e.subject_id === subjectId,
    )
    if (existingEnrollment) {
      errors.push(`Row ${rowNum}: ${user.name} is already enrolled in ${subject?.name}`)
      return
    }

    validData.push({
      user_id: userId,
      subject_id: subjectId,
    })
  })

  if (errors.length > 0) {
    validationErrors.value = errors
  } else {
    csvData.value = validData
  }
}

async function startUpload() {
  if (csvData.value.length === 0) return

  isUploading.value = true
  uploadProgress.value = { current: 0, total: csvData.value.length }
  uploadResults.value = { success: [], errors: [] }

  for (let i = 0; i < csvData.value.length; i++) {
    const enrollment = csvData.value[i]
    const user = getUser(enrollment.user_id)
    const subjectName = getSubjectName(enrollment.subject_id)

    try {
      await createEnrollment(enrollment)
      uploadResults.value.success.push(`${user?.name} enrolled in ${subjectName}`)
      uploadProgress.value.current++
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
      uploadResults.value.errors.push(`${user?.name} in ${subjectName}: ${errorMessage}`)
      uploadProgress.value.current++
    }
  }

  isUploading.value = false

  // Reload the enrollments list
  await load()
}

function closeBulkUpload() {
  showBulkUpload.value = false
  bulkUploadSubjectId.value = null
  csvData.value = []
  validationErrors.value = []
  uploadResults.value = { success: [], errors: [] }
  uploadProgress.value = { current: 0, total: 0 }
  isUploading.value = false

  // Reset file input
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>
