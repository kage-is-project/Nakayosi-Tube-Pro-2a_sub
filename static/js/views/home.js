import { api, fmtViews, thumb } from '../api.js';

function videoCard(v) {
  const id = v.videoId;
  return `<a class="card" href="/watch?v=${id}" data-link>
    <img loading="lazy" src="${thumb(v)}" alt="">
    <div class="title">${escapeHtml(v.title || '')}</div>
    <div class="meta">${escapeHtml(v.author || '')} · ${fmtViews(v.viewCount)}</div>
  </a>`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
}

export async function renderHome() {
  const app = document.getElementById('app');
  // ホームはトレンディングを流用 (軽量・最速)
  const data = await api.trending('JP');
  const list = Array.isArray(data) ? data : (data?.videos || []);
  app.innerHTML = `<h2 style="margin:8px 0 16px">おすすめ</h2>
    <div class="grid">${list.slice(0, 48).map(videoCard).join('')}</div>`;
}

export { videoCard, escapeHtml };
