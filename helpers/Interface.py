import gspread, json

class Interface:
    def __init__(self, worksheet) -> None:
        self.gs = gspread.service_account()
        self.sheet = self.gs.open("Fiverr Keyword Research")
        self.worksheet = self.sheet.worksheet(worksheet)

        self.records = self.worksheet.get_all_records()

        self.file = open('tracker.json', 'r')
        self.json = json.load(self.file)
        self.rows = self.json[worksheet]['Row'] + 1
        self.file.close()

        self.current_row =  self.rows


    def dump(self):
        self.file = open('tracker.json', 'w')
        json.dump(self.json, self.file)
        self.file.close()

    def getRecordCount(self) -> int:
        return len(self.records) - 2


    def setCurrentRow(self, num) -> None:
        self.current_row = num


    def incrementCurrentRow(self) -> None:
        self.current_row += 1

    
    def getKeyword(self) -> str:
        keyword = self.records[self.current_row].get('Keyword').strip()

        if keyword == "" or keyword == " " or keyword == "//":
            keyword = self.records[self.current_row + 1].get('Keyword').strip()

            if keyword == "" or keyword == " ":
                return None, None
            
            self.incrementCurrentRow()
            return keyword, self.current_row - 1

        self.incrementCurrentRow()
        return keyword, self.current_row - 1
    

    def updateVolume(self, volume, row) -> None:
        self.worksheet.update_cell(row + 2, 2, volume)