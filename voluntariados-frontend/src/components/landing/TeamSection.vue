<!-- src/components/landing/TeamSection.vue -->
<template>
  <section class="team-section py-5">
    <div class="container">
      <h2 class="section-title text-center mb-3">
        {{ title }}
      </h2>
      <p class="section-subtitle text-center mb-5">
        {{ subtitle }}
      </p>

      <div class="row g-4">
        <div v-for="(member, index) in teamMembers" :key="index" class="col-md-6 col-lg-3">
          <div class="team-card">
            <div class="team-avatar">
              <img
                :src="member.imageUrl || member.avatar || 'https://via.placeholder.com/150'"
                :alt="member.name"
              />
            </div>
            <div class="team-info">
              <h4 class="member-name">{{ member.name }}</h4>
              <p class="member-role">{{ member.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue";

interface TeamMember {
  name: string;
  role: string;
  imageUrl?: string;
  avatar?: string;
}

export default defineComponent({
  name: "TeamSection",
  props: {
    title: {
      type: String,
      default: "Nuestro Equipo",
    },
    subtitle: {
      type: String,
      default: "",
    },
    teamMembers: {
      type: Array as PropType<TeamMember[]>,
      required: true,
    },
  },
});
</script>

<style scoped>
.team-section {
  background: #f8f9fa;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  max-width: 700px;
  margin: 0 auto;
}

.team-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
  height: 100%;
}

.team-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(139, 0, 0, 0.15);
}

.team-avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #8b0000;
  box-shadow: 0 4px 15px rgba(139, 0, 0, 0.2);
}

.team-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.team-card:hover .team-avatar img {
  transform: scale(1.1);
}

.member-name {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.member-role {
  font-size: 0.95rem;
  color: #6c757d;
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
}
</style>
