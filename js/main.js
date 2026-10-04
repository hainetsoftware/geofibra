// js/main.js - Coordinamento UI: mappa e modale cantieri

document.addEventListener("DOMContentLoaded", () => {

    // Inizializza Mappa Leaflet
    if (typeof initMap === 'function') {
        initMap();
    }

    // Modale Cantieri & Ordinanze Albo Pretorio
    const btnOpenCantieri = document.getElementById('btn-open-cantieri');
    const btnCloseCantieri = document.getElementById('btn-close-cantieri');
    const modalCantieri = document.getElementById('modal-cantieri');

    if (btnOpenCantieri && modalCantieri) {
        btnOpenCantieri.addEventListener('click', () => {
            modalCantieri.classList.remove('hidden');
            modalCantieri.classList.add('flex');
            if (window.initCantieriTracker) window.initCantieriTracker();
        });
    }

    if (btnCloseCantieri && modalCantieri) {
        btnCloseCantieri.addEventListener('click', () => {
            modalCantieri.classList.add('hidden');
            modalCantieri.classList.remove('flex');
        });
    }

    if (window.initCantieriTracker) {
        window.initCantieriTracker();
    }
});
