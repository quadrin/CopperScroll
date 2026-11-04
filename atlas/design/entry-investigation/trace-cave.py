"""Regenerate the native vector cave from the retained generated artwork.
Requires Pillow and vtracer. Run from any directory; no network access.
The binary alpha mask removes translucent fringes. Sixteen paint colors retain
the original lighting and rock planes. Output contains paths, no raster image.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
import vtracer

root=Path(__file__).resolve().parent
destination=root.parents[1]/'public/introduction/entry-investigation/limestone-cave.svg'
with TemporaryDirectory() as temp:
    image=Image.open(root/'cave-generated.png')
    image.thumbnail((1200,800))
    alpha=image.getchannel('A').point(lambda a:255 if a>128 else 0)
    palette=image.convert('RGB').quantize(colors=16).convert('RGBA')
    palette.putalpha(alpha)
    source=Path(temp)/'palette.png'
    palette.save(source)
    vtracer.convert_image_to_svg_py(str(source),str(destination),
        colormode='color',hierarchical='stacked',mode='spline',
        filter_speckle=18,color_precision=5,layer_difference=24,
        corner_threshold=70,length_threshold=5,splice_threshold=45,path_precision=2)
print(destination)
