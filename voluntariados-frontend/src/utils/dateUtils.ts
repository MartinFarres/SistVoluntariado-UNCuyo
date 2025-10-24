/**
 * Date utility functions for handling date parsing and formatting
 * across the application.
 */

/**
 * Safely parse 'YYYY-MM-DD' date strings as local dates to avoid timezone shifts.
 * 
 * When the backend sends a date like '2024-10-24', the native Date constructor
 * parses it as UTC midnight, which may shift to the previous day in your local timezone.
 * This function interprets pure date strings (YYYY-MM-DD) as local dates.
 * 
 * @param dateStr - Date string to parse (e.g., '2024-10-24' or '2024-10-24T10:30:00Z')
 * @returns Date object interpreted in local timezone
 * 
 * @example
 * parseLocalDate('2024-10-24') // Returns Oct 24 at 00:00 local time
 * parseLocalDate('2024-10-24T10:30:00Z') // Falls back to native parsing with timezone
 */
export function parseLocalDate(dateStr: string): Date {
  if (!dateStr) return new Date(NaN);
  
  // If it's a pure date like 'YYYY-MM-DD', build as local date
  const pureDate = /^\d{4}-\d{2}-\d{2}$/.exec(dateStr);
  if (pureDate) {
    const [yStr, moStr, dStr] = dateStr.split('-');
    const y = Number(yStr);
    const mo = Number(moStr);
    const d = Number(dStr);
    return new Date(y, mo - 1, d);
  }
  
  // Fallback to native parsing for full datetime strings
  return new Date(dateStr);
}

/**
 * Format a date string in Spanish locale (Argentina) with short month format.
 * 
 * @param dateString - Date string to format
 * @returns Formatted date string (e.g., '24 oct 2024')
 */
export function formatDateShort(dateString: string): string {
  const date = parseLocalDate(dateString);
  return date.toLocaleDateString('es-AR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format a date string with full month and weekday in Spanish locale.
 * 
 * @param dateString - Date string to format
 * @returns Formatted date string (e.g., 'miércoles, 24 de octubre de 2024')
 */
export function formatDateLong(dateString: string): string {
  const date = parseLocalDate(dateString);
  return date.toLocaleDateString('es-AR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

/**
 * Get the weekday name from a date string in Spanish locale.
 * 
 * @param dateString - Date string to parse
 * @returns Capitalized weekday name (e.g., 'Miércoles')
 */
export function getWeekdayName(dateString: string): string {
  const date = parseLocalDate(dateString);
  const dayName = date.toLocaleDateString('es-AR', { weekday: 'long' });
  return dayName.charAt(0).toUpperCase() + dayName.slice(1);
}

/**
 * Format a date string using the custom month names array.
 * Useful when you need specific abbreviated month names.
 * 
 * @param dateString - Date string to format
 * @returns Formatted date string (e.g., '24 Oct 2024')
 */
export function formatDateCustom(dateString: string): string {
  const date = parseLocalDate(dateString);
  const months = [
    'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic',
  ];
  return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
}
