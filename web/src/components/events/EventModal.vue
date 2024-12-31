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

    }
})
const emit = defineEmits([
    'closeEventModal'
])


import { ref, watch } from 'vue';

import { useAuthStore } from 'src/stores/auth';
import eventsService from 'src/services/events';

const { post: postEvent } = eventsService()

import Swal from 'sweetalert2'

const authStore = useAuthStore();

import ErrorMessage from '../base/FormFieldErrorMessage.vue';


const enteredDescription = ref("");

const definedStartDate = ref("");
const enteredStartTime = ref("");
const endDateConverted = ref("");
const enteredEndDate = ref("");
const enteredEndTime = ref("");

const isCreateEventRunning = ref(false);

const errorMessageStartPeriod = ref('');
const errorMessageEndPeriod = ref('');

const removeErrorMessageStartPeriod = () => {
    errorMessageStartPeriod.value = "";
}

const removeErrorMessageEndPeriod = () => {
    errorMessageEndPeriod.value = "";
}


watch(() => prop.startDate, (newStartDate) => {
    definedStartDate.value = newStartDate;
})
watch(() => prop.showModal, (newShowModal) => {
    if(!newShowModal){
        enteredDescription.value = "";
        enteredStartTime.value = "";
        endDateConverted.value = "";
        enteredEndDate.value = "";
        enteredEndTime.value = "";
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

async function createEvent(){
    if(enteredDescription.value && definedStartDate.value && enteredStartTime.value && enteredEndDate.value && enteredEndTime.value){
        isCreateEventRunning.value = true;

        const userID = await authStore.getUserId();

        if(userID === null){
            ToastError.fire({
                title: "Você precisar estar logado para agendar um evento!",
                width: 600,
                position: "center-right"
            })
        } else{
            const formattedStartDate = definedStartDate.value.split('/').reverse().join('-');

            const eventData = {
                'creator': userID,
                'description': enteredDescription.value,
                'start': `${formattedStartDate}T${enteredStartTime.value}:00Z`,
                'end': `${enteredEndDate.value.replaceAll("/","-")}T${enteredEndTime.value}:00Z`
            }

            const response = await postEvent(eventData)

            if(response.statusText === 'Created'){
                closeEventModal();
                ToastSuccess.fire({
                    title: "Evento criado com sucesso!",
                    position: "bottom-center"
                });
            } else if(response.statusText === 'Bad Request'){
                if(response.data.start_period){
                    errorMessageStartPeriod.value = response.data.start_period[0]
                } else if(response.data.end_period){
                    errorMessageEndPeriod.value = response.data.end_period[0]
                }
            }

            isCreateEventRunning.value = false;
        }
    }
}

function handleSubmit(){
    if(prop.action === 'add'){
        createEvent();
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
                <q-icon v-if="action === 'edit'" class="bi bi-trash3-fill"></q-icon>
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
                        >
            
                        </q-input>
                        <q-input
                            name="start-date"
                            id="start-date"
                            filled
                            type="text"
                            label="Data inicial:"
                            v-model="definedStartDate"
                            :disable="true"
                            :readonly="true"
                            :class="{invalidInput: errorMessageStartPeriod}"
                            @focus="removeErrorMessageStartPeriod"
                        >
                        </q-input>
                        <q-input
                            filled
                            v-model="enteredStartTime"
                            mask="time"
                            :rules="['time']"
                            label="Hora inicial:"
                            :class="{invalidInput: errorMessageStartPeriod}"
                            @focus="removeErrorMessageStartPeriod"
                        >
                            <template v-slot:append>
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
                        >
                            <template v-slot:append>
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
                        >
                            <template v-slot:append>
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
                            v-if="action === 'edit'"
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