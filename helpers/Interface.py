import gspread

class Interface:
    def __init__(self, worksheet) -> None:
        self.gs = gspread.service_account()
        self.sheet = self.gs.open("Fiverr Keyword Research")
        self.worksheet = self.sheet.worksheet(worksheet)

        self.records = self.worksheet.get_all_records()
        self.current_row =  2


    def getRecordCount(self) -> int:
        return len(self.records) - 2


    def setCurrentRow(self, num) -> None:
        self.current_row = num


    def incrementCurrentRow(self) -> None:
        self.current_row += 1

    
    def getKeyword(self) -> str:
        keyword = self.records[self.current_row].get('Keyword').strip()

        if keyword == "" or keyword == " ":
            keyword = self.records[self.current_row + 1].get('Keyword').strip()

            if keyword == "" or keyword == " ":
                self.setCurrentRow(2)
                return None
            
            self.incrementCurrentRow()
            return keyword

        self.incrementCurrentRow()
        return keyword
    

    def getKeywordRow(self) -> int:
        return self.current_row - 1
    

    def updateVolume(self, volume, row) -> None:
        self.worksheet.update_cell(row, 2, volume)