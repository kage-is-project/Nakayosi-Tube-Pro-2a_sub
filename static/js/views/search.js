import { api } from '../api.js';
import { videoCard, escapeHtml } from './home.js';

export async function renderSearch(q) {
  const app = document.getElementById('app');
  if (!q) { app.innerHTML = '<div class="error">検索語を入力してください</div>'; return; }
  document.getElementById('search-input').value = q;
  const data = await api.search(q);
  const list = (Array.isArray(data) ? data : []).filter(x => x.type === 'video' || x.videoId);
  app.innerHTML = `<h2 style="margin:8px 0 16px">検索結果: ${escapeHtml(q)}</h2>
    <div class="grid">${list.map(videoCard).join('')}</div>`;
}
