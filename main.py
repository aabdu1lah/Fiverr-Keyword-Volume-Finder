from helpers.Interface import Interface
from helpers.KeywordFinder import KeywordFinder
from helpers.sheets import Sheets
from time import sleep

def perform_keyword_search(interface, keywordFinder, keyword, keywordRow):
    for attempt in range(2):  # Try twice
        if attempt == 1:
            print("Trying again...")
        try:
            keywordFinder.search(keyword)
            data = keywordFinder.getData()

            if data.get('Title').lower() == keyword.lower():
                volume = data.get("Volume")
                if volume is not None:
                    interface.updateVolume(volume, keywordRow)
                    return volume  # Return True if update is successful
            else:
                pass

        except Exception as e:
            print(f"An error occurred while searching for the keyword: {e}")

    return None


if __name__ == "__main__":
    sheets = Sheets()
    current_sheet = sheets.SHOPIFY
    interface = Interface(current_sheet)
    keywordFinder = KeywordFinder()

    recordCount = interface.getRecordCount()


    for i in range(recordCount):
        keyword, keywordRow= interface.getKeyword()

        if keyword is None:
            interface.current_row -= 2
            break

        sleep(1)

        print(keywordRow, keyword)

        success = perform_keyword_search(interface, keywordFinder, keyword, keywordRow)

        if success is None:
            print(f"Encountered errors trying to find volume for {keyword} at row {keywordRow}\nExiting Program...")
            break

        print(f"{keyword} : {success}\nNext...")

    interface.json[current_sheet]['Row'] = interface.current_row
    interface.dump()
    print("Closing Program, Goodbye!")