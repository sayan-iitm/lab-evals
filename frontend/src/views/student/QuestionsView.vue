<!--
  QuestionsView.vue (Student)
  Consolidated view: subjects, questions, and evaluation status.
-->
<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">My Questions & Evaluations</h2>
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
        <th>Question</th>
        <th>Status</th>
      </template>
      <tr v-for="question in filteredQuestions" :key="question.id">
        <td>{{ question.id }}</td>
        <td>{{ getSubjectName(question.subject_id) }}</td>
        <td>{{ question.text }}</td>
        <td>
          <span
            :class="{
              'text-green-600': getEvaluationStatus(question.id) === 'Evaluated',
              'text-gray-500': getEvaluationStatus(question.id) === 'Not Evaluated',
            }"
          >
            {{ getEvaluationStatus(question.id) }}
          </span>
        </td>
      </tr>
    </AppTable>
  </div>
</template>

<script setup lang="ts">
// Student consolidated view: questions filtered by subject with evaluation status
import { ref, onMounted, computed } from 'vue'
import AppTable from '../../components/common/AppTable.vue'
import AppSelect from '../../components/common/AppSelect.vue'
import { getQuestions, getSubjects, getEvaluations } from '../../api/student'
import type { QuestionResponse, SubjectResponse, TAEvaluationResponse } from '../../types/api'

const questions = ref<QuestionResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const evaluations = ref<TAEvaluationResponse[]>([])
const selectedSubjectId = ref<number | null>(null)

async function load() {
  ;[questions.value, subjects.value, evaluations.value] = await Promise.all([
    getQuestions(),
    getSubjects(),
    getEvaluations(),
  ])
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

function getEvaluation(questionId: number) {
  return evaluations.value.find((e) => e.question_id === questionId)
}

function getEvaluationStatus(questionId: number) {
  return getEvaluation(questionId) ? 'Evaluated' : 'Not Evaluated'
}
</script>
