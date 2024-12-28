<script setup>
import { reactive, ref } from 'vue';

import FullCalendarComponent from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

import dayjs from 'dayjs'

const loadingFullCalendar = ref(false)
const viewType = ref("")

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
    events: [
        {
            id: 1,
            title: "Evento teste",
            start: '2024-12-26',
            end: '2024-12-28'
        }
    ],
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
    dateClick:handleDateClick

})

function handleDateClick(info){
    const infoData = info.date;

    console.log(infoData);
    console.log(dayjs());
}
</script>

<template>
    <section>
        <section v-if="loadingFullCalendar">
          <span>Carregando...</span>
        </section>
        <FullCalendarComponent :options="calendarOptions" />
      </section>
</template>