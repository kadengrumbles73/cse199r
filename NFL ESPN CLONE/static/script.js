document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Initialization
    const htmlElement = document.documentElement;
    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-theme', savedTheme);

    const themeBtn = document.getElementById('themeBtn');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            htmlElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // 2. Instant Loader Fix
    const loader = document.getElementById('loading');
    const content = document.getElementById('scoreList');
    if (loader && content) {
        loader.style.display = 'none';
        content.classList.remove('hidden');
    }

    // 3. Search logic with Division Hiding
    const searchInput = document.getElementById('liveSearch');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const blocks = document.querySelectorAll('.division-block');

            blocks.forEach(block => {
                const teams = block.querySelectorAll('.team-link');
                let hasVisibleTeam = false;

                teams.forEach(team => {
                    const name = team.textContent.toLowerCase();
                    if (name.includes(term)) {
                        team.style.display = 'block';
                        hasVisibleTeam = true;
                    } else {
                        team.style.display = 'none';
                    }
                });

                block.style.display = hasVisibleTeam ? 'block' : 'none';
            });
        });
    }
});