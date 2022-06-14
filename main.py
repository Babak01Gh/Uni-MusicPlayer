from logging import root
import vlc
from tkinter import *
from tkinter.ttk import Combobox, Style
from tkinter import filedialog as fd
import tkinter.font as font

# ? =========================Variables=========================

global PlayList, media_player, media_list
PlayList = []
media_player = vlc.MediaListPlayer()
media_list = vlc.Instance().media_list_new()

fontColor = '#E64398'
secondaryColor = '#A1C3D1'
btnColor = '#E7E3D4'
rootColor = '#B39BC8'
# ? =========================EndVariables=========================

# ? =========================Make Root=========================
mainWindow = Tk()
mainWindow.title('Music Player')
mainWindow.config(bg=rootColor)
mainWindow.geometry('450x200')
mainWindow.resizable(False, False)
mainWindow.option_add("*TCombobox*Background", secondaryColor)
mainWindow.option_add("*TCombobox*Foreground", fontColor)
music = StringVar(None, 'nothing Play')
# ? =========================End Make Root=========================

# ? =========================Typography & Styles=========================
myFont = font.Font(weight="bold", size=10)
style = Style()
style.theme_use('clam')

icon = PhotoImage(file='Photos/play-icon-5.png')
photoimage = icon.subsample(3, 3)
icon2 = PhotoImage(file='Photos/pause.png')
photoimage2 = icon2.subsample(3, 3)
icon3 = PhotoImage(file='Photos/previous-icon-13.png')
photoimage3 = icon3.subsample(15, 15)
icon4 = PhotoImage(file='Photos/next-icon-13.png')
photoimage4 = icon4.subsample(15, 15)
icon5 = PhotoImage(file='Photos/back.png')
photoimage5 = icon5.subsample(18, 18)
icon6 = PhotoImage(file='Photos/forw.png')
photoimage6 = icon6.subsample(18, 18)
icon7 = PhotoImage(file='Photos/reverse.png')
photoimage7 = icon7.subsample(11, 11)
# ? =========================End Typo & Styles=========================

# ! =========================Definations=========================


def openFiles():
    filename = fd.askopenfilenames(title='Open Your Files')
    for i in filename:
        PlayList.append(i[i.rfind('/')+1:])
        media_list.add_media(i)
    media_player.set_media_list(media_list)
    listbox.config(listvariable=StringVar(value=PlayList))


def next_def():
    if PlayList:
        media_player.next()
    else:
        music.set('Please Import files')


def Play_def():
    if PlayList:
        media_player.play()
        timerStart()
    else:
        music.set('Please Import files')


def Pause_def():
    if PlayList:
        media_player.pause()
    else:
        music.set('Please Import files')


def previous_def():
    if PlayList:
        media_player.previous()
    else:
        music.set('Please Import files')


def play_select(event):
    if event.widget.curselection():
        media_player.play_item_at_index(
            PlayList.index(PlayList[event.widget.curselection()[0]]))
        timerStart()


def set_rate(event):
    media_player.get_media_player().set_rate(float(event.widget.get()))


def forward_to():
    currentTime = media_player.get_media_player().get_position()
    addTime = int(lunge.get()) / \
        (media_player.get_media_player().get_length()//1000)
    media_player.get_media_player().set_position(currentTime+addTime)


def backward_to():
    currentTime = media_player.get_media_player().get_position()
    addTime = int(lunge.get()) / \
        (media_player.get_media_player().get_length()//1000)
    media_player.get_media_player().set_position(currentTime-addTime)


def Repeat_def():
    media_player.get_media_player().set_position(0)


def timerStart():
    fullTime = media_player.get_media_player().get_time()//1000
    second = fullTime % 60
    minute = divmod(fullTime, 60)[0]
    music.set('{0:02d}:{1:02d}:{2:02d}'.format(0, minute, second))
    musicName.after(int(1000//float(rate.get())), timerStart)


# ! =========================End Definations=========================

# ? =========================Objects On Window=========================
botFrame = Frame(mainWindow, bg='#A1C3D1', height=30)
Play = Button(botFrame, image=photoimage, width=25, fg=fontColor,
              height=27, bd=1, bg=btnColor, font=myFont, command=Play_def)
Pause = Button(botFrame, image=photoimage2, width=25, fg=fontColor,
               height=27, bd=1, bg=btnColor, font=myFont, command=Pause_def)
Repeat = Button(botFrame, image=photoimage7, width=25, fg=fontColor,
                height=27, bd=1, bg=btnColor, font=myFont, command=Repeat_def)
Next = Button(botFrame, image=photoimage4, width=25, height=27, fg=fontColor,
              bd=1, bg=btnColor, font=myFont, command=next_def)
previous = Button(botFrame, image=photoimage3, font=myFont, width=25, height=27, fg=fontColor,
                  bd=1, bg=btnColor, command=previous_def)
musicName = Label(mainWindow, textvariable=music, bg=rootColor,
                  fg=fontColor, font=font.Font(weight="bold", size=12), wraplength=80)

openf = Button(botFrame, text='open Files', width=28, bg=btnColor, fg=fontColor,
               height=1, command=openFiles, bd=1, font=myFont)

listbox = Listbox(mainWindow, width=21, height=10,
                  bg=secondaryColor, bd=0, fg=fontColor, selectbackground=fontColor, selectforeground='#fff')
listbox.bind("<<ListboxSelect>>", play_select)
forwardBtn = Button(botFrame, image=photoimage6, width=25, height=27, bd=1,
                    bg=btnColor, fg=fontColor, font=myFont, command=forward_to)
backwardBtn = Button(botFrame, image=photoimage5, width=25, bd=1,
                     bg=btnColor, fg=fontColor, height=27, font=myFont, command=backward_to)
speedLabel = Label(mainWindow, text='Speed', fg=fontColor,
                   bg=rootColor, font=myFont)
jumpLabel = Label(mainWindow, text='Lunge', fg=fontColor,
                  bg=rootColor, font=myFont)
Play.place(x=0, y=0)
Pause.place(x=30, y=0)
botFrame.pack(fill=BOTH, side=BOTTOM)
Next.place(x=90, y=0)
previous.place(x=60, y=0)
musicName.place(x=150, y=70)
openf.place(x=213, y=3)
listbox.place(x=318, y=5)
forwardBtn.place(x=150, y=0)
Repeat.place(x=180, y=0)
backwardBtn.place(x=120, y=0)
speedLabel.place(x=0, y=5)
jumpLabel.place(x=55, y=5)
# region ComboBox
rate = Combobox(mainWindow, width=4, state='readonly')
rate['values'] = (0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2)
rate.current(3)
rate.bind("<<ComboboxSelected>>", set_rate)
rate.place(x=3, y=25)
lunge = Combobox(mainWindow, width=4, state='readonly')
lunge['values'] = (5, 10, 15, 20, 30)
lunge.current(2)
lunge.place(x=55, y=25)
# endregion ComboBox
mainWindow.mainloop()
