import turtle
import json
import sys

def draw_from_json(json_file):
    # Cargar y validar regiones
    try:
        with open(json_file) as f:
            regions = json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{json_file}'")
        return
    except json.JSONDecodeError as e:
        print(f"Error al parsear JSON: {e}")
        return

    if not regions:
        print("El archivo JSON no contiene regiones.")
        return

    # Configurar Turtle
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.setup(800, 800)
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    screen.tracer(0)

    # Calcular límites para centrar el dibujo
    try:
        all_points = [(p[0], p[1]) for r in regions for p in r['contour']]
    except KeyError:
        print("Error: alguna región no tiene la clave 'contour'.")
        return

    min_x = min(p[0] for p in all_points)
    max_x = max(p[0] for p in all_points)
    min_y = min(p[1] for p in all_points)
    max_y = max(p[1] for p in all_points)

    # Calcular escala y centro (evitar división por cero)
    width = max_x - min_x or 1
    height = max_y - min_y or 1
    scale = min(600 / width, 600 / height)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    # Dibujar cada región
    for region in regions:
        try:
            r, g, b = int(region['color'][0]), int(region['color'][1]), int(region['color'][2])
        except (KeyError, IndexError, ValueError):
            print(f"Color inválido en región, se omite.")
            continue

        color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        t.color(color, color)

        points = region['contour']
        if not points:
            continue

        t.begin_fill()
        t.penup()
        x = (points[0][0] - center_x) * scale
        y = (center_y - points[0][1]) * scale
        t.goto(x, y)
        t.pendown()

        for point in points[1:]:
            x = (point[0] - center_x) * scale
            y = (center_y - point[1]) * scale
            t.goto(x, y)

        t.goto((points[0][0] - center_x) * scale,
               (center_y - points[0][1]) * scale)
        t.end_fill()
        screen.update()

    turtle.done()  # Más compatible que screen.mainloop()

if __name__ == '__main__':
    json_file = sys.argv[1] if len(sys.argv) > 1 else 'sunflowers.json'
    draw_from_json(json_file)