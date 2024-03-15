import os
import json
import tkinter as tk

PADDING_Y = 5

WIN_WIDTH = 250
WIN_HEIGHT = 125

def main():
    app = tk.Tk()

    app.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
    app.title("AtlasFlow Camera Configuration Tool")

    tk.Label(app, text="SD Card Directory").grid(row=0, pady=PADDING_Y)
    tk.Label(app, text="Network Name (SSID)").grid(row=1, pady=PADDING_Y)
    tk.Label(app, text="Network Password").grid(row=2, pady=PADDING_Y)

    box1 = tk.Entry(app)
    box2 = tk.Entry(app)
    box3 = tk.Entry(app)

    box1.grid(row=0, column=1, pady=PADDING_Y)
    box2.grid(row=1, column=1, pady=PADDING_Y)
    box3.grid(row=2, column=1, pady=PADDING_Y)

    def on_save():
        config_dict = dict()

        config_dict["ssid"] = box2.get()
        config_dict["pass"] = box3.get()

        config_gl = open(os.path.join(box1.get(), "config.json"), "w+")

        json.dump(config_dict, config_gl)


    btn1 = tk.Button(text="Save", command=on_save)
    btn1.grid(row=3)

    #tk.Label(app, text="Module IP").grid(row=4, pady=(PADDING_Y + 10))
    #tk.Label(app, text="Department Name").grid(row=4, column=1, pady=(PADDING_Y + 10))

    tk.mainloop()

if __name__ == "__main__":
    main()
