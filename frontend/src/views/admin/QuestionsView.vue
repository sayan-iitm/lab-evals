<!--
  QuestionsView.vue (Admin)
  Admin can view, create, edit, and delete questions.
-->
<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Questions</h2>
      <AppButton @click="showCreate = true">Add Question</AppButton>
    </div>
    <!-- Subject Filter -->
    <div class="mb-4">
      <label class="block text-sm font-medium mb-2">Filter by Subject:</label>
      <AppSelect v-model="selectedSubjectId" class="max-w-xs">
        <option value="">All Subjects</option>
        <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
          {{ subject.name }}
        </option>
      </AppSelect>
    </div>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>Subject</th>
        <th>Text</th>
        <th>Actions</th>
      </template>
      <tr v-for="question in filteredQuestions" :key="question.id">
        <td>{{ question.id }}</td>
        <td>{{ getSubjectName(question.subject_id) }}</td>
        <td v-if="editId !== question.id">{{ question.text }}</td>
        <td v-else>
          <AppInput v-model="editText" />
        </td>
        <td>
          <div class="flex gap-2">
            <AppButton v-if="editId !== question.id" @click="startEdit(question)">Edit</AppButton>
            <AppButton v-if="editId === question.id" @click="saveEdit(question.id)">Save</AppButton>
            <AppButton v-if="editId === question.id" @click="cancelEdit">Cancel</AppButton>
            <AppButton
              class="bg-red-600 hover:bg-red-500"
              @click="deleteQuestionHandler(question.id)"
              >Delete</AppButton
            >
          </div>
        </td>
      </tr>
    </AppTable>
    <!-- Create Modal -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/30 flex items-center justify-center z-10">
      <div class="bg-white p-6 rounded shadow w-96">
        <h3 class="font-semibold mb-2">Add Question</h3>
        <AppSelect v-model="newSubjectId">
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </AppSelect>
        <AppInput v-model="newText" placeholder="Question text" class="mt-2" />
        <div class="flex gap-2 mt-4">
          <AppButton @click="createQuestionHandler">Create</AppButton>
          <AppButton @click="showCreate = false">Cancel</AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admin Questions CRUD view
import { ref, onMounted, computed } from 'vue'
import AppButton from '../../components/common/AppButton.vue'
import AppInput from '../../components/common/AppInput.vue'
import AppSelect from '../../components/common/AppSelect.vue'
import AppTable from '../../components/common/AppTable.vue'
import {
  getQuestions,
  createQuestion,
  updateQuestion,
  deleteQuestion,
  getSubjects,
} from '../../api/admin'
import type { QuestionResponse, SubjectResponse } from '../../types/api'

const questions = ref<QuestionResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const selectedSubjectId = ref<number | null>(null)
const showCreate = ref(false)
const newSubjectId = ref<number | null>(null)
const newText = ref('')
const editId = ref<number | null>(null)
const editText = ref('')
const editSubjectId = ref<number | null>(null)

async function load() {
  ;[questions.value, subjects.value] = await Promise.all([getQuestions(), getSubjects()])
}
onMounted(load)
const filteredQuestions = computed(() => {
  if (selectedSubjectId.value === null) {
    return questions.value
  }
  return questions.value.filter((q) => q.subject_id === selectedSubjectId.value)
})

function getSubjectName(id: number) {
  return subjects.value.find((s) => s.id === id)?.name || ''
}

async function createQuestionHandler() {
  if (!newSubjectId.value || !newText.value.trim()) return
  await createQuestion({ subject_id: newSubjectId.value, text: newText.value })
  newSubjectId.value = null
  newText.value = ''
  showCreate.value = false
  await load()
}

function startEdit(question: QuestionResponse) {
  editId.value = question.id
  editText.value = question.text
  editSubjectId.value = question.subject_id
}

async function saveEdit(id: number) {
  if (!editText.value.trim() || !editSubjectId.value) return
  await updateQuestion(id, { subject_id: editSubjectId.value, text: editText.value })
  editId.value = null
  editText.value = ''
  editSubjectId.value = null
  await load()
}

function cancelEdit() {
  editId.value = null
  editText.value = ''
  editSubjectId.value = null
}

async function deleteQuestionHandler(id: number) {
  await deleteQuestion(id)
  await load()
}
</script>
