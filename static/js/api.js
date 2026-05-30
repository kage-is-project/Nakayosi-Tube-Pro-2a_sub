// 軽量 API クライアント
const cache = new Map();

async function jget(url) {
  if (cache.has(url)) return cache.get(url);
  const p = fetch(url).then(r => {
    if (!r.ok) throw new Error('HTTP ' + r.status);
    return r.json();
  });
  cache.set(url, p);
  p.catch(() => cache.delete(url));
  return p;
}

export const api = {
  trending: (region = 'JP') => jget(`/api/trending?region=${region}`),
  search: (q) => jget(`/api/search?v=${encodeURIComponent(q)}`),
  video: (id) => jget(`/api/video/${id}`),
  comments: (id) => jget(`/api/comments/${id}`),
  channel: (id) => jget(`/api/channel/${id}`),
};

export function fmtViews(n) {
  if (!n && n !== 0) return '';
  if (n >= 1e8) return (n / 1e8).toFixed(1) + '億回';
  if (n >= 1e4) return (n / 1e4).toFixed(1) + '万回';
  return n.toLocaleString() + '回';
}

export function thumb(v) {
  const id = v.videoId || v.url?.split('=')[1];
  return v.videoThumbnails?.[0]?.url || (id ? `https://i.ytimg.com/vi/${id}/mqdefault.jpg` : '');
}
