/* FraudShield — Light/Dark Theme Toggle */
function toggleTheme() {
  var html = document.documentElement;
  var current = html.getAttribute('data-theme');
  if (current === 'light') {
    html.removeAttribute('data-theme');
    localStorage.setItem('fraudshield-theme', 'dark');
  } else {
    html.setAttribute('data-theme', 'light');
    localStorage.setItem('fraudshield-theme', 'light');
  }
}
