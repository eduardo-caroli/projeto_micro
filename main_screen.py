import tkinter
import tkinter as tk
import buttonActions
from stringLookup import *
from paperDimensions import getPaperDimensionOptions
from TKComponents.BrailleCharacter import *
from TKComponents.LabeledEntry import LabeledEntry
from BrailleCharacter import *
from InterfaceState import InterfaceState


#Frames
root = tkinter.Tk(screenName="main_screen")
sheetFrame = tk.Frame(root)
sheetFrame.pack(side="left", fill="y")
textAndOptionsFrame = tk.Frame(root)
textAndOptionsFrame.pack(side="right", fill="y")
optionsFrame = tk.Frame(textAndOptionsFrame)
optionsFrame.pack(side="bottom", fill="x")
textFrame=tk.Frame(textAndOptionsFrame)
textFrame.pack(side="top", fill="x")
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
dot_radius=0.15#5/30
h_spacing=0.1#10/30
v_spacing=0.1#10/30
h_outer_spacing=0.3#10/30
v_outer_spacing=0.275#10/30


#TKInter variables
marginWidth = tkinter.StringVar(root, value="0")
charactersPerLine = tkinter.StringVar(root, value="20")
selectedPaperDimension = tkinter.StringVar(root, value=paperDimensionOptionNames[0])
textToConvert = tkinter.StringVar(root)

dot_radius_tkvar=tkinter.StringVar(root, value=dot_radius)
h_spacing_tkvar=tkinter.StringVar(root, value=h_spacing)
v_spacing_tkvar=tkinter.StringVar(root, value=v_spacing)
h_outer_spacing_tkvar=tkinter.StringVar(root, value=h_outer_spacing)
v_outer_spacing_tkvar=tkinter.StringVar(root, value=v_outer_spacing)
param_tkvars={
#    "Raio": dot_radius_tkvar,
#    "Espaço interno horizontal": h_spacing_tkvar,
#    "Espaço interno vertical": v_spacing_tkvar,
#    "Espaço externo horizontal": h_outer_spacing_tkvar,
#    "Espaço externo vertical": v_outer_spacing_tkvar,
    "Margem": marginWidth
}

#Button Actions
fooBarBaz = lambda: buttonActions.submitTextToConvertAction(
    textToConvertEntry.get('1.0', 'end - 1c'), brailleCanvas, float(marginWidth.get()), float(marginWidth.get()),
    [dimension for dimension in getPaperDimensionOptions() if dimension.name == selectedPaperDimension.get()][0],
    canvasWidth, marginWidth,
    dot_radius_tkvar, h_spacing_tkvar, v_spacing_tkvar, h_outer_spacing_tkvar, v_outer_spacing_tkvar
)

def sendButtonAction():
    buttonActions.sendButtonAction(brailleCanvas)    

def cvtOpenButtonAction():
    content=buttonActions.openButtonAction(textToConvertEntry)
    if content is not None:
        interface_state = InterfaceState.model_validate_json(content)
        dot_radius_tkvar.set(interface_state.radius)
        h_spacing_tkvar.set(interface_state.internal_hspace)
        v_spacing_tkvar.set(interface_state.internal_vspace)
        h_outer_spacing_tkvar.set(interface_state.external_hspace)
        v_outer_spacing_tkvar.set(interface_state.external_vspace)
        marginWidth.set(interface_state.margin)
        textToConvertEntry.delete('1.0', 'end')
        textToConvertEntry.insert('end-1c', interface_state.text)
        selectedPaperDimension.set(interface_state.paper_type)

    fooBarBaz()

def saveButtonAction():
    state = InterfaceState(
        radius=float(dot_radius_tkvar.get()),
        internal_hspace=float(h_spacing_tkvar.get()),
        internal_vspace=float(v_spacing_tkvar.get()),
        external_hspace=float(h_outer_spacing_tkvar.get()),
        external_vspace=float(v_outer_spacing_tkvar.get()),
        margin=float(marginWidth.get()),
        text=textToConvertEntry.get('1.0', tkinter.END)[:-1],
        paper_type=selectedPaperDimension.get()
    )
    buttonActions.saveButtonAction(
        state.model_dump_json()
    )

#Elements
row=0
col=0
for label, tkvar in param_tkvars.items():
   LabeledEntry(
       optionsFrame, textvariable=tkvar, width=15, label_text=label
   ).grid(row=row, column=col)
   col = (col + 1) % 3
   if col == 0:
       row += 1

openButton=tkinter.Button(buttonsFrame, text=openString, command = cvtOpenButtonAction).pack(side='left', expand=True, fill='x')

saveButton=tkinter.Button(buttonsFrame, text=saveString, command = saveButtonAction).pack(side='left', expand=True, fill='x')

sendButton=tkinter.Button(buttonsFrame, text=sendString, command = sendButtonAction).pack(side='left', expand=True, fill='x')

textToConvertEntry=tkinter.Text(textFrame, width=70)
textToConvertEntry.pack(pady=10,padx=10)
submitTextToConvertButton=tkinter.Button(
    buttonsFrame, text=submitTextToConvertString,
    command=fooBarBaz
).pack(side="left", expand=True, fill='x')

paperDimensionsSelection=tkinter.OptionMenu(
    root,
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

brailleCanvas.create_rectangle(50, 50, 250,150, fill='white', outline='blue')

root.mainloop()
