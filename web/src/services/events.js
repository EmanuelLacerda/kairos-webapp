import useApi from 'src/composables/UseApi'

export default function eventsService () {
  const { postEvent, getUserEvents } = useApi('/events/')

  return {
    "post": postEvent,
    "getUserEvents": getUserEvents
  }
}