<!--
  ProfileView.vue (TA)
  TA can view their own profile info.
-->
<template>
  <div>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-zinc-900">My Profile</h2>
      <p class="text-sm text-zinc-600 mt-1">Your account information and details</p>
    </div>

    <div class="bg-white rounded-lg shadow-sm border border-zinc-200 overflow-hidden">
      <div class="bg-gradient-to-r from-green-600 to-green-500 px-6 py-8">
        <div class="flex items-center gap-4">
          <div class="bg-white rounded-full p-4 relative">
            <svg
              class="w-12 h-12 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 14l9-5-9-5-9 5 9 5z"
              ></path>
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"
              ></path>
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 14l9-5-9-5-9 5 9 5z"
              ></path>
            </svg>
            <div class="absolute -bottom-1 -right-1 bg-green-600 rounded-full p-1.5">
              <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path
                  d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                ></path>
              </svg>
            </div>
          </div>
          <div class="text-white">
            <div class="flex items-center gap-2">
              <h3 class="text-2xl font-bold">{{ user?.name }}</h3>
              <span class="px-2 py-0.5 bg-green-700 rounded-full text-xs font-semibold">TA</span>
            </div>
            <p class="text-green-100 text-sm mt-1">{{ user?.email }}</p>
          </div>
        </div>
      </div>

      <div class="px-6 py-6 space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-medium text-zinc-500 uppercase tracking-wide">User ID</label>
            <p class="mt-1 text-lg font-semibold text-zinc-900">{{ user?.id }}</p>
          </div>
          <div>
            <label class="text-xs font-medium text-zinc-500 uppercase tracking-wide">Role</label>
            <div class="mt-1">
              <AppBadge variant="info" size="lg">{{ user?.role }}</AppBadge>
            </div>
          </div>
        </div>

        <div class="border-t border-zinc-200 pt-4">
          <label class="text-xs font-medium text-zinc-500 uppercase tracking-wide"
            >Account Created</label
          >
          <p class="mt-1 text-sm text-zinc-700">
            {{
              user?.created_at
                ? new Date(user.created_at).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                  })
                : '-'
            }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// TA profile view
import { ref, onMounted } from 'vue'
import AppBadge from '../../components/common/AppBadge.vue'
import { getMe } from '../../api/ta'
import type { UserResponse } from '../../types/api'

const user = ref<UserResponse | null>(null)
async function load() {
  user.value = await getMe()
}
onMounted(load)
</script>
