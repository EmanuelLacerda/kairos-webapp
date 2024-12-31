import { api } from 'boot/axios'

export default function useApi (url) {

  const postEvent = async (form) => {
    try {
      const response = await api.post(url, form)
      return response
    } catch (error) {
      return error.response
    }       
  }

  const getUserEvents = async (userId, startDate=null, endDate=null) => {
    try {
      if(startDate && endDate){
        return await api.get(`auth/user/${userId}/events/?start=${startDate}&end=${endDate}`);
      }

      return await api.get(`auth/user/${userId}/events/`);      
    } catch (error) {
      throw new Error(error)
    }       
  }

  return {
    postEvent,
    getUserEvents
  }
}