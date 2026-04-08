document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".sidebar input");
  const cards = Array.from(document.querySelectorAll(".card-link"));
  const pagination = document.getElementById("pagination");
  const cardsPerPage = 6;
  let currentPage = 1;

  function updateView() {
    const selected = Array.from(checkboxes)
      .filter(c => c.checked)
      .map(c => c.value);

    const filtered = selected.length === 0
      ? cards
      : cards.filter(card => {
          const types = card.querySelector(".card").dataset.type.split(" ");
          return selected.some(s => types.includes(s));
        });

    const totalPages = Math.ceil(filtered.length / cardsPerPage);
    if (currentPage > totalPages) currentPage = totalPages || 1;

    const start = (currentPage - 1) * cardsPerPage;
    const end = start + cardsPerPage;

    cards.forEach(card => card.style.display = "none");
    filtered.slice(start, end).forEach(card => card.style.display = "block");

    renderPagination(totalPages);
  }

  function renderPagination(totalPages) {
    let html = "";
    html += `<button ${currentPage===1?"disabled":""} onclick="goPage(${currentPage-1})">« 上一頁</button>`;
    for (let i = 1; i <= totalPages; i++) {
      html += `<button onclick="goPage(${i})" class="${i===currentPage?"active":""}">${i}</button>`;
    }
    html += `<button ${currentPage===totalPages?"disabled":""} onclick="goPage(${currentPage+1})">下一頁 »</button>`;
    pagination.innerHTML = html;
  }

  window.goPage = function(num) {
    currentPage = num;
    updateView();
  };

  checkboxes.forEach(cb => cb.addEventListener("change", () => {
    currentPage = 1;
    updateView();
  }));

  updateView();
});