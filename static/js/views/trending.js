import { api } from '../api.js';
import { videoCard } from './home.js';

export async function renderTrending() {
  const app = document.getElementById('app');
  const data = await api.trending('JP');
  const list = Array.isArray(data) ? data : (data?.videos || []);
  app.innerHTML = `<h2 style="margin:8px 0 16px">急上昇</h2>
    <div class="grid">${list.map(videoCard).join('')}</div>`;
}
