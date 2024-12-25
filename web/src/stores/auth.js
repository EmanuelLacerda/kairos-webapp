import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from 'src/boot/axios'
import { LocalStorage } from 'quasar'

export const useAuthStore = defineStore('auth', () => {
    const me = ref({})
    const token = ref('')
    const isAuthenticated = ref(false)

    function setAccessToken(tokenValue){
        token.value = tokenValue.access_token;
        isAuthenticated.value = true;

        LocalStorage.set("token", tokenValue);

        api.defaults.headers.common.Authorization = `Bearer ${tokenValue.access_token}`;
    }
    function removeAccessToken(){
        api.defaults.headers.common.Authorization = "";
        token.value = '';
        isAuthenticated.value = false;
        LocalStorage.set("token", "")
    }

    async function login(userCredentials) {
        const result = {}

        try{
            const response = await api.post('auth/login/', userCredentials);

            if(response.statusText === 'OK'){
                const { access_token, refresh_token } = response.data;

                setAccessToken({access_token, refresh_token});

                result.wasLoginSuccessfully = true;

                return result
            }
        } catch (e){
            result.wasLoginSuccessfully = false;

            if(e.response.statusText === "Unauthorized"){
                result.error_message = e.response.data.detail
            } else{
                result.error_message = e.response.data
            }

            return result
        }
    }

    function logout(){
        removeAccessToken();
    }

    async function register(userCredentials){
        const result = {}

        try{
            const response = await api.post('auth/register/', userCredentials);

            result.wasRegisterSuccessfully = true;

            console.log(response);

            return result;
        } catch (e){
            result.wasRegisterSuccessfully = false;

            if(e.response.statusText === "Bad Request"){
                result.error_message = e.response.data;
            }

            return result;
        }
        
    }

    async function verifyEmail(verificationCode) {
        const result = {}

        try {
            const response = await api.post('auth/verify-email/', verificationCode);

            if(response.statusText === "OK"){
                result.wasEmailVerify = true;

                return result;
            } else if(response.statusText === "No Content"){
                result.wasEmailVerify = false;

                result.error_message = "Código inválido, usuário já verificado";

                return result;
            }

            return result;
        } catch (e) {
            result.wasEmailVerify = false;

            if(e.response.statusText === "Not Found"){
                result.error_message = e.response.data.message;

                return result;
            }

            return result;
        }
    }

    async function init(){
        const access_token = LocalStorage.getItem("token");

        if(access_token){
            setAccessToken(access_token)
        } else{
            removeAccessToken();
        }
    }


    return {me, token, isAuthenticated, init, login, logout, register, verifyEmail}
})