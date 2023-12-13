import logging
import urllib.parse
import zipfile

import fire
from aiosumma import SummaClient
from trident.client import TridentClient




def process_zip(filepath):
    with zipfile.ZipFile(filepath) as archive:
        zip_infos = archive.infolist()
        # iterate through each file
        for zip_info in zip_infos:
            prefix, suffix = zip_info.filename.lower().split('/', 1)
            suffix = urllib.parse.unquote(suffix)
            doi = prefix + '/' + suffix
            data = archive.read(zip_info)
            yield [doi.removesuffix('.pdf'), data]


async def local_import(summa_client, trident_client, path: str):
    logging.getLogger('statbox').info({'action': 'import', 'path': path})
    for doi, data in process_zip(path):
        document = await summa_client.get_one_by_field_value(
            "nexus_science",
            "id.dois",
            doi,
        )
        if not document:
            logging.getLogger('statbox').info({
                'action': 'not_found',
                'doi': doi,
            })
            continue

        if 'nexus_id' not in document['id']:
            continue

        key = f'/kv/{document["id"]["nexus_id"]}.pdf'
        await trident_client.store(key, data)


async def import_file(summa_endpoint, trident_base_url, local_path):
    summa_client = SummaClient(endpoint=summa_endpoint)
    trident_client = TridentClient(base_url=trident_base_url)
    await summa_client.start()
    await trident_client.start()
    await local_import(summa_client, trident_client, local_path)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    fire.Fire(import_file)
