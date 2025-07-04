<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 px-4">
    <form @submit.prevent="login" class="bg-white p-8 rounded shadow-md w-full max-w-md space-y-4">
      <h1 class="text-2xl font-bold text-center mb-4">Login</h1>

      <input
        v-model="username"
        type="text"
        placeholder="Usuário"
        class="w-full border px-3 py-2 rounded"
        required
      />
      <input
        v-model="password"
        type="password"
        placeholder="Senha"
        class="w-full border px-3 py-2 rounded"
        required
      />
      <button
        type="submit"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 rounded"
      >
        Entrar
      </button>

      <p v-if="erro" class="text-red-600 text-sm">{{ erro }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCookie } from '#app'

const username = ref('')
const password = ref('')
const erro = ref('')
const token = useCookie('token')
const router = useRouter()

const login = async () => {
  erro.value = ''
  const { data, error } = await useFetch('http://127.0.0.1:8000/api/token/', {
    method: 'POST',
    body: {
      username: username.value,
      password: password.value
    }
  })

  if (data.value?.access) {
    token.value = data.value.access
    router.push('/clientes')
  } else {
    erro.value = 'Credenciais inválidas'
    console.error(error.value)
  }
}
</script>
