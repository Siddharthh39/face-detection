import tkinter as tk

def show_logged_in_window():
    root = tk.Tk()
    root.title("Login Status")
    root.geometry("300x100")
    
    label = tk.Label(root, text="You are logged in!", font=("Helvetica", 16))
    label.pack(pady=20)
    
    # Automatically close the window after 3 seconds
    root.after(3000, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    show_logged_in_window()
