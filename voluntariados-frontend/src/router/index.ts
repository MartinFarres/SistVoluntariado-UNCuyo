import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import authService from '@/services/authService'
import VoluntariadosView from '@/views/VoluntariadosView.vue'
import VoluntariadoDetail from '@/views/VoluntariadoDetail.vue'
import OrganizationDetail from '@/views/OrganizationDetail.vue'
import AboutView from '@/views/AboutView.vue'
import OrganizationsView from '@/views/OrganizationsView.vue'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/voluntariados',
    name: 'VoluntariadosView',
    component: VoluntariadosView
  },
  {
    path: '/organizaciones',
    name: 'OrganizacionesView',
    component: OrganizationsView
  },
  {
    path: '/about',
    name: 'AboutView',
    component: AboutView
  },
  {
    // path: '/voluntariado',
    path: '/voluntariados/:id',
    name: 'VoluntariadoDetail',
    component: VoluntariadoDetail
  },
  {
    // path: '/organization',
    path: '/organizaciones/:id',
    name: 'OrganizationDetail',
    component: OrganizationDetail
  },
  {
    path: '/area-personal/delegado',
    name: 'DelegadoAreaPersonal',
    component: () => import('../views/delegado/AreaPersonal.vue'),
    meta: { requiresAuth: true, requiresDelegado: true }
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: () => import('../views/SignIn.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: () => import('../views/SignUp.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/setup',
    name: 'Setup',
    component: () => import('../views/Setup.vue'),
    meta: { requiresAuth: true, requiresSetup: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/ProfileView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin/dashboard',
    name: 'Dashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/Users.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/personas',
    name: 'AdminPersonas',
    component: () => import('../views/admin/Personas.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/delegados',
    name: 'AdminDelegados',
    component: () => import('../views/admin/Delegados.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
    {
    path: '/admin/voluntarios',
    name: 'AdminVoluntarios',
    component: () => import('../views/admin/Voluntarios.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/administradores',
    name: 'AdminAdministradores',
    component: () => import('../views/admin/Administradores.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/voluntariados',
    name: 'AdminVoluntariados',
    component: () => import('../views/admin/Voluntariados.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/organizaciones',
    name: 'AdminOrganizaciones',
    component: () => import('../views/admin/Organizaciones.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/facultades',
    name: 'AdminFacultades',
    component: () => import('@/views/admin/Facultades.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/carreras',
    name: 'AdminCarreras',
    component: () => import('@/views/admin/Carreras.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },

  {
    path: '/admin/paises',
    name: 'AdminPaises',
    component: () => import('../views/admin/Paises.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/provincias',
    name: 'AdminProvincias',
    component: () => import('../views/admin/Provincias.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/departamentos',
    name: 'AdminDepartamentos',
    component: () => import('../views/admin/Departamentos.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/localidades',
    name: 'AdminLocalidades',
    component: () => import('../views/admin/Localidades.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
    {
      path: '/admin/landing-config',
      name: 'AdminLandingConfig',
      component: () => import('../views/admin/LandingConfig.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },

  // {
  //   path: '/opportunities/:id',
  //   name: 'OpportunityDetail',
  //   component: () => import('../views/OpportunityDetail.vue')
  // },
  // {
  //   path: '/my-applications',
  //   name: 'MyApplications',
  //   component: () => import('../views/MyApplications.vue')
  // },
  // {
  //   path: '/about',
  //   name: 'About',
  //   component: () => import('../views/About.vue')
  // },
  // {
  //   path: '/contact',
  //   name: 'Contact',
  //   component: () => import('../views/Contact.vue')
  // },
  // {
  //   path: '/faq',
  //   name: 'FAQ',
  //   component: () => import('../views/FAQ.vue')
  // },
  // {
  //   path: '/privacy',
  //   name: 'Privacy',
  //   component: () => import('../views/Privacy.vue')
  // }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()
  const isAdmin = authService.isAdmin()
  const isDelegado = authService.hasRole('DELEG')

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ path: '/signin', query: { redirect: to.fullPath } })
    return
  }

  // Check if route requires admin
  if (to.meta.requiresAdmin && !isAdmin) {
    next({ path: '/' })
    return
  }

  // Check if route requires Delegado
  if ((to.meta as any).requiresDelegado && !isDelegado) {
    next({ path: '/' })
    return
  }

  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && isAuthenticated) {
    // Check if user needs setup first
    if (authService.needsSetup()) {
      next({ path: '/setup' })
      return
    }
    next({ path: '/admin/dashboard' })
    return
  }

  // Check if authenticated user needs setup (except for setup and logout routes)
  if (isAuthenticated && authService.needsSetup() && to.path !== '/setup') {
    next({ path: '/setup' })
    return
  }

  // Prevent access to setup page if user is already settled up
  if (to.path === '/setup' && isAuthenticated && authService.isSettledUp()) {
    next({ path: '/admin/dashboard' })
    return
  }

  next()
})

export default router
