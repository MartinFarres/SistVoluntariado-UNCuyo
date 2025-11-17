<!-- src/components/landing/TeamSection.vue -->
<template>
  <section class="team-section py-5">
    <div class="container">
      <div class="text-center mb-5">
        <h2 class="section-title">{{ title }}</h2>
        <p v-if="subtitle" class="section-subtitle">{{ subtitle }}</p>
      </div>
      <div class="row g-4 justify-content-center">
        <div v-for="(member, index) in teamMembers" :key="index" class="col-md-6 col-lg-3">
          <div class="team-member-card">
            <div class="member-avatar">
              <img :src="member.imageUrl || member.avatar || placeholder" :alt="member.name" />
            </div>
            <div class="member-info">
              <h3 class="member-name">{{ member.name }}</h3>
              <p class="member-role">{{ member.role }}</p>
              <p v-if="member.description" class="member-description">{{ member.description }}</p>
            </div>
          </div>
        </div>
        <div v-if="teamMembers.length === 0" class="col-12">
          <div class="alert alert-secondary text-center mb-0">
            No hay miembros del equipo configurados todavía.
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
  description?: string;
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
  setup() {
    const placeholder = "https://via.placeholder.com/150";
    return { placeholder };
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
.team-member-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid #e9ecef;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.team-member-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}
.member-avatar {
  width: 120px;
  height: 120px;
  margin: 0 auto 1.5rem;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid #0d6efd;
  box-shadow: 0 4px 15px rgba(13, 110, 253, 0.25);
}
.member-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}
.team-member-card:hover .member-avatar img {
  transform: scale(1.1);
}
.member-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.35rem;
}
.member-role {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
}
.member-description {
  font-size: 0.85rem;
  color: #555;
  margin: 0;
}
@media (max-width: 768px) {
  .section-title {
    font-size: 2rem;
  }
  .team-member-card {
    padding: 1.5rem;
  }
  .member-avatar {
    width: 100px;
    height: 100px;
  }
}
</style>
