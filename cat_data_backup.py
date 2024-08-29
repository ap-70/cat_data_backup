from cat.mad_hatter.decorators import hook, tool
import shutil
import os
from datetime import datetime
import threading

def zip_folder(orig, dest_dir, num_bk, msg : bool, cat):
    try:
        # Verify that the source folder exists
        if not os.path.exists(orig):
            print(f"The source folder '{orig}' doesn't exist.")
            return
        
        # Adds date to ZIP file name
        date_current = datetime.now().strftime("%Y-%m-%d")
        base_dest = os.path.join(dest_dir, f"data_{date_current}")
        zip_dest = f"{base_dest}.zip"
        
        # Create a ZIP file from the source folder
        shutil.make_archive(base_dest, 'zip', orig)
        
        print(f"Folder '{orig}' zipped successfully in '{zip_dest}'.")
        if msg == True:
            cat.send_ws_message(f"Folder '{orig}' zipped successfully in '{zip_dest}'.")
        
        # Manage backups: keep only the most recent num_bk
        manage_backup(dest_dir, num_bk)
    
    except Exception as e:
        print(f"Error creating ZIP file: {e}")
        if msg == True:
            cat.send_ws_message(f"Error creating ZIP file: {e}")

def manage_backup(dest_dir, num_bk):
    print(f"\nMax number of backups: {num_bk}\n")

    try:
        # Gets the list of all ZIP files in the destination folder
        file_zip = [f for f in os.listdir(dest_dir) if f.endswith('.zip')]
        print(f"\nGets the list of all ZIP files: {file_zip}\n")
        
        # Sort ZIP files by creation date (part of file name)
        file_zip.sort(key=lambda x: os.path.getctime(os.path.join(dest_dir, x)), reverse=True)
        print(f"\nSort ZIP files by creation date : {file_zip}\n")
        
        # If there are more than num_bk files, delete the oldest ones
        if len(file_zip) > num_bk:
            for file_to_delete in file_zip[num_bk:]:
                os.remove(os.path.join(dest_dir, file_to_delete))
                print(f"Deleted old backup: {file_to_delete}")
    
    except Exception as e:
        print(f"Error while managing backups: {e}")

def save_data(msg : bool, cat):
    settings = cat.mad_hatter.get_plugin().load_settings()
    num_bk = settings["max_num_backup"]

    origin = "./cat/data/"
    base_destination = "./cat/static/backup/"
    
    # Start the function in a separate thread
    thread = threading.Thread(target=zip_folder, args=[origin, base_destination, num_bk, msg, cat])
    thread.start()

@hook  # default priority = 1
def after_cat_bootstrap(cat):
    save_data(False, cat)

@tool(return_direct=True)
def save_ccat_data(none, cat):
    """To be used when the input says to save the cat's data."""
    
    cat.send_ws_message("Start save Cat memory...")

    save_data(True, cat)

    return "I'm saving my data..."