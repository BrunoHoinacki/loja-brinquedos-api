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
                    <p class="text-lg font-semibold text-blue-900 flex items-center justify-between">
                        <span>{{ cliente.nomeCompleto }}</span>
                        <span class="ml-2 px-2 py-0.5 text-xs font-semibold rounded-full"
                            :class="getMissingLetterClass(cliente.nomeCompleto)">
                            {{ getMissingLetter(cliente.nomeCompleto) }}
                        </span>
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

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Ref } from 'vue';
import { useCookie } from '#app';
import AppNavbar from '~/components/AppNavbar.vue';

const token = useCookie('token');

const nomeCompleto = ref('');
const email = ref('');
const dataNascimento = ref('');
const clientes: Ref<NormalizedClient[]> = ref([]);

const USE_SIMULATED_DATA = false; // Mude para `true` para usar os dados simulados

interface NormalizedClient {
    id: number;
    nomeCompleto: string;
    email: string;
    dataNascimento: string;
    vendas?: { data: string; valor: number }[];
}

interface UnorganizedClientItem {
    info: {
        nomeCompleto: string;
        detalhes: {
            email: string;
            nascimento: string;
        };
    };
    estatisticas?: {
        vendas: { data: string; valor: number }[];
    };
    duplicado?: {
        nomeCompleto: string;
    };
}

interface UnorganizedApiResponse {
    data: {
        clientes: UnorganizedClientItem[];
    };
    meta: {
        registroTotal: number;
        pagina: number;
    };
    redundante: {
        status: string;
    };
}

interface RealApiCliente {
    id: number;
    nomeCompleto: string;
    email: string;
    dataNascimento: string;
    createdAt: string;
}

interface RealApiResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: RealApiCliente[];
}

const normalizeClientsData = (apiResponse: UnorganizedApiResponse): NormalizedClient[] => {
    const normalizedClients: NormalizedClient[] = [];
    let currentId = 1;

    if (apiResponse && apiResponse.data && Array.isArray(apiResponse.data.clientes)) {
        apiResponse.data.clientes.forEach(item => {
            if (item.info && item.info.nomeCompleto && item.info.detalhes) {
                normalizedClients.push({
                    id: currentId++,
                    nomeCompleto: item.info.nomeCompleto,
                    email: item.info.detalhes.email,
                    dataNascimento: item.info.detalhes.nascimento,
                    vendas: item.estatisticas?.vendas || []
                });
            }
        });
    }
    return normalizedClients;
};

const normalizeRealApiData = (apiResponse: RealApiResponse): NormalizedClient[] => {
    if (apiResponse && Array.isArray(apiResponse.results)) {
        return apiResponse.results.map(client => ({
            id: client.id,
            nomeCompleto: client.nomeCompleto,
            email: client.email,
            dataNascimento: client.dataNascimento
        }));
    }
    return [];
};


const carregarClientes = async () => {
    if (!token.value) return;

    try {
        if (USE_SIMULATED_DATA) {
            const simulatedApiResponse: UnorganizedApiResponse = {
                "data": {
                    "clientes": [
                        {
                            "info": {
                                "nomeCompleto": "Ana Beatriz (Simulado)",
                                "detalhes": {
                                    "email": "ana.b.sim@example.com",
                                    "nascimento": "1992-05-01"
                                }
                            },
                            "estatisticas": {
                                "vendas": [
                                    { "data": "2024-01-01", "valor": 150 },
                                    { "data": "2024-01-02", "valor": 50 }
                                ]
                            }
                        },
                        {
                            "info": {
                                "nomeCompleto": "Carlos Eduardo (Simulado)",
                                "detalhes": {
                                    "email": "cadu.sim@example.com",
                                    "nascimento": "1987-08-15"
                                }
                            },
                            "duplicado": {
                                "nomeCompleto": "Carlos Eduardo (Duplicado)"
                            },
                            "estatisticas": {
                                "vendas": []
                            }
                        },
                        {
                            "info": {
                                "nomeCompleto": "Bruno",
                                "detalhes": {
                                    "email": "brunosim@example.com",
                                    "nascimento": "1990-01-01"
                                }
                            },
                            "estatisticas": {
                                "vendas": [
                                    { "data": "2024-03-01", "valor": 200 }
                                ]
                            }
                        },
                        {
                            "info": {
                                "nomeCompleto": "abcdefghijklmnopqrstvuxywz (Simulado)",
                                "detalhes": {
                                    "email": "pangram@example.com",
                                    "nascimento": "2000-01-01"
                                }
                            },
                            "estatisticas": {
                                "vendas": []
                            }
                        }
                    ]
                },
                "meta": {
                    "registroTotal": 4,
                    "pagina": 1
                },
                "redundante": {
                    "status": "ok"
                }
            };
            clientes.value = normalizeClientsData(simulatedApiResponse);
        } else {
            const realResponse = await $fetch<RealApiResponse>('http://127.0.0.1:8000/api/clients/', {
                headers: { Authorization: `Bearer ${token.value}` }
            });
            clientes.value = normalizeRealApiData(realResponse);
        }
    } catch (error) {
        console.error('Erro ao carregar ou normalizar clientes:', error);
        clientes.value = [];
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
        if (!USE_SIMULATED_DATA) {
            await carregarClientes();
        } else {
            alert('Cliente cadastrado na API real. Recarregue a página com USE_SIMULATED_DATA = false para vê-lo.');
        }

    } catch (error) {
        alert('Erro ao cadastrar cliente.');
        console.error(error);
    }
};

const formatarData = (data: string) => {
    const [ano, mes, dia] = data.split('T')[0].split('-');
    return `${dia}/${mes}/${ano}`;
};

/**
 * Retorna a primeira letra do alfabeto (a-z) que não está presente no nome do cliente.
 * Se todas as letras estiverem presentes, retorna '-'.
 * Ignora maiúsculas/minúsculas e caracteres não-alfabéticos.
 */
const getMissingLetter = (name: string): string => {
    const alphabet = 'abcdefghijklmnopqrstuvwxyz';
    const nameLower = name.toLowerCase();

    for (const char of alphabet) {
        if (!nameLower.includes(char)) {
            return char;
        }
    }
    return '-'; // Todas as letras de a-z estão presentes
};

/**
 * Retorna classes Tailwind CSS dinamicamente para o campo da letra ausente.
 */
const getMissingLetterClass = (name: string): string => {
    const missingLetter = getMissingLetter(name);
    if (missingLetter === '-') {
        return 'bg-green-200 text-green-800'; // Todas as letras presentes
    } else if (['a', 'e', 'i', 'o', 'u'].includes(missingLetter)) {
        return 'bg-yellow-200 text-yellow-800'; // Vogal ausente
    } else {
        return 'bg-red-200 text-red-800'; // Consoante ausente
    }
};

onMounted(() => {
    if (token.value) {
        carregarClientes();
    }
});
</script>