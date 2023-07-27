from helpers.Interface import Interface
from helpers.KeywordFinder import KeywordFinder
from helpers.sheets import Sheets


def perform_keyword_search(interface, keywordFinder, keyword, keywordRow):
    for attempt in range(2):  # Try twice
        try:
            keywordFinder.search(keyword)
            data = keywordFinder.getData()

            if data.get('Title').lower() == keyword.lower():
                volume = data.get("Volume")
                if volume is not None:
                    interface.updateVolume(volume, keywordRow)
                    return True  # Return True if update is successful
            else:
                pass

        except Exception as e:
            print(f"An error occurred while searching for the keyword: {e}")

    return False


if __name__ == "__main__":
    sheets = Sheets()
    interface = Interface(sheets.SHOPIFY)
    keywordFinder = KeywordFinder()

    recordCount = interface.getRecordCount()

    for i in range(recordCount):
        keyword = interface.getKeyword()
        keywordRow = interface.getKeywordRow()

        success = perform_keyword_search(interface, keywordFinder, keyword, keywordRow)

        if not success:
            print(f"Encountered errors trying to find volume for {keyword} at row {keywordRow}\nExiting Program...")
            break