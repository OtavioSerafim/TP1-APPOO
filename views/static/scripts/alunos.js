const studentPopup = document.getElementById('student-edit-popup');
const studentForm = document.getElementById('student-edit-form');
const nameInput = document.getElementById('student-name');
const emailInput = document.getElementById('student-email');
const personalSelect = document.getElementById('student-personal');
const planSelect = document.getElementById('student-plan');
const planStartInput = document.getElementById('student-plan-start');

const studentDeletePopup = document.getElementById('student-delete-popup');
const studentDeleteForm = document.getElementById('student-delete-form');
const studentDeleteName = document.getElementById('student-delete-name');

const popups = [studentPopup, studentDeletePopup].filter(Boolean);

const buildAction = (template, id) => {
    if (!template) {
        return '';
    }
    return template.replace('/0/', `/${id}/`);
};

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

const togglePlanStartState = () => {
    if (!planSelect || !planStartInput) {
        return;
    }
    const hasPlan = Boolean(planSelect.value);
    planStartInput.disabled = !hasPlan;
    if (!hasPlan) {
        planStartInput.value = '';
    }
};

if (planSelect) {
    planSelect.addEventListener('change', togglePlanStartState);
}

document.addEventListener('click', (event) => {
    const editButton = event.target.closest('.student-edit');
    if (editButton && studentForm) {
        const {
            id,
            nome,
            email,
            personal,
            plano,
            planoInicio,
        } = editButton.dataset;

        studentForm.action = buildAction(studentForm.dataset.updateActionTemplate, id);
        nameInput.value = nome || '';
        emailInput.value = email || '';

        if (personalSelect) {
            personalSelect.value = personal || '';
        }
        if (planSelect) {
            planSelect.value = plano || '';
        }
        if (planStartInput) {
            planStartInput.value = planoInicio || '';
        }

        togglePlanStartState();
        openPopup(studentPopup);
        return;
    }

    const deleteButton = event.target.closest('.student-delete');
    if (deleteButton && studentDeleteForm) {
        const { id, nome } = deleteButton.dataset;
        studentDeleteForm.action = buildAction(studentDeleteForm.dataset.deleteActionTemplate, id);
        if (studentDeleteName) {
            studentDeleteName.textContent = nome || '';
        }
        openPopup(studentDeletePopup);
        return;
    }

    if (event.target.classList.contains('student-popup-overlay')) {
        closeAllPopups();
    }
});

popups.forEach((popup) => {
    popup.querySelectorAll('.popup-close').forEach((button) => {
        button.addEventListener('click', closeAllPopups);
    });
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeAllPopups();
    }
});

togglePlanStartState();
