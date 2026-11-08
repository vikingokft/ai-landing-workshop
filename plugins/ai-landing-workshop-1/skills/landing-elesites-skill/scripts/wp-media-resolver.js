/* Include inline in the WordPress snippet, then call
   LandingDeliveryMediaV1.resolve(root, {batch, files, restRoot?, urlMap?}).
   Read-only public REST requests. No credentials or uploads. */
(function (scope) {
  'use strict';
  const running = new WeakMap();
  const imageName = /^[a-z0-9][a-z0-9-]*\.(?:jpe?g|png|webp|avif|gif)$/;
  const escapeRE = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  function basename(value) {
    try { return decodeURIComponent(String(value).split(/[?#]/)[0].split('/').pop()); }
    catch { return ''; }
  }
  function publicURL(value) {
    const url = new URL(value);
    if (!/^https?:$/.test(url.protocol) || url.username || url.password) {
      throw new Error('Invalid public media URL');
    }
    return url.href;
  }
  function validate(config) {
    if (!/^lp-[a-z0-9-]{6,80}$/.test(config.batch || '') || !Array.isArray(config.files)) {
      throw new Error('Invalid media manifest');
    }
    if (new Set(config.files).size !== config.files.length || config.files.some(file =>
      !imageName.test(file) || !file.startsWith(config.batch + '-'))) {
      throw new Error('Media filenames must be unique, lowercase, and prefixed with the batch');
    }
  }
  function buildMediaURL(restRoot, batch, page = 1) {
    const url = new URL(publicURL(restRoot));
    url.hash = '';
    if (url.searchParams.has('rest_route')) {
      const route = url.searchParams.get('rest_route').replace(/\/+$/, '');
      url.searchParams.set('rest_route', route + '/wp/v2/media');
    } else {
      url.pathname = url.pathname.replace(/\/+$/, '') + '/wp/v2/media';
    }
    url.searchParams.set('search', batch);
    url.searchParams.set('media_type', 'image');
    url.searchParams.set('per_page', '100');
    url.searchParams.set('page', String(page));
    url.searchParams.set('_fields', 'id,source_url,media_details');
    return url;
  }
  function mapMedia(files, records) {
    const unique = [...new Map(records.map(record => [record.id, record])).values()];
    const urls = Object.create(null);
    const issues = [];
    for (const file of files) {
      const stem = file.replace(/\.[^.]+$/, '');
      const variant = new RegExp('^' + escapeRE(stem) +
        '(?:-(?:scaled|rotated|[1-9][0-9]*))*\\.(?:jpe?g|png|webp|avif|gif)$', 'i');
      const candidates = unique.filter(record => {
        const names = [record.media_details?.file, record.media_details?.original_image,
          record.source_url].filter(Boolean).map(basename);
        return names.some(name => variant.test(name));
      });
      // Multiple attachment records are ambiguous, even if they have the same filename.
      if (candidates.length !== 1) {
        issues.push({file, reason: candidates.length ? 'ambiguous' : 'missing'});
        continue;
      }
      try { urls[file] = publicURL(candidates[0].source_url); }
      catch { issues.push({file, reason: 'invalid-url'}); }
    }
    return {urls, issues};
  }
  async function discover(config, doc, fetcher) {
    validate(config);
    const urls = Object.create(null);
    for (const file of config.files) {
      if (config.urlMap?.[file]) urls[file] = publicURL(config.urlMap[file]);
    }
    const needed = config.files.filter(file => !urls[file]);
    if (!needed.length) return {urls, issues: []};
    const restRoot = config.restRoot || doc?.querySelector('link[rel="https://api.w.org/"]')?.href;
    if (!restRoot) throw new Error('WordPress REST discovery link is missing');
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 10000);
    const records = [];
    try {
      let pages = 1;
      for (let page = 1; page <= pages; page++) {
        const response = await fetcher(buildMediaURL(restRoot, config.batch, page).href, {
          credentials: 'omit', headers: {Accept: 'application/json'}, signal: controller.signal
        });
        if (!response.ok) throw new Error('Media API HTTP ' + response.status);
        const body = await response.json();
        if (!Array.isArray(body) || body.some(record => !record || !Number.isInteger(record.id))) {
          throw new Error('Invalid media API response');
        }
        records.push(...body);
        const total = response.headers.get('X-WP-TotalPages');
        if (total !== null) {
          pages = Number(total);
          if (!Number.isInteger(pages) || pages < 0 || pages > 5) {
            throw new Error('Media search exceeded the bounded result limit');
          }
        } else if (body.length === 100) {
          // A full page without pagination headers could silently omit matches.
          throw new Error('Media search pagination is unavailable');
        }
      }
      const mapped = mapMedia(needed, records);
      return {urls: Object.assign(urls, mapped.urls), issues: mapped.issues};
    } finally { clearTimeout(timer); }
  }
  function apply(root, report) {
    function lookup(file) {
      if (report.urls[file]) return report.urls[file];
      if (!report.issues.some(issue => issue.file === file)) {
        report.issues.push({file, reason: 'unresolved-reference'});
      }
      return null;
    }
    root.querySelectorAll('img[data-lp-media]').forEach(img => {
      const url = lookup(img.getAttribute('data-lp-media'));
      if (url) img.setAttribute('src', url);
    });
    root.querySelectorAll('[data-lp-background]').forEach(element => {
      const url = lookup(element.getAttribute('data-lp-background'));
      if (url) element.style.setProperty('--lp-media-image', 'url(' + JSON.stringify(url) + ')');
    });
    root.querySelectorAll('[data-lp-srcset]').forEach(element => {
      try {
        const entries = JSON.parse(element.getAttribute('data-lp-srcset'));
        if (!Array.isArray(entries) || !entries.length) throw new Error('Empty srcset');
        const set = entries.map(entry => {
          if (!report.urls[entry.file] || !/^\d+(?:w|x)$/.test(entry.descriptor)) {
            throw new Error('Unresolved srcset');
          }
          return report.urls[entry.file] + ' ' + entry.descriptor;
        });
        element.setAttribute('srcset', set.join(', '));
      } catch { report.issues.push({reason: 'invalid-or-unresolved-srcset'}); }
    });
  }
  function notice(root, failed) {
    const element = root.querySelector('[data-lp-media-status]');
    if (element) {
      element.hidden = !failed;
      if (failed) element.textContent = 'Néhány kép nem tölthető be. Kérlek, frissítsd az oldalt.';
    }
  }
  function resolve(root, config, options = {}) {
    if (running.has(root)) return running.get(root);
    root.dataset.lpMediaState = 'loading';
    const promise = discover(config, options.document || scope.document,
      options.fetch || scope.fetch.bind(scope)).then(report => {
        apply(root, report);
        root.dataset.lpMediaState = report.issues.length ? 'partial' : 'ready';
        notice(root, report.issues.length > 0);
        return report;
      }).catch(error => {
        root.dataset.lpMediaState = 'error';
        notice(root, true);
        throw error;
      });
    running.set(root, promise);
    return promise;
  }
  const api = {buildMediaURL, mapMedia, discover, resolve};
  if (typeof module === 'object' && module.exports) module.exports = api;
  else scope.LandingDeliveryMediaV1 = scope.LandingDeliveryMediaV1 || api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
