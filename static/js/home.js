// Verificar carga del DOM
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar boton search ticket
    const searchTicketLink = document.getElementById('search-ticket-button');
    const editTicketLink = document.getElementById('edit-ticket-button');

    // Agregar evento click
    searchTicketLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir comportamiento por defecto
        const response = Swal.fire({
            title: 'Buscar Ticket',
            input: 'text',
            inputLabel: 'Ingrese el número de ticket',
            inputPlaceholder: 'Número de ticket',
            showCancelButton: true,
            confirmButtonText: 'Buscar',
            cancelButtonText: 'Cancelar',
            inputValidator: (value) => {
                if (!value) {
                    return 'Por favor ingrese un número de ticket';
                } else if (isNaN(value)) {
                    return 'El número de ticket debe ser numérico';
                }
            }
        });
        response.then(async (result) => {
            if (result.isConfirmed) {
                const ticketNumber = result.value;
                // Revisar si existe en base de datos
                const req = await fetch(`tickets/search_ticket/${ticketNumber}`);
                if (req.status === 200) {
                    // Enviar a la página del ticket
                    window.location.href = `tickets/get_ticket/${ticketNumber}/`;
                } else if(req.status === 404) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'El ticket no existe. Por favor verifique el número e intente nuevamente.'
                    });
                } else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Ocurrió un error inesperado. Por favor intente nuevamente más tarde.'
                    });
                }
            }
        });
    });

    // Agregar evento click para el edit ticket
    editTicketLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir comportamiento por defecto
        const response = Swal.fire({
            title: 'Editar Ticket',
            input: 'text',
            inputLabel: 'Ingrese el número de ticket a editar',
            inputPlaceholder: 'Número de ticket',
            showCancelButton: true,
            confirmButtonText: 'Buscar',
            cancelButtonText: 'Cancelar',
            inputValidator: (value) => {
                if (!value) {
                    return 'Por favor ingrese un número de ticket';
                } else if (isNaN(value)) {
                    return 'El número de ticket debe ser numérico';
                }
            }
        });
        response.then(async (result) => {
            if (result.isConfirmed) {
                const ticketNumber = result.value;
                // Revisar si existe en base de datos
                const req = await fetch(`tickets/search_ticket/${ticketNumber}`);
                if (req.status === 200) {
                    // Enviar a la página del ticket
                    window.location.href = `tickets/get_edit_ticket/${ticketNumber}/`;
                } else if(req.status === 404) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'El ticket no existe. Por favor verifique el número e intente nuevamente.'
                    });
                } else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Ocurrió un error inesperado. Por favor intente nuevamente más tarde.'
                    });
                }
            }
        });
    });
});