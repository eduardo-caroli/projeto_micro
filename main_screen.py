import tkinter
import tkinter as tk
import buttonActions
from stringLookup import *
from paperDimensions import getPaperDimensionOptions
from TKComponents.BrailleCharacter import *
from BrailleCharacter import *


#Frames
root = tkinter.Tk(screenName="main_screen")
sheetFrame = tk.Frame(root)
sheetFrame.pack(side="left", fill="y")
optionsFrame = tk.Frame(root)
optionsFrame.pack(side="right", fill="y")
buttonsFrame = tk.Frame(sheetFrame)
buttonsFrame.pack(side="bottom", fill="x")
leavesFrame = tk.Frame(sheetFrame)
leavesFrame.pack(side="top", fill="x")



#Local variables
canvasWidth=500
canvasHeight=canvasWidth * 1.41
paperDimensionOptions=getPaperDimensionOptions()
paperDimensionOptionNames=[
    option.name for option in paperDimensionOptions
]
dot_radius=5/30
h_spacing=10/30
v_spacing=10/30
h_outer_spacing=10/30
v_outer_spacing=10/30


#TKInter variables
marginWidth = tkinter.StringVar(root, value="0")
charactersPerLine = tkinter.StringVar(root, value="20")
selectedPaperDimension = tkinter.StringVar(root, value=paperDimensionOptionNames[0])
textToConvert = tkinter.StringVar(root)

dot_radius_tkvar=tkinter.StringVar(root)
h_spacing_tkvar=tkinter.StringVar(root)
v_spacing_tkvar=tkinter.StringVar(root)
h_outer_spacing_tkvar=tkinter.StringVar(root)
v_outer_spacing_tkvar=tkinter.StringVar(root)
param_tkvars=[
    dot_radius_tkvar, h_spacing_tkvar, v_spacing_tkvar,
    h_outer_spacing_tkvar, v_outer_spacing_tkvar
]

#Button Actions
fooBarBaz = lambda: buttonActions.submitTextToConvertAction(
    textToConvert, brailleCanvas, float(marginWidth.get()), float(marginWidth.get()),
    [dimension for dimension in getPaperDimensionOptions() if dimension.name == selectedPaperDimension.get()][0],
    canvasWidth, marginWidth,
    dot_radius_tkvar, h_spacing_tkvar, v_spacing_tkvar, h_outer_spacing_tkvar, v_outer_spacing_tkvar
)

def cvtOpenButtonAction():
    buttonActions.openButtonAction(textToConvert)
    fooBarBaz()

#Elements
for tkvar in param_tkvars:
    tkinter.Entry(
        optionsFrame, textvariable=tkvar, width=15
    ).pack()

openButton=tkinter.Button(buttonsFrame, text=openString, command = cvtOpenButtonAction).pack(side='left', expand=True, fill='x')

saveButton=tkinter.Button(buttonsFrame, text=saveString, command = buttonActions.saveButtonAction).pack(side='left', expand=True, fill='x')

sendButton=tkinter.Button(buttonsFrame, text=sendString, command = buttonActions.sendButtonAction).pack(side='left', expand=True, fill='x')

marginEntry=tkinter.Entry(optionsFrame, textvariable=marginWidth).pack(side="left", expand=True, fill="x")
textToConvertEntry=tkinter.Entry(optionsFrame, width=100, textvariable=textToConvert).pack()
submitTextToConvertButton=tkinter.Button(
    buttonsFrame, text=submitTextToConvertString,
    command=fooBarBaz
).pack(side="left", expand=True, fill='x')

paperDimensionsSelection=tkinter.OptionMenu(
    optionsFrame,
    selectedPaperDimension,
    *[option.name for option in getPaperDimensionOptions()]
).pack()

brailleCanvas = tkinter.Canvas(
    leavesFrame,
    width=canvasWidth,
    height=canvasHeight,
    bg='white'
)

brailleCanvas.pack(side="left")

cd = BrailleCharacter.chars_as_dict(
    get_all_braille_characters()
)

root.mainloop()
