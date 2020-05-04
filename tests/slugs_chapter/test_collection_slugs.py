from archive_client.client import ArchiveClient

staging_client = ArchiveClient()

staging_client_url = ArchiveClient(root_url="https://archive-staging.cnx.org")

pre_algebra = staging_client_url.get_collection("f0fa90be-fca8-43c9-9aad-715c0a2cee2b")

# print(pre_algebra.slug)


def test_slug_chapter_search():

    toc = pre_algebra.table_of_contents.contents

    for collection in toc:

        # print(collection.slug)

        if hasattr(collection, "contents"):

            for module in collection.contents:

                print(module.slug)

                assert "chapter" not in module.slug
