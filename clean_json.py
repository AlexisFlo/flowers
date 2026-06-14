# Script para limpiar el JSON existente
import json

with open('sunflowers.json') as f:
    regions = json.load(f)

for region in regions:
    region['contour'] = [[round(p[0]), round(p[1])] for p in region['contour']]
    region['color'] = [round(c) for c in region['color']]

with open('sunflowers_compact.json', 'w') as f:
    json.dump(regions, f, separators=(',', ':'))  # Sin espacios extra