import { api, fmtViews, thumb } from '../api.js';
import { escapeHtml } from './home.js';

function pickStream(v) {
  // Invidious: formatStreams (progressive mp4) / adaptiveFormats / hlsUrl
  if (v.hlsUrl) return { type: 'hls', url: v.hlsUrl };
  const fs = (v.formatStreams || []).filter(f => f.container === 'mp4');
  if (fs.length) {
    fs.sort((a, b) => (parseInt(b.size || 0)) - (parseInt(a.size || 0)));
    return { type: 'mp4', url: fs[0].url };
  }
  return null;
}

export async function renderWatch(id) {
  const app = document.getElementById('app');
  if (!id) { app.innerHTML = '<div class="error">動画 ID がありません</div>'; return; }
  const v = await api.video(id);

  const stream = pickStream(v);
  const recs = (v.recommendedVideos || []).slice(0, 12);

  app.innerHTML = `<div class="watch">
    <div>
      <video id="player" class="player" controls playsinline poster="${thumb(v)}"></video>
      <h1>${escapeHtml(v.title || '')}</h1>
      <div class="meta">${fmtViews(v.viewCount)} · ${escapeHtml(v.publishedText || '')}</div>
      <div class="ch">
        <img src="${v.authorThumbnails?.[0]?.url || ''}" alt="" loading="lazy">
        <a href="/channel/${v.authorId}" data-link><strong>${escapeHtml(v.author || '')}</strong></a>
      </div>
      <div class="desc">${escapeHtml(v.description || '')}</div>
    </div>
    <aside class="sidebar">
      <h3>関連動画</h3>
      ${recs.map(r => `<a class="card" href="/watch?v=${r.videoId}" data-link>
        <img loading="lazy" src="${thumb(r)}" alt="">
        <div>
          <div class="title">${escapeHtml(r.title || '')}</div>
          <div class="meta">${escapeHtml(r.author || '')} · ${fmtViews(r.viewCount)}</div>
        </div>
      </a>`).join('')}
    </aside>
  </div>`;

  const player = document.getElementById('player');
  if (stream?.type === 'hls' && window.Hls?.isSupported()) {
    const hls = new Hls();
    hls.loadSource(stream.url);
    hls.attachMedia(player);
  } else if (stream) {
    player.src = stream.url;
  } else {
    player.outerHTML = '<div class="error">再生可能なストリームが見つかりませんでした</div>';
  }
}
