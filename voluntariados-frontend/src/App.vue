<script setup lang="ts">
import { RouterView } from 'vue-router'

</script>

<template>
  <div id="app">
   
    <!-- Main Content Area - Router View -->
    <main class="py-4">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-4">
      <div class="container">
        <div class="row">
          <div class="col-md-4 mb-3">
            <h5>UniVolunteer</h5>
            <p class="text-muted">
              Connecting students with meaningful volunteering opportunities.
            </p>
          </div>
          <div class="col-md-4 mb-3">
            <h5>Quick Links</h5>
            <ul class="list-unstyled">
              <li>
                <router-link to="/about" class="text-muted text-decoration-none">About Us</router-link>
              </li>
              <li>
                <router-link to="/contact" class="text-muted text-decoration-none">Contact</router-link>
              </li>
              <li>
                <router-link to="/faq" class="text-muted text-decoration-none">FAQ</router-link>
              </li>
              <li>
                <router-link to="/privacy" class="text-muted text-decoration-none">Privacy Policy</router-link>
              </li>
            </ul>
          </div>
          <div class="col-md-4 mb-3">
            <h5>Contact</h5>
            <p class="text-muted">
              <i class="bi bi-envelope"></i> volunteer@university.edu<br>
              <i class="bi bi-phone"></i> (555) 123-4567
            </p>
            <div class="social-links">
              <a href="#" class="text-muted me-3"><i class="bi bi-facebook fs-5"></i></a>
              <a href="#" class="text-muted me-3"><i class="bi bi-twitter fs-5"></i></a>
              <a href="#" class="text-muted me-3"><i class="bi bi-instagram fs-5"></i></a>
            </div>
          </div>
        </div>
        <hr class="border-secondary">
        <div class="text-center text-muted">
          <p class="mb-0">&copy; 2025 UniVolunteer. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
export default {
  name: 'App'
}
</script>

<style>
/* Import Bootstrap Icons */
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css');
@import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* Footer link hover */
footer a:hover {
  color: #ffffff !important;
}

.social-links a {
  transition: color 0.2s;
}

.social-links a:hover {
  color: #ffffff !important;
}
</style>