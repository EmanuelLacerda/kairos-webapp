<script setup>
import moment from 'moment';
import 'moment/locale/pt-br';
import dayjs from 'dayjs';

import FullCalendarComponent from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

import { reactive, ref } from 'vue';

import EventModal from './EventModal.vue';

import eventsService from 'src/services/events';
import {useAuthStore} from 'src/stores/auth';
import { useDialog } from 'src/composables/UseDialog';
import { useToast } from 'src/composables/UseToast';


const authStore = useAuthStore();
const { get: getEvent, getUserEvents } = eventsService();
const {notificationErrorDialog} = useDialog();
const { ToastError, noStandardToastMixinInfo, positionToastError } = useToast();

const months = {
  janeiro: 1,
  fevereiro: 2,
  março: 3,
  abril: 4,
  maio: 5,
  junho: 6,
  julho: 7,
  agosto: 8,
  setembro: 9,
  outubro: 10,
  novembro: 11,
  dezembro: 12
};

const eventId = ref("");
const eventData = reactive({});
const loadingFullCalendar = ref(false)
const viewType = ref("")
const calendarKey = ref(0);
const calendarOptions = reactive({
    plugins: [dayGridPlugin, interactionPlugin],
    initialView: viewType.value === '' ? "dayGridDay" : viewType.value ? viewType.value : "dayGridMonth",
    locale: "pt-br",
    weekNumberCalculation: 'ISO',
    dayMaxEvents: true,
    eventStartEditable: false,
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,dayGridWeek,dayGridDay'
    },
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

        noStandardToastMixinInfo.title = "Calendário"

        if(userId === null){
            failureCallback("Você precisa estar logado para os seus eventos serem carregados!"); //esta mensagem deve ser mostrada como um toast

            noStandardToastMixinInfo.text = "Você precisa estar logado para os seus eventos serem carregados!"

            ToastError.fire({
              ...noStandardToastMixinInfo,
              position: positionToastError.value
            })
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
    datesSet: function(dateInfo) {
        const view = dateInfo.view;
        viewType.value = view.type

        if(view.type === 'dayGridMonth'){
            Array.from(document.querySelectorAll('a.fc-daygrid-day-number')).map(element => {
              if(element.getAttribute("aria-label")){
                moment.locale('pt-br')

                const extendedData = element.getAttribute("aria-label").split(" de ");
                const dataString = `${extendedData[2]}-${months[extendedData[1]]}-${('0'+extendedData[0]).slice(-2)}`

                element.innerHTML = returnWeekdayAndDateForm(moment(dataString));
              }
            })
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
            Array.from(document.querySelectorAll('.fc-dayGridWeek-view .fc-daygrid-day')).map(element => {
              const child = element.getElementsByClassName("fc-daygrid-day-frame")[0];

              if(!Array.from(child.children).some(child2 => child2.getAttribute("class") === "fc-daygrid-day-number")){
                const span = document.createElement("span")

                span.setAttribute("class", "fc-daygrid-day-number")

                child.appendChild(span);
              }


              moment.locale('pt-br')

              const span = Array.from(child.children).find(child2 => child2.getAttribute("class") === "fc-daygrid-day-number");

              span.innerHTML = returnWeekdayAndDateForm(moment(element.getAttribute("data-date")));
            })
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
        } else if(view.type === 'dayGridDay') {
          Array.from(document.querySelectorAll('.fc-dayGridDay-view .fc-daygrid-day')).map(element => {
            const child = element.getElementsByClassName("fc-daygrid-day-frame")[0];

            if(!Array.from(child.children).some(child2 => child2.getAttribute("class") === "fc-daygrid-day-number")){
              const span = document.createElement("span")

              span.setAttribute("class", "fc-daygrid-day-number")

              child.appendChild(span);
            }


            moment.locale('pt-br')

            const span = Array.from(child.children).find(child2 => child2.getAttribute("class") === "fc-daygrid-day-number");

            span.innerHTML = returnWeekdayAndDateForm(moment(element.getAttribute("data-date")));
          })
        }
    },
    dayCellDidMount: function(arg) {
      const dayEl = arg.el;
      const date = arg.date;

      dayEl.addEventListener('click', function(event) {

        eventId.value = "";

        if(!event.target.closest('.fc-daygrid-day-events')){
          if(dayjs().isAfter(date,"day")){
            notificationErrorDialog.fire({
                text: "Você não pode agendar eventos para uma data anterior à hoje!"
            })
        } else{
            eventId.value = "";
            startData.value = dayjs(date.toDateString()).format('DD/MM/YYYY');
            currentEventModalAction.value = 'add';

            eventData.id = "";
            eventData.description = "";
            eventData.start = "";
            eventData.end = "";

            showModal.value = true;
        }
        }
      });
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


function closeEventModal(){
    showModal.value = false
}

function forceCalendarRerender() {
    calendarKey.value += 1;
}

function returnWeekdayAndDateForm(date) {
  const dayOfWeek = ['dom.', 'seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.'];

  return `${dayOfWeek[date.day()]} ${("0"+date.date()).slice(-2)}/${("0"+(date.month()+1)).slice(-2)}`;
}
</script>

<template>
    <section>
        <section v-if="loadingFullCalendar" class="flex column items-center justify-center loading-events-indication">
            <p>Carregando seus eventos</p>
            <q-spinner
                color="primary"
                size="3rem"
                :thickness="10"
            />
        </section>
        <FullCalendarComponent :options="calendarOptions" :key="calendarKey" style="margin-top: 30px;" />
        <EventModal :show-modal="showModal" :start-date="startData" :action="currentEventModalAction" :event-id="eventId" :event-data="eventData" @close-event-modal="closeEventModal" @force-calendar-rerender="forceCalendarRerender"></EventModal>
      </section>
</template>

<style lang="scss">
.fc{
    font-family: "Montserrat", serif !important;

    .fc-dayGridMonth-view{
      span.fc-daygrid-day-number{
        display: none;
      }
    }


    .fc-dayGridWeek-view, .fc-dayGridDay-view{
      .fc-daygrid-day{
        .fc-daygrid-day-frame{
          display: flex;
          justify-content: flex-end;
        }
      }
    }

    .fc-day-other{
      .fc-daygrid-day-top{
        opacity: 1;
      }
    }

    .fc-daygrid-body-balanced{
      .fc-daygrid-day-events{
        top: 20px;
      }
    }

    .fc-toolbar.fc-header-toolbar{
      flex-direction: column-reverse;
      height: 20vh;
      justify-content: center;

      .fc-toolbar-chunk{
        .fc-button-group{
          gap: 15px;

          button{
            font-size: 1.2rem;
          }
        }

        button.fc-today-button{
          font-size: 1.2rem !important;
        }

        .fc-toolbar-title{
          font-size: 1.4rem;
        }
      }
    }


    .fc-view-harness{
      .fc-dayGridDay-view{
        .fc-scrollgrid{
          thead[role="rowgroup"]{
            display: none;
          }

          tbody[role="rowgroup"]{
            tr[role="presentation"]{
              td[role="presentation"]{
                height: 80vh;

                .fc-daygrid-day-frame{
                  height: 80vh;
                }
              }
            }
          }
        }
      }

      .fc-scrollgrid{
        thead[role="rowgroup"]{
          display: none;
        }

        tbody[role="rowgroup"]{
          tr[role="presentation"]{
            td[role="presentation"]{
              height: 80vh;

              .fc-daygrid-event-harness{
                .fc-event{
                  margin-right: 70%;
                }
              }
            }
          }
        }
      }
    }

    .fc-toolbar.fc-header-toolbar{
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


        tbody[role="presentation"]{
          display: flex;
          flex-direction: column;

          tr[role="row"]{
            display: flex;
            flex-wrap: wrap;
            flex-direction: column;

            .fc-daygrid-day-frame {
              width: 100%;
              height: 100px;
            }

            .fc-daygrid-day-number{
              font-size: 1.875rem;
            }
          }
        }
    }
}

.fc .fc-daygrid-body-balanced .fc-daygrid-day-events:hover{
    cursor: pointer;
}

.loading-events-indication{
    p{
        font-size: 1.5rem;
    }
}

@media (min-width: 360px) {
  .fc{
    .fc-toolbar.fc-header-toolbar{
      height: 28vh;
    }
  }
}

@media (min-width: 390px) {
  .fc{
    .fc-toolbar.fc-header-toolbar{
      height: 22vh;
    }
  }
}

@media (min-width: 768px) {
  .fc {
    .fc-toolbar.fc-header-toolbar{
      flex-direction: row;
      height: 97px;
      justify-content: space-between;

      .fc-toolbar-chunk{
        button.fc-today-button{
          font-size: 1rem !important;
        }
      }
    }

    .fc-view-harness{
      .fc-view{
          padding: 40px 61px;
      }

      .fc-scrollgrid{
        tbody[role=rowgroup]{
          tr[role=presentation]{
            td[role=presentation]{
              .fc-daygrid-event-harness{
                .fc-event{
                  margin-right: 0px;
                }
              }
            }
          }
        }
      }

      /*
      .fc .fc-view-harness .fc-scrollgrid tbody[role=rowgroup] tr[role=presentation] td[role=presentation] .fc-daygrid-event-harness .fc-event
    Specificity: (0,8,3)
    {
        // margin-right: 70%;
    }
      */

      tbody[role="presentation"]{
        display: table-row-group;

        tr[role="row"]{
          display: table-row;

          .fc-daygrid-day-number{
            font-size: 1em;
          }
        }
      }

      .fc-dayGridDay-view{
        .fc-scrollgrid{
          tbody[role=rowgroup]{
            tr[role=presentation]{
              td[role="presentation"]{
                height: 100px;

                .fc-daygrid-day-frame{
                  height: 100px;
                }
              }
            }
          }
        }
      }

      .fc-scrollgrid{
        tbody[role="rowgroup"]{
          tr[role="presentation"]{
            td[role="presentation"]{
              height: 100px;
            }
          }
        }
      }

    }
  }
}
</style>
