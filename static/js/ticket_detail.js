    document.addEventListener('DOMContentLoaded', function() {
        const container = document.querySelector('.ticket-container');
        const ticketId = document.getElementById('id_ticket').textContent.trim();

        // Animación de entrada
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            container.style.transition = 'all 0.5s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100);

        // Generar y mostrar el código QR
        const qrCodeDiv = document.getElementById('qrcode');
        const qrCode = new QRCode(qrCodeDiv, {
            text: ticketId,
            width: 85,
            height: 85,
            colorDark : "#000000",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.H
        });
    });