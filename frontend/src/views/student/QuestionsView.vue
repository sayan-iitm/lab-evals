<!--
  QuestionsView.vue (Student)
  Consolidated view: subjects, questions, and evaluation status.
-->
<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-zinc-900">My Questions & Evaluations</h2>
      <p class="text-sm text-zinc-600 mt-1">View your assigned questions and evaluation status</p>
    </div>

    <!-- Subject Filter -->
    <div class="mb-6 bg-white p-4 rounded-lg shadow-sm border border-zinc-200">
      <AppSelect v-model="selectedSubjectId" label="Filter by Subject" class="max-w-xs">
        <option value="">All Subjects</option>
        <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
          {{ subject.name }}
        </option>
      </AppSelect>
    </div>

    <AppTable
      :isEmpty="filteredQuestions.length === 0"
      emptyMessage="No questions available for you yet."
    >
      <template #head>
        <th>ID</th>
        <th>Subject</th>
        <th>Question</th>
        <th>Status</th>
      </template>
      <tr v-for="question in filteredQuestions" :key="question.id">
        <td class="font-mono text-xs text-zinc-500">{{ question.id }}</td>
        <td>
          <AppBadge variant="info">{{ getSubjectName(question.subject_id) }}</AppBadge>
        </td>
        <td class="max-w-md">{{ question.text }}</td>
        <td>
          <AppBadge :variant="getEvaluation(question.id) ? 'success' : 'default'">
            {{ getEvaluationStatus(question.id) }}
          </AppBadge>
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
import AppBadge from '../../components/common/AppBadge.vue'
import { getQuestions, getSubjects, getEvaluations } from '../../api/student'
import type { QuestionResponse, SubjectResponse, TAEvaluationResponse } from '../../types/api'

const questions = ref<QuestionResponse[]>([])
const subjects = ref<SubjectResponse[]>([])
const evaluations = ref<TAEvaluationResponse[]>([])
const selectedSubjectId = ref<number | string>('')

async function load() {
  ;[questions.value, subjects.value, evaluations.value] = await Promise.all([
    getQuestions(),
    getSubjects(),
    getEvaluations(),
  ])
}
onMounted(load)

const filteredQuestions = computed(() => {
  if (!selectedSubjectId.value) {
    return questions.value
  }
  return questions.value.filter((q) => q.subject_id === Number(selectedSubjectId.value))
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
