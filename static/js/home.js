// Verificar carga del DOM
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar boton search ticket
    const searchTicketLink = document.getElementById('search-ticket-button');
    const editTicketLink = document.getElementById('edit-ticket-button');

    // Agregar evento click
    searchTicketLink.addEventListener('click', async function(event) {
        event.preventDefault(); // Prevenir comportamiento por defecto
        const response = await Swal.fire({
            title: "Buscar Ticket",
            html: `
            <input id="ticket" class="swal2-input" placeholder="Número de ticket">
            <input id="curp" class="swal2-input" placeholder="CURP">
              `,
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: "Buscar",
            cancelButtonText: "Cancelar",
            preConfirm: () => {
              const ticket = document.getElementById("ticket").value;
              const curp = document.getElementById("curp").value;
              if (!ticket) {
                Swal.showValidationMessage(
                  "Por favor ingrese el número de ticket"
                );
              } else if (!curp) {
                Swal.showValidationMessage(
                  "Por favor ingrese el CURP registrado en el ticket"
                );
              }
              return { ticket, curp };
            },
          }).then(async (result) => {
            if (result.isConfirmed) {
                const { ticket, curp } = result.value;
                // Revisar si existe en base de datos
                const req = await fetch(`tickets/search_ticket/${ticket}/${curp}`);
                if (req.status === 200) {
                    // Enviar a la página del ticket
                    window.location.href = `tickets/get_ticket/${ticket}/${curp}`;
                } else if(req.status === 404) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'El ticket no existe. Por favor verifique el número y el CURP e intente nuevamente.'
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
    editTicketLink.addEventListener('click', async function(event) {
        event.preventDefault(); // Prevenir comportamiento por defecto
        const response = await Swal.fire({
            title: "Buscar Ticket",
            html: `
            <input id="ticket" class="swal2-input" placeholder="Número de ticket">
            <input id="curp" class="swal2-input" placeholder="CURP">
              `,
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: "Buscar",
            cancelButtonText: "Cancelar",
            preConfirm: () => {
              const ticket = document.getElementById("ticket").value;
              const curp = document.getElementById("curp").value;
              if (!ticket) {
                Swal.showValidationMessage(
                  "Por favor ingrese el número de ticket"
                );
              } else if (!curp) {
                Swal.showValidationMessage(
                  "Por favor ingrese el CURP registrado en el ticket"
                );
              }
              return { ticket, curp };
            },
          }).then(async (result) => {
            if (result.isConfirmed) {
                const { ticket, curp } = result.value;
                // Revisar si existe en base de datos
                const req = await fetch(`tickets/search_ticket/${ticket}/${curp}`);
                if (req.status === 200) {
                    // Enviar a la página del ticket
                    window.location.href = `tickets/get_edit_ticket/${ticket}/${curp}`;
                } else if(req.status === 404) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'El ticket no existe. Por favor verifique el número y el CURP e intente nuevamente.'
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