"""Compare publication to accepted PDFs using pypdf copied from the same image."""
import hashlib
import json
from pathlib import Path
import sys

scratch = Path(sys.argv[1])
sys.path.insert(0, str(scratch/'deps'))
from pypdf import PdfReader
from pypdf.generic import DictionaryObject, StreamObject, IndirectObject


def canonical(value):
    if isinstance(value, IndirectObject):
        return ('reference', value.idnum, value.generation)
    if isinstance(value, (DictionaryObject, dict)):
        excluded = {'/ID'} if value.get('/Type') == '/XRef' else set()
        content = {str(k): canonical(v) for k, v in value.items() if k not in excluded}
        if isinstance(value, StreamObject):
            content['decoded_stream_sha256'] = hashlib.sha256(value.get_data()).hexdigest()
        return content
    if isinstance(value, list):
        return [canonical(v) for v in value]
    if isinstance(value, bytes):
        return ('bytes', value.hex())
    return (type(value).__name__, str(value))


def objects(reader):
    refs = {(generation, number) for generation, entries in reader.xref.items()
            for number in entries if number and generation != 65535}
    refs |= {(0, number) for number in reader.xref_objStm}
    return {f'{generation}:{number}': canonical(reader.get_object(IndirectObject(number, generation, reader)))
            for generation, number in refs}


results = []
for index in range(3):
    before = PdfReader(scratch/'reference'/f'{index}.pdf')
    after = PdfReader(scratch/'published'/f'{index}.pdf')
    a, b = objects(before), objects(after)
    assert a == b, index
    assert canonical({k: v for k, v in before.trailer.items() if k != '/ID'}) == canonical({k: v for k, v in after.trailer.items() if k != '/ID'}), index
    assert len(before.pages) == len(after.pages)
    results.append(dict(index=index, pages=len(after.pages), objects=len(b),
                        all_objects_and_decoded_streams_equal=True))
print(json.dumps(results, indent=2))
