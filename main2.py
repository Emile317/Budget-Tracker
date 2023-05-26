from datetime import datetime
import tkinter as tk
from tkinter import ttk
import json
import time

profiles = []
existing_profile = False

def create_profile(profile_name):
    with open("config.json", "r+") as config_file:
        config_dict = json.load(config_file)

        config_dict["existing_profile"] = True
        config_dict["profiles"].append(profile_name)

        config_file.seek(0)
        json.dump(config_dict, config_file, indent=2)
        config_file.truncate()

    with open("main.json", "r+") as data_file:
        data_dict = json.load(data_file)
        
        data_dict[profile_name] = {
            "total_monthly_income": 0,
            "total_monthly_expenses": 0,
            "current_monthly_expenses": [],
            "current_monthly_income": [],
            "single_income_history": [],
            "single_expense_history": []
        }

        data_file.seek(0)
        json.dump(data_dict, data_file, indent=2)
        data_file.truncate()

    profiles.append(profile_name)

def delete_profile(profile_name):
    with open("config.json", "r+") as config_file:
        config_dict = json.load(config_file)

        config_dict["profiles"].remove(profile_name)
        if len(config_dict["profiles"]) == 0:
            config_dict["existing_profile"] = False

        config_file.seek(0)
        json.dump(config_dict, config_file, indent=2)
        config_file.truncate()

    with open("main.json", "r+") as data_file:
        data_dict = json.load(data_file)

        data_dict.pop(profile_name)

        data_file.seek(0)
        json.dump(data_dict, data_file, indent=2)
        data_file.truncate()
    
    profiles.remove(profile_name)

class Profile:
    def __init__(self, name, data):
        self.data = data
        self.name = name

class Main_window:

    def __init__(self, root, existing_profile):

        if existing_profile is False:
            create_profile_window(root)

        mainframe = ttk.Frame(root)
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        quit_button = ttk.Button(mainframe, text="quit", command=root.destroy)
        quit_button.grid(column=0, row=0, sticky="nesw")

        ttk.Button(mainframe, text="create new profile", command=lambda: create_profile_window(root)).grid(column=1, row=0, sticky="nesw")
        ttk.Button(mainframe, text="delete a profile", command=lambda: delete_profile_window(root)).grid(column=2, row=0, sticky="nesw")

        for column in range(mainframe.grid_size()[0]):
            mainframe.columnconfigure(column, weight=1)
        for row in range(mainframe.grid_size()[1]):
            mainframe.rowconfigure(row, weight=1)


def create_profile_window(root, first=False):
    profile_window = tk.Toplevel(root)
    profile_window.title("Create new profile")
    profile_window.columnconfigure(0, weight=1)
    profile_window.rowconfigure(0, weight=1)
    profile_window.bind("<space>", quit)
    profile_window.protocol("WM_DELETE_WINDOW", lambda: create_profile_window(root))

    frame = ttk.Frame(profile_window, padding="6")
    frame.grid(column=0, row=0, sticky="nesw")

    ttk.Label(frame, text="profile name:").grid(column=0, row=0, pady="0 5")
    
    def check_name(name, index, mode):
        if profile_name.get() == "":
            b.state(["disabled"])
        elif not profile_name.get() in profiles:
            b.state(["!disabled"])
            error.grid_forget()
        else:
            b.state(["disabled"])
            error.grid(column=1, row=1)


    profile_name = tk.StringVar()
    ttk.Entry(frame, textvariable=profile_name, width=12).grid(column=1, row=0, pady="0 5")
    profile_name.trace_add("write", check_name)
    error = ttk.Label(frame, text="profile name already in use", foreground="red", wraplength=75)

    b = ttk.Button(frame, text="create profile", command=lambda: [create_profile(profile_name.get()), profile_window.destroy()])
    b.grid(column=1, row=2, sticky="e")
    b.state(["disabled"])
    cancel = ttk.Button(frame, text="cancel", command=profile_window.destroy)
    cancel.grid(column=0, row=2, sticky="e")
    
def delete_profile_window(root):
    profile_window = tk.Toplevel(root)
    profile_window.title("Delete profile")
    profile_window.columnconfigure(0, weight=1)
    profile_window.rowconfigure(0, weight=1)
    profile_window.bind("<space>", quit)

    frame = ttk.Frame(profile_window, padding="6")
    frame.grid(column=0, row=0, sticky="nesw")

    ttk.Label(frame, text="Select profile:").grid(column=0, row=0)
    profile_to_delete = tk.StringVar()
    profile = ttk.Combobox(frame, textvariable=profile_to_delete, width=9)
    profile.grid(column=1, row=0)
    profile['values'] = profiles
    profile.state(["readonly"])

    ttk.Button(frame, text="delete profile", command=lambda: [delete_profile(profile_to_delete.get()), profile_window.destroy()]).grid(column=1, row=1, sticky="e")
    ttk.Button(frame, text="cancel", command=profile_window.destroy).grid(column=0, row=1, sticky="e")

root = tk.Tk()
root.title("Budget Tracker")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.bind("<space>", quit)

with open("config.json") as config_file:
    config_dict = json.load(config_file)
    existing_profile = config_dict["existing_profile"]
    print(existing_profile)
    current_profile_name = config_dict["current_profile"]
    profiles = config_dict["profiles"]

if existing_profile:
    with open("main.json") as data_file:
        data_dict = json.load(data_file)
        current_profile = Profile(current_profile_name, data_dict[current_profile_name])

Main_window(root, existing_profile)

root.mainloop()
