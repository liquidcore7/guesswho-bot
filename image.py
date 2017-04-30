from PIL import Image, ImageDraw, ImageFont

def optimalmode(imgsz):
    for i in range(7, 23):
        if imgsz[0] % i == 0 and imgsz[1] % i == 0:
            return i
        else:
            pass
    else:
        return 10

def msg_to_pos(txt, mode) :
    chpos = ord(txt.lower()[0]) - 97
    return (ord(txt[1]) - 48) * mode + chpos


def generatebackground(size, mode) :
        bck = Image.new('RGBA', size, (194, 194, 194, 255))
        fnt = ImageFont.truetype('Roboto-Bold.ttf', 15)
        drawer = ImageDraw.Draw(bck)
        for c in range(0, mode):
            x = 30 + (size[0] - 30) // mode * c
            y = 30 + (size[1] - 30) // mode * c
            drawer.line([(x, 0), (x, size[1])], (0, 0, 0, 255), 2)
            drawer.line([(0, y), (size[0], y)], (0, 0, 0, 255), 2)
            drawer.text((x + (size[0] - 30) // (mode * 2), 10), chr(c + 65), font=fnt, fill=(0, 0, 0, 255))
            drawer.text((10 if c < 10 else 5, y + (size[1] - 30) // (mode * 2) - 5), str(c), font=fnt, fill=(0, 0, 0, 255))
        return bck

def splitim(img, mode) :
    x, y = img.size[0] // mode, img.size[1] // mode
    zones = [(x * b, y * a, x * (b + 1), y * (a + 1)) for a in range(mode) for b in range(mode)]
    cropped = [(img.crop(zn), zn) for zn in zones]
    return cropped

def addguessed(img, arr) :
    img.paste(arr[0], tuple(map(lambda x: x + 30, arr[1])))
    return None

def temp(img, text=''):
    img.save('{}.jpg'.format(text), "JPEG")


