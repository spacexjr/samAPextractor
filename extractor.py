import os
import tarfile
import lz4.frame
import threading
import subprocess
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

WORKDIR = "AP_TRABALHO"

class APExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Samsung AP Extractor Pro")
        self.root.geometry("720x680")

        self.ap_path = ""
        self.check_vars = {}
        self.members = {}

        os.makedirs(WORKDIR, exist_ok=True)

        self.setup_dark_theme()
        self.create_widgets()

    def setup_dark_theme(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        bg = "#1e1e1e"
        fg = "#ffffff"
        accent = "#3a7afe"
        self.root.configure(bg=bg)
        style.configure(".", background=bg, foreground=fg, fieldbackground=bg)
        style.configure("TButton", background="#2b2b2b", foreground=fg, padding=6)
        style.map("TButton", background=[("active", accent)])
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TFrame", background=bg)
        style.configure("Horizontal.TProgressbar", thickness=20, background=accent, troughcolor="#2b2b2b")

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        # Cabeçalho / Seleção
        ttk.Button(frame, text="Selecionar AP (.tar.md5)", command=self.select_ap).pack(fill="x")
        self.label_ap = ttk.Label(frame, text="Nenhum arquivo selecionado", wraplength=680, font=("Segoe UI", 8), foreground="#aaaaaa")
        self.label_ap.pack(pady=6)

        # Botões de Seleção Rápida
        btn_fm = ttk.Frame(frame)
        btn_fm.pack(fill="x", pady=5)
        ttk.Button(btn_fm, text="Selecionar Tudo", command=self.select_all).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(btn_fm, text="Limpar Seleção", command=self.clear_all).pack(side="left", expand=True, fill="x", padx=2)

        ttk.Label(frame, text="Partições (.img.lz4):", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 2))

        # Lista com Scroll
        container = ttk.Frame(frame)
        container.pack(fill="both", expand=True, pady=5)
        canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.list_frame = ttk.Frame(canvas)
        self.list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Progresso e Status
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100, style="Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=10)

        self.status = ttk.Label(frame, text="Aguardando...", font=("Segoe UI", 9))
        self.status.pack(anchor="w")

        ttk.Button(frame, text="EXTRAIR SELECIONADAS", command=self.start_extract).pack(fill="x", pady=10)

        # --- SEÇÃO DE CRÉDITOS ---
        credits_label = ttk.Label(
            self.root, 
            text="Developed by spacexjr", 
            font=("Segoe UI", 8, "italic"),
            foreground="#555555"
        )
        credits_label.pack(side="bottom", pady=5)

    def select_all(self):
        for var in self.check_vars.values(): var.set(True)

    def clear_all(self):
        for var in self.check_vars.values(): var.set(False)

    def open_folder(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def select_ap(self):
        path = filedialog.askopenfilename(title="Selecione o AP", filetypes=[("Samsung AP", "*.tar.md5 *.tar")])
        if not path: return
        self.ap_path = path
        self.label_ap.config(text=path)
        for w in self.list_frame.winfo_children(): w.destroy()
        self.check_vars.clear()
        self.members.clear()
        try:
            with tarfile.open(self.ap_path) as tar:
                imgs = [m for m in tar.getmembers() if m.name.endswith(".img.lz4")]
                imgs.sort(key=lambda x: x.name)
                for m in imgs:
                    var = tk.BooleanVar()
                    self.check_vars[m.name] = var
                    self.members[m.name] = m
                    cb = tk.Checkbutton(self.list_frame, text=f"{m.name} ({m.size/(1024*1024):.1f} MB)", 
                                        variable=var, bg="#1e1e1e", fg="#ffffff", selectcolor="#3a7afe",
                                        activebackground="#2b2b2b", activeforeground="#ffffff", anchor="w")
                    cb.pack(fill="x", anchor="w")
            self.status.config(text=f"{len(imgs)} partições carregadas.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def start_extract(self):
        selecionadas = [n for n, v in self.check_vars.items() if v.get()]
        if not selecionadas:
            messagebox.showwarning("Aviso", "Selecione ao menos uma partição!")
            return
        self.progress_var.set(0)
        threading.Thread(target=self.extract_imgs, args=(selecionadas,), daemon=True).start()

    def extract_imgs(self, imgs):
        outdir = os.path.abspath(os.path.join(WORKDIR, "EXTRAIDAS"))
        os.makedirs(outdir, exist_ok=True)
        chunk_size = 1024 * 1024 
        try:
            with tarfile.open(self.ap_path) as tar:
                for img_name in imgs:
                    member = self.members[img_name]
                    out_path = os.path.join(outdir, img_name.replace(".lz4", ""))
                    self.root.after(0, lambda n=img_name: self.status.config(text=f"Extraindo: {n}"))
                    
                    with tar.extractfile(member) as f_in, open(out_path, "wb") as f_out:
                        decompressor = lz4.frame.LZ4FrameDecompressor()
                        bytes_lidos = 0
                        while True:
                            chunk = f_in.read(chunk_size)
                            if not chunk: break
                            bytes_lidos += len(chunk)
                            self.root.after(0, lambda p=(bytes_lidos/member.size)*100: self.progress_var.set(p))
                            decompressed = decompressor.decompress(chunk)
                            if decompressed: f_out.write(decompressed)
                
            self.root.after(0, lambda: self.status.config(text="Concluído por spacexjr!"))
            self.root.after(0, lambda: self.progress_var.set(0))
            if messagebox.askyesno("Sucesso", f"Extração concluída!\nDeseja abrir a pasta agora?"):
                self.open_folder(outdir)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", str(e)))

if __name__ == "__main__":
    root = tk.Tk()
    app = APExtractorGUI(root)
    root.mainloop()