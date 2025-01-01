import useApi from 'src/composables/UseApi'

export default function eventsService () {
  const { getEvent, postEvent, putEvent, patchEvent, getUserEvents } = useApi('/events/')

  return {
    "get": getEvent,
    "post": postEvent,
    "put": putEvent,
    "patch": patchEvent,
    "getUserEvents": getUserEvents
  }
}