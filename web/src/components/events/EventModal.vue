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


import { computed, ref, watch } from 'vue';

import ErrorMessage from '../base/FormFieldErrorMessage.vue';
import ButtonBase from '../base/ButtonBase.vue';

import { useToast } from 'src/composables/UseToast';
import { useDialog } from 'src/composables/UseDialog';
import { useAuthStore } from 'src/stores/auth';
import eventsService from 'src/services/events';


const { post: postEvent, patch: patchEvent, delete: deleteEvent } = eventsService()
const authStore = useAuthStore();
const { ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccess, positionToastError } = useToast();
const { confirmEditDialog, confirmDeleteEventDialog } = useDialog();


const nowDate = new Date();

const dateFormat = "##/##/####";
const timeFormat = "time";
const dateFormatRules = [v => /^-?[0-3]\d\/[0-1]\d\/[\d]+$/.test(v)];
const timeFormatRules = ['time'];

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
    updateNowDate();

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
                } else if(response.data.complete_period){
                    noStandardToastMixinInfo.text = response.data.complete_period[0];

                    ToastError.fire({
                        ...noStandardToastMixinInfo,
                        position: positionToastError.value
                    })
                } else{
                  console.log(response);
                  noStandardToastMixinInfo.text = "Não foi possível criar o evento! Entre em contato com o suporte ou tente novamente."

                  ToastError.fire({
                    ...noStandardToastMixinInfo,
                    position: positionToastError.value
                  })
                }
            }  else{
              console.log(response);
              noStandardToastMixinInfo.text = "Não foi possível criar o evento! Entre em contato com o suporte ou tente novamente."

              ToastError.fire({
                ...noStandardToastMixinInfo,
                position: positionToastError.value
              })
            }
        }

        isCreateEventRunning.value = false;
    }
}
async function editEvent(){
    if(enteredDescription.value && enteredStartDate.value && enteredStartTime.value && enteredEndDate.value && enteredEndTime.value){
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
                        if(response.data.start_period){
                            errorMessageStartPeriod.value = response.data.start_period[0]
                        } else if(response.data.end_period){
                            errorMessageEndPeriod.value = response.data.end_period[0]
                        }  else if(response.data.complete_period){
                            noStandardToastMixinInfo.text = response.data.complete_period[0];

                            ToastError.fire({
                                ...noStandardToastMixinInfo,
                                position: positionToastError.value
                            })
                        } else{
                          console.log(response);
                          noStandardToastMixinInfo.text = "Não foi possível criar o evento! Entre em contato com o suporte ou tente novamente."

                          ToastError.fire({
                            ...noStandardToastMixinInfo,
                            position: positionToastError.value
                          })
                        }
                    } else{
                      console.log(response);
                      noStandardToastMixinInfo.text = "Não foi possível criar o evento! Entre em contato com o suporte ou tente novamente."

                      ToastError.fire({
                        ...noStandardToastMixinInfo,
                        position: positionToastError.value
                      })
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
            noStandardToastMixinInfo.text = "Não foi possível remover este evento! Entre em contato com o suporte ou tente novamente."

            ToastError.fire({
              ...noStandardToastMixinInfo,
              position: positionToastError.value
            })
        }
    }

    isDeleteEventRunning.value = false;
}

function closeEventModal(){
    emit("closeEventModal");
}
function forceCalendarRerender(){
    emit("forceCalendarRerender");
}

function submitForm(){
    if(prop.action === 'add'){
        createEvent();
    } else if(prop.action === 'edit'){
        editEvent();
    }
}

function updateNowDate(){
  nowDate.value = new Date()
}

function updateStartDateConverted(){
  startDateConverted.value = enteredStartDate.value.split('/').reverse().join('/')
}
function updateEndDateConverted(){
  endDateConverted.value = enteredEndDate.value.split('/').reverse().join('/')
}


const modalTitle = computed(() =>  `${prop.action === 'add' ? 'Agendar' : 'Editar'}  Evento`)

const startPeriodClass = computed(() => ({
  invalidInput: errorMessageStartPeriod.value
}))
const endPeriodClass = computed(() => ({
  invalidInput: errorMessageEndPeriod.value
}))

const canChangeTheStartDate = computed(() => {
  return prop.action === 'edit' && nowDate.value < initialPeriod.value;
})
const isNowDateAfterTheInitialPeriod = computed(() => {
  return nowDate.value > initialPeriod.value;
})
const isNowDateAfterTheFinalPeriod = computed(() => {
  return nowDate.value > finalPeriod.value;
})

const isAddAction = computed(() => {
  return prop.action === 'add';
})
const arrayOfFieldsValue = computed(() => [ enteredStartTime.value, enteredEndDate.value, enteredEndTime.value, enteredDescription.value ])
const canItChangeAndRemoveTheEvent = computed(() => {
  return prop.action === 'edit' && nowDate.value < finalPeriod.value;
})
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
                <h1 class="title">{{ modalTitle }}</h1>
                <button class="close-modal" type="button" @click="closeEventModal"><span aria-hidden="true">&times;</span></button>
            </q-card-section>
            <q-card-section class="modal-body">
                <q-form
                    class="form-event"
                    method="post"
                    @submit.prevent="submitForm"
                >
                    <q-card-section class="form-body">
                        <q-card-section class="datetime-field flex column">
                            <section class="flex no-wrap">
                                <q-input
                                    label="Data Inicial:"
                                    name="start-date"
                                    id="start-date"
                                    :class="startPeriodClass"
                                    :disable="!canChangeTheStartDate"
                                    :readonly="!canChangeTheStartDate"
                                    :mask="dateFormat"
                                    :rules="dateFormatRules"
                                    @focus="removeErrorMessageStartPeriod"
                                    filled
                                    v-model="startDateConverted"
                                >
                                    <template v-slot:append v-if="canChangeTheStartDate">
                                        <q-icon name="event" class="cursor-pointer">
                                        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                            <q-date v-model="enteredStartDate" @update:model-value="updateStartDateConverted">
                                            <div class="row items-center justify-end">
                                                <q-btn v-close-popup label="Fechar" color="primary" flat />
                                            </div>
                                            </q-date>
                                        </q-popup-proxy>
                                        </q-icon>
                                    </template>
                                </q-input>
                                <q-input
                                    label="Hora inicial:"
                                    name="start-time"
                                    id="start-time"
                                    :class="startPeriodClass"
                                    :disable="isNowDateAfterTheInitialPeriod"
                                    :readonly="isNowDateAfterTheInitialPeriod"
                                    :mask="timeFormat"
                                    :rules="timeFormatRules"
                                    @focus="removeErrorMessageStartPeriod"
                                    filled
                                    v-model="enteredStartTime"
                                >
                                    <template v-slot:append v-if="!isNowDateAfterTheInitialPeriod">
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
                                    label="Data Final:"
                                    name="end-date"
                                    id="end-date"
                                    :class="endPeriodClass"
                                    :disable="isNowDateAfterTheFinalPeriod"
                                    :readonly="isNowDateAfterTheFinalPeriod"
                                    :mask="dateFormat"
                                    :rules="dateFormatRules"
                                    @focus="removeErrorMessageEndPeriod"
                                    filled
                                    v-model="endDateConverted"
                                >
                                    <template v-slot:append v-if="!isNowDateAfterTheFinalPeriod">
                                        <q-icon name="event" class="cursor-pointer">
                                        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                            <q-date v-model="enteredEndDate" @update:model-value="updateEndDateConverted">
                                            <div class="row items-center justify-end">
                                                <q-btn v-close-popup label="Fechar" color="primary" flat />
                                            </div>
                                            </q-date>
                                        </q-popup-proxy>
                                        </q-icon>
                                    </template>
                                </q-input>
                                <q-input
                                    label="Hora Final:"
                                    name="end-time"
                                    id="end-time"
                                    :class="endPeriodClass"
                                    :disable="isNowDateAfterTheFinalPeriod"
                                    :readonly="isNowDateAfterTheFinalPeriod"
                                    :mask="timeFormat"
                                    :rules="timeFormatRules"
                                    @focus="removeErrorMessageEndPeriod"
                                    filled
                                    v-model="enteredEndTime"
                                >
                                    <template v-slot:append v-if="!isNowDateAfterTheFinalPeriod">
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
                            :disable="isNowDateAfterTheFinalPeriod"
                            :readonly="isNowDateAfterTheFinalPeriod"
                        >

                        </q-input>
                    </q-card-section>
                    <q-card-section class="form-footer">
                        <ButtonBase
                          label="Agendar"
                          class="btn-primary"
                          type="submit"
                          :allFieldsValue="arrayOfFieldsValue"
                          :loading="isCreateEventRunning"
                          v-if="isAddAction"
                        >
                        </ButtonBase>

                        <ButtonBase
                          class="btn-primary"
                          type="submit"
                          :allFieldsValue="arrayOfFieldsValue"
                          :loading="isEditEventRunning"
                          v-if="canItChangeAndRemoveTheEvent"
                        >
                          <i class="bi bi-pencil"></i> <span>Editar</span>
                        </ButtonBase>

                        <ButtonBase
                          class="btn-danger"
                          type="button"
                          :loading="isDeleteEventRunning"
                          @click="removeEvent"
                          v-if="canItChangeAndRemoveTheEvent"
                        >
                          <i class="bi bi-trash3"></i> <span>Remover</span>
                        </ButtonBase>

                        <ButtonBase
                          label="Cancelar"
                          class="btn-secondary"
                          type="button"
                          @click="closeEventModal"
                        >
                        </ButtonBase>
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
