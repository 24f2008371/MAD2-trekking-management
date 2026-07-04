import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/auth',
    redirect: '/auth/login'
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: () => import('../views/AuthView.vue')
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: () => import('../views/AuthView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
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

