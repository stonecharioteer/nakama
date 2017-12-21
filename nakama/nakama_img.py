from __future__ import division
import os
import datetime

from PIL import Image, ImageFont

from .nakama import get_latest_one_piece_chapter_jb, get_latest_one_piece_chapter_ms

def get_bnw_image(i_path, canvas="#000000"):
    image = Image.open(i_path)
    height = 100
    new_height = height
    new_width = int(height/image.size[1]*image.size[0])
    image = image.resize((new_width, new_height), Image.ANTIALIAS)

    canvas_width, canvas_height = 264, 176
    x_pos_1 = int((canvas_width-image.size[0])/2)
    x_pos_2 = int((canvas_width-image.size[0])/2+image.size[0])
    template = Image.new("RGB",(canvas_width, canvas_height), canvas)
    box = (x_pos_1,0,x_pos_2,image.size[1])
    template.paste(image, box)
    return template.convert("L")

def get_images(got_op=False):
    directory = os.path.dirname(os.path.realpath(__file__))

    images = ["strawhatjollyroger.jpg","strawhatjollyroger_red.jpg","strawhatjollyroger_black.jpg"]
    images = [os.path.join(directory, "..","images",img) for img in images]
    if got_op:
        black_active = get_bnw_image(images[2])
        red_active = get_bnw_image(images[1], canvas="#ffffff")
        return black_active, red_active
    else:
        black_normal = get_bnw_image(images[0])
        red_normal = Image.new("L", (264,176), "#ffffff")
        return black_normal, red_normal

def get_op_stat_image():
    from PIL import ImageDraw, ImageFont
    recent_jb = get_latest_one_piece_chapter_jb()
    recent_ms = get_latest_one_piece_chapter_ms()
    ms_out = False
    jb_out = False
    if recent_ms["days_passed"] <=4:
        chapter_number = recent_ms["chapter_number"]
        chapter_name = recent_ms["chapter_name"]
        release_date = recent_ms["release_date"]
        ms_out = True

    if recent_jb["days_passed"] <=4:
        chapter_number = recent_jb["chapter_number"]
        chapter_name = recent_jb["chapter_name"]
        release_date = recent_jb["release_date"]
        jb_out = True
    
    if ms_out or jb_out:
        if not jb_out:
            where = "Mangastream"
        elif not ms_out:
            where = "Jaimini's Box"
        else:
            where = "Mangastream or Jaimini's Box"
        msg = "#{} - {}\nout now!\nCheck {}".format(chapter_number, chapter_name, where)
        image_b, image_r = get_images(True)
    else:
        if recent_ms["release_date"]>recent_jb["release_date"]:
            msg = "{chapter_number} - {chapter_name}\n@ {release_date} [Mangastream]".format(**recent_ms)
        else:
            msg = "{chapter_number} - {chapter_name}\n@ {release_date} [Jaimini's Box]".format(**recent_jb)

        
        msg = "Yohohoho! Last released was: \n{}".format(msg)
        image_b, image_r = get_images()
    directory = os.path.dirname(os.path.realpath(__file__))
    font_path = os.path.abspath(os.path.join(directory, "..","fonts","RobotoSlab-Regular.ttf"))
    font = ImageFont.truetype(font_path, 12)
    draw = ImageDraw.Draw(image_b)
    draw.text((25, 100), msg, fill="#ffffff", font=font)
    font = ImageFont.truetype(font_path, 12)

    msg_r = datetime.datetime.now().strftime("[%y-%m-%d (%H-%M)]")
    draw = ImageDraw.Draw(image_r)
    draw.text((170, 150), msg_r, fill="#000000", font=font)
    return image_b, image_r

