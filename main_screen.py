import tkinter
import buttonActions
from stringLookup import *
from paperDimensions import getPaperDimensionOptions
from TKComponents.BrailleCharacter import *
from BrailleCharacter import *

canvasWidth=300
canvasHeight=300
root = tkinter.Tk(screenName="main_screen")
paperDimensionOptions=getPaperDimensionOptions()
paperDimensionOptionNames=[
    option.name for option in paperDimensionOptions
]

marginWidth = tkinter.StringVar(root, value="0")
selectedPaperDimension = tkinter.StringVar(root, value=paperDimensionOptionNames[0])

openButton=tkinter.Button(root, text=openString, command = buttonActions.openButtonAction).pack()
saveButton=tkinter.Button(root, text=saveString, command = buttonActions.saveButtonAction).pack()
sendButton=tkinter.Button(root, text=sendString, command = buttonActions.sendButtonAction).pack()

marginEntry=tkinter.Entry(root, width=10, textvariable=marginWidth).pack()

paperDimensionsSelection=tkinter.OptionMenu(
    root,
    selectedPaperDimension,
    *[option.name for option in getPaperDimensionOptions()]
).pack()

brailleCanvas = tkinter.Canvas(
    root,
    width=canvasWidth,
    height=canvasHeight,
    bg='white'
)

brailleCanvas.pack()

cd = BrailleCharacter.chars_as_dict(
    get_all_braille_characters()
)

draw_character_string(brailleCanvas, [cd['A'], cd['B'], cd['C'], cd['D']], 0, 0, 3)

root.mainloop()
