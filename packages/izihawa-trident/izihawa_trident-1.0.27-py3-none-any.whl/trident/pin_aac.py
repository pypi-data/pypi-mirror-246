import asyncio
import logging
import os
import random
import sys
import time

import aiofiles
import orjson
from aiokit import MultipleAsyncExecution
from aiosumma import SummaClient
from izihawa_textparser import md
from stc_geck.advices import LinksWrapper

from fabrica.actions.recognize_epub import recognize_epub
from fabrica.configs import get_config
from library.integral.file_flow import FileFlow


async def job(summa_client, file_flow, zlibrary_id, path, extension):
    document = await summa_client.get_one_by_field_value('nexus_science', 'id.zlibrary_ids', zlibrary_id)

    if not document:
        print('not found', zlibrary_id)
        return

    print(document['id'])

    if os.stat(path).st_size > 100 * 1024 * 1024:
        print('too big', path)
        return

    links = LinksWrapper(document.get('links', []))
    if not links.get_link_with_extension('pdf') and extension == 'pdf':
        async with aiofiles.open(path, 'rb') as f:
            await file_flow.pin_add(document, await f.read(), with_commit=False, extension=extension)
    elif not links.get_link_with_extension('epub') and extension == 'epub':
        async with aiofiles.open(path, 'rb') as f:
            data = await f.read()
            try:
                content = recognize_epub(data)
                if content:
                    document['content'] = content
                    document.setdefault('metadata', {})
                    document['metadata']['content'] = {
                        'source_extension': 'epub',
                        'parser': 'textparser-0.1.21',
                        'parsed_at': int(time.time())
                    }
            except Exception as e:
                print(e)
            if abstract := document.get('abstract'):
                document['abstract'] = md.convert(abstract)
            await file_flow.pin_add(document, data, with_commit=True, extension=extension)


async def main():
    config = get_config()
    infra = config['infra']
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    summa_client = SummaClient('10.1.2.3:10082')
    file_flow = FileFlow(
        summa_client=summa_client,
        config=infra,
        index_alias='nexus_science',
    )
    items = [
        summa_client,
        file_flow
    ]

    for c in items:
        await c.start()

    a_dictionary = {}
    with open('/home/pasha/annas_archive_meta__aacid__zlib3_records__20230808T014342Z--20231102T230010Z.jsonl') as f:
        for line in f:
            a = orjson.loads(line)
            if 'missing' in a['metadata']:
                continue
            a_dictionary[str(a['metadata']['zlibrary_id'])] = (a['metadata']['md5_reported'], a['metadata']['extension'])

    prepared_files = []
    for root, dirs, files in os.walk('/home/pasha/aa/20230808'):
        for filename in files:
            if filename.endswith('.torrent'):
                continue
            zlibrary_id = filename.split('__')[3]
            md5, extension = a_dictionary.get(zlibrary_id)
            if not md5:
                continue
            prepared_files.append((zlibrary_id, root + '/' + filename, extension))

    random.shuffle(prepared_files)
    executor = MultipleAsyncExecution(4)

    for zlibrary_id, path, extension in prepared_files:
        await executor.execute(job(summa_client, file_flow, zlibrary_id, path, extension))

    await asyncio.sleep(10)
    await executor.join()

asyncio.run(main())
