/* ============================================================
   LEADCORE AI — app.js
   Scroll-driven canvas, GSAP animations, Lenis smooth scroll
   ============================================================ */

const FRAME_COUNT = 97;
const FRAME_SPEED = 2.0; // product animation completes by ~55% scroll
const IMAGE_SCALE = 0.85;
const FAST_LOAD   = 10;   // frames to load immediately for first paint

/* ---- ELEMENT REFS ---- */
const loader       = document.getElementById('loader');
const loaderBar    = document.getElementById('loader-bar');
const loaderPct    = document.getElementById('loader-percent');
const canvas       = document.getElementById('canvas');
const canvasWrap   = document.getElementById('canvas-wrap');
const scrollCont   = document.getElementById('scroll-container');
const darkOverlay  = document.getElementById('dark-overlay');
const marqueeWrap  = document.getElementById('marquee-wrap');
const header       = document.getElementById('site-header');
const ctx          = canvas.getContext('2d');

let frames        = new Array(FRAME_COUNT).fill(null);
let currentFrame  = 0;
let bgColor       = '#06060f';
let lenisRef      = null;

/* ============================================================
   1. LENIS SMOOTH SCROLL
   ============================================================ */
function initLenis() {
  const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smoothWheel: true,
  });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
  lenisRef = lenis;
}

/* ============================================================
   2. CANVAS RESIZE
   ============================================================ */
function resizeCanvas() {
  const dpr = window.devicePixelRatio || 1;
  canvas.width  = window.innerWidth  * dpr;
  canvas.height = window.innerHeight * dpr;
  ctx.scale(dpr, dpr);
  drawFrame(currentFrame);
}
window.addEventListener('resize', resizeCanvas);

/* ============================================================
   3. BACKGROUND COLOR SAMPLER
   ============================================================ */
function sampleBgColor(img) {
  if (!img) return;
  const offscreen = document.createElement('canvas');
  offscreen.width  = 10;
  offscreen.height = 10;
  const octx = offscreen.getContext('2d');
  octx.drawImage(img, 0, 0, 10, 10);
  const d = octx.getImageData(0, 0, 1, 1).data;
  bgColor = `rgb(${d[0]},${d[1]},${d[2]})`;
}

/* ============================================================
   4. CANVAS RENDERER — padded cover
   ============================================================ */
function drawFrame(index) {
  const img = frames[index];
  if (!img) return;
  const cw = canvas.width  / (window.devicePixelRatio || 1);
  const ch = canvas.height / (window.devicePixelRatio || 1);
  const iw = img.naturalWidth;
  const ih = img.naturalHeight;
  const scale = Math.max(cw / iw, ch / ih) * IMAGE_SCALE;
  const dw = iw * scale;
  const dh = ih * scale;
  const dx = (cw - dw) / 2;
  const dy = (ch - dh) / 2;
  ctx.fillStyle = bgColor;
  ctx.fillRect(0, 0, cw, ch);
  ctx.drawImage(img, dx, dy, dw, dh);
}

/* ============================================================
   5. FRAME PRELOADER (two-phase)
   ============================================================ */
function loadFrame(i) {
  return new Promise((resolve) => {
    const img = new Image();
    const num = String(i + 1).padStart(4, '0');
    img.src = `frames/frame_${num}.webp`;
    img.onload = () => {
      frames[i] = img;
      if (i % 20 === 0) sampleBgColor(img);
      resolve();
    };
    img.onerror = resolve;
  });
}

async function preloadFrames() {
  // Phase 1: first FAST_LOAD frames immediately
  const phase1 = Array.from({ length: FAST_LOAD }, (_, i) => loadFrame(i));
  await Promise.all(phase1);
  resizeCanvas();
  drawFrame(0);

  // Phase 2: rest in background, track progress
  const total = FRAME_COUNT;
  let loaded = FAST_LOAD;
  const updateUI = () => {
    const pct = Math.round((loaded / total) * 100);
    loaderBar.style.width = pct + '%';
    loaderPct.textContent = pct + '%';
  };
  updateUI();

  const phase2 = [];
  for (let i = FAST_LOAD; i < FRAME_COUNT; i++) {
    phase2.push(
      loadFrame(i).then(() => {
        loaded++;
        updateUI();
      })
    );
  }
  await Promise.all(phase2);

  // Hide loader
  loader.classList.add('hidden');
  initScene();
}

/* ============================================================
   6. FRAME-TO-SCROLL BINDING
   ============================================================ */
function initFrameScroll() {
  ScrollTrigger.create({
    trigger: scrollCont,
    start: 'top top',
    end: 'bottom bottom',
    scrub: true,
    onUpdate: (self) => {
      const accelerated = Math.min(self.progress * FRAME_SPEED, 1);
      const index = Math.min(Math.floor(accelerated * FRAME_COUNT), FRAME_COUNT - 1);
      if (index !== currentFrame) {
        currentFrame = index;
        requestAnimationFrame(() => drawFrame(currentFrame));
      }
    },
  });
}

/* ============================================================
   7. HERO CIRCLE-WIPE TRANSITION
   ============================================================ */
function initHeroTransition() {
  const heroSection = document.getElementById('hero');
  ScrollTrigger.create({
    trigger: scrollCont,
    start: 'top top',
    end: 'bottom bottom',
    scrub: true,
    onUpdate: (self) => {
      const p = self.progress;
      // Hero fades out quickly
      heroSection.style.opacity = Math.max(0, 1 - p * 18).toString();
      heroSection.style.transform = `translateY(${-p * 40}px)`;
      // Canvas circle-wipe reveal
      const wipeProgress = Math.min(1, Math.max(0, (p - 0.01) / 0.07));
      const radius = wipeProgress * 80;
      canvasWrap.style.clipPath = `circle(${radius}% at 50% 50%)`;
    },
  });
}

/* ============================================================
   8. MARQUEE
   ============================================================ */
function initMarquee() {
  const speed = parseFloat(marqueeWrap.dataset.scrollSpeed) || -28;
  gsap.to(marqueeWrap.querySelector('.marquee-text'), {
    xPercent: speed,
    ease: 'none',
    scrollTrigger: {
      trigger: scrollCont,
      start: 'top top',
      end: 'bottom bottom',
      scrub: true,
    },
  });

  // Show/hide marquee during scroll window
  ScrollTrigger.create({
    trigger: scrollCont,
    start: 'top top',
    end: 'bottom bottom',
    scrub: false,
    onEnter: () => marqueeWrap.classList.add('visible'),
    onLeave: () => marqueeWrap.classList.remove('visible'),
    onEnterBack: () => marqueeWrap.classList.add('visible'),
    onLeaveBack: () => marqueeWrap.classList.remove('visible'),
  });
}

/* ============================================================
   9. DARK OVERLAY (stats section, enter 58%, leave 73%)
   ============================================================ */
function initDarkOverlay(enterPct, leavePct) {
  const enter = enterPct / 100;
  const leave = leavePct / 100;
  const fadeRange = 0.04;

  ScrollTrigger.create({
    trigger: scrollCont,
    start: 'top top',
    end: 'bottom bottom',
    scrub: true,
    onUpdate: (self) => {
      const p = self.progress;
      let opacity = 0;
      if (p >= enter - fadeRange && p <= enter) {
        opacity = (p - (enter - fadeRange)) / fadeRange;
      } else if (p > enter && p < leave) {
        opacity = 0.9;
      } else if (p >= leave && p <= leave + fadeRange) {
        opacity = 0.9 * (1 - (p - leave) / fadeRange);
      }
      darkOverlay.style.opacity = opacity;
    },
  });
}

/* ============================================================
   10. SECTION POSITION — absolute at midpoint of enter/leave
   ============================================================ */
function positionSections() {
  const containerH = scrollCont.offsetHeight;
  document.querySelectorAll('.scroll-section').forEach((section) => {
    const enter = parseFloat(section.dataset.enter) / 100;
    const leave = parseFloat(section.dataset.leave) / 100;
    const midpoint = (enter + leave) / 2;
    section.style.top = `${midpoint * containerH}px`;
    section.style.transform = 'translateY(-50%)';
  });
}

/* ============================================================
   11. SECTION ANIMATION SYSTEM
   ============================================================ */
function setupSectionAnimation(section) {
  const type    = section.dataset.animation;
  const persist = section.dataset.persist === 'true';
  const enter   = parseFloat(section.dataset.enter) / 100;
  const leave   = parseFloat(section.dataset.leave) / 100;

  const children = section.querySelectorAll(
    '.section-label, .section-heading, .section-body, .section-note, .cta-button, .stat, .pain-list, .pillar-list, .steps-list, .service-list, .pillar, .step, .service-item, .cta-buttons, .btn, .stats-footnote, .pain-list li'
  );

  // Make section visible (controlled by scroll)
  section.style.visibility = 'visible';

  const tl = gsap.timeline({ paused: true });

  switch (type) {
    case 'fade-up':
      tl.from(children, { y: 50, opacity: 0, stagger: 0.12, duration: 0.9, ease: 'power3.out' });
      break;
    case 'slide-left':
      tl.from(children, { x: -80, opacity: 0, stagger: 0.13, duration: 0.9, ease: 'power3.out' });
      break;
    case 'slide-right':
      tl.from(children, { x: 80, opacity: 0, stagger: 0.13, duration: 0.9, ease: 'power3.out' });
      break;
    case 'scale-up':
      tl.from(children, { scale: 0.88, opacity: 0, stagger: 0.12, duration: 1.0, ease: 'power2.out' });
      break;
    case 'rotate-in':
      tl.from(children, { y: 40, rotation: 3, opacity: 0, stagger: 0.1, duration: 0.9, ease: 'power3.out' });
      break;
    case 'stagger-up':
      tl.from(children, { y: 60, opacity: 0, stagger: 0.15, duration: 0.8, ease: 'power3.out' });
      break;
    case 'clip-reveal':
      tl.from(children, { clipPath: 'inset(100% 0 0 0)', opacity: 0, stagger: 0.15, duration: 1.2, ease: 'power4.inOut' });
      break;
    default:
      tl.from(children, { opacity: 0, stagger: 0.1, duration: 0.8, ease: 'power2.out' });
  }

  // Drive animation via scroll progress
  ScrollTrigger.create({
    trigger: scrollCont,
    start: 'top top',
    end: 'bottom bottom',
    scrub: false,
    onUpdate: (self) => {
      const p = self.progress;
      const range = leave - enter;
      const buffer = range * 0.1;

      if (p >= enter && p < leave) {
        // How far into the window (0-1)
        const local = (p - enter) / range;
        gsap.set(section, { opacity: 1 });
        tl.progress(Math.min(local * 2, 1)); // full anim in first half of window
        if (!persist && local > 0.85) {
          // fade out near end of window
          gsap.to(section, { opacity: Math.max(0, 1 - (local - 0.85) / 0.15), duration: 0.1, overwrite: true });
        }
      } else if (persist && p >= leave) {
        gsap.set(section, { opacity: 1 });
        tl.progress(1);
      } else {
        gsap.set(section, { opacity: 0 });
        if (!persist) tl.progress(0);
      }
    },
  });
}

/* ============================================================
   12. COUNTER ANIMATIONS
   ============================================================ */
function initCounters() {
  document.querySelectorAll('.stat-number').forEach((el) => {
    const target   = parseFloat(el.dataset.value);
    const decimals = parseInt(el.dataset.decimals || '0');
    const statSection = el.closest('.scroll-section');
    if (!statSection) return;

    const enter = parseFloat(statSection.dataset.enter) / 100;

    ScrollTrigger.create({
      trigger: scrollCont,
      start: 'top top',
      end: 'bottom bottom',
      onUpdate: (self) => {
        if (self.progress >= enter && !el._counted) {
          el._counted = true;
          gsap.fromTo(
            el,
            { textContent: 0 },
            {
              textContent: target,
              duration: 2,
              ease: 'power1.out',
              snap: { textContent: decimals === 0 ? 1 : 0.1 },
              onUpdate() {
                el.textContent = decimals === 0
                  ? Math.round(parseFloat(el.textContent))
                  : parseFloat(el.textContent).toFixed(decimals);
              },
            }
          );
        }
        // Reset on scroll back
        if (self.progress < enter - 0.05) {
          el._counted = false;
          el.textContent = '0';
        }
      },
    });
  });
}

/* ============================================================
   13. STICKY NAV SCROLL STATE
   ============================================================ */
function initNav() {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  // Mobile menu toggle
  const toggle = document.getElementById('nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      document.querySelector('.nav-links')?.classList.toggle('mobile-open');
      document.querySelector('.nav-cta')?.classList.toggle('mobile-open');
    });
  }
}

/* ============================================================
   14. FAQ ACCORDION
   ============================================================ */
function initFAQ() {
  document.querySelectorAll('.faq-q').forEach((btn) => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll('.faq-item.open').forEach((i) => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });
}

/* ============================================================
   15. HERO WORD SPLIT ENTRANCE
   ============================================================ */
function initHeroEntrance() {
  const words = document.querySelectorAll('.hero-word');
  gsap.from(words, {
    y: 80,
    opacity: 0,
    stagger: 0.12,
    duration: 1.1,
    ease: 'power4.out',
    delay: 0.3,
  });
  gsap.from('.hero-tagline, .hero-ctas, .hero-trust-strip, .hero-scroll-indicator', {
    y: 30,
    opacity: 0,
    stagger: 0.1,
    duration: 0.9,
    ease: 'power3.out',
    delay: 0.7,
  });
  gsap.from('.hero-label', {
    y: 20,
    opacity: 0,
    duration: 0.7,
    ease: 'power2.out',
    delay: 0.2,
  });
}

/* ============================================================
   16. POST-SCROLL SECTION REVEALS
   ============================================================ */
function initPostScrollAnimations() {
  const sections = [
    '.section-trust',
    '.section-why',
    '.section-industries',
    '.section-faq',
    '.section-final-cta',
  ];
  sections.forEach((sel) => {
    const el = document.querySelector(sel);
    if (!el) return;
    const children = el.querySelectorAll(
      '.trust-tags span, .trust-stat, .why-card, .industry-card, .section-label-static, .section-heading-static, .trust-intro, .trust-stats, .faq-item, .final-cta-heading, .final-cta-sub, .btn-xl, .final-cta-micro'
    );
    gsap.from(children, {
      y: 40,
      opacity: 0,
      stagger: 0.07,
      duration: 0.8,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: el,
        start: 'top 80%',
        toggleActions: 'play none none reverse',
      },
    });
  });
}

/* ============================================================
   INIT SCENE (called after all frames loaded)
   ============================================================ */
function initScene() {
  gsap.registerPlugin(ScrollTrigger);
  initLenis();
  resizeCanvas();
  positionSections();

  initHeroTransition();
  initFrameScroll();
  initMarquee();
  initDarkOverlay(58, 73);

  document.querySelectorAll('.scroll-section').forEach(setupSectionAnimation);
  initCounters();
  initHeroEntrance();
  initPostScrollAnimations();
  initNav();
  initFAQ();

  // Recalculate on resize
  window.addEventListener('resize', () => {
    positionSections();
    resizeCanvas();
  });
}

/* ============================================================
   BOOT
   ============================================================ */
preloadFrames();
