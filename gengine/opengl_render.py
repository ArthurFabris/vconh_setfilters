import os
import json
import subprocess
import pygame
from pygame.locals import *
from OpenGL.GL import *
import loadchars_
import shutil
import time

class OpenGL_render:
    def __init__(self, font_path, font_size, text_color, scale, background_color, nobg):
        self.font_path = font_path
        self.font_size = font_size
        self.text_color = text_color
        self.scale = scale
        self.background_color = background_color
        self.nobg = nobg

    def render_frame_to_surface(self, ascii_lines):
        pygame.init()

        font = pygame.font.Font(self.font_path, self.font_size)

        surface_width = max(font.size(line)[0] for line in ascii_lines) * self.scale
        surface_height = len(ascii_lines) * font.get_height() * self.scale
        surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA, 32)

        if not self.nobg:
            surface.fill(self.background_color)
        
        y_offset = 0
        for line in ascii_lines:
            text_surface = font.render(line, True, self.text_color)
            scaled_text_surface = pygame.transform.scale(text_surface, 
                                                         (int(text_surface.get_width() * self.scale), 
                                                          int(text_surface.get_height() * self.scale)))
            surface.blit(scaled_text_surface, (0, y_offset))
            y_offset += scaled_text_surface.get_height()

        return surface

    def process_and_save_ascii_image(self, file_path, output_path,resolution):
        ascii_gen = loadchars_.AsciiFilter()
        ascii_gen.ascii_filter(file_path,resolution)
        ascii_lines = ascii_gen.get_ascii_frames()

        surface = self.render_frame_to_surface(ascii_lines[0])
        pygame.image.save(surface, output_path)
        print(f"Saved ASCII image to {output_path}")


def video_input(filepath,resolution, **cfg_path):

    filename = os.path.splitext(os.path.basename(filepath))[0]
    print(filename)
    config_file = cfg_path.get('config_file', 'config/default.json')

    with open(config_file, 'r') as file:
        config = json.load(file)

    wnd = OpenGL_render(
        config['font_path'],
        config['font_size'],
        tuple(config['text_color']),
        config['scale'],
        tuple(config['background_color']),
        config['nobg'],
    )

    runs_dir = os.path.join(os.getcwd(), 'RUNS')
    os.makedirs(runs_dir, exist_ok=True)

    video_dir = os.path.join(runs_dir, filename)
    os.makedirs(video_dir, exist_ok=True)


    rendered_frames_dir = os.path.join(video_dir, 'rendered_frames')
    os.makedirs(rendered_frames_dir, exist_ok=True)

    temp_frames_dir = os.path.join(video_dir, 'temp_frames')
    os.makedirs(temp_frames_dir, exist_ok=True)

    progress_file = os.path.join(video_dir, 'progress.json')

    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            progress = json.load(file)
        last_processed_frame = progress.get('last_frame', 0)
        frames_extracted = progress.get('frames_extracted', False)
        last_extracted_frame = progress.get('last_extracted_frame', 0) 
    else:
        last_processed_frame = 0
        frames_extracted = False
        last_extracted_frame = 0

    if not frames_extracted:
        print(f"Resuming frame extraction from frame {last_extracted_frame + 1}...")


        extract_cmd = f"ffmpeg -i {filepath} -start_number {last_extracted_frame + 1} {temp_frames_dir}/frame_%04d.png"
        subprocess.run(extract_cmd, shell=True, check=True)

        extracted_frames = sorted(os.listdir(temp_frames_dir))
        total_extracted = len(extracted_frames)

        with open(progress_file, 'w') as file:
            json.dump({'last_frame': last_processed_frame, 
                       'frames_extracted': True, 
                       'last_extracted_frame': total_extracted}, file)
    else:
        print("Frames already extracted, skipping extraction...")


    frames = sorted(os.listdir(temp_frames_dir))

    print(f"Processing frames starting from frame {last_processed_frame + 1}...")

    for i, frame in enumerate(frames):
        frame_number = i + 1

        if frame_number <= last_processed_frame:
            continue

        input_image_path = os.path.join(temp_frames_dir, frame)
        output_image_path = os.path.join(rendered_frames_dir, frame)
        wnd.process_and_save_ascii_image(input_image_path, output_image_path,resolution)

        with open(progress_file, 'w') as file:
            json.dump({'last_frame': frame_number, 'frames_extracted': True, 'last_extracted_frame': len(frames)}, file)

    output_video_path = os.path.join(video_dir, f"{filename}_ascii.mp4")
    concat_cmd = f"ffmpeg -r 30 -i {rendered_frames_dir}/frame_%04d.png -vcodec ffv1 -pix_fmt rgba {output_video_path}.mkv"
    subprocess.run(concat_cmd, shell=True, check=True)

    shutil.rmtree(temp_frames_dir)

    print(f"Processed video saved at {output_video_path}")


def img_input(filepath, resolution, **cfg_path):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    print(f"Processing file: {filename}")
    
    config_file = cfg_path.get('config_file', 'config/default.json')

    with open(config_file, 'r') as file:
        config = json.load(file)

    wnd = OpenGL_render(
        config['font_path'],
        config['font_size'],
        tuple(config['text_color']),
        config['scale'],
        tuple(config['background_color']),
        config['nobg'],
    )

    runs_dir = os.path.join(os.getcwd(),  'RUNS')
    os.makedirs(runs_dir, exist_ok=True)

    video_dir = os.path.join(runs_dir, filename)
    os.makedirs(video_dir, exist_ok=True)

    rendered_img_dir = os.path.join(video_dir, 'RENDERED_IMG')
    os.makedirs(rendered_img_dir, exist_ok=True)

    output_file_path = os.path.join(rendered_img_dir, f'{filename}_ascii_rendered.png')

    wnd.process_and_save_ascii_image(filepath, output_file_path, resolution)

    print(f"Finished rendering image. Saved at: {output_file_path}")

video_input("path/to/video.mp4",100)

#img_input("path/to/image/png(png,jpeg etc..)",1000)
