<template>
    <nav class="bg-blue-600 p-4 shadow-md">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-6">
                <NuxtLink to="/" class="text-white text-xl font-bold hover:text-blue-200 transition">Home</NuxtLink>
                <NuxtLink to="/clientes" class="text-white text-lg hover:text-blue-200 transition">Clientes</NuxtLink>
                <NuxtLink to="/estatisticas" class="text-white text-lg hover:text-blue-200 transition">Estatísticas
                </NuxtLink>
            </div>
            <button @click="logout"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded text-sm font-medium transition">
                Sair
            </button>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { useRouter, useCookie } from '#app';

const router = useRouter();
const token = useCookie('token');

const logout = () => {
    token.value = null;
    router.push('/');
};
</script>

<style scoped></style>