import { defineRouter } from '#q-app/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'

import { useAuthStore } from 'src/stores/auth'

export default defineRouter(function () {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach(async (to, from, next) => {

    if(to.matched.some(record => record.meta.requireLogin)){
      const authStore = useAuthStore();

      const result = await authStore.checkIfUserAuthenticated();

      if(result.isUserAuthenticated){
        if(result.new_access_token){
          authStore.updateAccessToken(result.new_access_token);
        }

        next();
      } else{
        authStore.removeAuthenticatedStatus();
        next({
          name: 'LogIn',
          query: {to: to.path}
        });
      }
    } else{
      next();
    }
  })

  return Router
})
