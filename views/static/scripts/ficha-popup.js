const popup = document.getElementById('ficha-popup');

// Abrir popup ao clicar na ficha
document.addEventListener('click', (e) => {
    const ficha = e.target.closest('.ficha');
    if (ficha && popup) {
        e.preventDefault();
        popup.classList.add('active');
        document.body.style.overflow = 'hidden';
        return;
    }

    // Fechar popup ao clicar fora do conteúdo (no overlay)
    if (e.target.classList.contains('ficha-detalhes-container') && popup) {
        popup.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Fechar popup ao pressionar ESC
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && popup && popup.classList.contains('active')) {
        popup.classList.remove('active');
        document.body.style.overflow = '';
    }
});