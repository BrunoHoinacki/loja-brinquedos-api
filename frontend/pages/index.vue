<template>
    <div class="max-w-2xl mx-auto p-6">
        <h1 class="text-2xl font-bold mb-4">Cadastro de Clientes</h1>

        <form @submit.prevent="cadastrarCliente" class="space-y-4">
            <input v-model="nomeCompleto" type="text" placeholder="Nome Completo" class="w-full p-2 border rounded"
                required />
            <input v-model="email" type="email" placeholder="E-mail" class="w-full p-2 border rounded" required />
            <input v-model="dataNascimento" type="date" class="w-full p-2 border rounded" required />
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                Cadastrar
            </button>
        </form>

        <h2 class="text-xl font-semibold mt-8 mb-2">Clientes Cadastrados</h2>
        <ul>
            <li v-for="cliente in clientes" :key="cliente.id" class="border-b py-2">
                {{ cliente.nomeCompleto }} - {{ cliente.email }}
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '#app'

// JWT armazenado (exemplo simples, depois trocamos para login real)
const token = useCookie('token') // Deve ser setado em login

const nomeCompleto = ref('')
const email = ref('')
const dataNascimento = ref('')
const clientes = ref([])

// Fetch clientes ao montar a página
const carregarClientes = async () => {
    const { data, error } = await useFetch('http://127.0.0.1:8000/api/clients/', {
        headers: {
            Authorization: `Bearer ${token.value}`
        }
    })
    if (data.value) {
        clientes.value = data.value.results
    } else {
        console.error(error.value)
    }
}

const cadastrarCliente = async () => {
    const payload = {
        nomeCompleto: nomeCompleto.value,
        email: email.value,
        dataNascimento: dataNascimento.value
    }

    const { error } = await useFetch('http://127.0.0.1:8000/api/clients/', {
        method: 'POST',
        headers: {
            Authorization: `Bearer ${token.value}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })

    if (!error.value) {
        alert('Cliente cadastrado com sucesso!')
        nomeCompleto.value = ''
        email.value = ''
        dataNascimento.value = ''
        await carregarClientes()
    } else {
        alert('Erro ao cadastrar cliente.')
        console.error(error.value)
    }
}

onMounted(() => {
    carregarClientes()
})
</script>
