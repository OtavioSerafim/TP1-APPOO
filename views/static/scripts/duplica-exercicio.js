document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.querySelector('.add-exercicio');
    const container = document.querySelector('.exercicios-container');
    let exercicioCount = 0; // começar do 0 (primeiro exercício será 0)

    // Ao carregar, converter o primeiro exercício para formato de array
    const primeiroContainer = document.querySelector('.exercicio-container');
    primeiroContainer.querySelectorAll('input, textarea').forEach(input => {
        if (input.name && !input.name.includes('[')) {
            input.name = `exercicios[0][${input.name}]`;
        }
    });

    addBtn.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Incrementar contador ANTES de clonar
        exercicioCount++;
        
        // Clonar o primeiro bloco de exercícios (exercicio-container)
        const originalContainer = document.querySelector('.exercicio-container');
        const clone = originalContainer.cloneNode(true);
        
        // Atualizar IDs e names dos inputs clonados para serem únicos
        clone.querySelectorAll('input, textarea').forEach(input => {
            // Limpar valor
            if (input.type === 'radio' || input.type === 'checkbox') {
                input.checked = false;
            } else {
                input.value = '';
            }
            
            // Atualizar IDs - adicionar sufixo único
            if (input.id) {
                // Remove sufixo numérico existente e adiciona novo
                const baseId = input.id.replace(/\d+$/, '');
                input.id = baseId + exercicioCount;
            }
            
            // Atualizar name para o índice correto
            if (input.name) {
                // Extrai o nome do campo (ex: "nome", "equipamento_id", etc)
                const match = input.name.match(/\[([^\]]+)\]$/);
                if (match) {
                    const fieldName = match[1];
                    input.name = `exercicios[${exercicioCount}][${fieldName}]`;
                }
            }
        });
        
        // Atualizar labels para apontarem para os novos IDs
        clone.querySelectorAll('label').forEach(label => {
            if (label.htmlFor) {
                const baseFor = label.htmlFor.replace(/\d+$/, '');
                label.htmlFor = baseFor + exercicioCount;
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