<script setup>
defineOptions({
  name: 'RedirectButton'
})

defineProps({
    buttonLabel: {
        type: String,
        required: true
    },
    redirectLink: {
        type: String,
        required: true
    }
})
</script>

<template>
    <q-btn
        :label="buttonLabel"
        :to="redirectLink"
        type="button"
        :outline="false"
        class="redirect-button"
    >

    </q-btn>
</template>

<style lang="scss">
.q-btn.redirect-button{
    width: 300px;
    height: 45px;
    color: $custom-full-white;
    margin-top: 43px;
    font-family: "Montserrat", serif;
    font-weight: 600;
    font-size: 20px;
    background-color: $custom-blue-1;
}
</style>
