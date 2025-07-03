function iniciarCarrossel(containerId, intervalo = 5000) {
    const container = document.getElementById(containerId);
    const slides = container.querySelectorAll('.carrossel-slide');
    let indice = 0;

    setInterval(() => {
        slides[indice].classList.remove('ativo');
        indice = (indice + 1) % slides.length;
        slides[indice].classList.add('ativo');
    }, intervalo);
}

window.onload = () => {
    iniciarCarrossel('carrossel1', 7000); // troca a cada 7 segundos
};
