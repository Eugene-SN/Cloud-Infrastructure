"""Compare standalone CLI outputs with published outputs on isolated snapshots."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

import pymupdf


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    manifest = json.loads(Path('/input/selection.json').read_text())
    results = []
    for item in manifest:
        started = time.monotonic()
        source = Path('/input') / item['snapshot']
        reference = Path('/reference') / item['snapshot']
        output = Path('/work') / item['snapshot']
        assert sha(source) == item['source_sha256']
        assert sha(reference) == item['reference_sha256']
        saved_cli = output.with_suffix('.cli.json')
        if output.exists():
            cli = json.loads(saved_cli.read_text())
        else:
            process = subprocess.run(['pdf-cleanup', str(source), str(output)],
                                     capture_output=True, text=True, timeout=900)
            cli = dict(returncode=process.returncode, stderr=process.stderr,
                       report=json.loads(process.stdout))
            saved_cli.write_text(json.dumps(cli, indent=2)+'\n')
        report = cli['report']
        assert cli['returncode'] == 0, (item['path'], report, cli['stderr'])
        assert not cli['stderr'], (item['path'], cli['stderr'])
        assert report['validation'] == 'passed'
        with pymupdf.open(output) as actual, pymupdf.open(reference) as expected:
            assert len(actual) == len(expected)
            assert actual.metadata == expected.metadata
            assert actual.get_toc(simple=False) == expected.get_toc(simple=False)
            assert actual.get_page_labels() == expected.get_page_labels()
            assert actual.xref_length() == expected.xref_length()
            # The PDF trailer ID is regenerated; compare every referenced object
            # and decoded stream instead of comparing whole-file hashes.
            for xref in range(1, actual.xref_length()):
                if actual.xref_get_key(xref, 'Type') == ('name', '/XRef'):
                    keys = set(actual.xref_get_keys(xref))
                    assert keys == set(expected.xref_get_keys(xref))
                    for key in keys - {'ID'}:
                        assert actual.xref_get_key(xref, key) == expected.xref_get_key(xref, key), (item['path'], xref, key)
                else:
                    assert actual.xref_object(xref) == expected.xref_object(xref), (item['path'], xref)
                assert actual.xref_stream(xref) == expected.xref_stream(xref), (item['path'], xref)
            for index in range(len(actual)):
                a, b = actual[index], expected[index]
                assert (a.mediabox, a.cropbox, a.rotation) == (b.mediabox, b.cropbox, b.rotation)
                assert a.get_text('rawdict') == b.get_text('rawdict'), (item['path'], index, 'text')
                ap, bp = a.get_pixmap(matrix=pymupdf.Matrix(1, 1)), b.get_pixmap(matrix=pymupdf.Matrix(1, 1))
                assert (ap.width, ap.height, ap.n, ap.samples) == (bp.width, bp.height, bp.n, bp.samples), (item['path'], index, 'pixels')
            pages = len(actual)
            objects = actual.xref_length() - 1
        assert sha(source) == item['source_sha256']
        assert sha(reference) == item['reference_sha256']
        result = dict(item, pages=pages, objects_compared=objects,
                      output_sha256=sha(output), cli_report=report,
                      stderr=cli['stderr'], seconds=round(time.monotonic()-started, 2),
                      all_objects_streams_text_and_72dpi_pixels_equal=True)
        results.append(result)
        Path('/work/results.json').write_text(json.dumps(results, indent=2)+'\n')
        print(json.dumps({'path': item['path'], 'pages': pages, 'seconds': result['seconds'], 'status': 'PASS'}), flush=True)
    print(json.dumps({'files': len(results), 'pages': sum(r['pages'] for r in results), 'status': 'PASS'}), flush=True)


if __name__ == '__main__':
    main()
