/* ============================================================
   CHRISTIAN JERIA — Portfolio Script
   ============================================================ */

(() => {
  'use strict';

  /* ----------------------------------------------------------
     1. Navigation — add .scrolled class after 40px scroll
     ---------------------------------------------------------- */
  const nav = document.getElementById('nav');

  function onScroll() {
    if (window.scrollY > 40) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load in case page is already scrolled


  /* ----------------------------------------------------------
     2. Intersection Observer — reveal elements on scroll
     ---------------------------------------------------------- */
  const revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // animate once only
          }
        });
      },
      {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    revealElements.forEach((el) => observer.observe(el));
  } else {
    // Fallback: show all immediately if IntersectionObserver not supported
    revealElements.forEach((el) => el.classList.add('visible'));
  }


  /* ----------------------------------------------------------
     3. Smooth scroll for all anchor links (href="#...")
     ---------------------------------------------------------- */
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return; // skip bare # links

      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();

      const navHeight = nav ? nav.offsetHeight : 0;
      const targetY = target.getBoundingClientRect().top + window.scrollY - navHeight;

      window.scrollTo({
        top: targetY,
        behavior: 'smooth',
      });
    });
  });

})();
