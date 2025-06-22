import os
import json
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.all import crop
import platform
import moviepy.config as mpy_conf

if platform.system() == "Windows":
    mpy_conf.change_settings({
        "IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"
    })
FONT_PATH = "./Montserrat-Bold.ttf"  # Update this path as needed

def generate_captioned_video(folder_path,folder_name):
    video_filename = f"{folder_name}.mp4"
    video_path = os.path.join(folder_path, video_filename)
    #video_path = os.path.join(folder_path, "short_1.mp4")
    script_path = os.path.join(folder_path, "script.json")
    output_path = os.path.join(folder_path, "output_captioned.mp4")

    if not os.path.exists(video_path) or not os.path.exists(script_path):
        print(f"❌ Skipping {folder_path} — missing video or script.json")
        return

    print(f"🎬 Processing: {folder_path}")

    # Load video
    clip = VideoFileClip(video_path)
    duration = clip.duration

    # Crop to 9:16
    W, H = clip.size
    target_ratio = 9 / 16
    target_width = int(H * target_ratio)
    x_center = W // 2
    x1 = max(0, x_center - target_width // 2)
    x2 = x1 + target_width
    clip = crop(clip, x1=x1, x2=x2)

    # Load story
    with open(script_path, "r") as f:
        story = json.load(f)["story"]

    words = story.split()
    n = len(words)
    segments = [
        " ".join(words[i * n // 3:(i + 1) * n // 3])
        for i in range(3)
    ]

    caption_clips = []
    for i, segment in enumerate(segments):
        txt = TextClip(
            segment,
            fontsize=60,
            font=FONT_PATH,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(clip.w * 0.9, None),
            align="center"
        ).set_position(("center", clip.h * 0.55)).set_duration(duration / 3)

        txt = txt.set_start(i * duration / 3)
        caption_clips.append(txt)

    final = CompositeVideoClip([clip, *caption_clips])
    final.write_videofile(output_path, fps=clip.fps, codec="libx264")
    print(f"✅ Saved: {output_path}\n")

def process_all_folders():
    for folder_name in os.listdir():
        folder_path = os.path.join(os.getcwd(), folder_name)
        if folder_name.startswith("short_") and os.path.isdir(folder_path):
            generate_captioned_video(folder_path, folder_name)

if __name__ == "__main__":
    process_all_folders()
