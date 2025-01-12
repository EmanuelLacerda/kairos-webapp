import Swal from 'sweetalert2'


export function useDialog() {
    const confirmDialog = Swal.mixin({
        title: "Tem certeza?",
        icon: "info",
        showCancelButton: true,
        cancelButtonText: "Cancelar",
    });

    const confirmDeleteDialog = confirmDialog.mixin({
        confirmButtonText: "Deletar",
        customClass: {confirmButton: 'btn-danger', cancelButton: 'btn-secondary'},
    })
    const confirmDeleteEventDialog = confirmDeleteDialog.mixin({
        text: "Se você deletar este evento, não será possível recuperar ele."
    })

    const confirmEditDialog = confirmDialog.mixin({
        confirmButtonText: "Editar",
        customClass: {confirmButton: 'btn-primary', cancelButton: 'btn-secondary'},
    })

    const confirmLogoutDialog = confirmDialog.mixin({
        text: "Se você confirmar, será deslogado do Kairos.",
        confirmButtonText: "Sair",
        customClass: {confirmButton: 'btn-primary', cancelButton: 'btn-secondary'},
    });


    const notificationErrorDialog = Swal.mixin({
        icon: "error",
        showCancelButton: false,
        confirmButtonText: "OK",
        animation: true,
        customClass: {confirmButton: 'btn-primary'}
    });

    return {confirmDialog, confirmDeleteDialog, confirmDeleteEventDialog, confirmEditDialog, confirmLogoutDialog, notificationErrorDialog}
}