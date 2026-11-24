from pywinauto import WindowSpecification
from getSelector import getSelector

def extractItemData(item_record: WindowSpecification):
    """Extract circulation data for selectors"""
    edits = item_record.children(class_name="Edit")

    def getEdit(index):
        try:
            return edits[index].window_text() if len(edits) > index else ''
        except Exception:
            return 'error'
    
    barcode = getEdit(0)
    title = getEdit(2)
    author = getEdit(4)
    callNum = getEdit(7) # Call once instead of twice, # performance # I am speed
    relDate = getEdit(45)
    ytdCirc = getEdit(56)
    prevYTDCirc = getEdit(57)
    selector = getSelector(callNum)

    item_record.close()



    return {
        'Barcode': barcode,
        'Title': title,
        'Author': author,
        'Call Number': callNum,
        'PO Release Date': relDate,
        'YTD Circulation': ytdCirc,
        'Prev YTD Circulation': prevYTDCirc,
        'Selector': selector
    }
