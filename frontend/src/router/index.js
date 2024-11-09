import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },

    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },

    {
      path: '/thread/:id',
      name: 'thread',
      component: () => import('../views/ThreadView.vue')
    },

    {
      path: '/error/:status',
      name: 'error',
      component: () => import('../views/ErrorView.vue')
    },
    
  ]
})

export default router
