// Highlight nav link on scroll
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navLinks.forEach((link) => {
          link.classList.toggle(
            'nav-link-active',
            link.getAttribute('href') === `#${entry.target.id}`
          );
        });
      }
    });
  },
  { rootMargin: '-40% 0px -55% 0px' }
);

sections.forEach((s) => observer.observe(s));

// Animate stat numbers on scroll into view
function animateValue(el, start, end, duration, prefix = '', suffix = '') {
  let startTime = null;
  const format = (n) => {
    if (n >= 1e9) return prefix + (n / 1e9).toFixed(1) + 'B' + suffix;
    if (n >= 1e6) return prefix + (n / 1e6).toFixed(1) + 'M' + suffix;
    return prefix + n.toLocaleString() + suffix;
  };
  const step = (timestamp) => {
    if (!startTime) startTime = timestamp;
    const progress = Math.min((timestamp - startTime) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = format(Math.floor(start + (end - start) * eased));
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = format(end);
  };
  requestAnimationFrame(step);
}

const bigStat = document.querySelector('.big-stat');
const mathBig = document.querySelector('.math-big');

const statsObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        entry.target.dataset.animated = 'true';
        if (entry.target === bigStat) {
          animateValue(entry.target, 0, 81500000000, 1800, '$');
        } else if (entry.target === mathBig) {
          // Just fade in the text — it's already styled
          entry.target.style.opacity = '0';
          entry.target.style.transform = 'scale(0.8)';
          entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'scale(1)';
          }, 100);
        }
      }
    });
  },
  { threshold: 0.5 }
);

if (bigStat) statsObserver.observe(bigStat);
if (mathBig) statsObserver.observe(mathBig);

// Stagger-in cards on scroll
const cards = document.querySelectorAll('.scam-card, .step, .tech-item');

const cardObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting && !entry.target.dataset.visible) {
        entry.target.dataset.visible = 'true';
        const delay = (parseInt(entry.target.dataset.index || 0)) * 60;
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, delay);
      }
    });
  },
  { threshold: 0.1 }
);

cards.forEach((card, i) => {
  card.dataset.index = i % 6;
  card.style.opacity = '0';
  card.style.transform = 'translateY(24px)';
  card.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
  cardObserver.observe(card);
});
