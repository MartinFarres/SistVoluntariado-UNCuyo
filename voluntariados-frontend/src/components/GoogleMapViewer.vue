<template>
  <div class="google-map-viewer">
    <!-- Loading overlay -->
    <div v-if="loading" class="loading-overlay d-flex justify-content-center align-items-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando mapa...</span>
      </div>
    </div>

    <!-- Error overlay -->
    <div v-if="error" class="error-overlay alert alert-warning d-flex align-items-center">
      <i class="bi bi-exclamation-triangle me-2"></i>
      No se pudo cargar el mapa: {{ error }}
    </div>

    <!-- Map container - always rendered -->
    <div ref="mapContainer" class="map-container" :class="{ 'map-hidden': loading || error }"></div>
  </div>
</template>

<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from "vue";
import {
  GOOGLE_MAPS_CONFIG,
  isGoogleMapsConfigured,
  getGoogleMapsUrl,
  formatCoordinates,
} from "@/utils/mapsUtils";

declare global {
  interface Window {
    google: any;
  }
}

interface Props {
  latitud?: number | null;
  longitud?: number | null;
  place_id?: string | null;
  title?: string;
  zoom?: number;
}

const props = withDefaults(defineProps<Props>(), {
  zoom: 15,
  title: "Ubicación del Voluntariado",
});

const mapContainer = ref<HTMLDivElement | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

let googleMap: any = null;
let marker: any = null;

function loadGoogleMapsScript() {
  return new Promise<void>((resolve, reject) => {
    if (!isGoogleMapsConfigured()) {
      reject(
        new Error(
          "Google Maps API key not configured. Please set VITE_GOOGLE_MAPS_API_KEY in your .env file."
        )
      );
      return;
    }

    if (window.google && window.google.maps) {
      resolve();
      return;
    }

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${
      GOOGLE_MAPS_CONFIG.apiKey
    }&libraries=${GOOGLE_MAPS_CONFIG.libraries.join(",")}&language=${
      GOOGLE_MAPS_CONFIG.language
    }&region=${GOOGLE_MAPS_CONFIG.region}`;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = (err) => {
      reject(
        new Error(
          "Failed to load Google Maps API. Please check your API key and network connection."
        )
      );
    };
    document.head.appendChild(script);
  });
}

const initMap = async () => {
  if (!props.latitud || !props.longitud) {
    error.value = "Ubicación no disponible";
    loading.value = false;
    return;
  }

  try {
    await loadGoogleMapsScript();

    // Wait for the DOM element to be ready
    await nextTick();

    // Check if the map container is available
    if (!mapContainer.value) {
      error.value = "Error: elemento del mapa no disponible";
      loading.value = false;
      return;
    }

    const mapOptions = {
      center: { lat: props.latitud, lng: props.longitud },
      zoom: props.zoom,
      mapTypeControl: false,
      streetViewControl: true,
      fullscreenControl: true,
      zoomControl: true,
      disableDefaultUI: false,
    };

    googleMap = new window.google.maps.Map(mapContainer.value, mapOptions);

    // Add marker
    marker = new window.google.maps.Marker({
      position: { lat: props.latitud, lng: props.longitud },
      map: googleMap,
      title: props.title,
      animation: window.google.maps.Animation.DROP,
    });

    // Add info window
    const infoWindow = new window.google.maps.InfoWindow({
      content: `
        <div style="padding: 12px; max-width: 280px;">
          <h6 style="margin: 0 0 8px 0; color: #333; font-weight: 600;">${props.title}</h6>
          <p style="margin: 0 0 8px 0; font-size: 13px; color: #666;">
            <i class="bi bi-geo-alt-fill" style="color: #dc3545;"></i> 
            ${formatCoordinates(props.latitud, props.longitud)}
          </p>
          <a href="${getGoogleMapsUrl(props.latitud, props.longitud)}" target="_blank" 
             style="font-size: 12px; color: #0066cc; text-decoration: none;">
            <i class="bi bi-box-arrow-up-right"></i> Ver en Google Maps
          </a>
        </div>
      `,
    });

    marker.addListener("click", () => {
      infoWindow.open(googleMap, marker);
    });

    loading.value = false;
  } catch (err: any) {
    console.error("Error loading Google Maps:", err);
    if (err.message.includes("API key not configured")) {
      error.value =
        "Google Maps API key no configurada. Por favor configura VITE_GOOGLE_MAPS_API_KEY en tu archivo .env";
    } else if (err.message.includes("Failed to load Google Maps API")) {
      error.value =
        "Error al cargar la API de Google Maps. Verifica tu clave API y conexión a internet.";
    } else {
      error.value = `Error al cargar Google Maps: ${err.message}`;
    }
    loading.value = false;
  }
};

// Watch for prop changes
watch(
  [() => props.latitud, () => props.longitud],
  () => {
    if (googleMap && marker && props.latitud && props.longitud) {
      const newPosition = { lat: props.latitud, lng: props.longitud };
      googleMap.setCenter(newPosition);
      marker.setPosition(newPosition);
    }
  },
  { deep: true }
);

onMounted(() => {
  initMap();
});
</script>

<style scoped>
.google-map-viewer {
  position: relative;
  width: 100%;
  height: 350px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.map-hidden {
  visibility: hidden;
}

.loading-overlay,
.error-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 10;
  border-radius: 8px;
}

.loading-overlay {
  background: rgba(248, 249, 250, 0.9);
}

.error-overlay {
  margin: 0;
  border-radius: 8px;
  justify-content: center;
  align-items: center;
}
</style>
