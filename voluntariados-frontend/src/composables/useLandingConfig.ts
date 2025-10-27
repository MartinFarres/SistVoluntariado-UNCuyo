// src/composables/useLandingConfig.ts
import { ref, readonly } from 'vue'
import { landingConfigAPI } from '@/services/api'

// TypeScript interfaces for dynamic content
export interface InfoItem {
  icon: string
  title: string
  description: string
}

export interface Testimonial {
  name: string
  role: string
  text: string
  imageUrl?: string
}

export interface HowItWorksStep {
  title: string
  description: string
}

export interface TeamMember {
  name: string
  role: string
  imageUrl?: string
}

export interface LandingConfig {
  page_title: string
  site_name: string
  welcome_message: string
  description: string
  contact_email: string
  phone_number: string
  instagram_handle: string
  instagram_url: string
  footer_text: string
  // Dynamic content fields
  info_items: InfoItem[]
  testimonials: Testimonial[]
  how_it_works_steps: HowItWorksStep[]
  team_members: TeamMember[]
}

// Shared state across all components
const landingConfig = ref<LandingConfig>({
  page_title: 'Voluntariado UNCuyo',
  site_name: 'Voluntariado UNCuyo',
  welcome_message: 'Convertite en el cambio que querés ver.',
  description: '¡Sumáte a los voluntariados!',
  contact_email: '',
  phone_number: '',
  instagram_handle: '',
  instagram_url: '',
  footer_text: '© 2025 Voluntariado UNCuyo.',
  // Default empty arrays for dynamic content
  info_items: [],
  testimonials: [],
  how_it_works_steps: [],
  team_members: []
})

const isLoading = ref(false)
const isLoaded = ref(false)

// Single source of truth for fetching config
const fetchLandingConfig = async (): Promise<void> => {
  // Don't fetch if already loaded or currently loading
  if (isLoaded.value || isLoading.value) {
    return
  }

  isLoading.value = true
  
  try {
    const response = await landingConfigAPI.getPublicConfig()
    if (response.data) {
      landingConfig.value = {
        page_title: response.data.page_title || 'Voluntariado UNCuyo',
        site_name: response.data.site_name || 'Voluntariado UNCuyo',
        welcome_message: response.data.welcome_message || 'Convertite en el cambio que querés ver.',
        description: response.data.description || '¡Sumáte a los voluntariados!',
        contact_email: response.data.contact_email || '',
        phone_number: response.data.phone_number || '',
        instagram_handle: response.data.instagram_handle || '',
        instagram_url: response.data.instagram_url || '',
        footer_text: response.data.footer_text || '© 2025 Voluntariado UNCuyo.',
        // Dynamic content fields from backend
        info_items: response.data.info_items || [],
        testimonials: response.data.testimonials || [],
        how_it_works_steps: response.data.how_it_works_steps || [],
        team_members: response.data.team_members || []
      }
      
      // Update document title
      document.title = landingConfig.value.page_title
      isLoaded.value = true
    }
  } catch (error) {
    console.warn('Error fetching landing config:', error)
    // Keep default values if API fails
  } finally {
    isLoading.value = false
  }
}

// Composable hook
export const useLandingConfig = () => {
  return {
    landingConfig: landingConfig,
    isLoading: readonly(isLoading),
    isLoaded: readonly(isLoaded),
    fetchLandingConfig
  }
}