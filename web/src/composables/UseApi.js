import { api } from 'boot/axios'

export default function useApi (url) {

  const postEvent = async (form) => {
    try {
      const response = await api.post(url, form)
      return response
    } catch (error) {
      throw new Error(error)
    }       
  }

  return {
    postEvent
  }
}