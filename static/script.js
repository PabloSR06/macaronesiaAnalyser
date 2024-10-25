document.addEventListener('DOMContentLoaded', () => {
    const input = document.querySelector('#question');
    const placeholders = [
        'Mejor arquero por categoría',
        'Mejor puntuación del arquero',
        '¿Cuántos arqueros tiene el Club Centenero?',
        '¿Qué clubs hay?',
        'Total de puntos por arquero',
        'Total de puntos del Club Centenero en 2023',
        '¿Cuántos puntos tiene el Club Centenero?',
        '¿Qué categorias hay?',
    ];    
    let index = 0;

    setInterval(() => {
        input.setAttribute('placeholder', placeholders[index]);
        index = (index + 1) % placeholders.length;
    }, 2000); // Cambia cada 2 segundos
});
