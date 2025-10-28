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

/**
 * Reverse geocode coordinates to a human-readable address using Google Geocoding API.
 * Returns a short formatted address when possible.
 */
export const reverseGeocode = async (
  lat: number,
  lng: number
): Promise<string | null> => {
  const apiKey = GOOGLE_MAPS_CONFIG.apiKey;
  if (!apiKey) return null;

  const url = new URL('https://maps.googleapis.com/maps/api/geocode/json');
  url.searchParams.set('latlng', `${lat},${lng}`);
  url.searchParams.set('key', apiKey);
  url.searchParams.set('language', GOOGLE_MAPS_CONFIG.language);
  url.searchParams.set('region', GOOGLE_MAPS_CONFIG.region);

  try {
    const res = await fetch(url.toString());
    if (!res.ok) return null;
    const data = await res.json();
    if (data.status !== 'OK' || !Array.isArray(data.results) || data.results.length === 0) {
      return null;
    }
    // Prefer a locality-level address if available, else the first formatted address
    const locality = data.results.find((r: unknown) => {
      const rec = r as { types?: unknown };
      const types = Array.isArray(rec.types) ? rec.types as string[] : [];
      return types.includes('locality') || types.includes('sublocality');
    }) as { formatted_address?: unknown } | undefined;
    const first = data.results[0] as { formatted_address?: unknown } | undefined;
    const formatted = (locality?.formatted_address ?? first?.formatted_address);
    return typeof formatted === 'string' ? formatted : null;
  } catch {
    return null;
  }
};