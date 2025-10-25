<template>
  <div>
    <div ref="map" style="width: 100%; height: 350px"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
const props = defineProps<{
  latitud?: number | string;
  longitud?: number | string;
  placeId?: string;
}>();
const emit = defineEmits<{
  (e: "location-selected", payload: { latitud: number; longitud: number; place_id: string }): void;
}>();

const map = ref<HTMLDivElement | null>(null);
let googleMap: any = null;
let marker: any = null;

const defaultLat = typeof props.latitud === "number" ? props.latitud : -32.8894;
const defaultLng = typeof props.longitud === "number" ? props.longitud : -68.8458;

function loadGoogleMapsScript() {
  return new Promise<void>((resolve, reject) => {
    if (window.google && window.google.maps) {
      resolve();
      return;
    }
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${
      import.meta.env.VITE_GOOGLE_MAPS_API_KEY
    }&libraries=places`;
    script.async = true;
    script.onload = () => resolve();
    script.onerror = reject;
    document.head.appendChild(script);
  });
}

onMounted(async () => {
  await loadGoogleMapsScript();
  googleMap = new window.google.maps.Map(map.value!, {
    center: { lat: defaultLat, lng: defaultLng },
    zoom: 13,
  });

  marker = new window.google.maps.Marker({
    position: { lat: defaultLat, lng: defaultLng },
    map: googleMap,
    draggable: true,
  });

  googleMap.addListener("click", (e: any) => {
    const lat = e.latLng?.lat();
    const lng = e.latLng?.lng();
    if (lat && lng) {
      marker.setPosition({ lat, lng });
      const service = new window.google.maps.places.PlacesService(googleMap);
      const request = { location: { lat, lng }, radius: 1 };
      service.nearbySearch(request, (results: any, status: any) => {
        let place_id = "";
        if (
          status === window.google.maps.places.PlacesServiceStatus.OK &&
          results &&
          results.length > 0
        ) {
          place_id = results[0].place_id;
        }
        emit("location-selected", { latitud: lat, longitud: lng, place_id });
      });
    }
  });

  marker.addListener("dragend", (e: any) => {
    const lat = e.latLng?.lat();
    const lng = e.latLng?.lng();
    if (lat && lng) {
      const service = new window.google.maps.places.PlacesService(googleMap);
      const request = { location: { lat, lng }, radius: 1 };
      service.nearbySearch(request, (results: any, status: any) => {
        let place_id = "";
        if (
          status === window.google.maps.places.PlacesServiceStatus.OK &&
          results &&
          results.length > 0
        ) {
          place_id = results[0].place_id;
        }
        emit("location-selected", { latitud: lat, longitud: lng, place_id });
      });
    }
  });
});

watch(
  () => [props.latitud, props.longitud],
  ([lat, lng]) => {
    if (googleMap && marker && lat && lng) {
      const latNum = typeof lat === "number" ? lat : parseFloat(lat as string);
      const lngNum = typeof lng === "number" ? lng : parseFloat(lng as string);
      googleMap.setCenter({ lat: latNum, lng: lngNum });
      marker.setPosition({ lat: latNum, lng: lngNum });
    }
  }
);
</script>
