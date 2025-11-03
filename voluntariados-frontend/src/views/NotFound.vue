<template>
  <div class="d-flex flex-column align-items-center justify-content-center vh-100 text-center px-3">
    <div class="mb-4">
      <i class="bi bi-exclamation-circle notfound-icon" style="font-size: 4rem;"></i>
    </div>

    <h2 class="fw-bold mb-3 notfound-title">Página no encontrada (404)</h2>

    <p class="text-muted mb-4" style="max-width: 480px;">
      La página que buscás no existe o fue movida. Podés volver al inicio o comprobar la URL.
    </p>

    <div class="d-flex gap-3">
      <button class="btn btn-primary themed-primary" @click="volverInicio">
        <i class="bi bi-house-door me-2"></i> Ir al inicio
      </button>
      <button class="btn btn-outline-secondary" @click="volverAtras">
        <i class="bi bi-arrow-left me-2"></i> Volver
      </button>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'NotFound',
  methods: {
    volverInicio() {
      this.$router.push('/')
    },
    volverAtras() {
      if (window.history.length > 1) {
        window.history.back()
      } else {
        this.$router.push('/')
      }
    }
  }
}
</script>

<style scoped>
.vh-100 { height: 100vh; }
/* theme-based styles */
.notfound-icon { color: var(--brand-start); }
.notfound-title { color: var(--brand-mid); }
.themed-primary { background: linear-gradient(90deg, var(--brand-start), var(--brand-end)); border: none; box-shadow: 0 4px 10px var(--brand-accent-shadow); }
</style>
