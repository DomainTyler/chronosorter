import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime
import webbrowser

class ChronoSorterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chrono Sorter")
        self.geometry("900x600")
        self.minsize(700, 500)
        self.iconbitmap('')  # Remove window icon (Windows only)
        
        self.is_light_mode = True
        self.last_operation = None  # For undo
        
        self.configure(bg="#f0f4ff")
        
        self.create_widgets()
        self.apply_theme()
        
    def create_widgets(self):
        # Folder selection
        self.frame_top = tk.Frame(self, bg=self['bg'])
        self.frame_top.pack(fill='x', pady=10, padx=10)

        self.folder_path_var = tk.StringVar()
        self.entry_folder = tk.Entry(self.frame_top, textvariable=self.folder_path_var, font=("Segoe UI", 12), state="readonly",
                                    readonlybackground="white", fg="black", relief='flat', borderwidth=1)
        self.entry_folder.pack(side='left', fill='x', expand=True, padx=(0,10))
        
        self.btn_browse = tk.Button(self.frame_top, text="Browse Folder", command=self.browse_folder, font=("Segoe UI", 11),
                                   relief='flat', highlightthickness=0, borderwidth=0)
        self.btn_browse.pack(side='left')
        
        # Buttons frame
        self.frame_buttons = tk.Frame(self, bg=self['bg'])
        self.frame_buttons.pack(fill='x', padx=10, pady=(0,10))
        
        self.btn_organize = tk.Button(self.frame_buttons, text="Organize Files", command=self.organize_files, font=("Segoe UI", 11),
                                     relief='flat', highlightthickness=0, borderwidth=0)
        self.btn_organize.pack(side='left', expand=True, fill='x', padx=(0, 5))
        
        self.btn_undo = tk.Button(self.frame_buttons, text="Undo Last", command=self.undo_last_operation, font=("Segoe UI", 11),
                                 relief='flat', highlightthickness=0, borderwidth=0, state='disabled')
        self.btn_undo.pack(side='left', expand=True, fill='x', padx=(5, 5))
        
        self.btn_toggle_theme = tk.Button(self.frame_buttons, text="Switch to Dark Mode", command=self.toggle_theme, font=("Segoe UI", 11),
                                         relief='flat', highlightthickness=0, borderwidth=0)
        self.btn_toggle_theme.pack(side='left', expand=True, fill='x', padx=(5, 0))
        
        # Log area
        self.frame_log = tk.Frame(self, bg=self['bg'])
        self.frame_log.pack(fill='both', expand=True, padx=10, pady=(0,10))
        
        self.log_text = scrolledtext.ScrolledText(self.frame_log, font=("Consolas", 11), state='disabled', relief='sunken', borderwidth=2)
        self.log_text.pack(fill='both', expand=True)

        # Footer frame
        self.frame_footer = tk.Frame(self, bg=self['bg'])
        self.frame_footer.pack(fill='x', padx=10, pady=5)

        self.footer_label = tk.Label(self.frame_footer, text="by DomainTyler", font=("Segoe UI", 9))
        self.footer_label.pack(side='left')

        self.btn_github = tk.Button(self.frame_footer, text="Visit GitHub", command=self.open_github, font=("Segoe UI", 9),
                                    relief='flat', highlightthickness=0, borderwidth=0)
        self.btn_github.pack(side='right')

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            self.log(f"Selected folder: {folder_selected}")
        
    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state='disabled')
        
    def organize_files(self):
        folder = self.folder_path_var.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder.")
            return
        
        self.btn_organize.config(state='disabled')
        self.btn_undo.config(state='disabled')
        self.last_operation = {'moved': [], 'original': []}
        
        try:
            for root, dirs, files in os.walk(folder):
                base_folder_name = os.path.basename(root)
                for filename in files:
                    try:
                        file_path = os.path.join(root, filename)
                        created_time = os.path.getctime(file_path)
                        date_str = datetime.fromtimestamp(created_time).strftime("%Y-%m-%d")
                        
                        dated_folder = os.path.join(folder, base_folder_name, date_str)
                        os.makedirs(dated_folder, exist_ok=True)
                        
                        base, ext = os.path.splitext(filename)
                        dest_path = os.path.join(dated_folder, filename)
                        
                        counter = 1
                        while os.path.exists(dest_path):
                            dest_path = os.path.join(dated_folder, f"{base}_{counter}{ext}")
                            counter += 1
                        
                        shutil.move(file_path, dest_path)
                        self.last_operation['moved'].append(dest_path)
                        self.last_operation['original'].append(file_path)
                        self.log(f"Moved: {file_path} → {dest_path}")
                    except Exception as e:
                        self.log(f"Error moving {file_path}: {e}")
            
            self.btn_undo.config(state='normal')
            messagebox.showinfo("Success", "Files organized successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        finally:
            self.btn_organize.config(state='normal')
        
    def undo_last_operation(self):
        if not self.last_operation:
            messagebox.showinfo("Undo", "Nothing to undo.")
            return
        
        self.btn_organize.config(state='disabled')
        self.btn_undo.config(state='disabled')
        
        errors = []
        for moved_path, original_path in zip(self.last_operation['moved'], self.last_operation['original']):
            try:
                orig_dir = os.path.dirname(original_path)
                os.makedirs(orig_dir, exist_ok=True)
                shutil.move(moved_path, original_path)
                self.log(f"Moved back: {moved_path} → {original_path}")
            except Exception as e:
                errors.append(f"Error moving back {moved_path}: {e}")
        
        if errors:
            messagebox.showwarning("Undo Completed with Errors", "\n".join(errors))
        else:
            messagebox.showinfo("Undo Completed", "Undo operation completed successfully.")
        
        self.last_operation = None
        self.btn_undo.config(state='disabled')
        self.btn_organize.config(state='normal')
        
    def toggle_theme(self):
        self.is_light_mode = not self.is_light_mode
        self.apply_theme()
        
    def apply_theme(self):
        if self.is_light_mode:
            bg = "#f0f4ff"
            fg = "black"
            btn_bg = "#0078d7"
            btn_active_bg = "#005a9e"
            log_bg = "white"
            log_fg = "black"
            toggle_text = "Switch to Dark Mode"
            footer_fg = "#555555"
        else:
            bg = "#2b2b2b"
            fg = "white"
            btn_bg = "#0a84ff"
            btn_active_bg = "#0050a0"
            log_bg = "#3c3c3c"
            log_fg = "white"
            toggle_text = "Switch to Light Mode"
            footer_fg = "#aaa"
        
        self.configure(bg=bg)
        # Frames
        self.frame_top.configure(bg=bg)
        self.frame_buttons.configure(bg=bg)
        self.frame_log.configure(bg=bg)
        self.frame_footer.configure(bg=bg)
        
        # Entry
        self.entry_folder.configure(background=log_bg, foreground=fg, readonlybackground=log_bg)
        # Log
        self.log_text.configure(bg=log_bg, fg=log_fg)
        
        # Buttons
        for btn in [self.btn_browse, self.btn_organize, self.btn_undo, self.btn_toggle_theme, self.btn_github]:
            btn.configure(bg=btn_bg, fg="white", activebackground=btn_active_bg, activeforeground="white")
        
        self.btn_toggle_theme.configure(text=toggle_text)
        self.footer_label.configure(bg=bg, fg=footer_fg)
        
    def open_github(self):
        webbrowser.open("https://github.com/DomainTyler")

if __name__ == "__main__":
    app = ChronoSorterApp()
    app.mainloop()
