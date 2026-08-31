/**
 * Nirnay Decision Audit AI - Interactive & Animation Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  initBgCanvas();
  initScrollProgress();
  initScrollReveal();
  initNavbarScroll();
  initInteractiveSimulators();
});

/* -------------------------------------------------------------------------- */
/* 1. Cryptographic Node Mesh Canvas Background                                */
/* -------------------------------------------------------------------------- */
function initBgCanvas() {
  let canvas = document.getElementById('bg-canvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'bg-canvas';
    document.body.prepend(canvas);
  }

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  let mouse = { x: null, y: null, radius: 150 };

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    createParticles();
  }

  window.addEventListener('resize', resize);
  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });
  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.4;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.size = Math.random() * 2.5 + 1;
      const colors = ['rgba(28, 82, 206, 0.4)', 'rgba(18, 33, 63, 0.3)', 'rgba(63, 108, 232, 0.4)', 'rgba(123, 137, 172, 0.3)'];
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.isHashNode = Math.random() > 0.8;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;

      if (mouse.x !== null && mouse.y !== null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouse.radius) {
          const force = (mouse.radius - dist) / mouse.radius;
          this.x -= (dx / dist) * force * 1.5;
          this.y -= (dy / dist) * force * 1.5;
        }
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = this.color;
      ctx.fill();

      if (this.isHashNode) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 2.5, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(42, 91, 215, 0.15)';
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    }
  }

  function createParticles() {
    particles = [];
    const count = Math.min(Math.floor((width * height) / 18000), 55);
    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }
  }

  resize();

  function animate() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 130) {
          const alpha = (1 - dist / 130) * 0.18;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(42, 91, 215, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    particles.forEach((p) => {
      p.update();
      p.draw();
    });

    requestAnimationFrame(animate);
  }

  animate();
}

/* -------------------------------------------------------------------------- */
/* 2. Scroll Progress Bar                                                      */
/* -------------------------------------------------------------------------- */
function initScrollProgress() {
  let bar = document.getElementById('scroll-progress-bar');
  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'scroll-progress-bar';
    document.body.appendChild(bar);
  }

  window.addEventListener('scroll', () => {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    bar.style.width = (scrolled || 0) + '%';
  });
}

/* -------------------------------------------------------------------------- */
/* 3. Intersection Observer Scroll Reveal                                      */
/* -------------------------------------------------------------------------- */
function initScrollReveal() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      }
    });
  }, observerOptions);

  const revealElements = document.querySelectorAll('.reveal-on-scroll, .reveal-scale, .reveal-left, .reveal-right');
  revealElements.forEach(el => observer.observe(el));
}

/* -------------------------------------------------------------------------- */
/* 4. Sticky Glass Navbar Scroll Transition                                   */
/* -------------------------------------------------------------------------- */
function initNavbarScroll() {
  const nav = document.querySelector('nav');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      nav.classList.add('nav-scrolled');
    } else {
      nav.classList.remove('nav-scrolled');
    }
  });
}

/* -------------------------------------------------------------------------- */
/* 5. Interactive Simulators across Pages                                     */
/* -------------------------------------------------------------------------- */
function initInteractiveSimulators() {
  const verifyBtn = document.getElementById('verify-hash-btn');
  const hashInput = document.getElementById('decision-hash-input');
  const verifyResult = document.getElementById('verification-result');

  if (verifyBtn && hashInput && verifyResult) {
    verifyBtn.addEventListener('click', () => {
      verifyBtn.disabled = true;
      verifyBtn.innerHTML = `
        <span class="inline-block animate-spin mr-2">
          <span class="material-symbols-outlined text-[18px]">sync</span>
        </span>
        Checking Ledger...
      `;

      setTimeout(() => {
        verifyBtn.disabled = false;
        verifyBtn.innerHTML = `
          <span>Verify Hash</span>
          <span class="material-symbols-outlined text-[18px]">verified</span>
        `;
        verifyResult.classList.remove('hidden');
        verifyResult.classList.add('reveal-scale', 'is-visible');
        verifyResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 1200);
    });
  }

  const askForm = document.getElementById('ask-question-form');
  const aiAnswerCard = document.getElementById('ai-answer-card');
  const aiAnswerText = document.getElementById('ai-answer-text');

  if (askForm && aiAnswerCard && aiAnswerText) {
    askForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const questionInput = document.getElementById('question-input');
      if (!questionInput || !questionInput.value.trim()) return;

      aiAnswerCard.classList.remove('hidden');
      aiAnswerCard.classList.add('reveal-on-scroll', 'is-visible');
      aiAnswerText.innerHTML = '<span class="animate-pulse text-secondary">Analyzing ingested policy documents and verifying cryptographic merkle proofs...</span>';

      const fullAnswer = `Based on <strong>Policy Document 4.2 (Section 8.1 - Expenditure Authorization)</strong>, emergency purchases under $50,000 do not require prior board approval provided they receive dual-signoff from the Department Head and CFO. All decisions are registered with cryptographic SHA-256 signatures.`;

      setTimeout(() => {
        aiAnswerText.innerHTML = fullAnswer;
        aiAnswerCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 1400);
    });
  }

  const dropZone = document.getElementById('upload-drop-zone');
  const fileInput = document.getElementById('file-upload-input');
  const uploadStatus = document.getElementById('upload-status-card');

  if (dropZone && uploadStatus) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.add('border-secondary', 'bg-secondary/5');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.remove('border-secondary', 'bg-secondary/5');
      }, false);
    });

    dropZone.addEventListener('drop', (e) => {
      handleFiles(e.dataTransfer.files);
    });

    if (fileInput) {
      fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
      });
    }

    function handleFiles(files) {
      if (!files || files.length === 0) return;
      const file = files[0];

      uploadStatus.classList.remove('hidden');
      uploadStatus.classList.add('reveal-scale', 'is-visible');
      
      const fileNameEl = document.getElementById('upload-filename');
      const progressEl = document.getElementById('upload-progress-bar');
      const badgeEl = document.getElementById('upload-status-badge');

      if (fileNameEl) fileNameEl.textContent = file.name;
      if (progressEl) progressEl.style.width = '0%';
      if (badgeEl) badgeEl.textContent = 'Ingesting & Hashing...';

      let prog = 0;
      const interval = setInterval(() => {
        prog += 25;
        if (progressEl) progressEl.style.width = prog + '%';
        if (prog >= 100) {
          clearInterval(interval);
          if (badgeEl) {
            badgeEl.textContent = 'Indexed & Blockchain Anchored';
            badgeEl.className = 'text-[10px] bg-emerald-500/10 text-emerald-600 px-2 py-0.5 rounded-full font-semibold flex items-center gap-1';
            badgeEl.innerHTML = '<span class="material-symbols-outlined text-[14px]">check_circle</span> Verified';
          }
        }
      }, 300);
    }
  }
}
