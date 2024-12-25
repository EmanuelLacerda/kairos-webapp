export default function authService() {
    const validatePassword = (password, confirmPassword=null) => {
        const lowerCaseLetters = /[a-z]/g;
        if(!password.match(lowerCaseLetters)) {
          return {
            "isPasswordInvalid": true,
            "errorMessage": "A senha deve conter ao menos uma letra minúscula!",
            "field": "password"
          }
        }
    
        const upperCaseLetters = /[A-Z]/g;
        if(!password.match(upperCaseLetters)) {
          return {
            "isPasswordInvalid": true,
            "errorMessage": "A senha deve conter ao menos uma letra maiúscula!",
            "field": "password"
          }
        }
    
        const numbers = /[0-9]/g;
        if(!password.match(numbers)) {
          return {
            "isPasswordInvalid": true,
            "errorMessage": "A senha deve conter ao menos um número!",
            "field": "password"
          }
        }
    
        if(!(password.length >= 8)) {
          return {
            "isPasswordInvalid": true,
            "errorMessage": "A senha deve conter ao menos 8 caracteres!",
            "field": "password"
          }
        }

        if(confirmPassword !== null && confirmPassword != password){
            return {
                "isPasswordInvalid": true,
                "errorMessage": "As senhas devem ser iguais!",
                "field": "confirm password"
              }
        }
    
        return {
          "isPasswordInvalid": false
        }
    }

    return {
        validatePassword
    }
}