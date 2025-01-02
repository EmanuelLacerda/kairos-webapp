import useApi from 'src/composables/UseApi'

export default function eventsService () {
  const { getEvent, postEvent, putEvent, patchEvent, deleteEvent, getUserEvents } = useApi('/events/')

  return {
    "get": getEvent,
    "post": postEvent,
    "put": putEvent,
    "patch": patchEvent,
    "delete": deleteEvent,
    "getUserEvents": getUserEvents
  }
}