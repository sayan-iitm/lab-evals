<!--
  SubjectsView.vue (Admin)
  Admin can view, create, edit, and delete subjects.
-->
<template>
  <div class="flex justify-end mb-4 gap-2">
    <AppButton @click="showCreate = true">Add Subject</AppButton>
    <AppButton @click="showBulkUpload = true" class="bg-blue-600 hover:bg-blue-500"
      >Bulk Upload CSV</AppButton
    >
  </div>
  <h2 class="text-xl font-semibold mb-4">Subjects</h2>
  <AppTable>
    <template #head>
      <th>ID</th>
      <th>Name</th>
      <th>Description</th>
      <th>Actions</th>
    </template>
    <tr v-for="subject in subjects" :key="subject.id">
      <td>{{ subject.id }}</td>
      <td v-if="editId !== subject.id">{{ subject.name }}</td>
      <td v-else>
        <AppInput v-model="editName" />
      </td>
      <td v-if="editId !== subject.id">{{ subject.description || '-' }}</td>
      <td v-else>
        <AppInput v-model="editDescription" />
      </td>
      <td>
        <div class="flex gap-2">
          <AppButton v-if="editId !== subject.id" @click="startEdit(subject)">Edit</AppButton>
          <AppButton v-if="editId === subject.id" @click="saveEdit(subject.id)">Save</AppButton>
          <AppButton v-if="editId === subject.id" @click="cancelEdit">Cancel</AppButton>
          <AppButton class="bg-red-600 hover:bg-red-500" @click="deleteSubjectHandler(subject.id)"
            >Delete</AppButton
          >
        </div>
      </td>
    </tr>
  </AppTable>
  <!-- Create Modal -->
  <div v-if="showCreate" class="fixed inset-0 bg-black/30 flex items-center justify-center z-10">
    <div class="bg-white p-6 rounded shadow w-80">
      <h3 class="font-semibold mb-2">Add Subject</h3>
      <AppInput v-model="newName" placeholder="Subject name" class="mb-2" />
      <AppInput v-model="newDescription" placeholder="Description (optional)" />
      <div class="flex gap-2 mt-4">
        <AppButton @click="createSubjectHandler">Create</AppButton>
        <AppButton @click="showCreate = false">Cancel</AppButton>
      </div>
    </div>
  </div>

  <!-- Bulk Upload Modal -->
  <div
    v-if="showBulkUpload"
    class="fixed inset-0 bg-black/30 flex items-center justify-center z-10"
  >
    <div class="bg-white p-6 rounded shadow w-[600px] max-h-[80vh] overflow-auto">
      <h3 class="font-semibold mb-4">Bulk Upload Subjects</h3>

      <div class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm">
        <p class="font-semibold mb-1">CSV Format:</p>
        <p>Your CSV file should have the following columns:</p>
        <ul class="list-disc list-inside mt-1">
          <li><strong>name</strong> (required): Subject name</li>
          <li><strong>description</strong> (optional): Subject description</li>
        </ul>
        <p class="mt-2">Example:</p>
        <code class="block mt-1 p-2 bg-white rounded">
          name,description<br />
          Mathematics,Introduction to Algebra<br />
          Physics,Classical Mechanics
        </code>
      </div>

      <input
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
        <p class="font-semibold mb-2">Preview ({{ csvData.length }} subjects):</p>
        <div class="border rounded max-h-60 overflow-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 sticky top-0">
              <tr>
                <th class="px-3 py-2 text-left">Name</th>
                <th class="px-3 py-2 text-left">Description</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in csvData" :key="idx" class="border-t">
                <td class="px-3 py-2">{{ row.name }}</td>
                <td class="px-3 py-2">{{ row.description || '-' }}</td>
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
      <div v-if="uploadResults.success.length > 0 || uploadResults.errors.length > 0" class="mb-4">
        <div
          v-if="uploadResults.success.length > 0"
          class="mb-2 p-3 bg-green-50 border border-green-200 rounded"
        >
          <p class="text-green-800 font-semibold">
            ✓ Successfully uploaded {{ uploadResults.success.length }} subjects
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
          Upload {{ csvData.length }} Subjects
        </AppButton>
        <AppButton @click="closeBulkUpload" :disabled="isUploading">
          {{ isUploading ? 'Uploading...' : 'Close' }}
        </AppButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admin Subjects CRUD view
import { ref, onMounted } from 'vue'
import Papa from 'papaparse'
import AppButton from '../../components/common/AppButton.vue'
import AppInput from '../../components/common/AppInput.vue'
import AppTable from '../../components/common/AppTable.vue'
import { getSubjects, createSubject, updateSubject, deleteSubject } from '../../api/admin'
import type { SubjectResponse, SubjectCreate } from '../../types/api'

const subjects = ref<SubjectResponse[]>([])
const showCreate = ref(false)
const newName = ref('')
const newDescription = ref('')
const editId = ref<number | null>(null)
const editName = ref('')
const editDescription = ref('')

// Bulk upload state
const showBulkUpload = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const csvData = ref<SubjectCreate[]>([])
const validationErrors = ref<string[]>([])
const isUploading = ref(false)
const uploadProgress = ref({ current: 0, total: 0 })
const uploadResults = ref<{ success: string[]; errors: string[] }>({ success: [], errors: [] })

async function load() {
  subjects.value = await getSubjects()
}
onMounted(load)

async function createSubjectHandler() {
  if (!newName.value.trim()) return
  await createSubject({
    name: newName.value,
    description: newDescription.value.trim() || null,
  })
  newName.value = ''
  newDescription.value = ''
  showCreate.value = false
  await load()
}

function startEdit(subject: SubjectResponse) {
  editId.value = subject.id
  editName.value = subject.name
  editDescription.value = subject.description || ''
}

async function saveEdit(id: number) {
  if (!editName.value.trim()) return
  await updateSubject(id, {
    name: editName.value,
    description: editDescription.value.trim() || null,
  })
  editId.value = null
  editName.value = ''
  editDescription.value = ''
  await load()
}

function cancelEdit() {
  editId.value = null
  editName.value = ''
  editDescription.value = ''
}

async function deleteSubjectHandler(id: number) {
  const subject = subjects.value.find((s) => s.id === id)
  const subjectName = subject ? subject.name : 'this subject'
  if (!confirm(`Are you sure you want to delete ${subjectName}? This action cannot be undone.`)) {
    return
  }
  await deleteSubject(id)
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
  const validData: SubjectCreate[] = []

  if (data.length === 0) {
    errors.push('CSV file is empty')
    validationErrors.value = errors
    return
  }

  data.forEach((row, index) => {
    const rowNum = index + 2 // +2 because of header row and 0-based index

    // Validate required fields
    if (!row.name || !row.name.trim()) {
      errors.push(`Row ${rowNum}: 'name' is required`)
      return
    }

    // Check if name is too short
    if (row.name.trim().length < 2) {
      errors.push(`Row ${rowNum}: 'name' must be at least 2 characters`)
      return
    }

    validData.push({
      name: row.name.trim(),
      description: row.description?.trim() || null,
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
    const subject = csvData.value[i]
    try {
      await createSubject(subject)
      uploadResults.value.success.push(`"${subject.name}" uploaded successfully`)
      uploadProgress.value.current++
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Unknown error'
      uploadResults.value.errors.push(`"${subject.name}": ${errorMessage}`)
      uploadProgress.value.current++
    }
  }

  isUploading.value = false

  // Reload the subjects list
  await load()
}

function closeBulkUpload() {
  showBulkUpload.value = false
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
