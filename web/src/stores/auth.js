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
            const response = await api.post('auth/login/', userCredentials)

            if(response.statusText === 'OK'){
                const { access_token, refresh_token } = response.data;

                setAccessToken({access_token, refresh_token});

                result.wasLoginSuccessfully = true;

                return result
            }
        } catch (e){
            result.wasLoginSuccessfully = false;

            console.log(e.response)

            if(e.response.statusText === "Unauthorized"){
                result.error_message = e.response.data.detail
            }

            return result
        }
    }

    function logout(){
        removeAccessToken();
    }

    async function init(){
        const access_token = LocalStorage.getItem("token");

        if(access_token){
            setAccessToken(access_token)
        } else{
            removeAccessToken();
        }
    }


    return {me, token, isAuthenticated, init, login, logout}
})