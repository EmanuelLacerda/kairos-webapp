<template>
<q-layout view="hhh lpr fff">
    <q-page-container>
        <router-view></router-view>
    </q-page-container>
</q-layout>
</template>

<style lang="scss" scoped>
    .q-layout{
        background-image: url('../assets/auth_background.svg');
        background-repeat: no-repeat;
        background-size: cover;
    }
</style>