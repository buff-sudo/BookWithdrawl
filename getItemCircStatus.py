from pywinauto import WindowSpecification, Application
import re

def getItemCircStatus(item_record: WindowSpecification, app: Application, barcode) -> bool:    
    """Returns True if any linked item has a circulatable status"""
    item_record.wait('ready')
    item_record.set_focus()

    item_record.type_keys("^g")
    bib_record = app.window(title_re="Bibliographic Record*")
    bib_record.wait('exists', timeout=10)

    edits = item_record.children(class_name="Edit")
    def getEdit(index):
        try:
            return edits[index].window_text() if len(edits) > index else ''
        except Exception:
            return 'error'
        
    callNum = getEdit(7)
    if re.match(r"^YA\s+MANGA\b", callNum):
        print("Manga")
        bib_record.close()
        return False

    bib_record.type_keys("^t")
    linked_record = app.window(title_re=".*Linked Item Records$")

    

    if not linked_record.exists(timeout=3):
        print(f"{barcode} : Only")
        bib_record.close()
        return False

    list_view = linked_record.child_window(class_name="SysListView32")

    circulatable = ["In", "Out", "Held", "To Be Shelved"]
    STATUS_COLUMN = 7

    for row in range(list_view.item_count()):
        print(row)
        try:
            status = list_view.get_item(row, STATUS_COLUMN).text()
            if status in circulatable:
                print(f"{barcode} : {status}")
                linked_record.close()
                bib_record.close()
                item_record.close()
                return True
        except Exception:
            pass

    print(f"{barcode} : No Circ Copy")
    linked_record.close()
    bib_record.close()
    return False
