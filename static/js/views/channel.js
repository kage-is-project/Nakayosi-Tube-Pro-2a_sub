import { api } from '../api.js';
import { videoCard, escapeHtml } from './home.js';

export async function renderChannel(id) {
  const app = document.getElementById('app');
  const c = await api.channel(id);
  const vids = c.latestVideos || c.videos || [];
  app.innerHTML = `<h2>${escapeHtml(c.author || '')}</h2>
    <p class="meta">${escapeHtml(c.description || '')}</p>
    <div class="grid">${vids.map(videoCard).join('')}</div>`;
}
