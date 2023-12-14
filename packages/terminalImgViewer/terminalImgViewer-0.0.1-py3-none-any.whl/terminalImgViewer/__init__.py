from colored import fg
from PIL import Image
from lib import reduce_resolution


def display(image_name, width):
    im = reduce_resolution(Image.open(image_name).getdata().convert("RGB"), width)

    for i in range(len(im)):
        color = fg('#%02x%02x%02x' % im[i])
        if i % im.size[0] == 0:
            print(color + "■■", end="\n")
            
        else:
            print(color + "■■", end="")

