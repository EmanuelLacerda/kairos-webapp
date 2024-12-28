import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import { api, axios } from 'src/boot/axios'
import { jwtDecode } from 'jwt-decode'
import dayjs from 'dayjs'
import { LocalStorage } from 'quasar'

export const useAuthStore = defineStore('auth', () => {
    const user = reactive({})
    const access_token = ref('')
    const refresh_token = ref('')
    const isAuthenticated = ref(false)

    function updateAccessToken(newAccessToken){
        access_token.value = newAccessToken;
        LocalStorage.set("access_token", newAccessToken);

        if(newAccessToken){
            api.defaults.headers.common.Authorization = `Bearer ${newAccessToken}`;
        } else{
            api.defaults.headers.common.Authorization = "";
        }
    }
    function updateRefreshToken(newRefreshToken){
        refresh_token.value = newRefreshToken;
        LocalStorage.set("refresh_token", newRefreshToken);
    }
    function updateUserData(userData){
        user.name = userData.name ? userData.name : "";
        user.email = userData.email ? userData.email : "";

        LocalStorage.set("user", userData);
    }

    function setAuthenticatedStatus(userData, tokenValue){
        updateAccessToken(tokenValue.access_token);
        updateRefreshToken(tokenValue.refresh_token);
        updateUserData(userData);

        isAuthenticated.value = true;
    }
    function removeAuthenticatedStatus(){
        updateAccessToken("");
        updateRefreshToken("");
        updateUserData({});

        isAuthenticated.value = false;
    }

    async function init(){
        const user = LocalStorage.getItem("user");
        const access_token = LocalStorage.getItem("access_token");
        const refresh_token = LocalStorage.getItem("refresh_token");

        if(access_token){
            setAuthenticatedStatus(user, {access_token, refresh_token})
        } else{
            removeAuthenticatedStatus();
        }
    }

    async function register(userCredentials){
        const result = {}

        try{
            const response = await api.post('auth/register/', userCredentials);

            if(response.statusText === "Created"){
                result.wasRegisterSuccessfully = true;

                return result;
            }

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

    async function login(userCredentials) {
        const result = {}

        try{
            const response = await api.post('auth/login/', userCredentials);

            if(response.statusText === 'OK'){
                const { name, email, access_token, refresh_token } = response.data;

                setAuthenticatedStatus({name, email},{access_token, refresh_token});

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
    async function logout(){
        const result = {};

        try{
            const response = await api.post('auth/logout/', {"refresh_token": refresh_token.value});
            if(response.statusText === "OK"){
                removeAuthenticatedStatus();

                result.wasLogoutSuccessfully = true;

                return result;
            }

            result.wasLogoutSuccessfully = false;
            result.error_message = response;

            return result;
        } catch(e){
            result.wasLogoutSuccessfully = false;
            result.error_message = e.response;

            return result;
        }
    }

    async function checkIfUserAuthenticated() {
        const access_token = LocalStorage.getItem('access_token')
        const refresh_token = LocalStorage.getItem('refresh_token')
      
        if(access_token){
          const user = jwtDecode(access_token)
          const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;
          
          if(!isExpired){
            return {"isUserAuthenticated": true};
          } else{
            try {
                const response = await axios.post(`http://127.0.0.1:8000/api/v1/auth/token/refresh/`, {'refresh': refresh_token});

                if(response.statusText === "OK"){
                    return {"isUserAuthenticated": true, "new_access_token": response.data.access};
                } else{
                    return {"isUserAuthenticated": false};
                }
            } catch (error) {
                if(error.response.statusText === "Unauthorized"){
                    return {"isUserAuthenticated": false};
                }
            }
          }
        } else if(refresh_token){
            try {
                const response = await axios.post(`http://127.0.0.1:8000/api/v1/auth/token/refresh/`, {'refresh': refresh_token});

                if(response.statusText === "OK"){
                    return {"isUserAuthenticated": true, "new_access_token": response.data.access};
                } else{
                    return {"isUserAuthenticated": false};
                }
            } catch (error) {
                if(error.response.statusText === "Unauthorized"){
                    return {"isUserAuthenticated": false};
                }
            }
        } else{
            return {"isUserAuthenticated": false};
        }
    }

    
    return {user, access_token, isAuthenticated, init, login, logout, register, verifyEmail, checkIfUserAuthenticated, updateAccessToken, removeAuthenticatedStatus, setAuthenticatedStatus}
})