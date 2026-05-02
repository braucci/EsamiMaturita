
// Scroll spy per la sidebar TOC
(() => {
  const headings = document.querySelectorAll('.exam-article h2, .exam-article h3');
  const tocLinks = document.querySelectorAll('.toc-list a');
  if (!tocLinks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        tocLinks.forEach(link => {
          link.classList.toggle('active', link.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-80px 0px -70% 0px' });

  headings.forEach(h => observer.observe(h));
})();

// Smooth-scroll con offset header
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', (e) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({ top, behavior: 'smooth' });
      history.replaceState(null, '', link.getAttribute('href'));
    }
  });
});
