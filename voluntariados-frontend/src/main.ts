import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// main.ts
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js' // Important for dropdown!

const app = createApp(App)

app.use(router)

app.mount('#app')