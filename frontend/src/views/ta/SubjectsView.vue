<!--
  SubjectsView.vue (TA)
  TA can view list of subjects.
-->
<template>
  <div>
    <h2 class="text-xl font-semibold mb-4">Subjects</h2>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>Name</th>
      </template>
      <tr v-for="subject in subjects" :key="subject.id">
        <td>{{ subject.id }}</td>
        <td>{{ subject.name }}</td>
      </tr>
    </AppTable>
  </div>
</template>

<script setup lang="ts">
// TA Subjects list view
import { ref, onMounted } from 'vue'
import AppTable from '../../components/common/AppTable.vue'
import { getSubjects } from '../../api/ta'
import type { SubjectResponse } from '../../types/api'

const subjects = ref<SubjectResponse[]>([])

async function load() {
  subjects.value = await getSubjects()
}
onMounted(load)
</script>
