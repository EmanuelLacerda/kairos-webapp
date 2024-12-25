const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue'), meta: {requireLogin: true} }
    ]
  },
  {
    path: '/auth',
    component: () => import('layouts/AuthLayout.vue'),
    children: [
      { name: 'LogIn', path: 'login', component: () => import('pages/LoginPage.vue') },
      { name: 'RegisterUser', path: 'criar-conta', component: () => import('pages/RegisterUserPage.vue') },
      { name: 'VerifyUserEmail', path: 'verificar-email', component: () => import('pages/VerifyEmailPage.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
