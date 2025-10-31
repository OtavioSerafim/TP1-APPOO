// Dispensa flash-messages ao clicar
document.addEventListener('click', (e) => {
  const msg = e.target.closest('.flash-message');
  if (!msg) return;

  msg.style.transition = 'opacity .2s ease, transform .2s ease';
  msg.style.opacity = '0';
  msg.style.transform = 'scale(0.98)';
  msg.addEventListener('transitionend', () => msg.remove(), { once: true });
});