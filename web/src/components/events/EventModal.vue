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


const enteredDescription = ref("");

const definedStartDate = ref("");
const enteredStartTime = ref("");
const endDateConverted = ref("");
const enteredEndDate = ref("");
const enteredEndTime = ref("");


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


function closeEventModal(){
    emit("closeEventModal");
}

function handleSubmit(){
    console.log("submit");
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
                    @submit.prevent="console.log('submit')"
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
                        >
                        </q-input>
                        <q-input
                            filled
                            v-model="enteredStartTime"
                            mask="time"
                            :rules="['time']"
                            label="Hora inicial:"
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
                        <q-input
                            name="start-date"
                            id="start-date"
                            filled
                            v-model="endDateConverted"
                            mask="##/##/####"
                            :rules="[v => /^-?[0-3]\d\/[0-1]\d\/[\d]+$/.test(v)]"
                            label="Data Final:"
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
                    </q-card-section>
                    <q-card-section class="form-footer">
                        <q-btn
                            label="Agendar"
                            type="submit"
                            :disable="!enteredDescription || !enteredStartTime || !enteredEndDate || !enteredEndTime"
                            @submit.prevent="handleSubmit"
                            v-if="action === 'add'"
                        >

                        </q-btn>
                        <q-btn
                            label="Editar"
                            type="submit"
                            :disable="!enteredDescription || !enteredStartTime || !enteredEndDate || !enteredEndTime"
                            @submit.prevent="handleSubmit"
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