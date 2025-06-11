from pathlib import Path
from moviepy import VideoFileClip


PROJECT_ROOT = Path(__file__).parent
input_dir = PROJECT_ROOT / "data"
output_dir = PROJECT_ROOT / "output"

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
    for mov_file in input_dir.glob("*.mov"):
        print(f"Found .mov file: {mov_file}, starting conversion...")
        current_file_name = mov_file.name
        output_file_name = current_file_name.replace(".mov", ".mp4")
        output_file_path = output_dir / output_file_name

        convert_mov_to_mp4(input_dir / current_file_name, output_file_path)
