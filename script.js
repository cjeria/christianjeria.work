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

  /* ----------------------------------------------------------
     4. Lightbox — click project images to view in carousel
     ---------------------------------------------------------- */
  const projectImgs = Array.from(document.querySelectorAll('.project-img'));

  if (projectImgs.length > 0) {
    // Build lightbox DOM
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.innerHTML = `
      <div class="lightbox-inner">
        <img class="lightbox-img" src="" alt="" />
        <button class="lightbox-close" aria-label="Close">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1 1l14 14M15 1L1 15" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>
          </svg>
        </button>
        <button class="lightbox-btn prev" aria-label="Previous image">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 2L4 8l6 6" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <button class="lightbox-btn next" aria-label="Next image">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M6 2l6 6-6 6" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
        <span class="lightbox-counter"></span>
      </div>
    `;
    document.body.appendChild(lightbox);

    const lbImg     = lightbox.querySelector('.lightbox-img');
    const lbClose   = lightbox.querySelector('.lightbox-close');
    const lbPrev    = lightbox.querySelector('.lightbox-btn.prev');
    const lbNext    = lightbox.querySelector('.lightbox-btn.next');
    const lbCounter = lightbox.querySelector('.lightbox-counter');

    let current = 0;

    function openLightbox(index) {
      current = index;
      update();
      lightbox.style.display = 'flex';
      requestAnimationFrame(() => lightbox.classList.add('is-open'));
      document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.classList.remove('is-open');
      lightbox.addEventListener('transitionend', () => {
        lightbox.style.display = 'none';
        document.body.style.overflow = '';
      }, { once: true });
    }

    function update() {
      const img = projectImgs[current];
      lbImg.src = img.src;
      lbImg.alt = img.alt;
      lbCounter.textContent = `${current + 1} / ${projectImgs.length}`;
      lbPrev.disabled = current === 0;
      lbNext.disabled = current === projectImgs.length - 1;
    }

    // Click on any project image
    projectImgs.forEach((img, i) => {
      img.addEventListener('click', () => openLightbox(i));
    });

    // Controls
    lbClose.addEventListener('click', closeLightbox);
    lbPrev.addEventListener('click', (e) => { e.stopPropagation(); if (current > 0) { current--; update(); } });
    lbNext.addEventListener('click', (e) => { e.stopPropagation(); if (current < projectImgs.length - 1) { current++; update(); } });

    // Click backdrop to close
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
      if (!lightbox.classList.contains('is-open')) return;
      if (e.key === 'Escape')      closeLightbox();
      if (e.key === 'ArrowLeft'  && current > 0)                       { current--; update(); }
      if (e.key === 'ArrowRight' && current < projectImgs.length - 1)  { current++; update(); }
    });

    // Hide initially
    lightbox.style.display = 'none';
  }

})();
