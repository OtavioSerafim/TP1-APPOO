const equipmentEditPopup = document.getElementById('equipment-edit-popup');
const equipmentDeletePopup = document.getElementById('equipment-delete-popup');
const equipmentEditForm = document.getElementById('equipment-edit-form');
const equipmentDeleteForm = document.getElementById('equipment-delete-form');
const equipmentDeleteName = document.getElementById('equipment-delete-name');

const equipmentPopups = [equipmentEditPopup, equipmentDeletePopup].filter(Boolean);

const closeEquipmentPopups = () => {
    equipmentPopups.forEach((popup) => popup.classList.remove('active'));
    document.body.style.overflow = '';
};

const openEquipmentPopup = (popup) => {
    if (!popup) {
        return;
    }
    equipmentPopups.forEach((element) => {
        if (element !== popup) {
            element.classList.remove('active');
        }
    });
    popup.classList.add('active');
    document.body.style.overflow = 'hidden';
};

const buildEquipmentAction = (template, id) => {
    if (!template) {
        return '';
    }
    return template.replace('/0/', `/${id}/`);
};

const selectStatusRadio = (value) => {
    if (!equipmentEditForm) {
        return;
    }
    const radios = equipmentEditForm.querySelectorAll('input[name="status"]');
    radios.forEach((radio) => {
        radio.checked = radio.value === value;
    });
};

document.addEventListener('click', (event) => {
    const editButton = event.target.closest('.equipment-edit');
    if (editButton && equipmentEditForm) {
        const { id, nome, valor, status } = editButton.dataset;
        equipmentEditForm.action = buildEquipmentAction(
            equipmentEditForm.dataset.updateActionTemplate,
            id,
        );
        equipmentEditForm.querySelector('#equipment-name').value = nome || '';
        equipmentEditForm.querySelector('#equipment-value').value = valor || '';
        selectStatusRadio(status);
        openEquipmentPopup(equipmentEditPopup);
        return;
    }

    const deleteButton = event.target.closest('.equipment-delete');
    if (deleteButton && equipmentDeleteForm) {
        const { id, nome } = deleteButton.dataset;
        equipmentDeleteForm.action = buildEquipmentAction(
            equipmentDeleteForm.dataset.deleteActionTemplate,
            id,
        );
        if (equipmentDeleteName) {
            equipmentDeleteName.textContent = nome || '';
        }
        openEquipmentPopup(equipmentDeletePopup);
        return;
    }

    if (event.target.classList.contains('equipment-popup-overlay')) {
        closeEquipmentPopups();
    }
});

document.querySelectorAll('.popup-close').forEach((button) => {
    button.addEventListener('click', closeEquipmentPopups);
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeEquipmentPopups();
    }
});
