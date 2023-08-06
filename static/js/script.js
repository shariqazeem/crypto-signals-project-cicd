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



