import time

def withdraw(item_record):
    circ_status = item_record.child_window(class_name="ComboBox", found_index=4)

    try:
        circ_status.select("Withdrawn")
    except Exception:
        open_button = circ_status.child_window(title="Open", auto_id="DropDown")
        open_button.wait('exists', timeout=5)
        open_button.click_input()
        time.sleep(.2)  # dropdown animation
        circ_status.type_keys("W{ENTER}")

    item_record.wait('ready')
    item_record.type_keys("^s")