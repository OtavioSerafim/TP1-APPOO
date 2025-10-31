document.querySelector('form[action*="logout"]')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const response = await fetch(e.target.action, { method: 'POST' });
    const data = await response.json();
    if (data.redirect) {
        window.location.href = data.redirect;
    }
});