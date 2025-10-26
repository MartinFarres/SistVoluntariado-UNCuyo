/**
 * Google Maps utilities for the frontend application
 */

export const GOOGLE_MAPS_CONFIG = {
  apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
  libraries: ['places'] as const,
  version: 'weekly' as const,
  language: 'es' as const,
  region: 'AR' as const, // Argentina
};

/**
 * Check if Google Maps API key is configured
 */
export const isGoogleMapsConfigured = (): boolean => {
  return Boolean(GOOGLE_MAPS_CONFIG.apiKey && GOOGLE_MAPS_CONFIG.apiKey !== 'your_google_maps_api_key_here');
};

/**
 * Generate Google Maps URL for external link
 */
export const getGoogleMapsUrl = (lat: number, lng: number, zoom: number = 15): string => {
  return `https://www.google.com/maps?q=${lat},${lng}&z=${zoom}`;
};

/**
 * Generate Google Maps directions URL
 */
export const getGoogleMapsDirectionsUrl = (lat: number, lng: number, label?: string): string => {
  const destination = label ? `${label}@${lat},${lng}` : `${lat},${lng}`;
  return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(destination)}`;
};

/**
 * Format coordinates for display
 */
export const formatCoordinates = (lat: number, lng: number, decimals: number = 6): string => {
  return `${lat.toFixed(decimals)}, ${lng.toFixed(decimals)}`;
};