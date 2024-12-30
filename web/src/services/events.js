import useApi from 'src/composables/UseApi'

export default function eventsService () {
  const { postEvent } = useApi('/events/')

  return {
    "post": postEvent
  }
}