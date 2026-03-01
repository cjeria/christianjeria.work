/* ============================================================
   CHRISTIAN JERIA — Portfolio Script
   ============================================================ */

(() => {
  'use strict';

  /* ----------------------------------------------------------
     0. Hash scroll offset — correct anchor position on page load
        so the floating nav doesn't overlap the target section
     ---------------------------------------------------------- */
  if (window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) {
      // Let the browser do its default jump first, then correct
      requestAnimationFrame(() => {
        const navHeight = document.getElementById('nav')?.offsetHeight || 0;
        const targetY = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
        window.scrollTo({ top: targetY, behavior: 'smooth' });
      });
    }
  }

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
     4. Hero avatar tilt + glare on hover
     ---------------------------------------------------------- */
  const avatar = document.querySelector('.hero-avatar');
  if (avatar) {
    const glare = document.createElement('div');
    glare.className = 'avatar-glare';
    avatar.appendChild(glare);

    let raf;
    let rotX = 0, rotY = 0;
    let tRotX = 0, tRotY = 0;
    let active = false;

    const lerp = (a, b, n) => a + (b - a) * n;

    function animateAvatar() {
      rotX = lerp(rotX, tRotX, 0.1);
      rotY = lerp(rotY, tRotY, 0.1);

      avatar.style.transform =
        `perspective(600px) rotateX(${rotX.toFixed(3)}deg) rotateY(${rotY.toFixed(3)}deg) scale(1.10)`;

      const settling =
        Math.abs(rotX - tRotX) > 0.05 ||
        Math.abs(rotY - tRotY) > 0.05;

      if (active || settling) {
        raf = requestAnimationFrame(animateAvatar);
      } else {
        avatar.style.transform = '';
      }
    }

    avatar.addEventListener('mouseenter', () => {
      active = true;
      avatar.style.transition = 'box-shadow 0.3s ease';
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(animateAvatar);
    });

    avatar.addEventListener('mousemove', (e) => {
      const r = avatar.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width;
      const y = (e.clientY - r.top)  / r.height;
      tRotX = (y - 0.5) * -30;
      tRotY = (x - 0.5) *  30;
      glare.style.background =
        `radial-gradient(circle at ${(x * 100).toFixed(1)}% ${(y * 100).toFixed(1)}%, rgba(255,255,255,0.245) 0%, transparent 65%)`;
    });

    avatar.addEventListener('mouseleave', () => {
      active  = false;
      tRotX   = 0;
      tRotY   = 0;
      avatar.style.transition = '';
      glare.style.background  = '';
    });
  }


  /* ----------------------------------------------------------
     5. Project card tilt + glare on hover (Andy Merskin style)
     ---------------------------------------------------------- */
  document.querySelectorAll('.project-card').forEach((card) => {
    // Inject glare overlay
    const glare = document.createElement('div');
    glare.className = 'card-glare';
    card.appendChild(glare);

    let raf;
    let rotX = 0, rotY = 0, lift = 0;
    let tRotX = 0, tRotY = 0, tLift = 0;
    let active = false;

    const lerp = (a, b, n) => a + (b - a) * n;

    function animate() {
      rotX = lerp(rotX, tRotX, 0.1);
      rotY = lerp(rotY, tRotY, 0.1);
      lift = lerp(lift, tLift,  0.1);

      card.style.transform =
        `perspective(800px) rotateX(${rotX.toFixed(3)}deg) rotateY(${rotY.toFixed(3)}deg) translateY(${lift.toFixed(3)}px)`;

      const settling =
        Math.abs(rotX - tRotX) > 0.05 ||
        Math.abs(rotY - tRotY) > 0.05 ||
        Math.abs(lift - tLift)  > 0.05;

      if (active || settling) {
        raf = requestAnimationFrame(animate);
      } else {
        card.style.transform   = '';
        card.style.transition  = '';
      }
    }

    card.addEventListener('mouseenter', () => {
      active = true;
      tLift  = -8;
      // Override the .reveal transition so JS owns the transform
      card.style.transition = 'box-shadow 0.3s ease, border-color 0.3s ease';
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(animate);
    });

    card.addEventListener('mousemove', (e) => {
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width;
      const y = (e.clientY - r.top)  / r.height;
      tRotX = (y - 0.5) * -14;
      tRotY = (x - 0.5) *  14;
      glare.style.background =
        `radial-gradient(circle at ${(x * 100).toFixed(1)}% ${(y * 100).toFixed(1)}%, rgba(255,255,255,0.28) 0%, transparent 65%)`;
    });

    card.addEventListener('mouseleave', () => {
      active = false;
      tRotX  = 0;
      tRotY  = 0;
      tLift  = 0;
      glare.style.background = '';
    });
  });


  /* ----------------------------------------------------------
     5. Lightbox — click project images to view in carousel
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
