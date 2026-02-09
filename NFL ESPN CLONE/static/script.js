document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('themeBtn');
    const htmlElement = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    const searchInput = document.getElementById('liveSearch');
    const teamLinks = document.querySelectorAll('.team-link');

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            teamLinks.forEach(link => {
                const name = link.querySelector('h3').textContent.toLowerCase();
                link.style.display = name.includes(term) ? 'block' : 'none';
            });
        });
    }

    const loader = document.getElementById('loading');
    const content = document.getElementById('scoreList');
    if (loader && content) {
        window.addEventListener('load', () => {
            loader.style.display = 'none';
            content.classList.remove('hidden');
        });
    }
});