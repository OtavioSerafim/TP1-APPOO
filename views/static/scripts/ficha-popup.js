document.addEventListener('DOMContentLoaded', () => {
  const popup = document.getElementById('ficha-popup');
  const elAluno = document.getElementById('popup-aluno');
  const elPersonal = document.getElementById('popup-personal');
  const elDesc = document.getElementById('popup-descricao');
  const elTbody = document.getElementById('popup-exercicios');

  const openPopup = () => {
    popup.classList.add('active');
    document.body.style.overflow = 'hidden';
  };
  const closePopup = () => {
    popup.classList.remove('active');
    document.body.style.overflow = '';
  };

  // Click na ficha: carrega dados e abre
  document.addEventListener('click', async (e) => {
    const a = e.target.closest('.ficha');
    if (!a) return;
    e.preventDefault();

    const id = a.dataset.fichaId;
    if (!id) return;

    try {
      const resp = await fetch(`/api/fichas/${id}`);
      if (!resp.ok) throw new Error('Falha ao carregar ficha');
      const data = await resp.json();

      const f = data.ficha;
      const xs = data.exercicios || [];

      elAluno.textContent = f.aluno_nome || '-';
      elPersonal.textContent = f.personal_nome || '-';
      elDesc.textContent = f.descricao || 'Sem descrição';

      // Limpar tbody
      elTbody.innerHTML = '';

      if (xs.length === 0) {
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 7;
        td.textContent = 'Nenhum exercício cadastrado.';
        tr.appendChild(td);
        elTbody.appendChild(tr);
      } else {
        xs.forEach(ex => {
          const tr = document.createElement('tr');
          
          // Nome do exercício
          const tdNome = document.createElement('td');
          tdNome.textContent = ex.nome || '-';
          tr.appendChild(tdNome);
          
          // Equipamento
          const tdEquip = document.createElement('td');
          tdEquip.textContent = ex.equipamento_nome || '-';
          tr.appendChild(tdEquip);
          
          // Séries
          const tdSeries = document.createElement('td');
          tdSeries.textContent = ex.series || '-';
          tr.appendChild(tdSeries);
          
          // Repetições
          const tdReps = document.createElement('td');
          tdReps.textContent = ex.repeticoes || '-';
          tr.appendChild(tdReps);
          
          // Carga
          const tdCarga = document.createElement('td');
          tdCarga.textContent = ex.carga || '-';
          tr.appendChild(tdCarga);
          
          // Descanso
          const tdDescanso = document.createElement('td');
          tdDescanso.textContent = ex.tempo_descanso || '-';
          tr.appendChild(tdDescanso);
          
          // Observações
          const tdObservacoes = document.createElement('td');
          tdObservacoes.textContent = ex.observacoes || '-';
          tr.appendChild(tdObservacoes);
          
          elTbody.appendChild(tr);
        });
      }

      openPopup();
    } catch (err) {
      console.error(err);
    }
  });

  // Fechar popup (X, overlay, ESC)
  document.addEventListener('click', (e) => {
    if (e.target === popup) closePopup();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && popup.classList.contains('active')) closePopup();
  });
});