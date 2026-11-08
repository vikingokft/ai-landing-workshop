'use strict';
const assert = require('node:assert/strict');
const api = require('./wp-media-resolver.js');
const batch = 'lp-test1234';
const hero = batch + '-a1b2c3d4-hero.webp';
const portrait = batch + '-e5f6a7b8-portrait.webp';
const record = (id, file, url, extra = {}) => ({id, source_url: url,
  media_details: {file, ...extra}, slug: 'not-the-filename'});
const response = (body, pages = '1', status = 200) => ({ok: status < 400, status,
  headers: {get: () => pages}, json: async () => body});
const tests = [];
function test(name, fn) { tests.push([name, fn]); }
const config = {batch, files: [hero], restRoot: 'https://example.test/blog/wp-json/'};

test('returned URLs work across upload months, custom folders and CDN hosts', () => {
  for (const url of ['https://example.test/wp-content/uploads/2026/11/' + hero,
    'https://example.test/wp-content/uploads/2027/02/' + hero,
    'https://cdn.example.test/custom/' + hero]) {
    const result = api.mapMedia([hero], [record(1, 'any/path/' + hero, url)]);
    assert.equal(result.urls[hero], url); assert.deepEqual(result.issues, []);
  }
});
test('scaled and collision-renamed files resolve without depending on attachment title/slug', () => {
  const scaled = hero.replace('.webp', '-scaled-2.webp');
  const result = api.mapMedia([hero], [record(1, '2027/03/' + scaled,
    'https://example.test/uploads/' + scaled)]);
  assert.equal(result.urls[hero], 'https://example.test/uploads/' + scaled);
});
test('original_image preserves matching with a rewritten CDN filename', () => {
  const url = 'https://cdn.example.test/opaque.avif';
  const result = api.mapMedia([hero], [record(1, 'opaque.avif', url, {original_image: hero})]);
  assert.equal(result.urls[hero], url);
});
test('duplicates are reported instead of selecting an arbitrary photo', () => {
  const rows = [record(1, hero, 'https://x.test/a/' + hero),
    record(2, hero, 'https://x.test/b/' + hero)];
  const result = api.mapMedia([hero], rows);
  assert.equal(result.urls[hero], undefined); assert.equal(result.issues[0].reason, 'ambiguous');
});
test('unrelated filenames, missing media and unsafe URLs are not accepted', () => {
  assert.equal(api.mapMedia([hero], [record(1, hero + '-unrelated.webp',
    'https://x.test/' + hero + '-unrelated.webp')]).issues[0].reason, 'missing');
  assert.equal(api.mapMedia([hero], []).issues[0].reason, 'missing');
  assert.equal(api.mapMedia([hero], [record(1, hero, 'javascript:alert(1)')])
    .issues[0].reason, 'invalid-url');
});
test('REST URL handles subdirectory and plain-permalink discovery roots', () => {
  let url = api.buildMediaURL('https://x.test/blog/wp-json/', batch);
  assert.equal(url.pathname, '/blog/wp-json/wp/v2/media');
  url = api.buildMediaURL('https://x.test/blog/?rest_route=/', batch, 2);
  assert.equal(url.pathname, '/blog/');
  assert.equal(url.searchParams.get('rest_route'), '/wp/v2/media');
  assert.equal(url.searchParams.get('page'), '2');
});
test('read-only discovery uses the WordPress link and omits credentials', async () => {
  let count = 0;
  const result = await api.discover({batch, files: [hero]}, {
    querySelector: () => ({href: 'https://x.test/site/?rest_route=/'})
  }, async (address, options) => {
    count++; const url = new URL(address);
    assert.equal(url.searchParams.get('search'), batch);
    assert.equal(url.searchParams.get('media_type'), 'image');
    assert.equal(options.credentials, 'omit');
    assert.equal(options.method, undefined);
    return response([record(1, hero, 'https://x.test/2030/12/' + hero)]);
  });
  assert.equal(count, 1); assert.ok(result.urls[hero]);
});
test('bounded pagination includes later results', async () => {
  let count = 0;
  const result = await api.discover({...config, files: [hero, portrait]}, null, async url => {
    count++;
    const file = new URL(url).searchParams.get('page') === '1' ? hero : portrait;
    return response([record(count, file, 'https://x.test/' + file)], '2');
  });
  assert.equal(count, 2); assert.ok(result.urls[hero]); assert.ok(result.urls[portrait]);
});
test('blocked API stops after one attempt', async () => {
  let count = 0;
  await assert.rejects(api.discover(config, null, async () => {
    count++; return response({}, '1', 403);
  }), /HTTP 403/);
  assert.equal(count, 1);
});
test('missing discovery and excessive results fail instead of guessing paths or scanning indefinitely', async () => {
  await assert.rejects(api.discover({batch, files: [hero]}, {querySelector: () => null},
    async () => { throw new Error('should not fetch'); }), /discovery link/);
  await assert.rejects(api.discover(config, null,
    async () => response([], '6')), /bounded result limit/);
});
test('resolved URL map requires no API access', async () => {
  const url = 'https://x.test/2019/04/' + hero;
  const result = await api.discover({batch, files: [hero], urlMap: {[hero]: url}}, null,
    async () => {throw new Error('should not fetch');});
  assert.equal(result.urls[hero], url);
});
test('DOM application covers images, CSS backgrounds and srcset; repeated initialization does not refetch', async () => {
  const image = {getAttribute: () => hero, setAttribute(key, val) {this[key] = val;}};
  const bg = {getAttribute: () => hero, style: {setProperty(key, val) {this[key] = val;}}};
  const source = {getAttribute: () => JSON.stringify([{file: hero, descriptor: '800w'}]),
    setAttribute(key, val) {this[key] = val;}};
  const notice = {hidden: true};
  const root = {dataset: {}, querySelector: () => notice, querySelectorAll(selector) {
    return selector === 'img[data-lp-media]' ? [image] :
      selector === '[data-lp-background]' ? [bg] : [source];
  }};
  const url = 'https://x.test/2028/06/' + hero;
  let count = 0;
  const options = {fetch: async () => {
    count++; return response([record(1, hero, url)]);
  }};
  const first = api.resolve(root, config, options);
  assert.equal(first, api.resolve(root, config, options));
  await first;
  assert.equal(count, 1); assert.equal(root.dataset.lpMediaState, 'ready');
  assert.equal(image.src, url); assert.equal(source.srcset, url + ' 800w');
  assert.ok(bg.style['--lp-media-image'].includes(url)); assert.equal(notice.hidden, true);
});
test('a DOM image omitted from the manifest is reported, not silently accepted', async () => {
  const image = {getAttribute: () => portrait, setAttribute() {throw new Error('wrong image');}};
  const notice = {hidden: true};
  const root = {dataset: {}, querySelector: () => notice, querySelectorAll(selector) {
    return selector === 'img[data-lp-media]' ? [image] : [];
  }};
  const result = await api.resolve(root, {...config, urlMap: {[hero]: 'https://x.test/' + hero}},
    {fetch: async () => {throw new Error('should not fetch');}});
  assert.equal(root.dataset.lpMediaState, 'partial'); assert.equal(notice.hidden, false);
  assert.equal(result.issues[0].reason, 'unresolved-reference');
});
test('partial results keep matched images and surface a visible notice', async () => {
  const notice = {hidden: true};
  const root = {dataset: {}, querySelector: () => notice, querySelectorAll: () => []};
  await api.resolve(root, config, {fetch: async () => response([])});
  assert.equal(root.dataset.lpMediaState, 'partial'); assert.equal(notice.hidden, false);
});
(async () => {
  for (const [name, fn] of tests) { await fn(); process.stdout.write('PASS ' + name + '\n'); }
  process.stdout.write(tests.length + ' checks passed (simulated REST responses, no live WordPress).\n');
})().catch(error => {process.stderr.write(error.stack + '\n'); process.exitCode = 1;});
