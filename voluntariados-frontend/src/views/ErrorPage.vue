<template>
  <div class="d-flex flex-column align-items-center justify-content-center vh-100 text-center bg-light px-3">
    <div class="mb-4">
      <i class="bi bi-wifi-off text-danger" style="font-size: 5rem;"></i>
    </div>

    <h2 class="fw-bold mb-3 text-dark">Ups... algo salió mal 😔</h2>

    <p class="text-muted mb-4" style="max-width: 480px;">
      No pudimos conectar con el servidor o se produjo un error inesperado.
      Por favor, verificá tu conexión o intentá nuevamente en unos momentos.
    </p>

    <div class="d-flex gap-3">
      <button class="btn btn-primary" @click="recargar">
        <i class="bi bi-arrow-clockwise me-2"></i> Reintentar
      </button>

      <button class="btn btn-outline-secondary" @click="volverInicio">
        <i class="bi bi-house-door me-2"></i> Ir al inicio
      </button>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: "ErrorPage",
  methods: {
    recargar() {
      window.location.reload()
    },
    volverInicio() {
      this.$router.push("/")
    }
  }
}
</script>

<style scoped>
.vh-100 {
  height: 100vh;
}
.bi {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
