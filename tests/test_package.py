import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('builder',ROOT/'tools/build.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class Packaging(unittest.TestCase):
    def test_manifests_and_references(self):
        self.assertEqual(builder.validate()['name'],'rankbeam-laravel')

    def test_deterministic_zip_and_roundtrip(self):
        with tempfile.TemporaryDirectory(prefix='rankbeam-package-') as tmp:
            root=Path(tmp)
            first=builder.build(root/'a');second=builder.build(root/'b')
            self.assertEqual(first['sha256'],second['sha256'])
            with zipfile.ZipFile(root/'a'/first['file']) as archive:
                self.assertEqual(len(archive.namelist()),len(builder.FILES))
                archive.extractall(root/'extracted')
            self.assertEqual(builder.validate(root/'extracted/rankbeam-laravel')['version'],'1.0.0')

    def test_unexpected_file_rejected(self):
        with tempfile.TemporaryDirectory(prefix='rankbeam-package-') as tmp:
            root=Path(tmp)/'plugin';shutil.copytree(builder.PLUGIN,root)
            (root/'.env').write_text('DO_NOT_SHIP=sentinel')
            with self.assertRaises(ValueError):builder.validate(root)
