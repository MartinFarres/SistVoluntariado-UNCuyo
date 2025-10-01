import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/adminDashboard',
    name: 'Dashboard',
    component: () => import('../views/admin/Dashboard.vue')
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
  // },
  // {
  //   path: '/signin',
  //   name: 'SignIn',
  //   component: () => import('../views/SignIn.vue')
  // },
  // {
  //   path: '/signup',
  //   name: 'SignUp',
  //   component: () => import('../views/SignUp.vue')
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

export default router