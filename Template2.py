#!/usr/bin/env python3
"""
Template2.py - A CustomTkinter-based Installer UI Application

This module provides an installer interface using CustomTkinter library
with proper image handling to avoid CTkImage attribute access errors.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import os
import sys
from PIL import Image, ImageTk
import threading
import time

# Configure CustomTkinter appearance
ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class InstallerUI:
    """Main installer UI class using CustomTkinter."""
    
    def __init__(self):
        """Initialize the installer UI."""
        self.window = ctk.CTk()
        self.window.title("Installer Application")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Initialize logo image
        self.logo_ctk = None
        self._load_logo()
        
        # Initialize UI components
        self.canvas = None
        self.progress_bar = None
        self.status_label = None
        self.install_button = None
        
        # Build the UI
        self._build_ui()
    
    def _load_logo(self):
        """Load the logo image for the installer."""
        try:
            # Try to load logo from common locations
            logo_paths = [
                "logo.png",
                "assets/logo.png", 
                "images/logo.png",
                os.path.join(os.path.dirname(__file__), "logo.png"),
                os.path.join(os.path.dirname(__file__), "assets", "logo.png"),
                os.path.join(os.path.dirname(__file__), "images", "logo.png"),
            ]
            
            logo_loaded = False
            for path in logo_paths:
                if os.path.exists(path):
                    try:
                        # Load image using PIL first, then create CTkImage
                        pil_image = Image.open(path)
                        pil_image = pil_image.resize((100, 100), Image.Resampling.LANCZOS)
                        self.logo_ctk = ctk.CTkImage(pil_image, size=(100, 100))
                        logo_loaded = True
                        break
                    except Exception as e:
                        print(f"Failed to load logo from {path}: {e}")
                        continue
            
            if not logo_loaded:
                # Create a default placeholder image if no logo is found
                placeholder_image = Image.new('RGB', (100, 100), color='lightblue')
                self.logo_ctk = ctk.CTkImage(placeholder_image, size=(100, 100))
                
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Create a simple placeholder
            placeholder_image = Image.new('RGB', (100, 100), color='lightgray')
            self.logo_ctk = ctk.CTkImage(placeholder_image, size=(100, 100))
    
    def _build_ui(self):
        """Build the main user interface."""
        # Main container frame
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Calculate header height
        header_h = 120
        
        # Create a frame for the header content instead of using canvas
        header_content_frame = ctk.CTkFrame(header_frame, height=header_h)
        header_content_frame.pack(fill="x", padx=10, pady=10)
        header_content_frame.pack_propagate(False)
        
        # Logo section - use CTkLabel with image instead of canvas
        if self.logo_ctk:
            logo_label = ctk.CTkLabel(
                header_content_frame,
                image=self.logo_ctk,
                text=""  # No text, just image
            )
            logo_label.pack(side="left", padx=20, pady=10)
        
        # Title section
        title_frame = ctk.CTkFrame(header_content_frame)
        title_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Application Installer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Welcome to the installation wizard",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack()
        
        # Content section
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Installation options
        options_frame = ctk.CTkFrame(content_frame)
        options_frame.pack(fill="x", padx=20, pady=20)
        
        options_label = ctk.CTkLabel(
            options_frame,
            text="Installation Options",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        options_label.pack(pady=10)
        
        # Installation path
        path_frame = ctk.CTkFrame(options_frame)
        path_frame.pack(fill="x", padx=20, pady=10)
        
        path_label = ctk.CTkLabel(path_frame, text="Installation Path:")
        path_label.pack(anchor="w", padx=10, pady=5)
        
        path_entry_frame = ctk.CTkFrame(path_frame)
        path_entry_frame.pack(fill="x", padx=10, pady=5)
        
        self.path_entry = ctk.CTkEntry(
            path_entry_frame,
            placeholder_text="Select installation directory..."
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        browse_button = ctk.CTkButton(
            path_entry_frame,
            text="Browse",
            width=80,
            command=self._browse_path
        )
        browse_button.pack(side="right", padx=5)
        
        # Checkboxes for installation options
        self.create_desktop_var = ctk.BooleanVar(value=True)
        desktop_check = ctk.CTkCheckBox(
            options_frame,
            text="Create desktop shortcut",
            variable=self.create_desktop_var
        )
        desktop_check.pack(anchor="w", padx=30, pady=5)
        
        self.create_startmenu_var = ctk.BooleanVar(value=True)
        startmenu_check = ctk.CTkCheckBox(
            options_frame,
            text="Add to Start Menu",
            variable=self.create_startmenu_var
        )
        startmenu_check.pack(anchor="w", padx=30, pady=5)
        
        # Progress section
        progress_frame = ctk.CTkFrame(content_frame)
        progress_frame.pack(fill="x", padx=20, pady=20)
        
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to install",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=10)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        # Buttons section
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Button container for right alignment
        button_container = ctk.CTkFrame(button_frame)
        button_container.pack(side="right", padx=20, pady=10)
        
        self.cancel_button = ctk.CTkButton(
            button_container,
            text="Cancel",
            width=100,
            command=self._cancel_installation
        )
        self.cancel_button.pack(side="left", padx=5)
        
        self.install_button = ctk.CTkButton(
            button_container,
            text="Install",
            width=100,
            command=self._start_installation
        )
        self.install_button.pack(side="left", padx=5)
        
        # Set default installation path
        default_path = os.path.join(os.path.expanduser("~"), "Program Files", "MyApplication")
        self.path_entry.insert(0, default_path)
    
    def _browse_path(self):
        """Open directory browser for installation path."""
        try:
            directory = filedialog.askdirectory(
                title="Select Installation Directory",
                initialdir=self.path_entry.get() or os.path.expanduser("~")
            )
            if directory:
                self.path_entry.delete(0, tk.END)
                self.path_entry.insert(0, directory)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open directory browser: {e}")
    
    def _start_installation(self):
        """Start the installation process."""
        install_path = self.path_entry.get().strip()
        
        if not install_path:
            messagebox.showerror("Error", "Please select an installation directory.")
            return
        
        # Validate installation path
        try:
            os.makedirs(install_path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot create installation directory: {e}")
            return
        
        # Disable buttons during installation
        self.install_button.configure(state="disabled")
        self.cancel_button.configure(text="Close", state="disabled")
        
        # Start installation in a separate thread
        threading.Thread(target=self._perform_installation, daemon=True).start()
    
    def _perform_installation(self):
        """Perform the actual installation (simulated)."""
        try:
            # Simulate installation steps
            steps = [
                ("Preparing installation...", 0.1),
                ("Copying files...", 0.3),
                ("Creating shortcuts...", 0.6),
                ("Registering application...", 0.8),
                ("Finalizing installation...", 1.0)
            ]
            
            for step_text, progress in steps:
                # Update UI in main thread
                self.window.after(0, self._update_installation_progress, step_text, progress)
                
                # Simulate work
                time.sleep(1)
            
            # Installation complete
            self.window.after(0, self._installation_complete)
            
        except Exception as e:
            self.window.after(0, self._installation_error, str(e))
    
    def _update_installation_progress(self, status_text, progress):
        """Update installation progress in the UI."""
        self.status_label.configure(text=status_text)
        self.progress_bar.set(progress)
    
    def _installation_complete(self):
        """Handle installation completion."""
        self.status_label.configure(text="Installation completed successfully!")
        self.progress_bar.set(1.0)
        self.cancel_button.configure(text="Finish", state="normal")
        
        messagebox.showinfo("Success", "Installation completed successfully!")
    
    def _installation_error(self, error_message):
        """Handle installation error."""
        self.status_label.configure(text=f"Installation failed: {error_message}")
        self.progress_bar.set(0)
        self.install_button.configure(state="normal")
        self.cancel_button.configure(text="Cancel", state="normal")
        
        messagebox.showerror("Installation Error", f"Installation failed: {error_message}")
    
    def _cancel_installation(self):
        """Cancel installation or close the application."""
        if self.cancel_button.cget("text") == "Finish":
            self.window.quit()
        else:
            result = messagebox.askyesno(
                "Confirm Exit",
                "Are you sure you want to cancel the installation?"
            )
            if result:
                self.window.quit()
    
    def run(self):
        """Run the installer application."""
        try:
            # Center the window on screen
            self.window.update_idletasks()
            width = self.window.winfo_width()
            height = self.window.winfo_height()
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f"{width}x{height}+{x}+{y}")
            
            # Start the main loop
            self.window.mainloop()
            
        except Exception as e:
            messagebox.showerror("Application Error", f"An error occurred: {e}")
            sys.exit(1)


def main():
    """Main entry point for the application."""
    try:
        # Ensure required libraries are available
        import customtkinter
        import PIL
        
        print("Starting Installer Application...")
        
        # Create and run the installer UI
        app = InstallerUI()
        app.run()
        
    except ImportError as e:
        error_msg = f"Required library not found: {e}\n\nPlease install required dependencies:\npip install customtkinter pillow"
        print(error_msg)
        
        # Try to show error in GUI if tkinter is available
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()  # Hide root window
            messagebox.showerror("Missing Dependencies", error_msg)
        except:
            pass
        
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Application startup failed: {e}"
        print(error_msg)
        
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()