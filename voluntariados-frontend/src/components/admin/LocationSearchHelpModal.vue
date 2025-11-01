<template>
  <!-- Help modal for location search -->
  <div
    class="modal fade"
    :class="{ show: show, 'd-block': show }"
    tabindex="-1"
    v-if="show"
    style="z-index: 1065"
    @click.self="$emit('close')"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="bi bi-info-circle me-2"></i>Cómo buscar una ubicación
          </h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <h6>Opciones de búsqueda:</h6>
          <ul>
            <li><strong>Dirección completa:</strong> Ej: "Av. San Martín 1234, Mendoza"</li>
            <li><strong>Nombre del lugar:</strong> Ej: "Plaza Independencia, Mendoza"</li>
            <li><strong>Punto de interés:</strong> Ej: "Universidad Nacional de Cuyo"</li>
            <li><strong>Plus Code de Google:</strong> Ej: "25J2+Q5F Luján de Cuyo, Mendoza"</li>
          </ul>

          <hr />

          <h6>¿Cómo obtener un Plus Code?</h6>
          <ol>
            <li>
              Abre
              <a href="https://maps.google.com" target="_blank">Google Maps</a> en tu navegador
            </li>
            <li>Busca o haz clic en la ubicación deseada</li>
            <li>Haz clic en el lugar para ver sus detalles</li>
            <li>Verás el Plus Code debajo del nombre del lugar (ej: <code>25J2+Q5F</code>)</li>
            <li>Copia y pega el código completo en el buscador</li>
          </ol>

          <div class="alert alert-info mt-3">
            <i class="bi bi-lightbulb me-2"></i>
            <strong>Tip:</strong> Después de seleccionar una ubicación, puedes ajustar el pin
            manualmente en el mapa para mayor precisión.
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="$emit('close')">Entendido</button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show" v-if="show" style="z-index: 1060"></div>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean;
}>();

defineEmits<{
  (e: "close"): void;
}>();
</script>
