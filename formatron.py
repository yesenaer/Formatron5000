from pathlib import Path
from moviepy import VideoFileClip
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

ROOT = Path(__file__).parent
input_dir = ROOT / "data"
output_dir = ROOT / "output"

class FormatronUI:
    def __init__(self, master):
        self.master = master
        master.title("Formatron5000")
        master.geometry("400x200")

        self.input_dir = tk.StringVar(value=str(input_dir))
        self.output_dir = tk.StringVar(value=str(output_dir))
        self.conversion_thread = None
        self.stop_flag = threading.Event()

        tk.Label(master, text="Input Directory:").pack(pady=(10, 0))
        input_frame = tk.Frame(master)
        input_frame.pack()
        tk.Entry(input_frame, textvariable=self.input_dir, width=40).pack(side=tk.LEFT)
        tk.Button(input_frame, text="Browse", command=self.browse_input).pack(side=tk.LEFT)

        tk.Label(master, text="Output Directory:").pack(pady=(10, 0))
        output_frame = tk.Frame(master)
        output_frame.pack()
        tk.Entry(output_frame, textvariable=self.output_dir, width=40).pack(side=tk.LEFT)
        tk.Button(output_frame, text="Browse", command=self.browse_output).pack(side=tk.LEFT)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=20)
        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start_conversion)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop_conversion, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

    def browse_input(self):
        directory = filedialog.askdirectory(initialdir=self.input_dir.get())
        if directory:
            self.input_dir.set(directory)

    def browse_output(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)

    def start_conversion(self):
        self.stop_flag.clear()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.conversion_thread = threading.Thread(target=self.run_conversion)
        self.conversion_thread.start()

    def stop_conversion(self):
        self.stop_flag.set()
        self.stop_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL)

    def run_conversion(self):
        try:
            in_dir = Path(self.input_dir.get())
            out_dir = Path(self.output_dir.get())
            if not in_dir.exists():
                messagebox.showerror("Error", f"Input directory {in_dir} does not exist.")
                return
            out_dir.mkdir(parents=True, exist_ok=True)
            mov_files = list(in_dir.glob("*.mov"))
            if not mov_files:
                messagebox.showinfo("Info", "No .mov files found in the input directory.")
                return
            for mov_file in mov_files:
                if self.stop_flag.is_set():
                    break
                current_file_name = mov_file.name
                output_file_name = current_file_name.replace(".mov", ".mp4")
                output_file_path = out_dir / output_file_name
                try:
                    convert_mov_to_mp4(mov_file, output_file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to convert {mov_file}: {e}")
            if not self.stop_flag.is_set():
                messagebox.showinfo("Done", "Conversion completed.")
        finally:
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

def launch_ui():
    root = tk.Tk()
    app = FormatronUI(root)
    root.mainloop()

def convert_mov_to_mp4(input_path: Path, output_path: Path) -> None:
    """
    Convert a .mov video file to .mp4 format using moviepy.
    Args:
        input_path (Path): Path to the input .mov file.
        output_path (Path): Path where the output .mp4 file will be saved.
    """
    if not input_path.exists():
        raise FileNotFoundError(f"The input file {input_path} does not exist.")
    if not input_path.suffix.lower() == '.mov':
        raise ValueError(f"The input file {input_path} is not a .mov file.")
    
    # Load the .mov file
    video = VideoFileClip(input_path)

    # Write the video to an .mp4 file
    try:
        video.write_videofile(output_path, codec='libx264', fps=video.fps)
        print(f"Video saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while writing the video: {e}")
        raise Exception("Failed to convert video.")


if __name__ == "__main__":
    launch_ui()
