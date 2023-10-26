import asyncio
import os
import random
import re
import textwrap
import aiofiles
import aiohttp
import logging
import numpy as np

from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter, ImageChops,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch
import numpy as np

from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL, BOT_ID, FAILED
from ... import app, app2


logging.basicConfig(level=logging.DEBUG, encoding="utf-8", format="\033[32m\033[1m%(asctime)s - %(levelname)s - %(message)s \033[0m")

def make_col():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""
    for i in list:
        if len(text1) + len(i) < 30:
            text1 += " " + i
        elif len(text2) + len(i) < 30:
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()
    return [text1, text2]

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


def add_corners(im):
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, im.split()[-1])
    im.putalpha(mask)


async def gen_thumb(videoid, user_id):
    # thumb = random.randint(1, 2)
    thumb = 2
    if os.path.isfile(f"cache/{videoid}_{user_id}.png"):
        return f"cache/{videoid}_{user_id}.png"
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                result["viewCount"]["short"]
            except:
                pass
            try:
                result["channel"]["name"]
            except:
                pass

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        try:
            wxy = await app.download_media(
                (await app.get_users(user_id)).photo.big_file_id,
                file_name=f"{user_id}.jpg",
            )
        except:
            wxy = await app.download_media(
                (await app.get_users(BOT_ID)).photo.big_file_id,
                file_name=f"{BOT_ID}.jpg",
            )

        xy = Image.open(wxy)
        a = Image.new("L", [640, 640], 0)
        b = ImageDraw.Draw(a)
        b.pieslice([(0, 0), (640, 640)], 0, 360, fill=255, outline="white")
        c = np.array(xy)
        d = np.array(a)
        e = np.dstack((c, d))
        f = Image.fromarray(e)
        x = f.resize((107, 107))

        await app2.send_photo("@CoderX", f"cache/thumb{videoid}.png")
        youtube = Image.open(f"cache/thumb{videoid}.png")
        if thumb == 1:
            bg = Image.open(f"ZenPlay/Helpers/utils/circle.png")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(30))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)

            image3 = changeImageSize(1280, 720, bg)
            image5 = image3.convert("RGBA")
            Image.alpha_composite(background, image5).save(f"cache/temp{videoid}.png")

            Xcenter = youtube.width / 2
            Ycenter = youtube.height / 2
            x1 = Xcenter - 250
            y1 = Ycenter - 250
            x2 = Xcenter + 250
            y2 = Ycenter + 250
            logo = youtube.crop((x1, y1, x2, y2))
            logo.thumbnail((520, 520), Image.ANTIALIAS)
            logo.save(f"cache/chop{videoid}.png")
            if not os.path.isfile(f"cache/cropped{videoid}.png"):
                im = Image.open(f"cache/chop{videoid}.png").convert("RGBA")
                add_corners(im)
                im.save(f"cache/cropped{videoid}.png")

            crop_img = Image.open(f"cache/cropped{videoid}.png")
            logo = crop_img.convert("RGBA")
            logo.thumbnail((365, 365), Image.ANTIALIAS)
            width = int((1280 - 365) / 2)
            background = Image.open(f"cache/temp{videoid}.png")
            background.paste(logo, (width + 2, 138), mask=logo)
            background.paste(x, (710, 427), mask=x)
            background.paste(image3, (0, 0), mask=image3)

            draw = ImageDraw.Draw(background)
            font = ImageFont.truetype("ZenPlay/Helpers/utils/font2.ttf", 45)
            ImageFont.truetype("ZenPlay/Helpers/utils/font2.ttf", 70)
            arial = ImageFont.truetype("ZenPlay/Helpers/utils/font2.ttf", 30)
            ImageFont.truetype("ZenPlay/Helpers/utils/font.ttf", 30)
            para = textwrap.wrap(title, width=32)
            try:
                draw.text(
                    (450, 25),
                    f"STARTED PLAYING",
                    fill="white",
                    stroke_width=3,
                    stroke_fill="grey",
                    font=font,
                )
                if para[0]:
                    text_w, text_h = draw.textsize(f"{para[0]}", font=font)
                    draw.text(
                        ((1280 - text_w) / 2, 530),
                        f"{para[0]}",
                        fill="white",
                        stroke_width=1,
                        stroke_fill="white",
                        font=font,
                    )
                if para[1]:
                    text_w, text_h = draw.textsize(f"{para[1]}", font=font)
                    draw.text(
                        ((1280 - text_w) / 2, 580),
                        f"{para[1]}",
                        fill="white",
                        stroke_width=1,
                        stroke_fill="white",
                        font=font,
                    )
            except:
                pass
            text_w, text_h = draw.textsize(f"Duration: {duration} Mins", font=arial)
            draw.text(
                ((1280 - text_w) / 2, 660),
                f"Duration: {duration} Mins",
                fill="white",
                font=arial,
            )
        elif thumb == 2:
            try:
                para = textwrap.wrap(title, width = 20)
                print(para)
                img = youtube

                # circle bg
                im = Image.open(f"cache/thumb{videoid}.png").convert('RGBA').resize((640, 640))
                bigsize = (im.size[0] * 3, im.size[1] * 3)
                mask = Image.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + bigsize, fill=255)
                mask = mask.resize(im.size, Image.LANCZOS)
                im.putalpha(mask)
                im.thumbnail((222, 222))

                # Circle profile
                pfp = Image.open(wxy).convert('RGBA').resize((640, 640))
                bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
                mask = Image.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + bigsize, fill=255)
                mask = mask.resize(pfp.size, Image.LANCZOS)
                pfp.putalpha(mask)
                pfp.thumbnail((110, 110))



                overlay = Image.open('ZenPlay/Helpers/utils/zen_thumb.png')
                overlay1 = overlay.filter(ImageFilter.EDGE_ENHANCE)

                new_img = Image.new('RGBA', (overlay.size[0],+ overlay.size[1]))
                w, h = new_img.size[0], new_img.size[1]
                shape = [(50, 55), (919, 333)]
                odraw = ImageDraw.Draw(new_img)
                odraw.rectangle(shape, width = 15, outline = 'black')
                new_img = new_img.filter(ImageFilter.GaussianBlur(6))

                black_white = random.choice([False, False, False, True, False])
                if black_white == True:
                    im2 = img.filter(ImageFilter.BoxBlur(10)).convert('L').convert('RGBA')
                else:
                    im2 = img.filter(ImageFilter.BoxBlur(10))
                im2.paste(overlay1, mask = overlay1)
                im2.paste(im, mask = im, box = (im.size[0] // 2 + 145, im.size[1] // 2 + 143))
                im2.paste(pfp, mask = pfp, box = (888, im.size[1] // 2 + 144))
                im2.paste(new_img, box = (160, 166), mask = new_img)

                draw = ImageDraw.Draw(im2)
                unamefont = ImageFont.truetype('ZenPlay/Helpers/utils/KGTangledUpInYou.ttf', 30)
                username = (await app.get_users(user_id))
                if username.username:
                    draw.text((900, 380), text = username.username, font = unamefont, fill = 'hotpink')
                font = ImageFont.truetype("ZenPlay/Helpers/utils/Akira_Expanded_Demo.otf", 20)
                text = para[0]
                draw.text((500, 300), text = f"Title: {text}", font = font, fill = 'hotpink', spacing = 5)
                draw.text((500, 320), text = f"Duration: {duration}", font = font, fill = 'hotpink', spacing = 5)
                im3 = im2.filter(ImageFilter.DETAIL)
                background = im3
            except Exception as e:
                await app2.send_message('@CoderX', e)
                logging.exception(e)

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}_{user_id}.png")
        return f"cache/{videoid}_{user_id}.png"
    except Exception as e:
        LOGGER.error(e)
        return FAILED

async def gen_qthumb(videoid):
    try:
        if os.path.isfile(f"cache/q{videoid}.jpg"):
            return f"cache/q{videoid}.jpg"

        url = f"https://www.youtube.com/watch?v={videoid}"
        if 1 == 1:
            results = VideosSearch(url, limit=1)
            for result in (await results.next())["result"]:
                try:
                    title = result["title"]
                    title = re.sub("\W+", " ", title)
                    title = title.title()
                except:
                    title = "Unsupported Title"
                try:
                    duration = result["duration"]
                except:
                    duration = "Unknown Mins"
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                try:
                    views = result["viewCount"]["short"]
                except:
                    views = "Unknown Views"
                try:
                    channel = result["channel"]["name"]
                except:
                    channel = "Unknown Channel"

            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://img.youtube.com/vi/{videoid}/maxresdefault.jpg") as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(
                            f"cache/thumb{videoid}.jpg", mode="wb"
                        )
                        await f.write(await resp.read())
                        await f.close()

            youtube = Image.open(f"cache/thumb{videoid}.jpg")
            image1 = changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(30))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)
            image2 = background

            circle = Image.open("assets/circle.png")

            im = circle
            im = im.convert('RGBA')
            color = make_col()

            data = np.array(im)
            red, green, blue, alpha = data.T

            white_areas = (red == 255) & (blue == 255) & (green == 255)
            data[..., :-1][white_areas.T] = color

            im2 = Image.fromarray(data)
            circle = im2

            image3 = image1.crop((280, 0, 1000, 720))
            lum_img = Image.new('L', [720, 720], 0)
            draw = ImageDraw.Draw(lum_img)
            draw.pieslice([(0, 0), (720, 720)], 0, 360, fill=255, outline="white")
            img_arr = np.array(image3)
            lum_img_arr = np.array(lum_img)
            final_img_arr = np.dstack((img_arr, lum_img_arr))
            image3 = Image.fromarray(final_img_arr)
            image3 = image3.resize((600, 600))

            image2.paste(image3, (50, 70), mask=image3)
            image2.paste(circle, (0, 0), mask=circle)

            font1 = ImageFont.truetype('assets/font.ttf', 30)
            font2 = ImageFont.truetype('assets/font2.ttf', 70)
            font3 = ImageFont.truetype('assets/font2.ttf', 40)
            font4 = ImageFont.truetype('assets/font2.ttf', 35)

            image4 = ImageDraw.Draw(image2)
            image4.text((960, 10), f"{MUSIC_BOT_NAME}", fill="white", font=font1, align="left")
            image4.text((670, 150), "ADDED TO QUEUE", fill="white", font=font2, stroke_width=2, stroke_fill="red", align="left")

            title1 = truncate(title)
            image4.text((670, 300), text=title1[0], fill="white", stroke_width=1, stroke_fill="white", font=font3, align="left")
            image4.text((670, 350), text=title1[1], fill="white", stroke_width=1, stroke_fill="white", font=font3, align="left")

            views = f"Views : {views}"
            duration = f"Duration : {duration} Mins"
            channel = f"Channel : {channel}"

            image4.text((670, 450), text=views, fill="white", font=font4, align="left")
            image4.text((670, 500), text=duration, fill="white", font=font4, align="left")
            image4.text((670, 550), text=channel, fill="white", font=font4, align="left")

            image2 = ImageOps.expand(image2, border=20, fill=make_col())
            image2 = image2.convert('RGB')
            image2.save(f"cache/q{videoid}.jpg")
            file = f"cache/q{videoid}.jpg"
            return file
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
      
