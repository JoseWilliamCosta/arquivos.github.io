function toggleTexto(notaId) {
    const resumo = document.getElementById(`resumo-${notaId}`);
    const completo = document.getElementById(`completo-${notaId}`);
    const botao = document.getElementById(`btn-${notaId}`);

    if (completo.classList.contains('hidden')) {
        resumo.style.display = 'none';
        completo.classList.remove('hidden');
        botao.textContent = 'Ver menos';
    } else {
        resumo.style.display = 'block';
        completo.classList.add('hidden');
        botao.textContent = 'Ver mais';
    }
}