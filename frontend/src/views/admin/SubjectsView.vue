<!--
  SubjectsView.vue (Admin)
  Admin can view, create, edit, and delete subjects.
-->
<template>
  <div class="flex justify-end mb-4">
    <AppButton @click="showCreate = true">Add Subject</AppButton>
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
</template>

<script setup lang="ts">
// Admin Subjects CRUD view
import { ref, onMounted } from 'vue'
import AppButton from '../../components/common/AppButton.vue'
import AppInput from '../../components/common/AppInput.vue'
import AppTable from '../../components/common/AppTable.vue'
import { getSubjects, createSubject, updateSubject, deleteSubject } from '../../api/admin'
import type { SubjectResponse } from '../../types/api'

const subjects = ref<SubjectResponse[]>([])
const showCreate = ref(false)
const newName = ref('')
const newDescription = ref('')
const editId = ref<number | null>(null)
const editName = ref('')
const editDescription = ref('')

async function load() {
  subjects.value = await getSubjects()
}
onMounted(load)

async function createSubjectHandler() {
  if (!newName.value.trim()) return
  await createSubject({ 
    name: newName.value,
    description: newDescription.value.trim() || null
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
    description: editDescription.value.trim() || null
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
  await deleteSubject(id)
  await load()
}
</script>
