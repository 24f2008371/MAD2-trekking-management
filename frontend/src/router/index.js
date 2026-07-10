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
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/UserView.vue')
  },
  {
    path: '/admin',
    component: () => import('../views/AdminView.vue'),
    redirect: '/admin/dashboard',
    meta: { requiresAdmin: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../components/admin/AdminDashboard.vue')
      },
      {
        path: 'treks',
        name: 'AdminTreks',
        component: () => import('../components/admin/AdminTreks.vue')
      },
      {
        path: 'staff',
        name: 'AdminStaff',
        component: () => import('../components/admin/AdminStaff.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../components/admin/AdminUsers.vue')
      },
      {
        path: 'bookings',
        name: 'AdminBookings',
        component: () => import('../components/admin/AdminBookings.vue')
      },
      {
        path: 'search',
        name: 'AdminSearch',
        component: () => import('../components/admin/AdminSearch.vue')
      },
      {
        path: 'reports',
        name: 'AdminReports',
        component: () => import('../components/admin/AdminReports.vue')
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('../components/admin/AdminSettings.vue')
      }
    ]
  },
  {
    path: '/staff/dashboard',
    name: 'StaffDashboard',
    component: () => import('../views/StaffView.vue'),
    meta: { requiresStaff: true }
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

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  let user = null
  try {
    user = JSON.parse(localStorage.getItem('user'))
  } catch (e) {
    // ignore
  }

  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (!token || !user || user.role !== 'admin') {
      next('/auth/login')
    } else {
      next()
    }
  } else if (to.matched.some(record => record.meta.requiresStaff)) {
    if (!token || !user || user.role !== 'staff') {
      next('/auth/login')
    } else {
      next()
    }
  } else if (to.name === 'Dashboard') {
    if (!token) {
      next('/auth/login')
    } else if (user && user.role === 'admin') {
      next('/admin/dashboard')
    } else if (user && user.role === 'staff') {
      next('/staff/dashboard')
    } else {
      next()
    }
  } else if (to.path.startsWith('/auth') && token) {
    if (user && user.role === 'admin') {
      next('/admin/dashboard')
    } else if (user && user.role === 'staff') {
      next('/staff/dashboard')
    } else {
      next('/dashboard')
    }
  } else {
    next()
  }
})

export default router

