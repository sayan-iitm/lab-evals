<!--
  StudentsView.vue (TA)
  TA can view list of students (not admins/TAs).
-->
<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Students</h2>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>Name</th>
        <th>Email</th>
        <th>Subjects</th>
      </template>
      <tr v-for="student in students" :key="student.id">
        <td>{{ student.id }}</td>
        <td>{{ student.name }}</td>
        <td>{{ student.email }}</td>
        <td>
          <span v-if="getStudentSubjects(student.id).length > 0">
            {{ getStudentSubjects(student.id).join(', ') }}
          </span>
          <span v-else class="text-gray-400 italic">No subjects</span>
        </td>
      </tr>
    </AppTable>
  </div>
</template>

<script setup lang="ts">
// TA Students list view
import { ref, onMounted } from 'vue'
import AppTable from '../../components/common/AppTable.vue'
import { getStudents, getEnrollments, getSubjects } from '../../api/ta'
import type { UserResponse, EnrollmentResponse, SubjectResponse } from '../../types/api'

const students = ref<UserResponse[]>([])
const enrollments = ref<EnrollmentResponse[]>([])
const subjects = ref<SubjectResponse[]>([])

function getStudentSubjects(studentId: number): string[] {
  const studentEnrollments = enrollments.value.filter((e) => e.user_id === studentId)
  return studentEnrollments
    .map((e) => subjects.value.find((s) => s.id === e.subject_id)?.name)
    .filter((name): name is string => name !== undefined)
}

async function load() {
  const [studentsData, enrollmentsData, subjectsData] = await Promise.all([
    getStudents(),
    getEnrollments(),
    getSubjects(),
  ])
  students.value = studentsData
  enrollments.value = enrollmentsData
  subjects.value = subjectsData
}
onMounted(load)
</script>
