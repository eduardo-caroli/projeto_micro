from BrailleCharacter import *
from TKComponents.BrailleCharacter import draw_character_string
from tkinter import filedialog

def openButtonAction(variavelDeTexto):
    caminho = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("Arquivos de texto", "*.txt")]
    )
    if caminho:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
            variavelDeTexto.set(conteudo)

def saveButtonAction():
    pass

def sendButtonAction():
    pass


def calculateCharLim(
    dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing,
    paperDimensionOption, marginWidth
):
    canvasWidth = paperDimensionOption.width
    charWidth = (4 * dot_radius) + h_spacing
    charLim=(h_outer_spacing + canvasWidth - 2 * marginWidth) / (charWidth + h_outer_spacing)
    return charLim

def cmsToPixels(paperDimensionOption, paperScreenWidth, arg):
    return (arg * (paperScreenWidth / paperDimensionOption.width))

def submitTextToConvertAction(
    textVariable, brailleCanvas, iniX, iniY,
    paperDimensionOption, currCanvasWidthInPixels,
    marginWidth, dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing
):
    marginWidth = float(marginWidth.get())
    charLim = calculateCharLim(
        dot_radius, h_spacing, v_spacing,
        h_outer_spacing, v_outer_spacing,
        paperDimensionOption, marginWidth
    )
    dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing, marginWidth = (
        cmsToPixels(paperDimensionOption, currCanvasWidthInPixels, arg) 
        for arg in (
            dot_radius, h_spacing, v_spacing, h_outer_spacing, v_outer_spacing, marginWidth
        )
    )
    ratio = paperDimensionOption.height / paperDimensionOption.width
    newCanvasHeight = currCanvasWidthInPixels * ratio
    brailleCanvas.config(height=newCanvasHeight)
    brailleCanvas.delete('all')
    lkp=BrailleCharacter.chars_as_dict(get_all_braille_characters()) 
    text_variable_content = textVariable.get()
    default = [
        [True, True],
        [True, True],
        [True, True]
    ]
    draw_character_string(
        brailleCanvas,
        [
            lkp.get(char.upper()) or default
            for char in text_variable_content 
        ],
        iniX, iniY, charLim,
        dot_radius, h_spacing, v_spacing,
        h_outer_spacing, v_outer_spacing
    )
