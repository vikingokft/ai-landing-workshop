#!/usr/bin/env python3
"""Create browser regression fixtures and test preview wrapping, not CSS rendering."""
import argparse
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location('preview_builder', Path(__file__).with_name('build-wp-style-preview.py'))
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def markup(root):
    return f'''<div id="{root}">
<section class="dark"><h1 data-color-test="dark-heading">Világos cím <em data-color-test="accent">kiemeléssel</em></h1>
<p data-color-test="text">A landing saját szövege.</p>
<a data-color-test="link" href="#fixture-end">Szöveges link</a>
<a class="cta" data-color-test="cta" href="#fixture-end">Gombszerű link</a>
<button type="button" data-color-test="button">Elsődleges gomb</button>
<button type="button" class="secondary" data-color-test="secondary">Másodlagos gomb</button>
<button type="button" disabled data-color-test="disabled">Letiltott gomb</button>
<label data-color-test="label">Mezőcímke <input data-color-test="input" placeholder="Landing placeholder"></label>
<textarea data-color-test="textarea" placeholder="Szöveg"></textarea>
<select data-color-test="select"><option>Választás</option></select>
</section><section class="light"><h2 data-color-test="light-heading">Sötét cím világos felületen</h2>
<a data-color-test="light-link" href="#fixture-end">Világos panel linkje</a></section>
<div id="fixture-end"></div></div>'''


def styles(root):
    return '''
#ROOT { --lp-text:#fff7f9; --lp-heading:#fff7f9; --lp-link:#f2bfd0; --lp-accent:#e7a3bd; background:#342734; color:var(--lp-text); font-family:Georgia,serif; padding:30px; }
#ROOT .light { --lp-text:#302a33; --lp-heading:#302a33; --lp-link:#7c3f59; background:#fffaf7; padding:24px; }
#ROOT :is(h1,h2,h3,h4,h5,h6) { color:var(--lp-heading); }
#ROOT h1 em { color:var(--lp-accent); }
#ROOT p, #ROOT label { color:var(--lp-text); }
#ROOT a, #ROOT a:visited { color:var(--lp-link); }
#ROOT a:hover { color:#ffdfeb; }
#ROOT a:focus-visible { color:#fff; outline:3px solid #e7a3bd; }
#ROOT :is(button,.cta) { color:#2b2030; background-color:#f1c8d8; border:2px solid #b77b94; padding:10px; display:inline-block; }
#ROOT :is(button,.cta):hover { color:#fff7f9; background-color:#98556e; border-color:#e7a3bd; }
#ROOT :is(button,.cta):focus-visible { color:#fff7f9; background-color:#98556e; outline:3px solid #e7a3bd; }
#ROOT button.secondary { color:#fff7f9; background-color:transparent; border-color:#b77b94; }
#ROOT button.secondary:hover, #ROOT button.secondary:focus-visible { color:#2b2030; background-color:#f1c8d8; }
#ROOT button:disabled { color:#bfaeb8; background-color:#52434e; border-color:#b77b94; }
#ROOT :is(input,textarea,select) { color:#fff7f9; background-color:#463741; border:2px solid #b77b94; caret-color:#e7a3bd; padding:10px; }
#ROOT :is(input,textarea)::placeholder { color:#d6c1cc; opacity:1; }
#ROOT :is(input,textarea,select):focus { color:#fff7f9; background-color:#4c3848; border-color:#e7a3bd; outline:2px solid #e7a3bd; }
'''.replace('#ROOT', '#' + root)


def create_fixture(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    metadata = {}
    for scenario, kit in [('fixed', '7341'), ('inherited-bug', '9027'), ('leaky-bug', 'different-kit')]:
        inputs = output / scenario / 'inputs'
        inputs.mkdir(parents=True, exist_ok=True)
        root_ids = {kind: 'lp-fixture-' + scenario + '-' + kind for kind in ('elementor', 'gutenberg')}
        for kind, root in root_ids.items():
            css = styles(root)
            if scenario == 'inherited-bug':
                css = css.replace('#' + root + ' :is(h1,h2,h3,h4,h5,h6) { color:var(--lp-heading); }', '')
            if scenario == 'leaky-bug':
                css += '\n.wp-theme-simulation .entry-content [data-wp-preview-outside] h1 { color:lime; }'
            if kind == 'elementor':
                (inputs/'elementor.html').write_text('<style>' + css + '</style>' + markup(root), encoding='utf-8')
            else:
                (inputs/'gutenberg.html').write_text(markup(root), encoding='utf-8')
                (inputs/'gutenberg.css').write_text(css, encoding='utf-8')
        before = {p.name:p.read_bytes() for p in inputs.iterdir()}
        pages = builder.build(inputs/'elementor.html', inputs/'gutenberg.html', inputs/'gutenberg.css',
                              None, output/scenario/'preview', kit_token=kit)
        assert before == {p.name:p.read_bytes() for p in inputs.iterdir()}, 'An input export was modified'
        for page in pages:
            content = page.read_text(encoding='utf-8')
            assert content.count('data-wp-host-conflicts') == 1
            assert content.index('data-wp-host-conflicts') > content.index('data-wp-preview-outside="after"')
        assert (inputs/'elementor.html').read_text(encoding='utf-8') in pages[1].read_text(encoding='utf-8')
        metadata[scenario] = {'rootIds':root_ids, 'pages':[str(p.relative_to(output)) for p in pages]}
    source_root = 'lp-fixture-source'
    (output/'source.html').write_text('<!doctype html><html lang="hu"><meta charset="utf-8"><title>Forrásdesign tesztminta</title><style>' +
                                    styles(source_root) + '</style>' + markup(source_root) + '</html>', encoding='utf-8')
    metadata['sourceRoot'] = source_root
    metadata['expectedBehavior'] = {
        'fixed':'Both exports match source colors; outside probes match baseline.',
        'inherited-bug':'Both exports must expose the dark heading regression.',
        'leaky-bug':'Both exports must expose changed outside heading colors.'}
    (output/'cases.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    try:
        builder.build(inputs/'elementor.html', inputs/'gutenberg.html', inputs/'gutenberg.css',
                      None, output/'invalid', base_url='file:///tmp/not-allowed/')
    except ValueError:
        pass
    else:
        raise AssertionError('A file:// asset base was accepted')
    print('PASS: exports preserved; both formats wrapped; host conflicts loaded last; invalid base refused.')
    print('Browser fixtures:',output)
    print('CSS cascade, visual appearance and interaction states require browser verification.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    if args.output_dir:
        create_fixture(args.output_dir)
    else:
        with tempfile.TemporaryDirectory(prefix='landing-style-preview-') as directory:
            create_fixture(directory)
