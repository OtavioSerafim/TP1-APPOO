document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.querySelector('.add-exercicio');
    const container = document.querySelector('.exercicios-container');
    let exercicioCount = 1; // contador para IDs únicos

    addBtn.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Clonar o primeiro bloco de exercícios (exercicio-container)
        const originalContainer = document.querySelector('.exercicio-container');
        const clone = originalContainer.cloneNode(true);
        
        // Incrementar contador
        exercicioCount++;
        
        // Atualizar IDs e names dos inputs clonados para serem únicos
        clone.querySelectorAll('input, textarea').forEach(input => {
            // Limpar valor
            if (input.type === 'radio' || input.type === 'checkbox') {
                input.checked = false;
            } else {
                input.value = '';
            }
            
            // Atualizar IDs
            if (input.id) {
                input.id = input.id.replace(/\d+$/, '') + exercicioCount;
            }
            
            // Converter name em array para permitir múltiplos exercícios
            if (input.name && !input.name.includes('[')) {
                input.name = `exercicios[${exercicioCount - 1}][${input.name}]`;
            }
        });
        
        // Atualizar labels para apontarem para os novos IDs
        clone.querySelectorAll('label').forEach(label => {
            if (label.htmlFor) {
                label.htmlFor = label.htmlFor.replace(/\d+$/, '') + exercicioCount;
            }
        });
        
        // Adicionar botão de remover como filho direto do exercicio-container
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'remove-exercicio';
        removeBtn.textContent = 'Remover exercício';
        
        removeBtn.addEventListener('click', () => {
            clone.remove();
        });
        
        // Adicionar o botão de remover como filho direto do clone
        clone.appendChild(removeBtn);
        
        // Inserir o clone antes do botão "Adicionar exercício"
        container.insertBefore(clone, addBtn);
    });
});