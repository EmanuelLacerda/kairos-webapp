import { api } from 'boot/axios'

export default function useApi (url) {

  const getEvent = async (id=null) => {
    try {
      if(id){
        const response = await api.get(`${url}${id}/`);
        return response;
      }
      
      const response = await api.get(url);
      return response
    } catch (error) {
      return error.response
    }
  }

  const postEvent = async (form) => {
    try {
      const response = await api.post(url, form)
      return response
    } catch (error) {
      return error.response
    }       
  }

  const putEvent = async (id, form) => {
    try {
      const response = await api.put(`${url}${id}/`, form)
      return response
    } catch (error) {
      return error.response
    }
  }

  const patchEvent = async (id, form) => {
    try {
      const response = await api.put(`${url}${id}/`, form)
      return response
    } catch (error) {
      return error.response;
    }
  }

  const deleteEvent = async (id) => {
    try {
      const response = await api.delete(`${url}${id}/`)
      return response
    } catch (error) {
      return error.response;
    }
  }

  const getUserEvents = async (userId, startDate=null, endDate=null) => {
    try {
      if(startDate && endDate){
        return await api.get(`auth/user/${userId}/events/?start=${startDate}&end=${endDate}`);
      }

      return await api.get(`auth/user/${userId}/events/`);      
    } catch (error) {
      return error.response;
    }
  }

  return {
    postEvent,
    putEvent,
    patchEvent,
    getEvent,
    deleteEvent,
    getUserEvents
  }
}