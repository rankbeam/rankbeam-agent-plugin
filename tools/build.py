"""Validate and reproducibly package only the installable plugin files."""
import argparse
import hashlib
import json
import re
import struct
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/rankbeam-laravel'
FILES = {
    'plugin.json', '.codex-plugin/plugin.json', 'LICENSE', 'PRIVACY.md', 'assets/icon.png',
    'skills/laravel-seo/SKILL.md', 'skills/laravel-seo/agents/openai.yaml',
    'skills/laravel-seo/references/audit.md', 'skills/laravel-seo/references/setup.md',
    'skills/laravel-seo/references/rendering.md', 'skills/laravel-seo/scripts/lib.php',
    'skills/laravel-seo/scripts/inspect-project.php', 'skills/laravel-seo/scripts/check-head.php',
}

def validate(root=PLUGIN):
    if not __debug__:
        raise RuntimeError('Run validation without Python optimization (-O/-OO).')
    root = Path(root).resolve()
    entries = list(root.rglob('*'))
    if any(p.is_symlink() for p in entries):
        raise ValueError('Plugin symlinks are not permitted')
    actual = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    if actual != FILES:
        raise ValueError(f'Package file mismatch: missing={FILES-actual}, unexpected={actual-FILES}')
    data = json.loads((root/'plugin.json').read_text(encoding='utf-8'))
    compat = json.loads((root/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    assert data['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', data['name']) and len(data['name']) <= 64
    assert re.fullmatch(r'\d+\.\d+\.\d+', data['version'])
    for field in ('name', 'version', 'description', 'author', 'homepage', 'repository', 'license', 'keywords'):
        assert data[field] == compat[field], f'Compatibility manifest drift: {field}'
    interface = data['extensions']['com.openai']['interface']
    assert interface == compat['interface']
    assert compat['skills'] == './skills/'
    for field, limit in {'displayName':30, 'shortDescription':30, 'longDescription':4000, 'developerName':80}.items():
        assert isinstance(interface[field], str) and 0 < len(interface[field]) <= limit, field
    assert interface['category'] == 'Developer Tools'
    assert 1 <= len(interface['defaultPrompt']) <= 3
    assert all(0 < len(p) <= 128 and '@' not in p for p in interface['defaultPrompt'])
    for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        assert interface[field].startswith('https://github.com/rankbeam/')
    for field in ('composerIcon', 'logo'):
        value = interface[field]
        assert value.startswith('./') and '..' not in Path(value).parts
        icon = root/value
        assert icon.is_file() and icon.stat().st_size <= 5*1024*1024
        raw = icon.read_bytes()
        assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        width, height = struct.unpack('>II', raw[16:24])
        assert width == height and 48 <= width <= 4096
    skill = (root/'skills/laravel-seo/SKILL.md').read_text(encoding='utf-8')
    assert skill.startswith('---\nname: laravel-seo\ndescription: ')
    assert skill.split('---', 2)[1].count('description:') == 1
    for p in entries:
        if p.is_file() and p.suffix in {'.md', '.php', '.json', '.yaml'}:
            text = p.read_text(encoding='utf-8')
            assert not re.search(r'C:[/\\]Users[/\\]|/Users/|/home/|sk-[A-Za-z0-9]{20,}', text), f'Private path/secret in {p.name}'
            if p.suffix == '.md':
                for link in re.findall(r'\]\(([^)]+)\)', text):
                    if '://' not in link and not link.startswith('#'):
                        target = (p.parent/link.split('#')[0]).resolve()
                        assert target.is_relative_to(root) and target.is_file(), f'Broken reference: {p}: {link}'
    assert (root/'LICENSE').read_bytes() == (ROOT/'LICENSE').read_bytes()
    assert (root/'PRIVACY.md').read_bytes() == (ROOT/'PRIVACY.md').read_bytes()
    return data

def build(output, root=PLUGIN):
    metadata = validate(root)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    destination = output/f"{metadata['name']}-{metadata['version']}.zip"
    files = []
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted(FILES):
            raw = (Path(root)/relative).read_bytes()
            info = zipfile.ZipInfo(f"{metadata['name']}/{relative}", date_time=(2026,10,2,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw)
            files.append({'path': relative, 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})
    report = {'file':destination.name, 'bytes':destination.stat().st_size, 'sha256':hashlib.sha256(destination.read_bytes()).hexdigest(), 'files':files}
    (output/'package-manifest.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist')
    args = parser.parse_args()
    report = build(args.output)
    print(json.dumps({key:value for key,value in report.items() if key != 'files'}, indent=2))
