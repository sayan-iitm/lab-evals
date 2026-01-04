<!--
  LoginView.vue
  Login page for all users. Handles Google Sign-In and backend login.
-->
<template>
  <div class="min-h-screen flex items-center justify-center bg-zinc-50">
    <div class="bg-white p-8 rounded-lg shadow w-full max-w-sm flex flex-col items-center">
      <h2 class="text-2xl font-semibold mb-6">Sign in to Lab Evaluation</h2>

      <!-- Declarative Google Sign-In -->
      <div
        id="g_id_onload"
        :data-client_id="clientId"
        data-auto_prompt="false"
        data-callback="onGoogleSignIn"
      ></div>

      <div
        class="g_id_signin mb-4"
        data-type="standard"
        data-size="large"
        data-theme="outline"
        data-width="280"
      ></div>

      <p v-if="loading" class="text-gray-600">Signing in…</p>
      <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { loginWithIdToken, fetchMe } from '../api/auth'
import { useAuthStore } from '../store/auth'

const loading = ref(false)
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

// MUST be a plain string (used in template binding)
const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

/**
 * IMPORTANT:
 * Google expects the callback to be a GLOBAL function.
 * With <script setup>, we must explicitly attach it to window.
 */
onMounted(() => {
  ;(window as any).onGoogleSignIn = async (response: any) => {
    const idToken = response?.credential
    if (!idToken) {
      error.value = 'No ID token received'
      return
    }

    loading.value = true
    error.value = ''

    try {
      const { access_token } = await loginWithIdToken(idToken)

      auth.token = access_token
      const user = await fetchMe()
      auth.setAuth(access_token, user.role, user)

      if (user.role === 'admin') {
        router.replace('/admin/subjects')
      } else if (user.role === 'ta') {
        router.replace('/ta/evaluations')
      } else {
        router.replace('/student/questions')
      }
    } catch (e: any) {
      console.log(e)
      error.value = e?.message || 'Login failed'
      auth.clearAuth()
    } finally {
      loading.value = false
    }
  }
})
</script>
