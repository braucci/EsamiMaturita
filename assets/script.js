
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


// Filtro dell'indice generale degli argomenti
(() => {
  const input = document.querySelector('#topic-search');
  const links = Array.from(document.querySelectorAll('.topic-link'));
  const cards = Array.from(document.querySelectorAll('.topic-card'));
  const count = document.querySelector('#topic-count');
  if (!input || !links.length) return;

  const normalize = (text) => text.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

  input.addEventListener('input', () => {
    const query = normalize(input.value.trim());
    let visible = 0;
    links.forEach(link => {
      const haystack = normalize(link.dataset.topic || link.textContent);
      const match = !query || haystack.includes(query);
      link.classList.toggle('is-hidden', !match);
      if (match) visible += 1;
    });
    cards.forEach(card => {
      const hasVisibleLinks = card.querySelector('.topic-link:not(.is-hidden)');
      card.classList.toggle('is-empty', !hasVisibleLinks);
    });
    if (count) count.textContent = visible;
  });
})();
