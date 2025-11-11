from typing import List

def draw_braille(
    canvas, ini_x: float, ini_y: float,
    pattern, dot_radius, h_spacing, v_spacing
):
    for row in range(3):
        for col in range(2):
            #canvas.create_rectangle(ini_x, ini_y, ini_x + 6 * dot_radius, ini_y + 10 * dot_radius, fill='red')
            x = col * (h_spacing + 2*dot_radius) + ini_x + dot_radius
            y = row * (v_spacing + 2*dot_radius) + ini_y + dot_radius
            filled = pattern[row][col]
            if filled:
                canvas.create_oval(
                    x - dot_radius, y - dot_radius,
                    x + dot_radius, y + dot_radius,
                    fill='black'                )

def draw_character_string(
    canvas, string: List[List[List[bool]]], x: float, y: float,
    char_limit: int, dot_radius, h_spacing, v_spacing,
    v_outer_spacing, h_outer_spacing
):
    char_width=(4 * dot_radius) + h_spacing + h_outer_spacing 
    char_height=(6 * dot_radius) + (2 * v_spacing) + v_outer_spacing 
    cx=x
    cy=y
    for indicis, character in enumerate(string):
        draw_braille(canvas, cx, cy, character, dot_radius, h_spacing, v_spacing)
        if (indicis % char_limit) == char_limit - 1:
            cx=x
            cy+=line_height
        else:
            cx+=char_width

        
