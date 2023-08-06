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
  const calculateBtn = document.querySelector(".calculate-btn");
  calculateBtn.addEventListener("click", function () {
    // Get the portfolio size, risk percentage, entry price, take profit percentage, and stop loss from the user input
    const portfolioSize = parseFloat(document.querySelector(".portfolio-size").value);
    const riskPercentage = parseFloat(document.querySelector(".risk-percentage").value);
    const entryPrice = parseFloat(document.querySelector(".entry-price").value);
    const takeProfitPercentage = parseFloat(document.querySelector(".buy-range").dataset.tp);
    const stopLoss = parseFloat(document.querySelector(".stop-loss").textContent);

    // Calculate the total amount, number of coins to buy, amount after profit, and amount after stop loss
    const totalAmount = portfolioSize * (riskPercentage / 100);
    const coinsToBuy = (totalAmount / entryPrice).toFixed(2);
    const takeProfit = parseInt(takeProfitPercentage * 100);
    const amountAfterProfit = (totalAmount + totalAmount * takeProfit * 0.01).toFixed(2);
    const amountAfterStopLoss = (totalAmount - totalAmount * stopLoss).toFixed(2);

    // Set the result HTML element with the calculated values
    document.querySelector(".result").innerHTML = `
      Number of Coins to Buy: ${coinsToBuy}<br>
      Amount After Profit: $${amountAfterProfit}<br>
      Amount After Stop Loss: $${amountAfterStopLoss}
    `;
  });
});


