document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;

  // Додаємо кусок для плавного переходу (видаляється через 250ms)
  function withTransition(fn) {
    document.documentElement.classList.add('theme-transition');
    window.setTimeout(() => {
      document.documentElement.classList.remove('theme-transition');
    }, 250);
    fn && fn();
  }

  function applyTheme(theme) {
    try {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
        btn.textContent = '🌙';
        btn.setAttribute('aria-pressed', 'true');
      } else {
        document.documentElement.classList.remove('dark');
        btn.textContent = '☀️';
        btn.setAttribute('aria-pressed', 'false');
      }
      localStorage.setItem('theme', theme);
    } catch (e) { /* silent */ }
  }

  // Визначаємо початкову тему
  function detectInitialTheme() {
    try {
      const stored = localStorage.getItem('theme');
      if (stored === 'dark' || stored === 'light') return stored;
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
    } catch (e) {}
    return 'light';
  }

  // Ініціалізація стану
  const initial = detectInitialTheme();
  // застосуємо з плавним переходом
  withTransition(() => applyTheme(initial));

  btn.addEventListener('click', function () {
    const current = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    withTransition(() => applyTheme(next));
  });
});