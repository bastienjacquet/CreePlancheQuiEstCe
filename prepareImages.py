import os
from PIL import Image, ImageEnhance, ImageStat, ImageDraw

def prepare_images(dir_path):
    thumb_size = (200,240)
    images = [i for i in os.listdir(dir_path) if not i.startswith('thumb_') and (i.lower().endswith(".jpg") or i.lower().endswith(".jpeg"))]
    for i in images:
        im = Image.open(os.path.join(dir_path, i))
        
        width, height = im.size
        ratio = width / height
        if width < thumb_size[0] or height < thumb_size[1]:
            new_width = max(thumb_size[0], int(thumb_size[1] * ratio))
            new_height = max(thumb_size[1], int(thumb_size[0] / ratio))
            im = im.resize((new_width, new_height), Image.BICUBIC)
        im.thumbnail(thumb_size)
        new_im = Image.new("RGB", thumb_size, (255, 255, 255))
        new_im.paste(im, ((thumb_size[0] - im.size[0]) // 2, (thumb_size[1] - im.size[1]) // 2))
        new_im.save(os.path.join(dir_path, f'thumb_{i}'))
    #Egalisation de luminosité, saturation et contraste...

    images = [i for i in os.listdir(dir_path) if i.startswith('thumb_')]
    im_luminosity = []
    im_saturation = []
    im_contrast = []
    for image in images:
        im = Image.open(os.path.join(dir_path, image))
        im_luminosity.append(ImageStat.Stat(im).mean[0])
        #im_saturation.append(ImageEnhance.Color(im).enhance(1))
        #im_contrast.append(ImageEnhance.Contrast(im).enhance(1))
    mean_luminosity = sum(im_luminosity) / len(im_luminosity)
    #mean_saturation = sum(im_saturation) / len(im_saturation)
    #mean_contrast = sum(im_contrast) / len(im_contrast)
    for i in range(len(images)):
        im = Image.open(os.path.join(dir_path, images[i]))
        im = ImageEnhance.Brightness(im).enhance(mean_luminosity / im_luminosity[i])
        #im = ImageEnhance.Color(im).enhance(mean_saturation / im_saturation[i])
        #im = ImageEnhance.Contrast(im).enhance(mean_contrast / im_contrast[i])
        im.save(os.path.join(dir_path, images[i]))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python prepareImages.py <directory>")
        sys.exit()
    prepare_images(sys.argv[1])
