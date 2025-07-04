<script setup>
import { useCookie } from '#app'
import { useRouter } from 'vue-router'

const router = useRouter()
const token = useCookie('token')

const acessarClientes = () => {
    if (!token.value) {
        router.push('/login')
    } else {
        router.push('/clientes')
    }
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center px-4">
        <div class="bg-white shadow-xl rounded-2xl p-10 max-w-xl w-full text-center">
            <h1 class="text-4xl font-bold text-blue-700 mb-4">🎉 Loja de Brinquedos Front</h1>
            <p class="text-gray-700 text-lg mb-2">Bem-vindo ao sistema de gestão!</p>
            <p class="text-gray-600 mb-6">Gerencie seus clientes, vendas e acompanhe estatísticas de forma fácil.</p>
            <button @click="acessarClientes"
                class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition">
                Gerenciar Clientes
            </button>
        </div>
    </div>
</template>
