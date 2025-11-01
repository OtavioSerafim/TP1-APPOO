const editPopup = document.getElementById('plan-edit-popup');
const deletePopup = document.getElementById('plan-delete-popup');
const editForm = document.getElementById('plan-edit-form');
const deleteForm = document.getElementById('plan-delete-form');
const deleteName = document.getElementById('plan-delete-name');

const popups = [editPopup, deletePopup].filter(Boolean);

const closeAllPopups = () => {
    popups.forEach((popup) => popup.classList.remove('active'));
    document.body.style.overflow = '';
};

const openPopup = (popup) => {
    if (!popup) {
        return;
    }
    popups.forEach((element) => {
        if (element !== popup) {
            element.classList.remove('active');
        }
    });
    popup.classList.add('active');
    document.body.style.overflow = 'hidden';
};

const buildAction = (template, id) => {
    if (!template) {
        return '';
    }
    return template.replace('/0/', `/${id}/`);
};

document.addEventListener('click', (event) => {
    const editButton = event.target.closest('.plan-edit');
    if (editButton && editForm) {
        const { id, nome, descricao, valor, duracao } = editButton.dataset;
        editForm.action = buildAction(editForm.dataset.updateActionTemplate, id);
        editForm.querySelector('#edit-plan-name').value = nome || '';
        editForm.querySelector('#edit-plan-desc').value = descricao || '';
        editForm.querySelector('#edit-plan-value').value = valor || '';
        editForm.querySelector('#edit-plan-duration').value = duracao || '';
        openPopup(editPopup);
        return;
    }

    const deleteButton = event.target.closest('.plan-delete');
    if (deleteButton && deleteForm) {
        const { id, nome } = deleteButton.dataset;
        deleteForm.action = buildAction(deleteForm.dataset.deleteActionTemplate, id);
        if (deleteName) {
            deleteName.textContent = nome || '';
        }
        openPopup(deletePopup);
        return;
    }

    if (event.target.classList.contains('plan-popup-overlay')) {
        closeAllPopups();
    }
});

document.querySelectorAll('.popup-close').forEach((button) => {
    button.addEventListener('click', closeAllPopups);
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeAllPopups();
    }
});
