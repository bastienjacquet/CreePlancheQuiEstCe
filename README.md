# CreePlancheQuiEstCe
Scripts pour créer une planche de Qui-est-ce ? (jeu hasbro 2008) à partir des images d'un répertoire.

Scripts to make a custom sheet of Guess who Extra ? (hasbro game) from images in a repository.

# Dependancies
Dependences:
`pip3 install svgwrite wand cairosvg cv2 wand opencv-python`

# Run
python3 prepareImages.py -d AllImages/
python3 generateQuiESTCeSVG.py -d AllImages/ -t "La Famille" -b 'red,lightblue' -o "Auto FB"
\
# Details
## prepareImages.py
usage: prepareImages.py [-h] [-d DIR] [-f] [-b]
optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Répertoire des images miniatures
  -f, --auto_crop_faces
                        Auto crop around faces
  -b, --equalize_brightness
                        Automatically equalize brigthnees

## generateQuiESTCeSVG.py
usage: generateQuiESTCeSVG.py [-h] [-d DIR] [-t TITLE] [-b BACKGROUND] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Répertoire des images miniatures
  -t TITLE, --title TITLE
                        Titre du fichier SVG
  -b BACKGROUND, --background BACKGROUND
                        Les 2 couleurs de fond : red,blue
  -o OUTPUT, --output OUTPUT
                        Nom des fichiers de sortie svg et pdf
