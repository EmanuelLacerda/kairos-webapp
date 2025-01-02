<script setup>
import { reactive, ref } from 'vue';

import FullCalendarComponent from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

import Swal from 'sweetalert2'

import dayjs from 'dayjs'

import EventModal from './EventModal.vue';

import eventsService from 'src/services/events';
import {useAuthStore} from 'src/stores/auth';

const { get: getEvent, getUserEvents } = eventsService();
const authStore = useAuthStore();


const eventId = ref("");
const eventData = reactive({});
const loadingFullCalendar = ref(false)
const viewType = ref("")
const calendarKey = ref(0);
const calendarOptions = reactive({
    plugins: [dayGridPlugin, interactionPlugin],
    initialView: viewType.value === '' ? "dayGridDay" : viewType.value ? viewType.value : "dayGridMonth",
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,dayGridWeek,dayGridDay'
    },
    locale: "pt-br",
    weekNumberCalculation: 'ISO',
    buttonText: {
        today: 'Hoje',
        month: 'Mês',
        week: 'Semana',
        day: 'Dia',
    },
    events: async function(info, successCallback, failureCallback) {
        loadingFullCalendar.value = true;

        const start = info.startStr;
        const end = info.endStr;

        const userId = await authStore.getUserId();

        if(userId === null){
            failureCallback("Você precisa estar logado para os seus eventos serem carregados!"); //esta mensagem deve ser mostrada como um toast
        } else{
            const response = await getUserEvents(userId, start, end)

            let events = [];

            if(response.statusText === "OK"){
                events = response.data.map(event => {
                    return {
                        id: event.id,
                        title: event.description,
                        start: event.start.replace("Z",""),
                        end: event.end.replace("Z","")
                    }
                });
            } else if(response.statusText != 'Not Found'){
                console.log(response);
            }

            loadingFullCalendar.value = false;

            successCallback(events);
        }
    },
    dayMaxEvents: true,
    eventStartEditable: false,
    datesSet: function(dateInfo) {
        const view = dateInfo.view;
        viewType.value = view.type
        
        if(view.type === 'dayGridMonth'){
            Array.from(document.querySelectorAll('.fc-daygrid-day-bg')).map(element => {
                const div1 = document.createElement('div')
                div1.className = 'fc-daygrid-bg-harness';
                div1.style.left = '0px';
                div1.style.right = '0px';

                const div2 = document.createElement('div')
                div2.className = 'fc-non-business';

                div1.appendChild(div2);
                element.appendChild(div1);
            })
        } else if(view.type === 'dayGridWeek'){
            Array.from(document.querySelectorAll('.fc-timegrid-col-bg')).map(element => {
                const div1 = document.createElement('div')
                div1.className = 'fc-timegrid-bg-harness';
                div1.style.top = '0px';
                div1.style.bottom = '-648px';

                const div2 = document.createElement('div')
                div2.className = 'fc-non-business';

                div1.appendChild(div2);
                element.appendChild(div1);
            })
        }
    },
    dateClick(info){
        const infoData = info.date;
        eventId.value = "";

        if(dayjs().isAfter(infoData,"day")){
            notificationError.fire({
                text: "Você não pode agendar eventos para uma data anterior à hoje."
            })
        } else{
            eventId.value = "";
            startData.value = dayjs(infoData.toDateString()).format('DD/MM/YYYY');
            currentEventModalAction.value = 'add';
            
            eventData.id = "";
            eventData.description = "";
            eventData.start = "";
            eventData.end = "";

            showModal.value = true;
        }
    },
    eventClick: async function(info){
        document.body.style.cursor = 'wait';
        document.querySelector(".fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover").style.cursor = 'wait';

        eventId.value = info.event.id;
        startData.value = "";
        currentEventModalAction.value = 'edit';

        const response = await getEvent(eventId.value);

        if(response.statusText === "OK"){
            eventData.id = response.data.id;
            eventData.description = response.data.description;
            eventData.start = response.data.start.replace("Z","");
            eventData.end = response.data.end.replace("Z","");
        } else{
            eventData.id = "";
            eventData.description = "";
            eventData.start = "";
            eventData.end = "";
        }

        showModal.value = true;

        document.body.style.cursor = 'default';
        document.querySelector(".fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover").style.cursor = 'pointer';
    }

})

const showModal = ref(false);
const startData = ref("")
const currentEventModalAction = ref("edit")


const notificationError = Swal.mixin({
    icon: "error",
    showCancelButton: false,
    confirmButtonColor: "#2148C0",
    confirmButtonText: "OK",
    animation: true
});


const closeEventModal = ()=>{
    showModal.value = false
}

const forceCalendarRerender = () => {
    calendarKey.value += 1;
}
</script>

<template>
    <section>
        <section v-if="loadingFullCalendar" class="flex column items-center justify-center loading-events-indication">
            <p>Carregando seus eventos</p>
            <q-spinner
                color="primary"
                size="6em"
                :thickness="10"
            />
        </section>
        <FullCalendarComponent :options="calendarOptions" :key="calendarKey" />
        <EventModal :show-modal="showModal" :start-date="startData" :action="currentEventModalAction" :event-id="eventId" :event-data="eventData" @close-event-modal="closeEventModal" @force-calendar-rerender="forceCalendarRerender"></EventModal>
      </section>
</template>

<style lang="scss">
    .fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover{
        cursor: pointer;
    }
    .loading-events-indication{
        p{
            font-size: 2rem;
        }
    }
</style>