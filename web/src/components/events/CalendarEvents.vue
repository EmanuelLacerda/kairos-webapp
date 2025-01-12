<script setup>
import { reactive, ref } from 'vue';

import FullCalendarComponent from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

import dayjs from 'dayjs'

import EventModal from './EventModal.vue';

import eventsService from 'src/services/events';
import {useAuthStore} from 'src/stores/auth';
import { useDialog } from 'src/composables/UseDialog';

const { get: getEvent, getUserEvents } = eventsService();
const authStore = useAuthStore();
const {notificationErrorDialog} = useDialog();


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
    businessHours: {
        daysOfWeek: [ 0,1, 2, 3, 4,5,6 ],

        startTime: '00:00',
        endTime: '23:59',
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
            notificationErrorDialog.fire({
                text: "Você não pode agendar eventos para uma data anterior à hoje!"
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

        let clickedEventSelector = ""

        if(document.querySelector(".fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover")){
            clickedEventSelector = document.querySelector(".fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover");
        } else{
            clickedEventSelector = document.querySelector(".fc .fc-daygrid-event-harness:hover");
        }

        clickedEventSelector.style.cursor = 'wait';


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
        clickedEventSelector.style.cursor = 'pointer';
    }

})

const showModal = ref(false);
const startData = ref("")
const currentEventModalAction = ref("edit")


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
    .fc{
        font-family: "Montserrat", serif !important;

        .fc-toolbar.fc-header-toolbar{
            height: 97px;
            background-color: $custom-gray-2;
            color: $custom-full-white;
            padding: 0 27px;
            margin-bottom: 0;

            .fc-toolbar-chunk{
                .fc-button-group{
                    .fc-button-primary{
                        background-color: transparent;
                        border: 0px solid transparent;

                        height: 45px;

                        font-weight: 500;
                        color: $custom-full-white;
                    }
                    .fc-button-active{
                        background-color: $custom-full-white !important;
                        color: $custom-gray-2;
                    }
                }

                .fc-toolbar-title{
                    font-weight: 600;
                    
                }
                
                .fc-toolbar-title::first-letter{
                    text-transform: capitalize;
                }
            }
        }

        .fc-view-harness{
            border: 1px solid $custom-gray-3;
            border-top-width: 0px;

            .fc-view{
                padding: 40px 61px;
            }

            .fc-daygrid-day-bg .fc-non-business{
                background-color: $custom-full-white;
            }
            .fc-daygrid-day.fc-day-today{
                .fc-daygrid-day-top{
                    color: $custom-full-white;
                }

                .fc-non-business{
                    background: $custom-orange-2 !important;
                }
            }

            .fc-daygrid-day-number{
                font-weight: 500 !important;
            }

            .fc-daygrid-event-harness .fc-h-event{
                background-color: $custom-bg-owm-events;
                border: $custom-bg-owm-events;
            }

            .fc-daygrid-event-dot{
                border-color: $custom-bg-owm-events;
            }

            .fc-day-today .fc-daygrid-day-frame{
                background-color: $custom-orange-2;
            }
        }
    }

    .fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover{
        cursor: pointer;
    }
    .loading-events-indication{
        p{
            font-size: 2rem;
        }
    }
</style>