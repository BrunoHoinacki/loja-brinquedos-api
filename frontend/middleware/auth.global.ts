export default defineNuxtRouteMiddleware((to, from) => {
  const token = useCookie('token')

  const rotasProtegidas = ['/clientes', '/vendas', '/estatisticas']

  if (rotasProtegidas.includes(to.path) && !token.value) {
    return navigateTo('/login')
  }
})