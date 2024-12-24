import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'

const api = axios.create({ baseURL: 'http://127.0.0.1:8000/api/v1/' })

export default defineBoot(({ app }) => {
  app.config.globalProperties.$axios = axios

  app.config.globalProperties.$api = api
})

export { axios, api }