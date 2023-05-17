from ascii_magic import AsciiArt
import os 
folder = 'portraits'
for l in os.listdir(folder):
    if l.endswith('.jpeg'):
        print(l)
        my_art = AsciiArt.from_image(f'{folder}/{l}')

        my_art.to_html_file(f'{folder}/{l}.html', columns=200,width_ratio=2 )

