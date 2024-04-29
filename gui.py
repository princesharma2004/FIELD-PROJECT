"""
    AUTHOR  - Prince Sharma
    DATE    - 27/4/2024
    WORKING - Gui for our Software 
"""



import sys
import tkinter as tk
from tkinter import ttk
import pandas as pd
from laptop_price_predictor import Laptop_Price_Predictor



class Gui :
    """A simple class which have gui functions."""


    
    def __init__(self, root):
        """Initilize screen and data"""
        
        # Gui related initilizations.
        self.root = root
        self.root.title("Laptop Price Predictor")
        self.root.attributes("-fullscreen",True)
        self.root.minsize(400,500)
        self.fullscreen = True
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit)
        
        # Database inttilization.
        self.df = pd.read_csv("laptop_data.csv")
        
        # What information we needed for prediction. 
        self.info = {"op_sys" : "", "type_name" : "", "brand" : "", "cpu" : "", "gpu" : "", "touch_screen" : False, "weight" : 0, "ips" : False, "cpu_frequency" : 0, 'screen_width' : 0, 'screen_heigth' : 0, 'inches' : 0, "ssd" : 0, "ram" : 0, "price" : 0}
        
        self.laptop = []
        self.num = 1


        
    def get_data(self) :
        """Getting data from user."""
        
        self.create_label(f"LAPTOP {self.num}", "Times 14")
        
        # Brand.
        self.brand = self.create_combobox("Brand", list(self.df["Company"].unique()))
        
        # Type.
        self.type = self.create_combobox("Type", list(self.df["TypeName"].unique()))
        
        # Op Sys.
        self.op_sys = self.create_combobox("Op Sys", list(self.df["OpSys"].unique()))
        
        # Cpu Brand.
        self.cpu = self.create_combobox("Cpu Brand", list(self.df.Cpu.str.split(" ").apply(lambda x: x[0]).unique()))
        
        # Gpu Brand.
        self.gpu = self.create_combobox("Gpu Brand", list(self.df.Gpu.str.split(" ").apply(lambda x: x[0]).unique()))
        
        # Touch screen.
        self.touch_screen = self.create_radio_buttons("Touch Screen")
        
        # Ips.
        self.ips = self.create_radio_buttons("Ips")
        
        # Weight.
        self.weight = self.create_text_area("Weight")
        
        # Cpu Frequency.
        self.cpu_frequency = self.create_text_area("Cpu Frequency")
        
        # Screen Width.
        self.screen_width = self.create_text_area("Screen Width")
        
        # Screen Height.
        self.screen_height = self.create_text_area("Screen Height")
        
        # Inches.
        self.inches = self.create_text_area("Inches")
        
        # Ssd.
        self.ssd = self.create_text_area("Ssd (in GB)")
        
        # Ram.
        self.ram = self.create_text_area("Ram (in GB)")
        
        # Price
        self.price = self.create_text_area("Price (in Rs)")
        
        # Choose which button we want to use.
        if self.num < 2 :
            self.next_button()
        else :
            self.submit_button()
        

        
    def create_radio_buttons(self, text) :
        """Yes or No button."""
        
        # Create lable for button.
        self.create_label(text, "Times 10")
        
        # Create button and return value.
        option_var = tk.StringVar()
        option_var.set(False)
        radio_button1 = tk.Radiobutton(self.root, text="YES", variable=option_var, value = True)
        radio_button2 = tk.Radiobutton(self.root, text="NO", variable=option_var, value = False)
        radio_button1.pack()
        radio_button2.pack()
        return option_var



    def next_button(self) :
        """Create button and map with its command."""
        
        self.next_b = tk.Button(self.root, text="next", command=self.next)
        self.next_b.pack()



    def submit_button(self) :
        """Create button and map with its command."""
        
        self.submit_b = tk.Button(self.root, text="PRIDICTOR", command=self.pridictor)
        self.submit_b.pack()


    
    def create_combobox(self, text, options) :
        """Select box."""
        
        # Create lable for combobox.
        self.create_label(text, "Times 10")
        
        # Create combobox and return value.
        combobox = ttk.Combobox(self.root, values=options)
        combobox.set(options[0])
        combobox.pack()
        return combobox



    def create_text_area(self, text) :
        """Text box."""
        
        # Create lable for text_area.
        self.create_label(text, "Times 10")
        
        # Create text box and return value.
        text_area = tk.Text(self.root, height=1, width=25)
        text_area.pack()
        return text_area



    def next(self) :
        """Next laptop information command."""
        
        # Save data.
        self.save()
        
        # Clear screen.
        self.clear()
        
        # goto next laptop information section.
        self.num += 1
        my_gui.get_data()


        
    def pridictor(self) :
        """Next pridictor command."""
        
        # Save data.
        self.save()
        
        # Clear screen.
        self.clear()
        
        # Pridict data with given information.
        self.pridict_data()
        min_percentage_index = self.compare_max()
        
        # Show max profit laptop on given choices.
        self.show(min_percentage_index)
        self.root.bind("<Return>", self.thanks)
        
        
        
    def pridict_data(self) :
        """Pridict data and save it."""
        
        # Pridict data.
        self.predict = Laptop_Price_Predictor()
        self.predict.data_clean()
        self.predict.train_data()
        
        laptop = []
        for info in self.laptop :
            pridicted_price = self.predict.predict(info)
            profit_percentage = ((pridicted_price-info["price"])/pridicted_price)* 100 / info["price"]
            info.update({"pridicted_price" : pridicted_price, "profit_percentage" : profit_percentage})
            laptop.append(info)
        self.laptop = laptop
        
        
        
    def show(self, print_index) :
        """Show the given index laptop information."""
        
        for info_key, info_value in self.laptop[print_index].items() :
            self.create_label(f"{info_key} - {info_value}", "Times 25")
        
        
        
    def thanks(self, evant = None) :
        """Thanking window."""
        
        # Clear screen.
        self.clear()
        
        # Print text and bind enter button with exit.
        self.create_label("Thank You", "Times 128")
        self.create_label("Created By - Prince Sharma", "Times 26")
        self.root.bind("<Return>", self.exit)
        
        
        
    def compare_max(self) :
        """Compare for max profit percentage in among options and return index."""
        
        max_index = 0
        max_percentage = self.laptop[0]["profit_percentage"]
        for info_index in range(1,len(self.laptop)) :
            if self.laptop[info_index]["profit_percentage"] > max_percentage :
                max_percentage = self.laptop[info_index]["profit_percentage"]
                max_index = info_index
        return max_index
        
        
        
    def save(self) :
        """Save data."""
        
        self.info["brand"] = self.brand.get()
        self.info["op_sys"] = self.op_sys.get()
        self.info["type_name"] = self.type.get()
        self.info["cpu"] = self.cpu.get()
        self.info["gpu"] = self.gpu.get()
        self.info["touch_screen"] = self.touch_screen.get()
        self.info["ips"] = self.ips.get()
        self.info["weight"] = float(self.weight.get('1.0', tk.END))
        self.info["cpu_frequency"] = float(self.cpu_frequency.get('1.0', tk.END))
        self.info["screen_width"] = float(self.screen_width.get('1.0', tk.END))
        self.info["screen_heigth"] = float(self.screen_height.get('1.0', tk.END))
        self.info["ssd"] = float(self.ssd.get('1.0', tk.END))
        self.info["ram"] = float(self.ram.get('1.0', tk.END))
        self.info["inches"] = float(self.inches.get('1.0', tk.END))
        self.info["price"] = float(self.price.get('1.0', tk.END))
        self.laptop.append(self.info)
        
        
        
    def clear(self) :
        """Clear screen."""
        
        for widget in self.root.winfo_children() :
            widget.destroy()
        
        
        
    def create_label(self, text, font) :
        """Print text."""
        
        self.label = tk.Label(self.root, text=text, font=font)
        self.label.pack()
        
        
        
    def toggle_fullscreen(self, evant=None) :
        """Full_screen on or off."""
        
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
        return "break"
        
        
        
    def exit(self, evant=None) :
        """Exit the program."""
        
        sys.exit()



if __name__ == "__main__":
    root = tk.Tk()
    my_gui = Gui(root)
    my_gui.get_data()
    root.mainloop()