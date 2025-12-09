import tkinter as tk
from threading import Timer
from time import sleep
from BrailleCharacter import *
from TKComponents.BrailleCharacter import draw_character_string
from tkinter import filedialog
from math import floor

printing_rect_id = None
printed_rect_id = None
printing_line = None
printed_line = None
is_printing = False

def updateRect(canvas, line_width, line_height):
    global printing_rect_id
    global printed_rect_id
    global printing_line
    global printed_line
    if printing_rect_id is not None:
        canvas.delete(printing_rect_id)
        canvas.delete(printed_rect_id)
    printing_rect_id=canvas.create_rectangle(
        10, printing_line * line_height,
        line_width, line_height * (printing_line + 1),
        outline="green"
    )
    if printing_line >= 0:
        printed_rect_id=canvas.create_rectangle(
            10, 0,
            line_width - 10, line_height * printed_line
        )
    printing_line += 1
    printed_line += 1
    Timer(2, updateRect, args=(canvas, line_width, line_height)).start()


def openButtonAction(variavelDeTexto):
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[
            ("Arquivos de texto", "*.txt"),
            ("Estado da interface", "*.json")
        ]
    )
    if caminho:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
            if caminho.endswith('txt'):
                variavelDeTexto.insert(tk.END, conteudo)
                return None
            elif caminho.endswith('json'):
                return conteudo
                    
            

def saveButtonAction(text):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".json")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    f.write(text)
    f.close()

def sendButtonAction(canvas):
    line_height = 90
    line_width=500
    global printing_line
    global printed_line
    printing_line = 0
    printed_line = -1
    updateRect(canvas, line_width, line_height)


def calculateCharLim(
    dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing,
    paperDimensionOption, marginWidth
):
    canvasWidth = paperDimensionOption.width
    charWidth = (4 * dot_radius) + h_spacing
    charLim=(canvasWidth - (2 * marginWidth) + h_outer_spacing) / (charWidth + h_outer_spacing)
    return charLim

def cmsToPixels(paperDimensionOption, paperScreenWidth, arg):
    return (arg * (paperScreenWidth / paperDimensionOption.width))

def submitTextToConvertAction(
    textVariable, brailleCanvas, iniX, iniY,
    paperDimensionOption, currCanvasWidthInPixels,
    marginWidth, dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing
):
    (dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing) = (
        float(field.get())
        for field in (dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing)
    )
    marginWidth = float(marginWidth.get())
    charLim = calculateCharLim(
        dot_radius, h_spacing, v_spacing,
        h_outer_spacing, v_outer_spacing,
        paperDimensionOption, marginWidth
    )
    iniX, iniY, dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing, marginWidth = (
        cmsToPixels(paperDimensionOption, currCanvasWidthInPixels, arg) 
        for arg in (
           iniX, iniY,  dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing, marginWidth
        )
    )
    ratio = paperDimensionOption.height / paperDimensionOption.width
    newCanvasHeight = currCanvasWidthInPixels * ratio
    brailleCanvas.config(height=newCanvasHeight)
    brailleCanvas.delete('all')
    lkp=BrailleCharacter.chars_as_dict(get_all_braille_characters()) 
    text_variable_content = textVariable
    default = [
        [True, True],
        [True, True],
        [True, True]
    ]
    charLim=int(floor(charLim))
    draw_character_string(
        brailleCanvas,
        [
            lkp.get(char.upper()) or default
            for char in text_variable_content 
        ],
        iniX, iniY, charLim,
        dot_radius, h_spacing, v_spacing,
        h_outer_spacing, v_outer_spacing,
        text_variable_content
    )
    canvasWidth=currCanvasWidthInPixels
    brailleCanvas.create_line(iniX, 0, iniX, newCanvasHeight, dash=(2,2), fill="blue", width=1)
    brailleCanvas.create_line(canvasWidth - iniX, 0, canvasWidth - iniX, newCanvasHeight, dash=(2,2), fill="blue", width=1)
    brailleCanvas.create_line(0, iniY, canvasWidth, iniY, dash=(2,2), fill='green', width=1)
    brailleCanvas.create_line(0, newCanvasHeight-iniY, canvasWidth, newCanvasHeight-iniY, dash=(2,2), fill='green', width=1)
