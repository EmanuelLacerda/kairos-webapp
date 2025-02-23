<script setup>
defineOptions({
  name: 'ButtonAuth'
})


import ButtonBase from '../base/ButtonBase.vue';
</script>

<template>
    <ButtonBase
      class="bg-white"
      type="submit"
      :outline="false"
    >
    </ButtonBase>
</template>

<style lang="scss">
form.form-auth-base{
    button.q-btn{
        width: 100%;
        height: 45px;
        color: $custom-text-primary;
        margin-top: 43px;
        font-family: "Montserrat", serif;
        font-weight: 600;
        font-size: 20px;
    }
}
</style>
