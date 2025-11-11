from typing import List

def draw_braille(canvas, ini_x: float, ini_y: float, pattern, dot_radius=10, spacing=30):
    for row in range(3):
        for col in range(2):
            x = col * spacing + dot_radius + ini_x
            y = row * spacing + dot_radius + ini_y
            filled = pattern[row][col]
            if filled:
                canvas.create_oval(
                    x - dot_radius, y - dot_radius,
                    x + dot_radius, y + dot_radius,
                    fill='black', outline="black", width=2
                )

def draw_character_string(
    canvas, string: List[List[List[bool]]], x: float, y: float,
    char_limit: int, char_width: float = 90, line_height=150
):
    cx=x
    cy=y
    for indicis, character in enumerate(string):
        draw_braille(canvas, cx, cy, character)
        if (indicis % char_limit) == 0:
            cx=x
            cy+=line_height
        else:
            cx+=char_width

        
