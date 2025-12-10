import tkinter as tk
import numpy as np
from threading import Timer, Thread
from time import sleep
import threading
from BrailleCharacter import *
from TKComponents.BrailleCharacter import draw_character_string
from tkinter import filedialog
from math import floor
import serial

printing_rect_id = None
printed_rect_id = None
num_printed_lines = None
writing_to_printer = True
charLim=None

port="/dev/cu.usbmodem11201"

try:
    ard = serial.Serial(
        port=port,
        baudrate=9600
    )
except serial.serialutil.SerialException:
    print(f"Impossivel conectar ao Arduino com porta {port}")
    ard = None

def _encode_line(line):
    body = ""
    for char in line:
        body += '['
        for bit in char:
            body += str(bit)
            body += ','
        body=body[:-1]
        body += ']'
        body += ","
    body = body[:-1]
    return ("p:" + body).encode('utf-8')

def _write_to_printer(lines_of_text: list[list[bool]], canvas, lineWidth, lineHeight):
    print("started here")
    global writing_to_printer
    global num_printed_lines
    num_printed_lines=0
    total_lines_to_print = len(lines_of_text)
    _updateRect(canvas, lineWidth, lineHeight)
    first_line = True
    printed_chars=0
    line_to_print = lines_of_text[0]
    first_writing = False
    print("=====> ",line_to_print)
    print("am here")
    while True:
        if first_line or "p" in line:
            char = line_to_print[printed_chars] if not first_writing else "100"
            ard.write(char.encode('utf-8'))
            print("=====> ", char)
            printed_chars += 1
            if first_writing and printed_chars == 4:
                first_writing = False
                printed_chars = 0
            first_line = False
            if printed_chars == len(line_to_print):
                num_printed_lines += 1
                if num_printed_lines >= total_lines_to_print:
                    print("Impressao finalizada")
                    writing_to_printer = False
                    return
                _updateRect(canvas, lineWidth, lineHeight)
                line_to_print = lines_of_text[num_printed_lines]
                printed_chars = 0
        line = ard.readline().decode()
        sleep(0.2)
        print("line was: ", line)

def _updateRect(canvas, line_width, line_height):
    global printing_rect_id
    global printed_rect_id
    if printing_rect_id is not None:
        canvas.delete(printing_rect_id)
        canvas.delete(printed_rect_id)
    printing_rect_id=canvas.create_rectangle(
        line_width * 0.975, (num_printed_lines + 0.2) * line_height,
        line_width, line_height * (num_printed_lines + 0.8),
        fill="green"
    )
    printed_line = num_printed_lines + 1


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

def lineToStream(line: str):
    line=line[::-1]
    cd = {
        c.corresponding_character: c
        for c in get_all_braille_characters()
    }
    line = [
       cd[c.upper()]
       for c in line
    ]
    bitline = ""
    for char in line:
        bitline += char.as_bits()
    line1=""
    line2=""
    line3=""
    print(bitline)
    for i in range(len(bitline) // 6):
        line1 += bitline[i*6:i*6 + 2]
        line1 += "s"
    line1 += "j"
    for i in range(len(bitline) // 6):
        line2 += bitline[2 + i*6:i*6 + 4]
        line2 += "s"
    line2 += "j"
    for i in range(len(bitline) // 6):
        line3 += bitline[4 + i*6:i*6 + 6]
        line3 += "s"
    line3 += "n"
    return line1 + line2 + line3

def sendButtonAction(
    text: list[list[bool]], canvas,
    lineWidth, lineHeight, paperWidth,
    dot_radius, v_inner_spacing, v_outer_spacing,
    h_inner_spacing, h_outer_spacing
):
#    lineWidth = cmsToPixels(500, lineWidth, lineWidth)
#    lineHeight = cmsToPixels(500, lineWidth, lineHeight)
    text += " " * (charLim - (len(text) % charLim))
    lineWidth=500
    lineHeight *= (lineWidth / paperWidth)
    from math import ceil
    lines_of_text = [
        lineToStream(text[i*charLim : (i+1)*charLim])
        for i in range(ceil(len(text)/charLim))
    ]
    global writing_to_printer
    if ard is None:
        print("Arduino nao conectado")
        return
    inner_space = 2 * dot_radius + h_inner_spacing
    values = [
        dot_radius,
        v_outer_spacing,
        v_inner_spacing,
        h_outer_spacing,
    ]
    values = [
        int(ceil(2000 * float(v) / 4.5))
        for v in values
    ]
    first_line=True
    i=0
    from math import ceil
#    while i < 4:
#        if first_line or 'p' in line.decode():
#            line = ard.write(str(values[i]).encode('utf-8'))
#            first_line = False
#            i += 1
#        line = ard.readline()  
#        sleep(0.1)
    writing_to_printer=True
    Thread(target=_write_to_printer, daemon=True, args=(lines_of_text, canvas, lineWidth, lineHeight)).start()
    

def calculateCharLim(
    dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing,
    paperDimensionOption, marginWidth
):
    canvasWidth = paperDimensionOption.width
    charWidth = (4 * dot_radius) + h_spacing
    charLim=(canvasWidth - (2 * marginWidth) + h_outer_spacing) / (charWidth + h_outer_spacing)
    return charLim

def cmsToPixels(paperWidth, paperScreenWidth, arg):
    return (arg * (paperScreenWidth / paperWidth))

def cmsToPixelsWithPaper(paperDimensionOption, paperScreenWidth, arg):
    return (arg * (paperScreenWidth / paperDimensionOption.width))

def submitTextToConvertAction(
    textVariable, brailleCanvas, iniX, iniY,
    paperDimensionOption, currCanvasWidthInPixels,
    marginWidth, dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing
):
    global charLim
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
        cmsToPixelsWithPaper(paperDimensionOption, currCanvasWidthInPixels, arg) 
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
