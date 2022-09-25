import dataclasses
import os
import datetime
import subprocess
import ffmpeg
from PIL import Image


def get_length(filename: str):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def trim(in_file: str, out_file: str, begin: datetime, end: datetime):
    inp = f'videos/{in_file}'
    out1 = f'videos/1{out_file}'
    out2 = f'videos/2{out_file}'
    result = f'videos/1{in_file}'
    begin = begin.strftime('%H:%M:%S')
    end = end.strftime('%H:%M:%S')
    duration = get_length(f'{inp}')
    os.system(f'ffmpeg -ss 00:00:00 -to {begin}  -i {inp} -c copy {out1}')
    os.system(f'ffmpeg -ss {end} -to {duration}  -i {inp} -c copy {out2}')
    os.system(f'ffmpeg -i "concat:{out1}|{out2}" -c copy {result} -y')
    os.system(f'rm {out1} {out2}')


# trim('IMG_6317.avi','out.avi',datetime.time(0,0,5),datetime.time(0,0,10))

def insert(file_in: str, file_insert: str, begin: datetime):
    file_insert=f'videos/{file_insert}'
    inp = f'videos/{file_in}'
    out1 = f'videos/1{file_in}'
    out2 = f'videos/2{file_in}'
    begin = begin.strftime('%H:%M:%S')
    duration = get_length(f'{inp}')
    os.system(f'ffmpeg -ss 00:00:00 -to {begin}  -i {inp} -c copy {out1}-y ')
    os.system(f'ffmpeg -ss {begin} -to {duration}  -i {inp} -c copy {out2} -y')
    os.system(f'ffmpeg -i "concat:{out1}|{file_insert}" -c copy videos/333.mp4 -y')
    #os.system(f'rm {out1} {out2}')

def draw_text(file: str, text: str, x, y, font_color: str, font_size: str, box: bool, text_time_from:int, text_time_to:int):

    duration = get_length(f'videos/{file}')
    if text_time_to>0:
        pass
    else:
        text_time_to=duration

        (
            ffmpeg

            .drawtext(ffmpeg.input(f'videos/{file}'),text=f'{text}', x=x, y=y, fontcolor=font_color, fontsize=font_size, box=int(box), enable=f'between(t,{text_time_from},{text_time_to})')
            .output(ffmpeg.input(f'videos/{file}'),f'videos/edit-{file}')

            .overwrite_output()
            .run_async(overwrite_output=True)
        )

    #!!! Important don't delete
    #os.system(f'rm videos/{file}')
    #os.system(f'mv videos/1{file} videos/{file}')
    #!!!


def draw_img(file: str, file_img: str, x:float, y:float,img_height:int,img_wheight:int, img_time_from:float, img_time_to:float):

    duration = get_length(f'videos/{file}')
    if img_time_to>0:
        pass
    else:
        img_time_to=duration

    Image.open(f'videos/{file_img}').resize((img_height, img_wheight)).save(f'videos/{file_img}')

    (
        ffmpeg
        .overlay(ffmpeg.input(f'videos/{file}'), x=x,y=y, overlay_parent_node=ffmpeg.input(f'videos/{file_img}'),enable=f'between(t,{img_time_from},{img_time_to})')
        .output(ffmpeg.input(f'videos/{file}'),f'videos/1{file}')
        .run_async(overwrite_output=True)
    )


def change_size_video(file_in: str, file_out: str,size_h:int, size_w:int):
    os.system(f'ffmpeg -i videos/{file_in}.mp4 -aspect {size_h}:{size_w} videos/{file_out} -y')

