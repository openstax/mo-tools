import urllib.request

"""
searches webpage for a given word/string and outputs how many times it is present
"""


def fetch_page_text(url):

    # Gets the webpage and reads its content
    doc_page = urllib.request.urlopen(url)
    webpage_text = doc_page.read()

    # Converts webpage content from bytes into strings
    webpage_text_conv = webpage_text.decode("UTF-8")

    return webpage_text_conv


def word_searching(webpage_text_conv, wordx, url):

    if webpage_text_conv.find(wordx) > 0:
        szam = webpage_text_conv.count(wordx)
        print("--- SEARCH RESULT ---")
        print('Word "', wordx, '" found', szam, "times in", url)
    else:
        print("Word not found")
        return


def user_input(prompt=None):

    return input(prompt)


def main():

    while True:

        no = 0
        while no in range(2):

            url1 = user_input("Type in webapge or file address: ")
            wordx1 = user_input("and search for this word: ")

            if "https:" in url1 or "www" in url1 or "http:" in url1 or "file:" in url1:
                # print('correct webpage', url1)

                if wordx1.strip():
                    page_text = fetch_page_text(url1)
                    word_searching(page_text, wordx1, url1)
                    return

                else:
                    print("Empty or blank string. Try #{}/2".format(no + 1))

            else:
                print(
                    "Empty or blank string, or incorrect address format. Try #{}/2".format(no + 1)
                )

            no = no + 1
            if no == 3:
                break

        answer1 = user_input("do you want to continue? (y/n): ")
        if answer1 != "y":
            break


if __name__ == "__main__":
    main()
