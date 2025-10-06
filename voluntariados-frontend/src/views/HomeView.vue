<script lang="ts">
// import HeroSection from '@/components/HeroSection.vue'
// import CategoriesSection from '@/components/CategoriesSection.vue'
// import FeaturedOpportunities from '@/components/FeaturedOpportunities.vue'
import AppNavBar from '@/components/Navbar.vue'


export default {
  name: 'HomeView',
  components: {
    AppNavBar
    // HeroSection,
    // CategoriesSection,
    // FeaturedOpportunities
  }
}
</script>
ß
<template>
  <div class="home">
    <AppNavBar />
    <!-- <HeroSection /> -->
    <div class="container">
      <!-- <CategoriesSection />
      <FeaturedOpportunities /> -->
    </div>
  </div>
</template>

<style scoped>
.home {
  /* Add any home-specific styles here */
}
</style>
