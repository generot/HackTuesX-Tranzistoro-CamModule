import json
import tkinter as tk

DEF_DIR = "../detection/configs/conf.json"

def submit():
    try:
        num_prompts = int(entry.get())
        clear_prompts()
        create_prompts(num_prompts)
    except ValueError:
        status_label.config(text="Please enter a valid number!")

def clear_prompts():
    for prompt in prompts:
        prompt.destroy()
    prompts.clear()

def create_prompts(num_prompts):
    l = tk.Label(root, text="Module IPs")
    l.pack()
    prompts.append(l)

    for i in range(num_prompts):
        prompt = tk.Entry(root)
        prompt.pack(pady=5)
        prompts.append(prompt)

    b = tk.Button(root, text="Save", command=on_save)
    b.pack()
    prompts.append(b)

def on_save():
    json_fl = open(DEF_DIR, "w+")
    
    ips = []

    for obj in prompts:
        if isinstance(obj, tk.Entry):
            ips.append(obj.get())
    
    json.dump(ips, json_fl)

root = tk.Tk()
root.title("AtlasFlow Configuration Tool")

prompt_label = tk.Label(root, text="Number of modules:")
prompt_label.pack()

entry = tk.Entry(root)
entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

prompts = []

root.mainloop()

