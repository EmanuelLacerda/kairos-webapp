<script setup>
defineOptions({
  name: "InputAuthBase",
});

defineProps({
    autofocus: {
        type: Boolean,
        default: false
    },
    errorMessage: String
})

const emit = defineEmits([
  'removeMessageError'
])

const removeMessageError = () => {
    emit('removeMessageError');
}
</script>

<template>
    <q-input :outlined="true" :autofocus="autofocus" :class="{invalidInput: errorMessage}" @focus="removeMessageError" v-bind="$attrs">
        <slot></slot>
    </q-input>
    <p class="error-text-message" v-if="errorMessage">{{errorMessage}}</p>
</template>

<style lang="scss">
form.form-auth-base{
    label.q-field{
        .q-field__control{
            height: 45px !important;

            .q-field__control-container{
            display: flex;
            flex-direction: row-reverse;
            align-items: center;
            gap: 15px;
            }
        }

        .q-field__control::before{
            border-color: $custom-full-white !important;
        }

        .q-field__native, .q-icon{
            color: $custom-full-white;
            font-family: "Montserrat", serif;
            font-weight: 300;
            font-size: 18px;
        }
    }
}

form.form-auth-base{
    .invalidInput{
        .q-field__control::before{
            border-color: $custom-border-color-error !important;
        }

        .q-icon, input{
            color: $custom-text-color-error !important;
        }
    }

    .error-text-message{
        color: $custom-text-color-error;
        margin-top: 12px;
        font-weight: 600;
        text-align: justify;
    }
}
</style>