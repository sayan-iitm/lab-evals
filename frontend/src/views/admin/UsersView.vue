<!--
  UsersView.vue (Admin)
  Admin can view, create, edit, and delete users.
-->
<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-semibold">Users</h2>
      <div class="flex gap-3 items-center">
        <div class="flex items-center gap-2">
          <label for="roleFilter" class="text-sm font-medium">Role</label>
          <AppSelect id="roleFilter" v-model="roleFilter" class="w-40">
            <option value="">All</option>
            <option value="student">Student</option>
            <option value="ta">TA</option>
            <option value="admin">Admin</option>
          </AppSelect>
        </div>
        <AppButton @click="showCreate = true">Add User</AppButton>
      </div>
    </div>
    <AppTable>
      <template #head>
        <th>ID</th>
        <th>Name</th>
        <th>Email</th>
        <th>Role</th>
        <th>Actions</th>
      </template>
      <tr v-for="user in filteredUsers" :key="user.id">
        <td>{{ user.id }}</td>
        <td v-if="editId !== user.id">{{ user.name }}</td>
        <td v-else>
          <AppInput v-model="editName" />
        </td>
        <td v-if="editId !== user.id">{{ user.email }}</td>
        <td v-else>
          <AppInput v-model="editEmail" />
        </td>
        <td v-if="editId !== user.id">{{ user.role }}</td>
        <td v-else>
          <AppSelect v-model="editRole">
            <option value="student">student</option>
            <option value="ta">ta</option>
            <option value="admin">admin</option>
          </AppSelect>
        </td>
        <td>
          <div class="flex gap-2">
            <AppButton v-if="editId !== user.id" @click="startEdit(user)">Edit</AppButton>
            <AppButton v-if="editId === user.id" @click="saveEdit(user.id)">Save</AppButton>
            <AppButton v-if="editId === user.id" @click="cancelEdit">Cancel</AppButton>
            <AppButton class="bg-red-600 hover:bg-red-500" @click="deleteUserHandler(user.id)"
              >Delete</AppButton
            >
          </div>
        </td>
      </tr>
    </AppTable>
    <!-- Create Modal -->
    <div v-if="showCreate" class="fixed inset-0 bg-black/30 flex items-center justify-center z-10">
      <div class="bg-white p-6 rounded shadow w-96">
        <h3 class="font-semibold mb-2">Add User</h3>
        <AppInput v-model="newName" placeholder="Name" />
        <AppInput v-model="newEmail" placeholder="Email" class="mt-2" />
        <AppSelect v-model="newRole" class="mt-2">
          <option value="student">student</option>
          <option value="ta">ta</option>
          <option value="admin">admin</option>
        </AppSelect>
        <div class="flex gap-2 mt-4">
          <AppButton @click="createUserHandler">Create</AppButton>
          <AppButton @click="showCreate = false">Cancel</AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admin Users CRUD view
import { ref, onMounted, computed } from 'vue'
import AppButton from '../../components/common/AppButton.vue'
import AppInput from '../../components/common/AppInput.vue'
import AppSelect from '../../components/common/AppSelect.vue'
import AppTable from '../../components/common/AppTable.vue'
import { getUsers, createUser, updateUser, deleteUser } from '../../api/admin'
import type { UserResponse, UserRole } from '../../types/api'

const users = ref<UserResponse[]>([])
const roleFilter = ref<string>('')
const showCreate = ref(false)
const newName = ref('')
const newEmail = ref('')
const newRole = ref<UserRole>('student')
const editId = ref<number | null>(null)
const editName = ref('')
const editEmail = ref('')
const editRole = ref<UserRole>('student')
const filteredUsers = computed(() => {
  if (!roleFilter.value) {
    return users.value
  }
  return users.value.filter((user) => user.role === roleFilter.value)
})

async function load() {
  users.value = await getUsers()
}
onMounted(load)

async function createUserHandler() {
  if (!newName.value.trim() || !newEmail.value.trim() || !newRole.value) return
  await createUser({ name: newName.value, email: newEmail.value, role: newRole.value })
  newName.value = ''
  newEmail.value = ''
  newRole.value = 'student'
  showCreate.value = false
  await load()
}

function startEdit(user: UserResponse) {
  editId.value = user.id
  editName.value = user.name
  editEmail.value = user.email
  editRole.value = user.role
}

async function saveEdit(id: number) {
  if (!editName.value.trim() || !editEmail.value.trim() || !editRole.value) return
  await updateUser(id, { name: editName.value, email: editEmail.value, role: editRole.value })
  editId.value = null
  editName.value = ''
  editEmail.value = ''
  editRole.value = 'student'
  await load()
}

function cancelEdit() {
  editId.value = null
  editName.value = ''
  editEmail.value = ''
  editRole.value = 'student'
}

async function deleteUserHandler(id: number) {
  await deleteUser(id)
  await load()
}
</script>
