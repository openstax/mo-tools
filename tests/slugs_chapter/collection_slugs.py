from archive_client.client import ArchiveClient

staging_client = ArchiveClient()

staging_client_url = ArchiveClient(root_url="https://archive-qa.cnx.org")

hs_physics = staging_client_url.get_collection("cce64fde-f448-43b8-ae88-27705cceb0da")

print(hs_physics.slug)


def test_slug_chapter_search():

    toc = hs_physics.table_of_contents.contents

    for collection in toc:

        print(collection.slug)

        if hasattr(collection, "contents"):

            for module in collection.contents:

                with open("slug_with_hs_chapter.txt", "a") as out:
                    out.write(module.slug + "\n")
                    out.close()

                print("OOOO:", module.slug)

                # assert "chapter" not in module.slug
