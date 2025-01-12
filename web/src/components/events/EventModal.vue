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

import { useToast } from 'src/composables/UseToast';
import { useDialog } from 'src/composables/UseDialog';

const authStore = useAuthStore();

const { ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccess, positionToastError } = useToast();
const { confirmEditDialog, confirmDeleteEventDialog } = useDialog();

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
const isDeleteEventRunning = ref(false);

const errorMessageStartPeriod = ref('');
const errorMessageEndPeriod = ref('');


watch(() => prop.startDate, (newStartDate) => {
    if(newStartDate){
        startDateConverted.value = newStartDate;
        enteredStartDate.value = newStartDate.split('/').reverse().join('/');
    }
})
watch(() => prop.showModal, () => {
    eventID.value = prop.eventData.id;

    errorMessageEndPeriod.value = "";
    errorMessageStartPeriod.value = "";

    if(prop.eventData.id){
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

        enteredStartTime.value = "";
        initialPeriod.value = new Date("");

        endDateConverted.value = "";
        enteredEndDate.value = "";
        enteredEndTime.value = "";
        finalPeriod.value = new Date("");
    }
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

        noStandardToastMixinInfo.title = "Criação de evento";

        if(userID === null){
            noStandardToastMixinInfo.text = "Você precisar estar logado para agendar um evento!";

            ToastError.fire({    
                ...noStandardToastMixinInfo,
                position: positionToastError.value
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

                noStandardToastMixinInfo.text = "Evento criado com sucesso!"

                ToastSuccess.fire({
                    ...noStandardToastMixinInfo,
                    position: positionToastSuccess.value
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

        noStandardToastMixinInfo.title = "Edição de evento";

        if(userID === null){
            noStandardToastMixinInfo.text = "Você precisar estar logado para editar um evento!";

            ToastError.fire({
                ...noStandardToastMixinInfo,
                position: positionToastError.value
            })
        } else{
            if(!eventID.value){
                noStandardToastMixinInfo.text = "As alterações deste evento não podem ser salvas porque não foi possível obter o id deste evento! Entre em contato como o suporte."

                ToastError.fire({
                    ...noStandardToastMixinInfo,
                    position: positionToastError.value
                })
            } else{
                const result = await confirmEditDialog.fire({
                    text: `Seu evento ficará de ${enteredStartTime.value} do dia ${startDateConverted.value} até ${enteredEndTime.value} do dia ${endDateConverted.value}`
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

                        noStandardToastMixinInfo.text = "Evento editado com sucesso!";

                        ToastSuccess.fire({
                            ...noStandardToastMixinInfo,
                            position: positionToastSuccess.value
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
    isDeleteEventRunning.value = true;

    noStandardToastMixinInfo.title = "Remoção de evento";

    const result = await confirmDeleteEventDialog.fire({})
    
    if (result.isConfirmed) {
        const response = await deleteEvent(eventID.value);

        if(response.statusText === "No Content"){
            closeEventModal();

            noStandardToastMixinInfo.text = "Evento removido com sucesso!";

            ToastSuccess.fire({
                ...noStandardToastMixinInfo,
                position: positionToastSuccess.value
            });
            
            forceCalendarRerender();
        } else if(response.statusText === "Not Found") {
            noStandardToastMixinInfo.text = "Não foi possível encontrar este evento! Entre em contato com o suporte..."

            ToastError.fire({
                ...noStandardToastMixinInfo,
                position: positionToastError.value
            })
        } else if(response.statusText === "Bad Request" && response.data.message){
            noStandardToastMixinInfo.text = response.data.message;

            ToastError.fire({
                ...noStandardToastMixinInfo,
                position: positionToastError.value
            })
        }else{
            console.log(response);
        }
    }

    isDeleteEventRunning.value = false;
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
        class="event-modal"
    >
        <q-card>
            <q-card-section class="flex justify-between items-center modal-header">
                <h1 class="title">{{ action === 'add' ? 'Agendar' : 'Editar' }} Evento</h1>
                <button class="close-modal" type="button" @click="closeEventModal"><span aria-hidden="true">&times;</span></button>
            </q-card-section>
            <q-card-section class="modal-body">
                <q-form
                    class="form-event"
                    method="post"
                    @submit.prevent="handleSubmit"
                >
                    <q-card-section class="form-body">
                        <q-card-section class="datetime-field flex column">
                            <section class="flex no-wrap">
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
                            </section>
                            <ErrorMessage :error-message="errorMessageStartPeriod"></ErrorMessage>
                        </q-card-section>

                        <q-card-section class="datetime-field flex column">
                            <section class="flex no-wrap">
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
                            </section>
                            <ErrorMessage :error-message="errorMessageEndPeriod"></ErrorMessage>
                        </q-card-section>

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
                    </q-card-section>
                    <q-card-section class="form-footer">
                        <q-btn
                            label="Agendar"
                            type="submit"
                            :disable="!enteredDescription || !enteredStartTime || !enteredEndDate || !enteredEndTime"
                            :loading="isCreateEventRunning"
                            v-if="action === 'add'"
                            class="btn-primary"
                        >

                        </q-btn>
                        <q-btn
                            type="submit"
                            :disable="!enteredDescription || !enteredStartTime || !enteredEndDate || !enteredEndTime"
                            :loading="isEditEventRunning"
                            v-if="action === 'edit' && new Date() < finalPeriod"
                            class="btn-primary"
                        >
                            <i class="bi bi-pencil"></i> <span>Editar</span>
                        </q-btn>
                        <q-btn
                            type="button"
                            @click="removeEvent"
                            v-if="action === 'edit' && new Date() < finalPeriod" :loading="isDeleteEventRunning" 
                            class="btn-danger"
                        >
                            <i class="bi bi-trash3"></i> <span>Remover</span>
                        </q-btn>
                        <q-btn
                            label="Cancelar"
                            type="button"
                            @click="closeEventModal"
                            class="btn-secondary"
                        >

                        </q-btn>
                    </q-card-section>
                </q-form>
            </q-card-section>
        </q-card>
    </q-dialog>
</template>

<style lang="scss">
    .event-modal.q-dialog{
        .q-card{
            width: 100%;
            background-color: rgba(44,62,80,0.7);

            .q-card__section{
                gap: 16px;                
            }

            .modal-header{
                margin: 0 32px;
                padding: 0;

                h1{
                    font-size: 1.8rem;
                    color: $custom-full-white;
                    font-weight: 400;
                }

                .close-modal{
                    background: transparent;
                    color: $custom-full-white;
                    font-size: 2.8rem;
                    border: none;
                    margin: 0;
                }
            }

            .modal-body{
                padding: 0 16px;

                .form-event{
                    .q-card__section{
                        padding: 0 16px;
                    }

                    .form-body{
                        .q-field__inner{
                            .q-field__control-container{
                                background-color: $custom-full-white;
    
                                input,textarea{
                                    background-color: $custom-full-white;
                                } 
                            }
                            .q-field__append{
                                background-color: $custom-full-white;
                                color: $custom-full-black;
                            }
                            .q-field__control{
                                background-color: $custom-full-white;
                            }
                        }
    
                        .datetime-field{
                            padding: 0;
                            gap: 0;
    
                            label{
                                width: 50%;
                                padding-bottom: 0;
                            }
                            label:first-child{
                                margin-right: 16px;
                            }
                        }
                    }

                    .form-footer{
                        display: flex;
                        justify-content: center;
                        padding: 40px 16px 0;
                        margin-bottom: 40px;

                        .q-btn{
                            .q-btn__content{
                                font-weight: 600;
                                font-size: 16px;

                                display: flex;
                                flex-direction: row;
                                gap: 8px;
                                justify-content: center;
                                align-items: center;
                        }
                        }
                    }
                }
            }
        }
    }
</style>