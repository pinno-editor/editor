import datetime

from fastapi import FastAPI

import services.ffmpeg_local as ffmpeg_l

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/v1/сut/")
async def cut(video_id: int = 0,out_video: int = 0, start: float = 0, end: float = 0):
    ffmpeg_l.trim(f'{video_id}.mp4', f'{out_video}.mp4', datetime.time(0, 0, int(start)), datetime.time(0, 0, int(end)))
    return {"video_id": video_id, "start": start, 'end': end}


@app.get("/v1/insert/")
async def insert(file_in: str, file_insert: str, time:float):
    ffmpeg_l.insert(file_in=file_in,file_insert=file_insert,begin=datetime.time(0, 0, int(time)))
    return {'Status':'OK','file_out':file_in}

@app.get("/v1/draw_text/")
async def draw_text(text_time_from: int=0, text_time_to:int=0, video_id: str = 'IMG_6317', font_color: str = 'black', box: bool = False, font_size: str = '16',
                    text: str = 'afda', x: float = 0, y: float = 0, ):

    ffmpeg_l.draw_text(file=f'{video_id}.mp4', text=text, x=x, y=y, font_color=font_color, font_size=font_size, box=box,
                       text_time_from=text_time_from,text_time_to= text_time_to)
    return {"video_id": video_id, 'text': text, "x": x, 'y': y,'time_from':text_time_from, 'time_to':text_time_to}


@app.get("/v1/draw_img/")
async def draw_img(img_height:int,img_wheight:int,img_time_from:int =0, img_time_to:int=0, video_id: str = 'IMG_6317', file_img: str = 'download.jpeg',
                   x: float = 0, y: float = 0):

    ffmpeg_l.draw_img(f'{video_id}.mp4',img_height=img_height, img_wheight=img_wheight,file_img=f'{file_img}', x=x, y=y,img_time_from=img_time_from,img_time_to=img_time_to)
    return {"video_id": video_id, "x": x, 'y': y, 'time_from':img_time_from, 'time_to':img_time_to}


@app.get("/v1/export/")
async def export(file_in: str, file_out: str,size_h:int=1, size_w:int=1,):
    ffmpeg_l.change_size_video(file_in=file_in,file_out=file_out,size_h=size_h,size_w=size_w)

    return {'Status':'OK','file_out':file_out}
