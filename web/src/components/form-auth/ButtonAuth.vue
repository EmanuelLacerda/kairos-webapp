<script setup>
defineOptions({
  name: 'ButtonAuth'
})

defineProps({
    buttonLabel: {
        type: String,
        required: true
    },
    isDisabled: {
        type: Boolean,
        default: false
    },
    isProcessRunning: {
        type: Boolean,
        default: false
    }
})
</script>

<template>
    <q-btn
        :label="buttonLabel"
        type="submit"
        class="bg-white"
        :outline="false"
        :disable="isDisabled"
        :loading="isProcessRunning"
    >

    </q-btn>
</template>

<style lang="scss">
form.form-auth-base{
    button.q-btn{
        width: 100%;
        height: 45px;
        color: $custom-blue-1;
        margin-top: 43px;
        font-family: "Montserrat", serif;
        font-weight: 600;
        font-size: 20px;
    }
}
</style>