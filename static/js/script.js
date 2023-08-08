// script.js
const blogEntries = document.querySelectorAll('.h-full.border-2.border-gray-200.border-opacity-60.rounded-lg.overflow-hidden.image-container');

const options = {
  root: null,
  threshold: 0.2,
};

function animateOnScroll(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate__fadeInUp');
      observer.unobserve(entry.target);
    }
  });
}

// JavaScript to toggle the visibility of menu items when clicking the hamburger icon
document.addEventListener('DOMContentLoaded', function () {
  const menuBtn = document.getElementById('menuBtn');
  const menuItems = document.getElementById('menuItems');

  menuBtn.addEventListener('click', function () {
      menuItems.classList.toggle('active');
  });
});

    document.addEventListener("DOMContentLoaded", function () {
        const calculateBtns = document.querySelectorAll(".calculate-btn");

        calculateBtns.forEach((calculateBtn) => {
            calculateBtn.addEventListener("click", function () {
                const card = calculateBtn.closest(".signal-card");
                const portfolioSize = parseFloat(card.querySelector(".portfolio-size").value);
                const riskPercentage = parseFloat(card.querySelector(".risk-percentage").value);
                const entryPrice = parseFloat(card.querySelector(".entry-price").value);
                const stopLossPrice = parseFloat(card.querySelector(".stop-loss").textContent);

                const totalAmountAtRisk = (portfolioSize * riskPercentage) / 100;
                const positionSize = totalAmountAtRisk / (entryPrice - stopLossPrice);

                const resultElement = card.querySelector(".result");
                resultElement.innerHTML = `Position Size: ${positionSize.toFixed(2)}`;
            });
        });
    });





