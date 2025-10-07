import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import authService from '@/services/authService'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
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
    path: '/admin/voluntariados',
    name: 'AdminVoluntariados',
    component: () => import('../views/admin/Voluntariados.vue'),
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
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()
  const isAdmin = authService.isAdmin()

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

  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest && isAuthenticated) {
    next({ path: '/admin/dashboard' })
    return
  }

  next()
})

export default router