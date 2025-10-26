## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Project Setup

### Requirements

Installing npm

```sh
sudo apt install npm
```

Setting up backend `.env`

```sh
# API base URL for running locally
VITE_API_BASE_URL=http://localhost:8000/api
```

### Running the project

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

# Google Maps Integration Setup

This document explains how to set up Google Maps integration for displaying voluntariado locations.

## Prerequisites

1. **Google Maps API Key**: You need a valid Google Maps API key with the following APIs enabled:
   - Maps JavaScript API
   - Places API (optional, for enhanced location features)

## Setup Instructions

### 1. Get a Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Maps JavaScript API** and **Places API**
4. Create credentials (API Key)
5. Restrict the API key to your domain for security (optional but recommended)

### 2. Configure Environment Variables

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Add your Google Maps API key to the `.env` file:
   ```bash
   VITE_GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key_here
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

### 3. Backend Data Requirements

The backend should provide voluntariado data with the following location fields:

```json
{
  "id": 1,
  "nombre": "Voluntariado Example",
  "latitud": -32.8894,
  "longitud": -68.8458,
  "place_id": "ChIJ..." // optional, Google Places ID
}
```
