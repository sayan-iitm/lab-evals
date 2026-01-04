<!--
  EvaluationsView.vue (TA)
  TA can view, create, edit, and delete their own evaluations.
-->
<template>
  <div>
    <div class="flex justify-between items-center mb-4 gap-4">
      <h2 class="text-xl font-semibold">Evaluations</h2>
      <div class="flex gap-2 items-center shrink-0">
        <AppSelect v-model="filterSubjectId" class="w-48">
          <option value="">All Subjects</option>
          <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </AppSelect>
        <AppButton class="whitespace-nowrap" @click="showCreate = true">Add Evaluation</AppButton>
      </div>
    </div>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>Student Name</th>
        <th>Student Email</th>
        <th>Subject</th>
        <th>Question</th>
        <th>Marking</th>
        <th>Remarks</th>
        <th>Actions</th>
      </template>
      <tr v-for="evaluation in filteredEvaluations" :key="evaluation.id">
        <td>{{ evaluation.id }}</td>
        <td>{{ getUserName(evaluation.student_id) }}</td>
        <td>{{ getUserEmail(evaluation.student_id) }}</td>
        <td>{{ getQuestionSubject(evaluation.question_id) }}</td>
        <td>{{ getQuestionText(evaluation.question_id) }}</td>
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
      <div class="bg-white p-6 rounded shadow w-md">
        <h3 class="font-semibold mb-2">Add Evaluation</h3>
        <label class="block text-sm font-medium text-gray-700 mb-1">Select Student</label>
        <AppSelect v-model="newStudentId" @change="onStudentChange">
          <option :value="null">-- Select Student --</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name }} ({{ user.email }})
          </option>
        </AppSelect>
        <label class="block text-sm font-medium text-gray-700 mb-1 mt-2">Select Subject</label>
        <AppSelect
          v-model="newSubjectId"
          class="mt-1"
          :disabled="!newStudentId"
          @change="onSubjectChange"
        >
          <option
            v-for="subject in filteredSubjectsForStudent"
            :key="subject.id"
            :value="subject.id"
          >
            {{ subject.name }}
          </option>
        </AppSelect>
        <label class="block text-sm font-medium text-gray-700 mb-1 mt-2">Select Question</label>
        <AppSelect v-model="newQuestionId" class="mt-1" :disabled="!newSubjectId">
          <option
            v-for="question in filteredQuestionsForSubject"
            :key="question.id"
            :value="question.id"
          >
            {{ question.text }}
          </option>
        </AppSelect>
        <label class="block text-sm font-medium text-gray-700 mb-1 mt-2">Select Marking</label>
        <AppSelect v-model="newMarking" class="mt-1">
          <option value="done">done</option>
          <option value="partial">partial</option>
          <option value="not_done">not_done</option>
        </AppSelect>
        <label class="block text-sm font-medium text-gray-700 mb-1 mt-2">Remarks (Optional)</label>
        <AppInput v-model="newRemarks" placeholder="Remarks (optional)" class="mt-1" />
        <div class="flex gap-2 mt-4">
          <AppButton @click="createEvaluationHandler">Create</AppButton>
          <AppButton @click="showCreate = false">Cancel</AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// TA Evaluations CRUD (self only)
import { ref, onMounted, computed } from 'vue'
import AppButton from '@/components/common/AppButton.vue'
import AppInput from '@/components/common/AppInput.vue'
import AppSelect from '@/components/common/AppSelect.vue'
import AppTable from '@/components/common/AppTable.vue'
import {
  getEvaluations,
  createEvaluation,
  updateEvaluation,
  deleteEvaluation,
  getStudents,
  getQuestions,
  getSubjects,
  getEnrollments,
} from '@/api/ta'
import {
  type TAEvaluationResponse,
  type UserResponse,
  type QuestionResponse,
  type Marking,
  type SubjectResponse,
  type EnrollmentResponse,
} from '@/types/api'

const evaluations = ref<TAEvaluationResponse[]>([])
const users = ref<UserResponse[]>([])
const questions = ref<QuestionResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const showCreate = ref(false)
const newStudentId = ref<number | null>(null)
const newSubjectId = ref<number | null>(null)
const newQuestionId = ref<number | null>(null)
const newMarking = ref<Marking>('done')
const newRemarks = ref('')
const editId = ref<number | null>(null)
const editMarking = ref<Marking>('done')
const editRemarks = ref('')
const enrollments = ref<EnrollmentResponse[]>([])
const filterSubjectId = ref<number | string>('')

async function load() {
  ;[evaluations.value, users.value, questions.value, subjects.value, enrollments.value] =
    await Promise.all([
      getEvaluations(),
      getStudents(),
      getQuestions(),
      getSubjects(),
      getEnrollments(),
    ])
}
onMounted(load)

function getUserName(id: number) {
  return users.value.find((u) => u.id === id)?.name || ''
}

function getUserEmail(id: number) {
  return users.value.find((u) => u.id === id)?.email || ''
}

function getQuestionText(id: number) {
  return questions.value.find((q) => q.id === id)?.text || ''
}

function getQuestionSubject(questionId: number) {
  const question = questions.value.find((q) => q.id === questionId)
  if (!question) return ''
  return subjects.value.find((s) => s.id === question.subject_id)?.name || ''
}

const filteredEvaluations = computed(() => {
  if (filterSubjectId.value === '' || filterSubjectId.value === null) {
    return evaluations.value
  }
  return evaluations.value.filter((evaluation) => {
    const question = questions.value.find((q) => q.id === evaluation.question_id)
    return question?.subject_id === Number(filterSubjectId.value)
  })
})

// Get subjects that both the student and TA are enrolled in
const filteredSubjectsForStudent = computed(() => {
  if (!newStudentId.value) return []

  // Get student's enrolled subject IDs
  const studentSubjectIds = enrollments.value
    .filter((e) => e.user_id === newStudentId.value)
    .map((e) => e.subject_id)

  if (studentSubjectIds.length === 0) return []

  // Return subjects that the student is enrolled in
  return subjects.value.filter((s) => studentSubjectIds.includes(s.id))
})

// Get questions for the selected subject that don't have evaluations yet for this student
const filteredQuestionsForSubject = computed(() => {
  if (!newStudentId.value || !newSubjectId.value) return []

  // Get questions for the selected subject
  const subjectQuestions = questions.value.filter((q) => q.subject_id === newSubjectId.value)

  // Filter out questions that already have evaluations for this student
  return subjectQuestions.filter(
    (q) =>
      !evaluations.value.some(
        (ev) => ev.student_id === newStudentId.value && ev.question_id === q.id,
      ),
  )
})

function onStudentChange() {
  // Reset subject and question when student changes
  newSubjectId.value = null
  newQuestionId.value = null
}

function onSubjectChange() {
  // Reset question when subject changes
  newQuestionId.value = null
}

async function createEvaluationHandler() {
  if (!newStudentId.value || !newQuestionId.value || !newMarking.value) return
  await createEvaluation({
    student_id: newStudentId.value,
    question_id: newQuestionId.value,
    marking: newMarking.value,
    remarks: newRemarks.value || null,
  })
  newStudentId.value = null
  newQuestionId.value = null
  newMarking.value = 'done'
  newRemarks.value = ''
  showCreate.value = false
  await load()
}

function startEdit(evaluation: TAEvaluationResponse) {
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
