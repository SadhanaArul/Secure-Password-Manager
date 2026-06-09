"""
main.py - Modern Beautiful Password Manager UI (Fixed Table Alignment)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import DatabaseManager
from password_generator import PasswordGenerator

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure Password Manager")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)
        self.root.minsize(1100, 650)
        
        # Initialize database and password generator
        self.db = DatabaseManager()
        self.pw_generator = PasswordGenerator()
        
        # Modern color scheme
        self.colors = {
            'bg': '#1e1e2e',
            'surface': '#2d2d3f',
            'primary': '#89b4fa',
            'secondary': '#cba6f7',
            'accent': '#f38ba8',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'error': '#f38ba8',
            'text': '#cdd6f4',
            'text_secondary': '#a6adc8'
        }
        
        self.setup_styles()
        self.create_widgets()
        self.center_window()
    
    def setup_styles(self):
        """Configure modern styles"""
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Modern.Treeview', 
                       background=self.colors['surface'],
                       foreground=self.colors['text'],
                       fieldbackground=self.colors['surface'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       rowheight=35)
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['primary'],
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0)
        
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['secondary'])])
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create all beautiful widgets"""
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Header Section
        self.create_header(main_frame)
        
        # Input Section
        self.create_input_section(main_frame)
        
        # Button Section
        self.create_button_section(main_frame)
        
        # Results Section
        self.create_results_section(main_frame)
    
    def create_header(self, parent):
        """Create beautiful header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title = tk.Label(header_frame, 
                        text="🔐 Secure Password Manager",
                        font=('Segoe UI', 28, 'bold'),
                        bg=self.colors['bg'],
                        fg=self.colors['primary'])
        title.pack()
        
        # Subtitle
        subtitle = tk.Label(header_frame,
                          text="Store and manage your passwords securely",
                          font=('Segoe UI', 11),
                          bg=self.colors['bg'],
                          fg=self.colors['text_secondary'])
        subtitle.pack(pady=(5, 0))
        
        # Separator line
        separator = tk.Frame(header_frame, height=2, bg=self.colors['surface'])
        separator.pack(fill=tk.X, pady=(15, 0))
    
    def create_input_section(self, parent):
        """Create modern input section"""
        # Card frame
        card = tk.Frame(parent, bg=self.colors['surface'], relief=tk.FLAT)
        card.pack(fill=tk.X, pady=(0, 20))
        
        # Add padding inside card
        content = tk.Frame(card, bg=self.colors['surface'])
        content.pack(fill=tk.X, padx=25, pady=20)
        
        # Card title
        card_title = tk.Label(content,
                            text="📝 Password Details",
                            font=('Segoe UI', 14, 'bold'),
                            bg=self.colors['surface'],
                            fg=self.colors['secondary'])
        card_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Website input
        self.create_input_row(content, "🌐 Website / Application:", "website_entry", 0)
        
        # Username input
        self.create_input_row(content, "👤 Username / Email:", "username_entry", 1)
        
        # Password input with show/hide
        self.create_password_row(content, "🔑 Password:", 2)
        
        # Password strength
        strength_frame = tk.Frame(content, bg=self.colors['surface'])
        strength_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.strength_label = tk.Label(strength_frame,
                                      text="⚡ Password Strength: ",
                                      font=('Segoe UI', 10),
                                      bg=self.colors['surface'],
                                      fg=self.colors['text_secondary'])
        self.strength_label.pack(anchor=tk.W)
        
        # Strength meter
        self.strength_meter = tk.Canvas(strength_frame, height=5, 
                                       bg=self.colors['bg'],
                                       highlightthickness=0)
        self.strength_meter.pack(fill=tk.X, pady=(5, 0))
    
    def create_input_row(self, parent, label_text, attr_name, row):
        """Create a labeled input row"""
        frame = tk.Frame(parent, bg=self.colors['surface'])
        frame.pack(fill=tk.X, pady=8)
        
        label = tk.Label(frame,
                        text=label_text,
                        font=('Segoe UI', 10),
                        bg=self.colors['surface'],
                        fg=self.colors['text'],
                        width=22,
                        anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        entry = tk.Entry(frame,
                        font=('Segoe UI', 10),
                        bg=self.colors['bg'],
                        fg=self.colors['text'],
                        insertbackground=self.colors['text'],
                        relief=tk.FLAT,
                        highlightthickness=1,
                        highlightcolor=self.colors['primary'],
                        highlightbackground=self.colors['surface'])
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        setattr(self, attr_name, entry)
    
    def create_password_row(self, parent, label_text, row):
        """Create password row with show/hide button"""
        frame = tk.Frame(parent, bg=self.colors['surface'])
        frame.pack(fill=tk.X, pady=8)
        
        label = tk.Label(frame,
                        text=label_text,
                        font=('Segoe UI', 10),
                        bg=self.colors['surface'],
                        fg=self.colors['text'],
                        width=22,
                        anchor=tk.W)
        label.pack(side=tk.LEFT)
        
        self.password_entry = tk.Entry(frame,
                                      font=('Segoe UI', 10),
                                      bg=self.colors['bg'],
                                      fg=self.colors['text'],
                                      insertbackground=self.colors['text'],
                                      relief=tk.FLAT,
                                      show="*",
                                      highlightthickness=1,
                                      highlightcolor=self.colors['primary'],
                                      highlightbackground=self.colors['surface'])
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.show_password = tk.BooleanVar(value=False)
        self.toggle_btn = tk.Button(frame,
                                   text="👁 Show",
                                   command=self.toggle_password_visibility,
                                   bg=self.colors['primary'],
                                   fg=self.colors['bg'],
                                   font=('Segoe UI', 9),
                                   relief=tk.FLAT,
                                   cursor="hand2",
                                   padx=10,
                                   pady=3)
        self.toggle_btn.pack(side=tk.RIGHT)
        
        # Bind strength check
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)
    
    def create_button_section(self, parent):
        """Create modern button section"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Row 1 buttons
        row1 = tk.Frame(button_frame, bg=self.colors['bg'])
        row1.pack(pady=5)
        
        buttons = [
            ("🎲 Generate Password", self.generate_password, self.colors['secondary']),
            ("💾 Save Password", self.save_password, self.colors['success']),
            ("🗑 Clear Fields", self.clear_fields, self.colors['error'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(row1,
                           text=text,
                           command=command,
                           bg=color,
                           fg=self.colors['bg'],
                           font=('Segoe UI', 10, 'bold'),
                           relief=tk.FLAT,
                           cursor="hand2",
                           padx=20,
                           pady=10)
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Row 2 buttons
        row2 = tk.Frame(button_frame, bg=self.colors['bg'])
        row2.pack(pady=5)
        
        action_buttons = [
            ("📋 View All Passwords", self.view_passwords, self.colors['primary']),
            ("🔍 Search Password", self.search_password, self.colors['secondary']),
            ("🗑 Delete Password", self.delete_password, self.colors['error'])
        ]
        
        for text, command, color in action_buttons:
            btn = tk.Button(row2,
                           text=text,
                           command=command,
                           bg=color,
                           fg=self.colors['bg'],
                           font=('Segoe UI', 10, 'bold'),
                           relief=tk.FLAT,
                           cursor="hand2",
                           padx=20,
                           pady=10)
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def create_results_section(self, parent):
        """Create results table section with fixed alignment"""
        # Card frame
        card = tk.Frame(parent, bg=self.colors['surface'])
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = tk.Frame(card, bg=self.colors['surface'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 10))
        
        title = tk.Label(title_frame,
                        text="📋 Saved Passwords",
                        font=('Segoe UI', 14, 'bold'),
                        bg=self.colors['surface'],
                        fg=self.colors['secondary'])
        title.pack(anchor=tk.W)
        
        # Treeview frame
        tree_frame = tk.Frame(card, bg=self.colors['surface'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Create scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame,
                                columns=("ID", "Website", "Username", "Password"),
                                show="headings",
                                height=12,
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set,
                                style='Modern.Treeview')
        
        # Configure column headings
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Website", text="Website / Application", anchor=tk.W)
        self.tree.heading("Username", text="Username / Email", anchor=tk.W)
        self.tree.heading("Password", text="Password", anchor=tk.W)
        
        # IMPORTANT: Fixed column widths and alignment
        self.tree.column("ID", width=80, minwidth=80, anchor=tk.CENTER, stretch=False)
        self.tree.column("Website", width=350, minwidth=200, anchor=tk.W, stretch=True)
        self.tree.column("Username", width=350, minwidth=200, anchor=tk.W, stretch=True)
        self.tree.column("Password", width=280, minwidth=150, anchor=tk.W, stretch=True)
        
        # Configure scrollbars
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # Pack everything
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password_entry.configure(show="*")
            self.toggle_btn.configure(text="👁 Show")
            self.show_password.set(False)
        else:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="🙈 Hide")
            self.show_password.set(True)
    
    def generate_password(self):
        """Generate strong password"""
        password = self.pw_generator.generate_password(14)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.check_password_strength()
        messagebox.showinfo("Success", "✅ Strong password generated!")
    
    def check_password_strength(self, event=None):
        """Check and display password strength with meter"""
        password = self.password_entry.get()
        if password:
            strength, feedback = self.pw_generator.check_strength(password)
            self.strength_label.config(text=f"⚡ Password Strength: {strength}")
            
            # Update strength meter
            self.strength_meter.delete("all")
            meter_width = self.strength_meter.winfo_width()
            if meter_width < 10:
                meter_width = 400
            
            if strength == "Very Strong":
                color = self.colors['success']
                width_percent = 1.0
            elif strength == "Strong":
                color = "#a6e3a1"
                width_percent = 0.8
            elif strength == "Medium":
                color = self.colors['warning']
                width_percent = 0.6
            else:
                color = self.colors['error']
                width_percent = 0.3
            
            self.strength_meter.create_rectangle(0, 0, 
                                                meter_width * width_percent, 5,
                                                fill=color, outline="")
        else:
            self.strength_label.config(text="⚡ Password Strength: ")
            self.strength_meter.delete("all")
    
    def save_password(self):
        """Save password to database"""
        website = self.website_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not website or not username or not password:
            messagebox.showwarning("Warning", "⚠️ All fields are required!")
            return
        
        try:
            self.db.save_password(website, username, password)
            messagebox.showinfo("Success", "✅ Password saved successfully!")
            self.clear_fields()
            self.view_passwords()
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.website_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.strength_label.config(text="⚡ Password Strength: ")
        self.strength_meter.delete("all")
    
    def view_passwords(self):
        """Display all saved passwords"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            records = self.db.get_all_passwords()
            if records:
                for record in records:
                    # Mask password for display
                    password = record[3]
                    if len(password) > 8:
                        masked_pw = password[:4] + "..." + password[-2:]
                    else:
                        masked_pw = "*" * len(password)
                    
                    self.tree.insert("", tk.END, values=(record[0], record[1], record[2], masked_pw))
            else:
                messagebox.showinfo("Information", "📭 No passwords found!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")
    
    def search_password(self):
        """Search for passwords"""
        search_term = tk.simpledialog.askstring("🔍 Search", 
                                                "Enter website name or username:",
                                                parent=self.root)
        
        if search_term:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            try:
                records = self.db.search_passwords(search_term)
                if records:
                    for record in records:
                        password = record[3]
                        if len(password) > 8:
                            masked_pw = password[:4] + "..." + password[-2:]
                        else:
                            masked_pw = "*" * len(password)
                        
                        self.tree.insert("", tk.END, values=(record[0], record[1], record[2], masked_pw))
                else:
                    messagebox.showinfo("Information", "🔍 No matching passwords found!")
            except Exception as e:
                messagebox.showerror("Error", f"❌ {str(e)}")
    
    def delete_password(self):
        """Delete selected password"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "⚠️ Please select a password to delete!")
            return
        
        item = self.tree.item(selected[0])
        password_id = item['values'][0]
        
        if messagebox.askyesno("Confirm Delete", "🗑️ Are you sure you want to delete this password?"):
            try:
                if self.db.delete_password(password_id):
                    messagebox.showinfo("Success", "✅ Password deleted successfully!")
                    self.view_passwords()
                else:
                    messagebox.showerror("Error", "❌ Failed to delete password!")
            except Exception as e:
                messagebox.showerror("Error", f"❌ {str(e)}")

def main():
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()