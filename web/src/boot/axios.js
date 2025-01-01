import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'
import { useAuthStore } from 'src/stores/auth'

const baseUrl = 'http://127.0.0.1:8000/api/v1/';
const api = axios.create({ baseURL: baseUrl });

export default defineBoot(({ app }) => {
  app.config.globalProperties.$axios = axios

  app.config.globalProperties.$api = api
})

api.interceptors.request.use(async req => {
  const authStore = useAuthStore();

  const result = await authStore.checkIfUserAuthenticated();

  if(result.isUserAuthenticated){
    if(result.new_access_token){
      authStore.updateAccessToken(result.new_access_token)
      req.headers.Authorization = `Bearer ${result.new_access_token}`
    }
  } else{
    authStore.removeAuthenticatedStatus()
    req.headers.Authorization = "";
  }

  return req;
})



export { axios, api }