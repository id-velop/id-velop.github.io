const searchInput = document.querySelector('#tool-search');
const filterButtons = [...document.querySelectorAll('[data-filter]')];
const toolCards = [...document.querySelectorAll('.tool-card')];
const resultCount = document.querySelector('#result-count');
const emptyState = document.querySelector('#empty-state');
const resetButton = document.querySelector('#reset-search');

let activeFilter = 'all';

function updateCatalog() {
  const query = searchInput.value.trim().toLowerCase();
  let visibleCount = 0;

  toolCards.forEach((card) => {
    const platforms = card.dataset.platform.split(' ');
    const matchesFilter = activeFilter === 'all' || platforms.includes(activeFilter);
    const matchesSearch = !query || card.dataset.search.includes(query);
    const isVisible = matchesFilter && matchesSearch;

    card.classList.toggle('is-hidden', !isVisible);
    visibleCount += isVisible ? 1 : 0;
  });

  resultCount.textContent = `${visibleCount} ${visibleCount === 1 ? 'tool' : 'tools'}`;
  emptyState.hidden = visibleCount !== 0;
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    activeFilter = button.dataset.filter;
    filterButtons.forEach((item) => {
      const isActive = item === button;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-pressed', String(isActive));
    });
    updateCatalog();
  });
});

searchInput.addEventListener('input', updateCatalog);

resetButton.addEventListener('click', () => {
  searchInput.value = '';
  activeFilter = 'all';
  filterButtons.forEach((button) => {
    const isAll = button.dataset.filter === 'all';
    button.classList.toggle('is-active', isAll);
    button.setAttribute('aria-pressed', String(isAll));
  });
  updateCatalog();
  searchInput.focus();
});

document.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    searchInput.focus();
  }

  if (event.key === 'Escape' && document.activeElement === searchInput) {
    searchInput.value = '';
    updateCatalog();
    searchInput.blur();
  }
});
