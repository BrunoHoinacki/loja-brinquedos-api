<template>
    <div class="min-h-screen bg-gray-100">
        <AppNavbar />
        <div class="max-w-4xl mx-auto bg-white shadow-md rounded-xl p-8 mt-10">
            <h1 class="text-3xl font-bold text-blue-700 mb-6">
                👨‍👩‍👧‍👦 Cadastro de Clientes
            </h1>

            <form @submit.prevent="cadastrarCliente" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <input v-model="nomeCompleto" type="text" placeholder="Nome Completo"
                    class="p-3 border border-gray-300 rounded w-full" required />
                <input v-model="email" type="email" placeholder="E-mail"
                    class="p-3 border border-gray-300 rounded w-full" required />
                <input v-model="dataNascimento" type="date" class="p-3 border border-gray-300 rounded w-full"
                    required />
                <button type="submit"
                    class="col-span-1 md:col-span-3 bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded font-medium transition">
                    Cadastrar
                </button>
            </form>

            <h2 class="text-2xl font-semibold text-gray-800 mb-4">
                📋 Clientes Cadastrados
            </h2>

            <div class="grid gap-4">
                <div v-for="cliente in clientes" :key="cliente.id"
                    class="bg-blue-50 border border-blue-100 rounded p-4 shadow-sm">
                    <p class="text-lg font-semibold text-blue-900">
                        {{ cliente.nomeCompleto }}
                    </p>
                    <p class="text-sm text-gray-600">{{ cliente.email }}</p>
                    <p class="text-sm text-gray-500">
                        Nascimento: {{ formatarData(cliente.dataNascimento) }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCookie } from '#app';
import AppNavbar from '~/components/AppNavbar.vue';

const token = useCookie('token');

const nomeCompleto = ref('');
const email = ref('');
const dataNascimento = ref('');
const clientes = ref([]);

const carregarClientes = async () => {
    if (!token.value) return;
    try {
        const response = await $fetch('http://127.0.0.1:8000/api/clients/', {
            headers: {
                Authorization: `Bearer ${token.value}`
            }
        });
        clientes.value = response.results;
    } catch (error) {
        console.error('Erro ao carregar clientes:', error);
    }
};

const cadastrarCliente = async () => {
    try {
        await $fetch('http://127.0.0.1:8000/api/clients/', {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${token.value}`,
                'Content-Type': 'application/json'
            },
            body: {
                nomeCompleto: nomeCompleto.value,
                email: email.value,
                dataNascimento: dataNascimento.value
            }
        });

        alert('Cliente cadastrado com sucesso!');
        nomeCompleto.value = '';
        email.value = '';
        dataNascimento.value = '';
        await carregarClientes();
    } catch (error) {
        alert('Erro ao cadastrar cliente.');
        console.error(error);
    }
};

const formatarData = (data) => {
    const [ano, mes, dia] = data.split('T')[0].split('-');
    return `${dia}/${mes}/${ano}`;
};

onMounted(() => {
    if (token.value) {
        carregarClientes();
    }
});
</script>