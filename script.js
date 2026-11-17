// A única animação altera discretamente o cursor e respeita movimento reduzido.
const cursor = document.querySelector(".cursor");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const symbols = [" Δ", " δ", " ξ", " Ω", " ω"];
let timer;

function configureCursor() {
  clearInterval(timer);
  let index = 0;
  cursor.textContent = symbols[index];
  if (!reducedMotion.matches) {
    timer = setInterval(() => {
      index = (index + 1) % symbols.length;
      cursor.textContent = symbols[index];
    }, 3500);
  }
}

configureCursor();
reducedMotion.addEventListener("change", configureCursor);
