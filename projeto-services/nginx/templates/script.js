// Obtém referência aos elementos do formulário e da tabela
const form = document.getElementById("order-form");
const orderList = document.getElementById("order-list");

// Adiciona um evento de submit ao formulário
form.addEventListener("submit"), (event) => {
  event.preventDefault();

  // Obtém os valores dos campos do formulário
  const name = form.name.value;
  const address = form.address.value;
  const item = form.item.value;
  const quantity = form.quantity.value;

  // Cria uma nova linha na tabela com os val
}