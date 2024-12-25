<template>
<q-layout view="hhh lpr fff" class="auth-layout">
    <q-page-container>
        <router-view></router-view>
    </q-page-container>
</q-layout>
</template>

<style lang="scss">
    body{
        background-image: url('../assets/auth_background.svg');
        background-repeat: no-repeat;
        background-size: cover;
    }

    .q-page.auth-layout{
        .q-page{
            width: 50%;
        }
    }
</style>