import { ref, reactive } from 'vue';

import Swal from 'sweetalert2'


export function useToast() {
    const positionToastSuccess = ref("top-right");
    const positionToastSuccessAuth = ref("bottom");
    const positionToastError = ref("top-right");

    const noStandardToastMixinInfo = reactive({
        "title": "",
        "text": "",
        "position": "",
    })

    const ToastBaseMixin = Swal.mixin({
        toast: true,
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: true,
        customClass: {title: "toast-title", htmlContainer: "toast-container"},
        showCloseButton: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    });
    
    const ToastSuccess = ToastBaseMixin.mixin({
        icon: "success",
        position: "center"
    })
    const ToastError = ToastBaseMixin.mixin({
        icon: "error",
        position: "top-left",
        width: 600
    })

    return { ToastBaseMixin, ToastSuccess, ToastError, noStandardToastMixinInfo, positionToastSuccess, positionToastError, positionToastSuccessAuth }
}