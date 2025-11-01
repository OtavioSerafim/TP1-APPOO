const studentPopup = document.getElementById('student-edit-popup');
const studentForm = document.getElementById('student-edit-form');
const nameInput = document.getElementById('student-name');
const emailInput = document.getElementById('student-email');
const personalSelect = document.getElementById('student-personal');
const planSelect = document.getElementById('student-plan');
const planStartInput = document.getElementById('student-plan-start');

const buildAction = (template, id) => {
    if (!template) {
        return '';
    }
    return template.replace('/0/', `/${id}/`);
};

const closePopup = () => {
    if (!studentPopup) {
        return;
    }
    studentPopup.classList.remove('active');
    document.body.style.overflow = '';
};

const openPopup = () => {
    if (!studentPopup) {
        return;
    }
    studentPopup.classList.add('active');
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
    if (!studentForm) {
        return;
    }

    const editButton = event.target.closest('.student-edit');
    if (editButton) {
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
        openPopup();
        return;
    }

    if (event.target.classList.contains('student-popup-overlay')) {
        closePopup();
    }
});

if (studentPopup) {
    studentPopup.querySelectorAll('.popup-close').forEach((button) => {
        button.addEventListener('click', closePopup);
    });
}

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closePopup();
    }
});

togglePlanStartState();
