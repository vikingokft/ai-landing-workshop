#!/usr/bin/env python3
"""Wrap real exports in an active, intentionally conflicting local WP-style host.
This is a preview builder, not a CSS fixer or a live WordPress compatibility test.
"""
import argparse
import html
from pathlib import Path
from urllib.parse import urlsplit


def probes(position):
    return f'''<aside class="wp-preview-probes" data-wp-preview-outside="{position}">
<h1 data-wp-preview-probe="heading">Környező sablon — {position}</h1>
<p data-wp-preview-probe="text">Ennek a környező tartalomnak a sablon színeit kell megtartania.</p>
<a href="#wp-preview-end" data-wp-preview-probe="link">Környező hivatkozás</a>
<button type="button" data-wp-preview-probe="button">Környező gomb</button>
<button type="button" disabled data-wp-preview-probe="disabled">Letiltott környező gomb</button>
<label data-wp-preview-probe="label">Környező mező
<input type="text" placeholder="Környező placeholder" data-wp-preview-probe="input"></label>
</aside>'''


def build(elementor, gutenberg_html, gutenberg_css, gutenberg_js, output, base_url=None, kit_token='local-preview'):
    fixture = (Path(__file__).resolve().parent.parent / 'assets/wp-preview-host.css').read_text(encoding='utf-8')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    base = ''
    if base_url:
        if urlsplit(base_url).scheme not in ('http', 'https'):
            raise ValueError('base-url must be a served HTTP(S) location')
        base = f'<base href="{html.escape(base_url, quote=True)}">'
    # Layout applies ONLY to fixture-owned probes, never to landing selectors.
    frame_css = '.wp-preview-probes{padding:24px;margin:16px;border:1px dashed #8798a8}.wp-preview-probes>*{margin:8px}.wp-preview-probes input{padding:8px}'
    variants = {
        'baseline': ('', ''),
        'elementor': ('', Path(elementor).read_text(encoding='utf-8')),
        'gutenberg': ('<style data-wp-export-css>' + Path(gutenberg_css).read_text(encoding='utf-8') + '</style>',
                      Path(gutenberg_html).read_text(encoding='utf-8') +
                      ('<script>' + Path(gutenberg_js).read_text(encoding='utf-8') + '</script>' if gutenberg_js else '')),
    }
    files = []
    for kind, (head, fragment) in variants.items():
        page = f'''<!doctype html><html lang="hu"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Helyi WordPress stílusütközés — {kind}</title>{base}
<style>{frame_css}</style>{head}</head>
<body class="wp-theme-simulation elementor-kit-{html.escape(kit_token, quote=True)}" data-wp-preview-kind="{kind}">
<main class="wp-site-blocks"><div class="entry-content">
{probes('before')}
{fragment}
{probes('after')}
</div></main><div id="wp-preview-end"></div>
<!-- Deliberately last: passing must not depend on the landing loading last. -->
<style data-wp-host-conflicts>{fixture}</style>
</body></html>'''
        target = output / (kind + '-conflicts.html')
        # Refuse to overwrite any input export with a preview wrapper.
        inputs = [elementor, gutenberg_html, gutenberg_css, gutenberg_js]
        if any(value and target.resolve() == Path(value).resolve() for value in inputs):
            raise ValueError('Preview output must be separate from the input exports')
        target.write_text(page, encoding='utf-8')
        files.append(target)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--elementor', required=True, type=Path)
    parser.add_argument('--gutenberg-html', required=True, type=Path)
    parser.add_argument('--gutenberg-css', required=True, type=Path)
    parser.add_argument('--gutenberg-js', type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--base-url', help='Optional HTTP(S) base for preview asset URLs')
    parser.add_argument('--kit-token', default='local-preview', help='Fixture-only class suffix; no production selector may depend on it')
    args = parser.parse_args()
    for path in build(args.elementor, args.gutenberg_html, args.gutenberg_css,
                      args.gutenberg_js, args.output_dir, args.base_url, args.kit_token):
        print(path)


if __name__ == '__main__':
    main()
