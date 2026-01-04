<!--
  EvaluationsView.vue (Admin)
  Admin can view, create, edit, and delete evaluations (override, unrestricted).
-->
<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Evaluations</h2>
      <AppButton @click="showCreate = true">Add Evaluation</AppButton>
    </div>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>Student</th>
        <th>Question</th>
        <th>TA</th>
        <th>Marking</th>
        <th>Remarks</th>
        <th>Actions</th>
      </template>
      <tr v-for="evaluation in evaluations" :key="evaluation.id">
        <td>{{ evaluation.id }}</td>
        <td>{{ getUserName(evaluation.student_id) }}</td>
        <td>{{ getQuestionText(evaluation.question_id) }}</td>
        <td>{{ getUserName(evaluation.ta_id) }}</td>
        <td v-if="editId !== evaluation.id">{{ evaluation.marking }}</td>
        <td v-else>
          <AppSelect v-model="editMarking">
            <option value="done">done</option>
            <option value="partial">partial</option>
            <option value="not_done">not_done</option>
          </AppSelect>
        </td>
        <td v-if="editId !== evaluation.id">{{ evaluation.remarks }}</td>
        <td v-else>
          <AppInput v-model="editRemarks" />
        </td>
        <td>
          <div class="flex gap-2">
            <AppButton v-if="editId !== evaluation.id" @click="startEdit(evaluation)"
              >Edit</AppButton
            >
            <AppButton v-if="editId === evaluation.id" @click="saveEdit(evaluation.id)"
              >Save</AppButton
            >
            <AppButton v-if="editId === evaluation.id" @click="cancelEdit">Cancel</AppButton>
            <AppButton
              class="bg-red-600 hover:bg-red-500"
              @click="deleteEvaluationHandler(evaluation.id)"
              >Delete</AppButton
            >
          </div>
        </td>
      </tr>
    </AppTable>
    <!-- Create Modal -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/30 flex items-center justify-center z-10">
      <div class="bg-white p-6 rounded shadow w-[28rem]">
        <h3 class="font-semibold mb-2">Add Evaluation</h3>
        <AppSelect v-model="newStudentId">
          <option v-for="user in users" :key="user.id" :value="user.id">{{ user.name }}</option>
        </AppSelect>
        <AppSelect v-model="newQuestionId" class="mt-2">
          <option v-for="question in questions" :key="question.id" :value="question.id">
            {{ question.text }}
          </option>
        </AppSelect>
        <AppSelect v-model="newTaId" class="mt-2">
          <option v-for="user in users" :key="user.id" :value="user.id">{{ user.name }}</option>
        </AppSelect>
        <AppSelect v-model="newMarking" class="mt-2">
          <option value="done">done</option>
          <option value="partial">partial</option>
          <option value="not_done">not_done</option>
        </AppSelect>
        <AppInput v-model="newRemarks" placeholder="Remarks (optional)" class="mt-2" />
        <div class="flex gap-2 mt-4">
          <AppButton @click="createEvaluationHandler">Create</AppButton>
          <AppButton @click="showCreate = false">Cancel</AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admin Evaluations CRUD view
import { ref, onMounted } from 'vue'
import AppButton from '../../components/common/AppButton.vue'
import AppInput from '../../components/common/AppInput.vue'
import AppSelect from '../../components/common/AppSelect.vue'
import AppTable from '../../components/common/AppTable.vue'
import {
  getEvaluations,
  createEvaluation,
  updateEvaluation,
  deleteEvaluation,
  getUsers,
  getQuestions,
} from '../../api/admin'
import type { EvaluationResponse, UserResponse, QuestionResponse, Marking } from '../../types/api'

const evaluations = ref<EvaluationResponse[]>([])
const users = ref<UserResponse[]>([])
const questions = ref<QuestionResponse[]>([])
const showCreate = ref(false)
const newStudentId = ref<number | null>(null)
const newQuestionId = ref<number | null>(null)
const newTaId = ref<number | null>(null)
const newMarking = ref<Marking>('done')
const newRemarks = ref('')
const editId = ref<number | null>(null)
const editMarking = ref<Marking>('done')
const editRemarks = ref('')

async function load() {
  ;[evaluations.value, users.value, questions.value] = await Promise.all([
    getEvaluations(),
    getUsers(),
    getQuestions(),
  ])
}
onMounted(load)

function getUserName(id: number) {
  return users.value.find((u) => u.id === id)?.name || ''
}
function getQuestionText(id: number) {
  return questions.value.find((q) => q.id === id)?.text || ''
}

async function createEvaluationHandler() {
  if (!newStudentId.value || !newQuestionId.value || !newTaId.value || !newMarking.value) return
  await createEvaluation({
    student_id: newStudentId.value,
    question_id: newQuestionId.value,
    ta_id: newTaId.value,
    marking: newMarking.value,
    remarks: newRemarks.value || null,
  })
  newStudentId.value = null
  newQuestionId.value = null
  newTaId.value = null
  newMarking.value = 'done'
  newRemarks.value = ''
  showCreate.value = false
  await load()
}

function startEdit(evaluation: EvaluationResponse) {
  editId.value = evaluation.id
  editMarking.value = evaluation.marking
  editRemarks.value = evaluation.remarks || ''
}

async function saveEdit(id: number) {
  const ev = evaluations.value.find((e) => e.id === id)
  if (!ev) return
  await updateEvaluation(id, {
    student_id: ev.student_id,
    question_id: ev.question_id,
    ta_id: ev.ta_id,
    marking: editMarking.value,
    remarks: editRemarks.value || null,
  })
  editId.value = null
  editMarking.value = 'done'
  editRemarks.value = ''
  await load()
}

function cancelEdit() {
  editId.value = null
  editMarking.value = 'done'
  editRemarks.value = ''
}

async function deleteEvaluationHandler(id: number) {
  await deleteEvaluation(id)
  await load()
}
</script>
