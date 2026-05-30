// pushState ルーター (旧 #/home → /home に統一)
import { renderHome } from './views/home.js';
import { renderSearch } from './views/search.js';
import { renderWatch } from './views/watch.js';
import { renderTrending } from './views/trending.js';
import { renderChannel } from './views/channel.js';

const app = document.getElementById('app');

const routes = [
  { re: /^\/home\/?$/, view: renderHome },
  { re: /^\/trending\/?$/, view: renderTrending },
  { re: /^\/search\/?$/, view: (p, q) => renderSearch(q.get('v') || '') },
  { re: /^\/watch\/?$/, view: (p, q) => renderWatch(q.get('v')) },
  { re: /^\/channel\/([^/]+)\/?$/, view: (p, q, m) => renderChannel(m[1]) },
];

async function render() {
  const path = location.pathname;
  const query = new URLSearchParams(location.search);
  for (const r of routes) {
    const m = path.match(r.re);
    if (m) {
      app.innerHTML = '<div class="loading">読み込み中...</div>';
      try { await r.view(path, query, m, app); }
      catch (e) { app.innerHTML = `<div class="error">エラー: ${e.message}</div>`; }
      return;
    }
  }
  app.innerHTML = '<div class="error">ページが見つかりません</div>';
}

export function navigate(href) {
  history.pushState({}, '', href);
  render();
  window.scrollTo(0, 0);
}

// 旧 hash ルート (#/home, #/watch?v=..) を新形式へ変換
function normalizeHash() {
  const h = location.hash;
  if (h && h.startsWith('#/')) {
    const rest = h.slice(2); // "home" or "watch?v=xxx" or "@CHID"
    let newPath;
    if (rest.startsWith('@')) {
      newPath = '/channel/' + rest.slice(1);
    } else {
      // search?v=, watch?v=, home, trending etc.
      newPath = '/' + rest;
    }
    history.replaceState({}, '', newPath);
  }
}

document.addEventListener('click', (e) => {
  const a = e.target.closest('a[data-link]');
  if (!a) return;
  e.preventDefault();
  navigate(a.getAttribute('href'));
});

document.getElementById('search-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const v = document.getElementById('search-input').value.trim();
  if (v) navigate('/search?v=' + encodeURIComponent(v));
});

window.addEventListener('popstate', render);

normalizeHash();
render();

// グローバル公開 (view 内から使うため)
window.__navigate = navigate;
