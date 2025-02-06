import tkinter as tk
from tkinter import ttk

class ModulationBase:
    """Base class for modulation types with common UI elements and a constellation diagram."""
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent, padding="5")
        self.current_row = 0  # used for grid layout row tracking
        self.build_widgets()
        self.build_diagram()
    
    def build_widgets(self):
        # Create common widgets: modulation rate entry and data rate label.
        ttk.Label(self.frame, text="Modulation Rate (symbols/s):").grid(row=self.current_row, column=0, sticky=tk.W, padx=5, pady=5)
        self.rate_var = tk.StringVar(value="0")
        self.rate_entry = ttk.Entry(self.frame, textvariable=self.rate_var)
        self.rate_entry.grid(row=self.current_row, column=1, sticky=tk.E, padx=5, pady=5)
        self.current_row += 1
        
        ttk.Label(self.frame, text="Data Rate:").grid(row=self.current_row, column=0, sticky=tk.W, padx=5, pady=5)
        self.data_rate_var = tk.StringVar(value="0.00 bits/s")
        self.data_rate_label = ttk.Label(self.frame, textvariable=self.data_rate_var)
        self.data_rate_label.grid(row=self.current_row, column=1, sticky=tk.E, padx=5, pady=5)
        self.current_row += 1
    
    def build_diagram(self):
        # Create a label to display the constellation diagram.
        self.diagram_var = tk.StringVar(value=self.get_diagram())
        # Use a monospace font so the text diagram aligns nicely.
        self.diagram_label = ttk.Label(self.frame, textvariable=self.diagram_var, font=("Courier", 12))
        self.diagram_label.grid(row=self.current_row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10)
        self.current_row += 1
    
    def calculate_data_rate(self):
        try:
            rate = float(self.rate_var.get())
        except ValueError:
            return "Invalid input"
        # For the base modulation (BPSK), data rate equals modulation rate.
        return f"{rate:.2f} bits/s"
    
    def update(self):
        self.data_rate_var.set(self.calculate_data_rate())
        self.diagram_var.set(self.get_diagram())
    
    def get_frame(self):
        return self.frame
    
    def get_diagram(self):
        # Default constellation diagram for BPSK.
        return "*                *"

class QPSKModulation(ModulationBase):
    """QPSK modulation where the data rate is twice the modulation rate and constellation diagram differs."""
    def calculate_data_rate(self):
        try:
            rate = float(self.rate_var.get())
        except ValueError:
            return "Invalid input"
        data_rate = rate * 2.0
        return f"{data_rate:.2f} bits/s"
    
    def get_diagram(self):
        # A simple text diagram for QPSK constellation.
        return "    *\n*       *\n    *"

class FSKModulation(ModulationBase):
    """FSK modulation with an additional parameter (e.g., Frequency Deviation) and custom diagram."""
    def build_widgets(self):
        # Build the common widgets first.
        super().build_widgets()
        # Add an extra widget specific to FSK: Frequency Deviation.
        ttk.Label(self.frame, text="Frequency Deviation (Hz):").grid(row=self.current_row, column=0, sticky=tk.W, padx=5, pady=5)
        self.freq_dev_var = tk.StringVar(value="0")
        self.freq_dev_entry = ttk.Entry(self.frame, textvariable=self.freq_dev_var)
        self.freq_dev_entry.grid(row=self.current_row, column=1, sticky=tk.E, padx=5, pady=5)
        self.current_row += 1
    
    def calculate_data_rate(self):
        try:
            rate = float(self.rate_var.get())
        except ValueError:
            return "Invalid input"
        try:
            freq_dev = float(self.freq_dev_var.get())
        except ValueError:
            freq_dev = 0
        # Example calculation: modulation rate plus a fraction of frequency deviation.
        data_rate = rate + (freq_dev / 1000.0)
        return f"{data_rate:.2f} bits/s"
    
    def get_diagram(self):
        # Provide a placeholder diagram for FSK.
        return "FSK constellation diagram\n(not defined)"

class App:
    """Main application class for the signal parameter calculator."""
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Parameter Calculator")
        # Map modulation type names to their corresponding classes.
        self.mod_types = {
            "BPSK": ModulationBase,
            "QPSK": QPSKModulation,
            "FSK": FSKModulation
        }
        self.selected_mod_type = tk.StringVar(value="BPSK")
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        # Create the label and dropdown for selecting the modulation type.
        ttk.Label(self.main_frame, text="Modulation Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.mod_menu = ttk.OptionMenu(self.main_frame, self.selected_mod_type, "BPSK", *self.mod_types.keys(), command=self.change_mod_type)
        self.mod_menu.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Container for modulation-specific widgets.
        self.mod_frame_container = ttk.Frame(self.main_frame, padding="5", relief="groove")
        self.mod_frame_container.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.current_mod_obj = None
        self.change_mod_type("BPSK")
    
    def change_mod_type(self, mod_name):
        # Clear any existing modulation-specific widgets.
        for widget in self.mod_frame_container.winfo_children():
            widget.destroy()
        # Instantiate and display the selected modulation type.
        mod_class = self.mod_types.get(mod_name, ModulationBase)
        self.current_mod_obj = mod_class(self.mod_frame_container)
        self.current_mod_obj.get_frame().grid(row=0, column=0, sticky=(tk.W, tk.E))
        # Bind input changes to update calculations in real time.
        self.current_mod_obj.rate_var.trace_add("write", lambda *args: self.current_mod_obj.update())
        if hasattr(self.current_mod_obj, 'freq_dev_var'):
            self.current_mod_obj.freq_dev_var.trace_add("write", lambda *args: self.current_mod_obj.update())
        self.current_mod_obj.update()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# -----------------------------------------------------------------------------------
# How to add a new modulation type and unique data to the GUI:
#
# 1. Create a new subclass (e.g., class MyNewModulation(ModulationBase):) that inherits
#    from ModulationBase (or one of its subclasses if that is more appropriate).
#
# 2. In your new subclass, override the calculate_data_rate() method to implement your
#    specific logic for computing the data rate. For example, if your modulation requires
#    multiplying the modulation rate by a unique factor, include that in the calculation.
#
# 3. If your modulation type requires a different constellation diagram, override the
#    get_diagram() method to return a multi-line string that visually represents your
#    constellation points.
#
# 4. If your new modulation type needs additional input fields (unique parameters), override
#    the build_widgets() method. You can call super().build_widgets() to include the common
#    widgets, and then add your custom widgets below.
#
# 5. Finally, add your new modulation type to the self.mod_types dictionary in the App class.
#    For example, add:
#         "MyNewMod": MyNewModulation
#    This will automatically include your new modulation type in the drop-down menu, and when
#    selected, the corresponding widgets and logic will be loaded into the GUI.
# -----------------------------------------------------------------------------------
