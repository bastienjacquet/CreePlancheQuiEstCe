import os, argparse
from PIL import Image, ImageEnhance, ImageStat, ImageDraw

def prepare_images(dir_path, auto_crop_faces=True, equalize_brightness=True):
    thumb_size = (200,240)
    if auto_crop_faces:
        try:
            import cv2, numpy as np
        except ImportError:
            auto_crop_faces=False
            print('Ignoring face detection because OpenCv is not installed. run "pip3 uninstall opencv-python" to install it.')
    if auto_crop_faces:
        import cv2, numpy as np
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        def crop_face(im, faces):
            x, y, w, h = faces[0]
            margin_x = int(w * 0.2)
            margin_y = int(h * 0.4)
            margin_bottom = int(h * 0.4)

            aspect_ratio = thumb_size[0] / thumb_size[1]
            width = w +2 *margin_x
            height = margin_y + h + margin_bottom
            target_width = int(height * aspect_ratio)
            if width < target_width:
                dx=target_width-width
                x-=dx/2
                w+=dx
            else:
                target_width = int(height * aspect_ratio)
                right = left + target_width
            im = im.crop((max(0,x-margin_x),max(0,y-margin_y),min(im.size[0],x+w+margin_x),min(im.size[1],y+h+margin_bottom)))
            return im

    images = [i for i in os.listdir(dir_path) if not i.startswith('thumb_') and not i.startswith('faces_') and (i.lower().endswith(".jpg") or i.lower().endswith(".jpeg"))]
    for i in images:
        im = Image.open(os.path.join(dir_path, i))
        if auto_crop_faces:
            # Convertir en niveaux de gris pour une meilleure détection de visages
            gray = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2GRAY)        
            # Détecter les visages
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
            
            # Dessiner un rectangle rouge autour de chaque visage détecté
            for (x, y, w, h) in faces:
                cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 0, 255), 2)
            if len(faces):
                im=crop_face(im,faces)
            im2 = Image.fromarray(gray)
            im2.thumbnail(thumb_size)
            im2.save(os.path.join(dir_path, f'faces_{i}'))


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
    if equalize_brightness:
        print("Egalisation de la luminosité")
        images = [i for i in os.listdir(dir_path) if i.startswith('thumb_')]
        im_luminosity = []
        # im_saturation = []
        im_contrast = []
        for image in images:
            im = Image.open(os.path.join(dir_path, image))
            im_luminosity.append(ImageStat.Stat(im).mean[0])
            # im_saturation.append(ImageStat.Stat(ImageEnhance.Color(im)))
            #im_contrast.append(ImageEnhance.Contrast(im).enhance(1))
        # print(im_luminosity)
        mean_luminosity = sum(im_luminosity) / len(im_luminosity)
        # print(mean_luminosity)
        # mean_saturation = sum(im_saturation) / len(im_saturation)
        #mean_contrast = sum(im_contrast) / len(im_contrast)
        for i in range(len(images)):
            im = Image.open(os.path.join(dir_path, images[i]))
            # print(images[i],(mean_luminosity / im_luminosity[i]))
            im = ImageEnhance.Brightness(im).enhance(max(.85,min(mean_luminosity / im_luminosity[i],1.10)))
            # im = ImageEnhance.Color(im).enhance(mean_saturation / im_saturation[i])
            #im = ImageEnhance.Contrast(im).enhance(mean_contrast / im_contrast[i])
            im.save(os.path.join(dir_path, images[i]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Répertoire des images miniatures")
    parser.add_argument("-f", "--auto_crop_faces", help="Auto crop around faces", action='store_false')
    parser.add_argument("-b", "--equalize_brightness", help="Automatically equalize brigthnees", action='store_false')
    args = parser.parse_args()
    prepare_images(args.dir, args.auto_crop_faces,  args.equalize_brightness)