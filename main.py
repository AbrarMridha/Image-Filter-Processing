# Main function to run the GUI
import GUI
import tkinter as tk
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI.ImageProcessingApp(root)
    root.mainloop()