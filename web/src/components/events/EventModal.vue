<script setup>
defineOptions({
  name: 'EventModal'
})

const prop = defineProps({
    showModal: {
        type: Boolean,
        required: true
    },
    startDate: {
        type: String,
        required: true
    },
    action: {
        type: String,
        required: true,
        validator(value){
            return ["add", "edit"].includes(value);
        }

    },
    eventId: {
        type: String,
        required: true
    },
    eventData: {
        type: Object,
        required: true
    }
})
const emit = defineEmits([
    'closeEventModal',
    'forceCalendarRerender'
])


import { ref, watch } from 'vue';

import { useAuthStore } from 'src/stores/auth';
import eventsService from 'src/services/events';

const { post: postEvent, patch: patchEvent, delete: deleteEvent } = eventsService()

import Swal from 'sweetalert2'

const authStore = useAuthStore();

import ErrorMessage from '../base/FormFieldErrorMessage.vue';


const enteredDescription = ref("");

const startDateConverted = ref("");
const enteredStartDate = ref("");
const enteredStartTime = ref("");
const initialPeriod = ref(new Date(prop.eventData.start))

const endDateConverted = ref("");
const enteredEndDate = ref("");
const enteredEndTime = ref("");
const finalPeriod = ref(new Date(prop.eventData.end))

const eventID = ref("");

const isCreateEventRunning = ref(false);
const isEditEventRunning = ref(false);

const errorMessageStartPeriod = ref('');
const errorMessageEndPeriod = ref('');


watch(() => prop.startDate, (newStartDate) => {
    if(newStartDate){
        startDateConverted.value = newStartDate;
        enteredStartDate.value = newStartDate.split('/').reverse().join('/');
    }
})
watch(() => prop.eventData.id, (newEventID) => {
    eventID.value = newEventID;

    if(newEventID){
        let [ start_date, start_time ] = prop.eventData.start.split("T");
        start_date = start_date.replaceAll("-","/")
        start_time = start_time.slice(0,5);

        let [ end_date, end_time ] = prop.eventData.end.split("T");
        end_date = end_date.replaceAll("-","/")
        end_time = end_time.slice(0,5).replaceAll("-","/");

        enteredDescription.value = prop.eventData.description;

        startDateConverted.value = start_date.split('/').reverse().join('/');
        enteredStartDate.value = start_date;
        enteredStartTime.value = start_time;
        initialPeriod.value = new Date(prop.eventData.start);

        endDateConverted.value = end_date.split('/').reverse().join('/');
        enteredEndDate.value = end_date;
        enteredEndTime.value = end_time;
        finalPeriod.value = new Date(prop.eventData.end);
    } else{
        enteredDescription.value = "";

        endDateConverted.value = "";
        enteredEndDate.value = "";
        enteredEndTime.value = "";

        initialPeriod.value = new Date("");
        finalPeriod.value = new Date("");
    }
})


const ToastBaseMixin = Swal.mixin({
  toast: true,
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.onmouseenter = Swal.stopTimer;
    toast.onmouseleave = Swal.resumeTimer;
  }
});

const ToastSuccess = ToastBaseMixin.mixin({
    icon: "success"
})
const ToastError = ToastBaseMixin.mixin({
    icon: "error"
})


function closeEventModal(){
    emit("closeEventModal");
}
function forceCalendarRerender(){
    emit("forceCalendarRerender");
}

const removeErrorMessageStartPeriod = () => {
    errorMessageStartPeriod.value = "";
}
const removeErrorMessageEndPeriod = () => {
    errorMessageEndPeriod.value = "";
}

async function createEvent(){
    if(enteredDescription.value && enteredStartDate.value && enteredStartTime.value && enteredEndDate.value && enteredEndTime.value){
        isCreateEventRunning.value = true;

        const userID = await authStore.getUserId();

        if(userID === null){
            ToastError.fire({
                title: "Usuário não autenticado",
                text: "Você precisar estar logado para agendar um evento!",
                width: 600,
                position: "center-right"
            })
        } else{
            const eventData = {
                'creator': userID,
                'description': enteredDescription.value,
                'start': `${enteredStartDate.value.replaceAll("/","-")}T${enteredStartTime.value}:00Z`,
                'end': `${enteredEndDate.value.replaceAll("/","-")}T${enteredEndTime.value}:00Z`
            }

            const response = await postEvent(eventData)

            if(response.statusText === 'Created'){
                closeEventModal();
                ToastSuccess.fire({
                    title: "Criação de evento",
                    text: "Evento criado com sucesso!",
                    position: "bottom-center"
                });
                forceCalendarRerender();
            } else if(response.statusText === 'Bad Request'){
                if(response.data.start_period){
                    errorMessageStartPeriod.value = response.data.start_period[0]
                } else if(response.data.end_period){
                    errorMessageEndPeriod.value = response.data.end_period[0]
                }
            }
        }

        isCreateEventRunning.value = false;
    }
}
async function editEvent(){
    if(enteredDescription.value && enteredStartTime.value && enteredEndDate.value && enteredEndTime.value){
        isEditEventRunning.value = true;

        const userID = await authStore.getUserId();

        if(userID === null){
            ToastError.fire({
                title: "Edição do evento",
                text: "Você precisar estar logado para editar um evento!",
                width: 600,
                position: "center-right"
            })
        } else{
            if(!eventID.value){
                ToastError.fire({
                    title: "Edição do evento",
                    text: "As alterações deste evento não podem ser salvas porque não foi possível obter o id deste evento! Entre em contato como o suporte.",
                    width: 600,
                    position: "center-right"
                })
            } else{
                const result = await Swal.fire({
                    title: "Edição do evento",
                    text: `Deseja realmente que seu evento fique de ${enteredStartTime.value} do dia ${startDateConverted.value} até ${enteredEndTime.value} do dia ${endDateConverted.value}?`,
                    icon: "info",
                    showCancelButton: true,
                    confirmButtonColor: "#2148C0",
                    cancelButtonColor: "rgb(221, 92, 92)",
                    cancelButtonText: 'Não',
                    confirmButtonText: "Sim",
                    customClass: {confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
                })

                if (result.isConfirmed) {
                    const eventData = {
                        'creator': userID,
                        'description': enteredDescription.value,
                        'start': `${enteredStartDate.value.replaceAll("/","-")}T${enteredStartTime.value}:00Z`,
                        'end': `${enteredEndDate.value.replaceAll("/","-")}T${enteredEndTime.value}:00Z`
                    }

                    const response = await patchEvent(eventID.value, eventData);

                    if(response.statusText === "OK"){
                        closeEventModal();
                        ToastSuccess.fire({
                            title: "Edição de evento",
                            text: "Evento editado com sucesso!",
                            position: "bottom-center"
                        });
                        forceCalendarRerender();
                    } else if(response.statusText === 'Bad Request'){
                        console.log(response.data);
                        if(response.data.start_period){
                            errorMessageStartPeriod.value = response.data.start_period[0]
                        } else if(response.data.end_period){
                            errorMessageEndPeriod.value = response.data.end_period[0]
                        }
                    }
                }
            }
        }

        isEditEventRunning.value = false;
    }
}
async function removeEvent(){
    const result = await Swal.fire({
        title: "Remoção de eventos",
        text: "Deseja realmente remover esse evento?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#2148C0",
        cancelButtonColor: "rgb(221, 92, 92)",
        cancelButtonText: 'Não',
        confirmButtonText: "Sim",
        customClass: {confirmButton: 'swal2-confirm-custom', cancelButton: 'swal2-cancel-custom'},
    })
    
    if (result.isConfirmed) {
        const response = await deleteEvent(eventID.value);

        if(response.statusText === "No Content"){
            closeEventModal();
            ToastSuccess.fire({
                title: "Remoção de evento",
                text: "Evento removido com sucesso!",
                position: "bottom-center"
            });
            forceCalendarRerender();
        } else{
            console.log(response);
        }
    }
}

function handleSubmit(){
    if(prop.action === 'add'){
        createEvent();
    } else if(prop.action === 'edit'){
        editEvent();
    }
}
</script>

<template>
    <q-dialog
        :model-value="showModal"
        @update:model-value="closeEventModal"
        :no-shake="true"
    >
        <q-card>
            <q-card-section class="flex justify-center items-center">
                <h1 class="title">AGENDAMENTO</h1>
                <button class="close-modal" type="button" @click="closeEventModal"><span aria-hidden="true">&times;</span></button>
            </q-card-section>
            <q-card-section>
                <q-icon v-if="action === 'edit'" class="bi bi-trash3-fill" @click="removeEvent"></q-icon>
                <q-form
                    class="form-event"
                    method="post"
                    @submit.prevent="handleSubmit"
                >
                    <q-card-section class="form-body">
                        <q-input
                            type="textarea"
                            name="description"
                            id="description"
                            label="Descrição:"
                            v-model="enteredDescription"
                            :outlined="true"
                            :disable="new Date() > finalPeriod"
                            :readonly="new Date() > finalPeriod"
                        >
            
                        </q-input>
                        <q-input
                            name="start-date"
                            id="start-date"
                            filled
                            label="Data Inicial:"
                            v-model="startDateConverted"
                            mask="##/##/####"
                            :rules="[v => /^-?[0-3]\d\/[0-1]\d\/[\d]+$/.test(v)]"
                            :class="{invalidInput: errorMessageStartPeriod && action === 'edit'}"
                            @focus="removeErrorMessageStartPeriod"
                            :disable="action === 'add' || new Date() > initialPeriod"
                            :readonly="action === 'add' || new Date() > initialPeriod"
                        >
                            <template v-slot:append v-if="action === 'edit' && new Date() < initialPeriod">
                                <q-icon name="event" class="cursor-pointer">
                                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                    <q-date v-model="enteredStartDate" @update:model-value="startDateConverted = enteredStartDate.split('/').reverse().join('/')">
                                    <div class="row items-center justify-end">
                                        <q-btn v-close-popup label="Fechar" color="primary" flat />
                                    </div>
                                    </q-date>
                                </q-popup-proxy>
                                </q-icon>
                            </template>
                        </q-input>
                        <q-input
                            filled
                            v-model="enteredStartTime"
                            mask="time"
                            :rules="['time']"
                            label="Hora inicial:"
                            :class="{invalidInput: errorMessageStartPeriod}"
                            @focus="removeErrorMessageStartPeriod"
                            :disable="new Date() > initialPeriod"
                            :readonly="new Date() > initialPeriod"
                        >
                            <template v-slot:append v-if="action === 'add' || new Date() < initialPeriod">
                            <q-icon name="access_time" class="cursor-pointer">
                                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                <q-time v-model="enteredStartTime">
                                    <div class="row items-center justify-end">
                                    <q-btn v-close-popup label="Fechar" color="primary" flat />
                                    </div>
                                </q-time>
                                </q-popup-proxy>
                            </q-icon>
                            </template>
                        </q-input>
                        <ErrorMessage :error-message="errorMessageStartPeriod"></ErrorMessage>
                        <q-input
                            name="start-date"
                            id="start-date"
                            filled
                            v-model="endDateConverted"
                            mask="##/##/####"
                            :rules="[v => /^-?[0-3]\d\/[0-1]\d\/[\d]+$/.test(v)]"
                            label="Data Final:"
                            :class="{invalidInput: errorMessageEndPeriod}"
                            @focus="removeErrorMessageEndPeriod"
                            :disable="new Date() > finalPeriod"
                            :readonly="new Date() > finalPeriod"
                        >
                            <template v-slot:append v-if="action === 'add' || new Date() < finalPeriod">
                                <q-icon name="event" class="cursor-pointer">
                                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                    <q-date v-model="enteredEndDate" @update:model-value="endDateConverted = enteredEndDate.split('/').reverse().join('/')">
                                    <div class="row items-center justify-end">
                                        <q-btn v-close-popup label="Fechar" color="primary" flat />
                                    </div>
                                    </q-date>
                                </q-popup-proxy>
                                </q-icon>
                            </template>
                        </q-input>
                        <q-input
                            filled
                            v-model="enteredEndTime"
                            mask="time"
                            :rules="['time']"
                            label="Hora Final:"
                            :class="{invalidInput: errorMessageEndPeriod}"
                            @focus="removeErrorMessageEndPeriod"
                            :disable="new Date() > finalPeriod"
                            :readonly="new Date() > finalPeriod"
                        >
                            <template v-slot:append v-if="action === 'add' || new Date() < finalPeriod">
                            <q-icon name="access_time" class="cursor-pointer">
                                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                <q-time v-model="enteredEndTime">
                                    <div class="row items-center justify-end">
                                    <q-btn v-close-popup label="Fechar" color="primary" flat />
                                    </div>
                                </q-time>
                                </q-popup-proxy>
                            </q-icon>
                            </template>
                        </q-input>
                        <ErrorMessage :error-message="errorMessageEndPeriod"></ErrorMessage>
                    </q-card-section>
                    <q-card-section class="form-footer">
                        <q-btn
                            label="Agendar"
                            type="submit"
                            :disable="!enteredDescription || !enteredStartTime || !enteredEndDate || !enteredEndTime"
                            :loading="isCreateEventRunning"
                            v-if="action === 'add'"
                        >

                        </q-btn>
                        <q-btn
                            label="Editar"
                            type="submit"
                            :disable="!enteredDescription || !enteredStartTime || !enteredEndDate || !enteredEndTime"
                            :loading="isEditEventRunning"
                            v-if="action === 'edit' && new Date() < finalPeriod"
                        >

                        </q-btn>
                        <q-btn
                            label="Cancelar"
                            type="button"
                            @click="closeEventModal"
                        >

                        </q-btn>
                    </q-card-section>
                </q-form>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>

<style lang="scss">
    .q-dialog{
        .q-card{
            width: 100%;

            .q-card__section{
                gap: 16px;

                h1{
                    font-size: 3rem;
                }
            }
        }
    }
</style>