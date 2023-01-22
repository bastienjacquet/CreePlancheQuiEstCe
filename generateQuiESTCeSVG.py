import os
import argparse, random
import svgwrite
from PIL import Image, ImageEnhance, ImageStat, ImageDraw
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

def completeImagesTo24(images):
    """
    Cette fonction prend en entrée une liste d'images et complète cette liste pour qu'elle contienne 24 images.
    Si la liste d'entrée contient moins de 24 images, des images blanches et du texte vide sont ajoutées pour atteindre 24 images.
    Les images blanches sont ajoutées de manière à ce que les images initiales soient uniformément réparties dans la liste finale.
    """
    nb_images_initiales = len(images)
    nb_images_ajoutees = 24 - nb_images_initiales
    images_ajoutees = '' 
    # print(images)
    for i in range(nb_images_ajoutees):
        images.insert(int(i * nb_images_initiales / nb_images_ajoutees), images_ajoutees )
    return images

def generate_svgs(dir_path, title, background_colors, output_file):

    images = [i for i in os.listdir(dir_path) if i.startswith('thumb_')]
    if images[24:]:print("Les fichiers suivantes sont ignorés ",images[24:])
    images=images[:24]
    images = completeImagesTo24(images)
    
    if not output_file:
        output_file="".join( x for x in title if (x.isalnum() or x in "._- "))

    colors = background_colors.split(',')
    if len(colors)!=2: 
        print("Deux couleurs sont necessaires: red,blue")
    for i,color in enumerate(colors):
        filename =f"{output_file} {i}"
        generate_svg(dir_path, images, title, color, filename)
        random.shuffle(images) # Mélange de l'ordre pour éviter la triche

        with open(f"{filename}.svg", "rb") as f:
            drawing = svg2rlg(f)
        renderPDF.drawToFile(drawing, f"{filename}.pdf")
        import cairosvg
        cairosvg.svg2pdf(url=f"{filename}.svg", write_to=f"{filename}.pdf")


def make_pngdata(path):
    import svgwrite
    import base64
    from wand.image import Image

    # Load PNG Image
    dwg = svgwrite.Drawing()
    img = Image(filename=path)

    # Then get raw PNG data and encode DIRECTLY into the SVG file.
    image_data = img.make_blob(format='png')
    encoded = base64.b64encode(image_data).decode()
    pngdata = 'data:image/png;base64,{}'.format(encoded)
    return pngdata

def generate_svg(dir_path, images, title, background_color, output_file):
    dwg = svgwrite.Drawing(filename=f"{output_file}.svg", size=("27.2cm", "19.15cm"))
    dwg.add(dwg.rect(insert=(0,0), size=("27.2cm", "19.15cm"), fill='white', stroke="black", stroke_width=".5mm"))
    # t = dwg.g(style="font-size:30;font-family:Comic Sans MS, Arial;font-weight:bold;font-style:oblique;stroke:black;stroke-width:1;fill:none")
    t = dwg.g(style="font-size:30;font-family: Arial")


    group_a = dwg.g(id="group_a")
    group_b = dwg.g(id="group_b")
    
    # Groupe A (haut) : 2 lignes de 12 
    stroke_w=0.06
    w,h=2.075,2.6
    for i, image in enumerate(images):
        x = 1.5 + (i % 12) * w
        y = .6 + (i // 12) * 3.15
        text = os.path.splitext(image)[0].replace('thumb_', '')
        if text:
            g=dwg.g()
            g.add(dwg.image(href=make_pngdata(os.path.join(dir_path, image)), insert=(f'{x}cm', f'{y}cm'), size=("2cm", "2.4cm")))
            # Cadre autour de l'image
            g.add(dwg.rect(insert=(f'{x}cm', f'{y}cm'), size=(f"{w}cm",f"{h}cm"), fill='none', stroke=background_color, stroke_width=f"{stroke_w}cm"))
            # Cadre au dessous du text
            clip_path = dwg.defs.add(dwg.clipPath(id=f'clip_path_h{i}')) #name the clip path
            clip_path.add(dwg.rect((f'{x+(stroke_w)/2}cm', f'{y+(stroke_w)/2}cm'),(f'{w-stroke_w}cm', f'{h-stroke_w}cm'))) #things inside this shape will be drawn
            g.add(dwg.rect(insert=(f'{x}cm', f'{y+h-0.45}cm'), size=(f'{w}cm', "1cm"), fill='white', stroke=background_color, stroke_width=".3mm", rx=13, clip_path=f"url(#clip_path_h{i})"))
            
            g.add(dwg.text(text, insert=(f'{x+w/2}cm', f'{y+h-1.5*stroke_w}cm'), font_size=".35cm", text_anchor="middle"))
            group_b.add(g)
            
    # Groupe B (haut) : 3 lignes de 8 
    w,h=2.55,3.08
    for i, image in enumerate(images):
        x = 1.8 + (i % 8) * 3.1375
        y = 7.6 + (i // 8) * 4
        text = os.path.splitext(image)[0].replace('thumb_', '')
        if text:
            g=dwg.g()
            g.add(dwg.image(href=make_pngdata(os.path.join(dir_path, image)), insert=(f'{x}cm', f'{y}cm'), size=(f'{w}cm', f'{h}cm')))
            # Cadre autour de l'image
            g.add(dwg.rect(insert=(f'{x}cm', f'{y}cm'), size=(f'{w}cm', f'{h}cm'), fill='none', stroke=background_color, stroke_width=".6mm"))
            
            # Cadre au dessous du text
            clip_path = dwg.defs.add(dwg.clipPath(id=f'clip_path_b{i}')) #name the clip path
            clip_path.add(dwg.rect((f'{x+(stroke_w)/2}cm', f'{y+(stroke_w)/2}cm'),(f'{w-stroke_w}cm', f'{h-stroke_w}cm'))) #things inside this shape will be drawn
            g.add(dwg.rect(insert=(f'{x+.15}cm', f'{y+h-0.45}cm'), size=(f'{w-.3}cm', "1cm"), fill='white', stroke=background_color, stroke_width=".3mm", rx=13, clip_path=f"url(#clip_path_b{i})"))

            g.add(dwg.text(text, insert=(f'{x+w/2}cm', f'{y+h-1.5*stroke_w}cm'), font_size=".4cm", text_anchor="middle"))
            group_b.add(g)

    t.add(group_a)
    t.add(group_b)

    # Title
    t.add(dwg.rect(('-0.2cm','6mm'), ('1.5cm', '5.5cm'), fill=background_color, rx=10, transform='rotate(0 0 0)'))
    t.add(dwg.text(title, insert=('1.2cm', '5.3cm'), fill='black', font_size='0.9cm', transform='rotate(-90 45 210)',font_weight="bold"))
    dwg.add(t)
    dwg.save()

    print(f"Created : {output_file}.svg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", help="Répertoire des images miniatures")
    parser.add_argument("-t", "--title", help="Titre du fichier SVG")
    parser.add_argument("-b", "--background", help="Les 2 couleurs de fond : red,blue", default='red,blue')
    parser.add_argument("-o", "--output", help="Nom des fichiers de sortie : Title ")
    args = parser.parse_args()
    generate_svgs(args.dir, args.title, args.background, args.output)