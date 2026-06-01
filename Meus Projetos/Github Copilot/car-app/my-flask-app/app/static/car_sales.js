document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('button');
  
  buttons.forEach(button => {
    button.addEventListener('click', function(event) {
      const carCard = this.closest('[data-brand][data-name]');
      
      if (carCard) {
        const brand = carCard.getAttribute('data-brand');
        const name = carCard.getAttribute('data-name');
        alert(`Carro vendido: ${brand} ${name}`);
      } else {
        alert('Carro vendido com sucesso!');
      }
    });
  });
});
