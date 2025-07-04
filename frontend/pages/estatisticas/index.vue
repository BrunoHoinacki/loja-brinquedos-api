<template>
    <div class="min-h-screen bg-gray-100">
        <AppNavbar />
        <div class="max-w-4xl mx-auto bg-white shadow-md rounded-xl p-8 mt-10">
            <h1 class="text-3xl font-bold text-blue-700 mb-6">📊 Estatísticas de Vendas</h1>

            <div v-if="loading" class="text-center text-gray-600">Carregando estatísticas...</div>
            <div v-else-if="erro" class="text-center text-red-600">
                Ocorreu um erro ao carregar as estatísticas. Por favor, tente novamente.
            </div>
            <div v-else>
                <h2 class="text-2xl font-semibold text-gray-800 mb-4">Vendas por Dia</h2>
                <div class="bg-gray-50 p-4 rounded-lg shadow-inner mb-8">
                    <Line :data="chartData" :options="chartOptions" />
                </div>

                <h2 class="text-2xl font-semibold text-gray-800 mb-4">⭐ Clientes em Destaque</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

                    <div v-if="clienteMaiorVolume"
                        class="bg-green-50 border-l-4 border-green-500 rounded-lg shadow p-6">
                        <p class="text-xl font-bold text-green-800 mb-2">Maior Volume de Vendas</p>
                        <p class="text-lg text-green-700">
                            <span class="font-semibold">{{ clienteMaiorVolume.nome_completo }}</span>
                        </p>
                        <p class="text-sm text-green-600">Total: R$ {{ clienteMaiorVolume.total.toFixed(2) }}</p>
                    </div>
                    <div v-else class="bg-gray-50 border-l-4 border-gray-300 rounded-lg shadow p-6">
                        <p class="text-lg font-semibold text-gray-600">Maior Volume de Vendas</p>
                        <p class="text-sm text-gray-500">Nenhum dado disponível.</p>
                    </div>

                    <div v-if="clienteMaiorMedia" class="bg-blue-50 border-l-4 border-blue-500 rounded-lg shadow p-6">
                        <p class="text-xl font-bold text-blue-800 mb-2">Maior Média por Venda</p>
                        <p class="text-lg text-blue-700">
                            <span class="font-semibold">{{ clienteMaiorMedia.nome_completo }}</span>
                        </p>
                        <p class="text-sm text-blue-600">Média: R$ {{ clienteMaiorMedia.media.toFixed(2) }}</p>
                    </div>
                    <div v-else class="bg-gray-50 border-l-4 border-gray-300 rounded-lg shadow p-6">
                        <p class="text-lg font-semibold text-gray-600">Maior Média por Venda</p>
                        <p class="text-sm text-gray-500">Nenhum dado disponível.</p>
                    </div>

                    <div v-if="clienteMaiorFrequencia"
                        class="bg-purple-50 border-l-4 border-purple-500 rounded-lg shadow p-6">
                        <p class="text-xl font-bold text-purple-800 mb-2">Maior Frequência de Compras</p>
                        <p class="text-lg text-purple-700">
                            <span class="font-semibold">{{ clienteMaiorFrequencia.nome_completo }}</span>
                        </p>
                        <p class="text-sm text-purple-600">Total de dias com compras: {{ clienteMaiorFrequencia.dias }}
                        </p>
                    </div>
                    <div v-else class="bg-gray-50 border-l-4 border-gray-300 rounded-lg shadow p-6">
                        <p class="text-lg font-semibold text-gray-600">Maior Frequência de Compras</p>
                        <p class="text-sm text-gray-500">Nenhum dado disponível.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Ref } from 'vue'
import { useCookie } from '#app'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
} from 'chart.js'
import { Line } from 'vue-chartjs'
import AppNavbar from '~/components/AppNavbar.vue';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

interface VendasPorDiaResponse {
    [key: string]: number;
}

interface ClienteDestaqueItem {
    client_id: number;
    nome_completo: string;
    total?: number;
    media?: number;
    dias?: number;
}

interface ClientesStatsResponse {
    maior_volume: ClienteDestaqueItem | null;
    maior_media: ClienteDestaqueItem | null;
    maior_frequencia: ClienteDestaqueItem | null;
}

const token = useCookie('token')
const loading = ref(true)
const erro = ref(false)

const clienteMaiorVolume: Ref<ClienteDestaqueItem | null> = ref(null)
const clienteMaiorMedia: Ref<ClienteDestaqueItem | null> = ref(null)
const clienteMaiorFrequencia: Ref<ClienteDestaqueItem | null> = ref(null)

const chartData: Ref<{
    labels: string[];
    datasets: {
        label: string;
        data: number[];
        backgroundColor: string;
        borderColor: string;
        fill: boolean;
        tension: number;
    }[];
}> = ref({
    labels: [],
    datasets: [
        {
            label: 'Total de Vendas (R$)',
            data: [],
            backgroundColor: '#3b82f6',
            borderColor: '#3b82f6',
            fill: false,
            tension: 0.3
        }
    ]
})

const chartOptions = {
    responsive: true,
    plugins: {
        legend: { position: 'top' as const },
        title: { display: true, text: 'Vendas por Dia' }
    },
    scales: {
        y: { beginAtZero: true }
    }
}

const carregarEstatisticas = async () => {
    try {
        const vendasRes = await $fetch<VendasPorDiaResponse>('http://127.0.0.1:8000/api/stats/vendas-por-dia/', {
            headers: { Authorization: `Bearer ${token.value}` }
        })

        const datas = Object.keys(vendasRes).sort()
        const valores = datas.map((data) => vendasRes[data])

        chartData.value.labels = datas
        chartData.value.datasets[0].data = valores

        const clientesStatsRes = await $fetch<ClientesStatsResponse>('http://127.0.0.1:8000/api/stats/clientes/', {
            headers: { Authorization: `Bearer ${token.value}` }
        })

        clienteMaiorVolume.value = clientesStatsRes.maior_volume
        clienteMaiorMedia.value = clientesStatsRes.maior_media
        clienteMaiorFrequencia.value = clientesStatsRes.maior_frequencia

        loading.value = false
    } catch (e) {
        erro.value = true
        loading.value = false
        console.error('Erro ao carregar estatísticas:', e)
    }
}

onMounted(() => {
    carregarEstatisticas()
})
</script>