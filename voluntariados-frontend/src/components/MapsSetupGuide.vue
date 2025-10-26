<template>
  <div class="maps-setup-guide p-4">
    <div class="container-fluid">
      <div class="alert alert-info">
        <h5><i class="bi bi-info-circle me-2"></i>Google Maps Setup Guide</h5>
        <p class="mb-0">Follow these steps to configure Google Maps for your application:</p>
      </div>

      <div class="row">
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              <h6 class="mb-0">Setup Steps</h6>
            </div>
            <div class="card-body">
              <ol class="setup-steps">
                <li class="mb-3">
                  <strong>Get Google Maps API Key</strong>
                  <ul>
                    <li>
                      Go to
                      <a href="https://console.cloud.google.com/" target="_blank"
                        >Google Cloud Console</a
                      >
                    </li>
                    <li>Create a new project or select existing one</li>
                    <li>Enable "Maps JavaScript API" and "Places API"</li>
                    <li>Create credentials (API Key)</li>
                  </ul>
                </li>
                <li class="mb-3">
                  <strong>Create .env file</strong>
                  <div class="code-block mt-2">
                    <code>
                      # Copy .env.example to .env<br />
                      cp .env.example .env<br /><br />
                      # Then edit .env and add your API key:<br />
                      VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
                    </code>
                  </div>
                </li>
                <li class="mb-3">
                  <strong>Restart Development Server</strong>
                  <div class="code-block mt-2">
                    <code>npm run dev</code>
                  </div>
                </li>
              </ol>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              <h6 class="mb-0">Configuration Status</h6>
            </div>
            <div class="card-body">
              <div class="status-item mb-3">
                <div class="d-flex align-items-center">
                  <i :class="apiKeyStatus.icon" class="me-2"></i>
                  <span>API Key</span>
                </div>
                <small :class="apiKeyStatus.class">{{ apiKeyStatus.message }}</small>
              </div>

              <div class="status-item mb-3" v-if="apiKeyConfigured">
                <div class="d-flex align-items-center">
                  <i class="bi bi-map text-success me-2"></i>
                  <span>Test Map</span>
                </div>
                <small class="text-success">Ready to test</small>
              </div>

              <button v-if="apiKeyConfigured" class="btn btn-primary btn-sm" @click="testMap">
                <i class="bi bi-play me-1"></i>Test Map
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Test Map Section -->
      <div v-if="showTestMap" class="row mt-4">
        <div class="col-lg-8 mx-auto">
          <div class="card">
            <div class="card-header">
              <h6 class="mb-0">Test Map - Universidad Nacional de Cuyo</h6>
            </div>
            <div class="card-body p-0">
              <GoogleMapViewer
                :latitud="-32.8894"
                :longitud="-68.8458"
                title="Universidad Nacional de Cuyo - Test Location"
                :zoom="16"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { isGoogleMapsConfigured } from "@/utils/mapsUtils";
import GoogleMapViewer from "./GoogleMapViewer.vue";

const showTestMap = ref(false);

const apiKeyConfigured = computed(() => isGoogleMapsConfigured());

const apiKeyStatus = computed(() => {
  if (apiKeyConfigured.value) {
    return {
      icon: "bi bi-check-circle text-success",
      class: "text-success",
      message: "API Key configured",
    };
  } else {
    return {
      icon: "bi bi-x-circle text-danger",
      class: "text-danger",
      message: "API Key not configured",
    };
  }
});

const testMap = () => {
  showTestMap.value = true;
};
</script>

<style scoped>
.maps-setup-guide {
  background: #f8f9fa;
  min-height: 100vh;
}

.setup-steps {
  counter-reset: step-counter;
}

.setup-steps li {
  counter-increment: step-counter;
  position: relative;
  padding-left: 2rem;
}

.setup-steps li::before {
  content: counter(step-counter);
  position: absolute;
  left: 0;
  top: 0;
  background: #007bff;
  color: white;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: bold;
}

.code-block {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 1rem;
  font-family: "Courier New", monospace;
  font-size: 0.9rem;
}

.code-block code {
  background: none;
  padding: 0;
  color: #333;
}

.status-item {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 0.75rem;
}

.status-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.card {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border: none;
}

.card-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
}
</style>
