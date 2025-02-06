import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter, PdfMerger
from pdf2image import convert_from_path
from PIL import Image, ImageTk


class PDFViewer(tk.Toplevel):
    def __init__(self, master, pdf_path):
        super().__init__(master)
        self.pdf_path = pdf_path
        self.title("PDF Viewer")
        self.geometry("1200x800")
        self.config(bg="#ecf0f1")
        self.update_idletasks()

        self.top_margin = 50
        self.side_menu_width = 50
        self.extra_margin = 50
        self.zoom_factor = 1.0
        self.side_menu_visible = False


        self.pdf_reader = None
        self.original_images = []
        self.image_refs = []
        self.image_labels = []

        self.build_toolbar()
        self.build_ui()
        self.load_pdf()

        self.resize_after_id = None
        self.bind("<Configure>", self.on_resize)

    def build_toolbar(self):
        self.toolbar = tk.Frame(self, bg="#2c3e50")
        self.toolbar.pack(fill=tk.X)


        self.btn_download = tk.Button(self.toolbar, text="Download PDF",
                                      bg="#2ecc71", fg="black",
                                      activebackground="#27ae60", activeforeground="black",
                                      font=("Helvetica", 10, "bold"), bd=0,
                                      command=self.download_pdf)
        self.btn_download.pack(side=tk.LEFT, padx=5, pady=5)


        self.btn_rotate_all_cw = tk.Button(self.toolbar, text="Rotate All (CW)",
                                           bg="#e74c3c", fg="black",
                                           activebackground="#c0392b", activeforeground="black",
                                           font=("Helvetica", 10, "bold"), bd=0,
                                           command=self.rotate_all_cw)
        self.btn_rotate_all_cw.pack(side=tk.LEFT, padx=5, pady=5)


        self.btn_rotate_all_ccw = tk.Button(self.toolbar, text="Rotate All (CCW)",
                                            bg="#e74c3c", fg="black",
                                            activebackground="#c0392b", activeforeground="black",
                                            font=("Helvetica", 10, "bold"), bd=0,
                                            command=self.rotate_all_ccw)
        self.btn_rotate_all_ccw.pack(side=tk.LEFT, padx=5, pady=5)


        self.btn_zoom_in = tk.Button(self.toolbar, text="+",
                                     bg="#34495e", fg="black",
                                     activebackground="#2c3e50", activeforeground="black",
                                     font=("Helvetica", 10, "bold"), bd=0,
                                     command=self.zoom_in)
        self.btn_zoom_in.pack(side=tk.LEFT, padx=5, pady=5)


        self.btn_zoom_out = tk.Button(self.toolbar, text="-",
                                      bg="#34495e", fg="black",
                                      activebackground="#2c3e50", activeforeground="black",
                                      font=("Helvetica", 10, "bold"), bd=0,
                                      command=self.zoom_out)
        self.btn_zoom_out.pack(side=tk.LEFT, padx=5, pady=5)


        self.btn_toggle_side = tk.Button(self.toolbar, text="Hide Side Menu",
                                         bg="#3498db", fg="black",
                                         activebackground="#2980b9", activeforeground="black",
                                         font=("Helvetica", 10, "bold"), bd=0,
                                         command=self.toggle_side_menu)
        self.btn_toggle_side.pack(side=tk.LEFT, padx=5, pady=5)

    def build_ui(self):
        self.paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#ecf0f1")
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.paned, bg="white")
        self.paned.add(self.left_frame, stretch="always")
        self.canvas = tk.Canvas(self.left_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.left_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.image_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.image_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        self.right_frame = tk.Frame(self.paned, bg="#bdc3c7", relief=tk.RAISED, borderwidth=1)
        self.right_frame.config(width=self.side_menu_width)
        self.paned.add(self.right_frame)


        self.paned.paneconfigure(self.right_frame, minsize=self.side_menu_width, width=self.side_menu_width)

        self.lbl_side = tk.Label(self.right_frame, text="Page Selection", bg="#bdc3c7", fg="black",
                                 font=("Helvetica", 12, "bold"))
        self.lbl_side.pack(pady=10)
        self.listbox = tk.Listbox(self.right_frame, selectmode=tk.MULTIPLE, bg="white", fg="black",
                                  font=("Helvetica", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.btn_selected = tk.Button(self.right_frame, text="Create PDF with Selected",
                                      bg="#27ae60", fg="black",
                                      activebackground="#1e8449", activeforeground="black",
                                      font=("Helvetica", 10, "bold"), bd=0,
                                      command=self.create_pdf_selected)
        self.btn_selected.pack(pady=5, fill=tk.X, padx=10)
        self.btn_unselected = tk.Button(self.right_frame, text="Create PDF without Selected",
                                        bg="#e67e22", fg="black",
                                        activebackground="#d35400", activeforeground="black",
                                        font=("Helvetica", 10, "bold"), bd=0,
                                        command=self.create_pdf_unselected)
        self.btn_unselected.pack(pady=5, fill=tk.X, padx=10)

        self.rotate_frame = tk.Frame(self.right_frame, bg="#bdc3c7")
        self.rotate_frame.pack(pady=10, fill=tk.X, padx=10)

        self.btn_rotate_selected_cw = tk.Button(self.rotate_frame, text="Rotate Selected (CW)",
                                                bg="#e67e22", fg="black",
                                                activebackground="#d35400", activeforeground="black",
                                                font=("Helvetica", 10, "bold"), bd=0,
                                                command=self.rotate_selected_cw)
        self.btn_rotate_selected_cw.pack(pady=5, fill=tk.X)
        self.btn_rotate_selected_ccw = tk.Button(self.rotate_frame, text="Rotate Selected (CCW)",
                                                 bg="#e67e22", fg="black",
                                                 activebackground="#d35400", activeforeground="black",
                                                 font=("Helvetica", 10, "bold"), bd=0,
                                                 command=self.rotate_selected_ccw)
        self.btn_rotate_selected_ccw.pack(pady=5, fill=tk.X)


    def load_pdf(self):
        try:
            self.pdf_reader = PdfReader(self.pdf_path)
        except Exception as e:
            messagebox.showerror("Hata", f"PDF yüklenirken hata:\n{e}")
            return
        try:
            self.original_images = convert_from_path(self.pdf_path, dpi=150)
        except Exception as e:
            messagebox.showerror("Hata", f"PDF görüntüleme sırasında hata:\n{e}")
            return
        if not self.original_images:
            messagebox.showerror("Hata", "PDF sayfaları resme dönüştürülemedi.")
            return
        self.update_display(initial=True)

    def update_display(self, initial=False):
        current_width = self.winfo_width()
        current_height = self.winfo_height()
        current_side = self.side_menu_width if self.side_menu_visible else 0
        new_available_width = current_width - current_side - self.extra_margin
        new_available_height = current_height - self.top_margin - self.extra_margin

        new_refs = []
        for i, orig in enumerate(self.original_images):
            ratio_w = new_available_width / orig.width
            ratio_h = new_available_height / orig.height
            scale_ratio = min(ratio_w, ratio_h, 1.0) * self.zoom_factor
            new_w = int(orig.width * scale_ratio)
            new_h = int(orig.height * scale_ratio)
            resized = orig.resize((new_w, new_h), Image.Resampling.LANCZOS)
            new_photo = ImageTk.PhotoImage(resized)
            new_refs.append(new_photo)
            if i < len(self.image_labels):
                self.image_labels[i].config(image=new_photo)
            else:
                lbl = tk.Label(self.image_frame, image=new_photo, bg="white")
                lbl.pack(pady=5)
                self.image_labels.append(lbl)
        self.image_refs = new_refs

        if initial:
            self.listbox.delete(0, tk.END)
            for i in range(len(self.original_images)):
                self.listbox.insert(tk.END, f"Sayfa {i+1}")

    def on_resize(self, event):
        if hasattr(self, 'resize_after_id'):
            self.after_cancel(self.resize_after_id)
        self.resize_after_id = self.after(100, self.update_display)

    def toggle_side_menu(self):
        if self.side_menu_visible:
            self.paned.forget(self.right_frame)
            self.side_menu_visible = False
            self.btn_toggle_side.config(text="Show Side Menu")
        else:
            self.paned.add(self.right_frame)
            self.side_menu_visible = True
            self.btn_toggle_side.config(text="Hide Side Menu")
        self.update_display()

    def rotate_all_cw(self):
        for i in range(len(self.original_images)):
            self.original_images[i] = self.original_images[i].rotate(-90, expand=True)
        self.update_display()

    def rotate_all_ccw(self):
        for i in range(len(self.original_images)):
            self.original_images[i] = self.original_images[i].rotate(90, expand=True)
        self.update_display()

    def rotate_selected_cw(self):
        sel = list(self.listbox.curselection())
        if not sel:
            messagebox.showwarning("Warning", "No page selected.")
            return
        for i in sel:
            self.original_images[i] = self.original_images[i].rotate(-90, expand=True)
        self.update_display()

    def rotate_selected_ccw(self):
        sel = list(self.listbox.curselection())
        if not sel:
            messagebox.showwarning("Warning", "No page selected.")
            return
        for i in sel:
            self.original_images[i] = self.original_images[i].rotate(90, expand=True)
        self.update_display()


    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_display()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_display()


    def download_pdf(self):
        if not self.original_images:
            messagebox.showwarning("Warning", "There is no PDF to download.")
            return
        pdf_images = []
        for im in self.original_images:
            if im.mode != "RGB":
                im = im.convert("RGB")
            pdf_images.append(im)
        file_path = filedialog.asksaveasfilename(title="Download PDF",
                                                 defaultextension=".pdf",
                                                 filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            try:
                pdf_images[0].save(file_path, "PDF", resolution=100.0, save_all=True, append_images=pdf_images[1:])
                messagebox.showinfo("Success", "PDF downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Warning", f"PDF couldn't be saved:\n{e}")

    def create_pdf_selected(self):
        self.create_pdf(selected=True)

    def create_pdf_unselected(self):
        self.create_pdf(selected=False)

    def create_pdf(self, selected):
        if self.pdf_reader is None:
            messagebox.showerror("Warning", "There is no PDF.")
            return
        selected_indices = list(self.listbox.curselection())
        writer = PdfWriter()
        total_pages = len(self.pdf_reader.pages)
        if selected:
            if not selected_indices:
                messagebox.showwarning("Warning", "No page selected.")
                return
            pages_to_include = selected_indices
        else:
            pages_to_include = [i for i in range(total_pages) if i not in selected_indices]
            if not pages_to_include:
                messagebox.showwarning("Warning", "There is no page left.")
                return
        for idx in pages_to_include:
            writer.add_page(self.pdf_reader.pages[idx])

        file_path = filedialog.asksaveasfilename(title="Save PDF",
                                                 defaultextension=".pdf",
                                                 filetypes=[("PDF Files", "*.pdf")])

        if file_path:
            try:
                with open(file_path, "wb") as f:
                    writer.write(f)
                messagebox.showinfo("Success", "New PDF created successfully.")
            except Exception as e:
                messagebox.showerror("Warning", f"PDF couldn't be saved:\n{e}")


class PDFApp:
    def __init__(self, master):
        self.master = master
        self.build_main_menu()

    def build_main_menu(self):
        self.master.title("PDF App")
        self.master.config(bg="#ecf0f1")
        self.main_frame = tk.Frame(self.master, bg="#ecf0f1")
        self.main_frame.pack(pady=20)
        self.btn_view = tk.Button(self.main_frame, text="View a PDF File", width=20,
                                  bg="#3498db", fg="black", activebackground="#2980b9", activeforeground="black",
                                  font=("Helvetica", 12, "bold"), bd=0, command=self.view_pdf)
        self.btn_view.pack(pady=10)
        self.btn_merge = tk.Button(self.main_frame, text="Merge PDF Files", width=20,
                                   bg="#9b59b6", fg="black", activebackground="#8e44ad", activeforeground="black",
                                   font=("Helvetica", 12, "bold"), bd=0, command=self.merge_pdfs)
        self.btn_merge.pack(pady=10)

    def view_pdf(self):
        file_path = filedialog.askopenfilename(title="Select a PDF file", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            PDFViewer(self.master, file_path)

    def merge_pdfs(self):
        file_paths = filedialog.askopenfilenames(title="Select PDF files to be merged", filetypes=[("PDF Files", "*.pdf")])
        if not file_paths:
            return
        writer = PdfWriter()
        for file_path in file_paths:
            try:
                reader = PdfReader(file_path)
            except Exception as e:
                messagebox.showerror("Hata", f"'Could not open {file_path}' file:\n{e}")
                return
            for page in reader.pages:
                writer.add_page(page)
        file_path_save = filedialog.asksaveasfilename(title="Save Merged PDF",
                                                      defaultextension=".pdf",
                                                      filetypes=[("PDF Files", "*.pdf")])
        if file_path_save:
            try:
                with open(file_path_save, "wb") as f:
                    writer.write(f)
                messagebox.showinfo("Success", "PDF files merged successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't merge PDF files:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()