// Simple theme toggle for Django admin: stores choice in localStorage
(function(){
  const KEY = 'inventoryAdminTheme'; // 'auto' | 'light' | 'dark'
  function applyTheme(theme){
    document.documentElement.classList.remove('theme-auto','theme-light','theme-dark');
    document.documentElement.classList.add('theme-'+theme);
    // update buttons
    document.querySelectorAll('.theme-toggle button').forEach(btn=>{
      btn.setAttribute('aria-pressed', btn.dataset.theme === theme);
    });
  }

  function init(){
    const stored = localStorage.getItem(KEY) || 'auto';
    applyTheme(stored);
    document.addEventListener('click', function(e){
      const btn = e.target.closest && e.target.closest('.theme-toggle button');
      if(!btn) return;
      const theme = btn.dataset.theme;
      localStorage.setItem(KEY, theme);
      applyTheme(theme);
    });
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
