import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np

def check(element):

    if (element.isdigit() or element.lstrip("-").isdigit()): return 1
    if (element.isspace() or element == ''): return 2
    if (element.isalpha()): return 3

    partition = element.partition('.')

    if (partition[0].isdigit() and partition[1] == '.' and partition[2].isdigit()) or (
            partition[0] == '' and partition[1] == '.' and partition[2].isdigit()) or (
            partition[0].isdigit() and partition[1] == '.' and partition[2] == ''):
        return 1

def checkValues(values):

    if(int(values["-INPUT-"])!=1 and check(values[7])!=1):
        window['-S_Text-'].update('Wybierając sygnał prostokątny lub sinusoidę należy wprowadzić częstotliwość!')
        return False

    elif (check(values[1]) == 2 or check(values[2]) == 2 or check(values[3]) == 2 or check(values[4]) == 2 or check(values[5]) == 2 or check(values[6]) == 2):
        window['-S_Text-'].update('Pola tekstowe nie mogą być puste!')
        return False

    elif (check(values[1]) == 3 or check(values[2]) == 3 or check(values[3]) == 3 or check(values[4]) == 3 or check(values[5]) == 3 or check(values[6]) == 3 or check(values[7]) == 3):
        window['-S_Text-'].update('W polach tekstowych nie może znajdować się tekst!')
        return False

    elif(check(values[1])==1 and check(values[2])==1 and check(values[3])==1 and check(values[4])==1 and check(values[5])==1 and check(values[6])==1):
        Stablinosc(float(values[1]), float(values[2]), float(values[3]), float(values[4]), float(values[5]))
        return True


def drawGraph(t_x, y, u):
    plt.clf()
    plt.subplot(1, 2, 1)
    plt.plot(t_x, y)
    plt.title("Sygnał wyjściowy y(t)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    plt.subplot(1, 2, 2)
    plt.plot(t_x, u)
    plt.title("Pobudzenie u(t)")
    plt.xlabel("Czas [s]")
    plt.ylabel("Amplituda")
    plt.tight_layout(pad=2.0)
    plt.show()



def Obliczanie(k1, k2, t0, t1, t2, t, F, Skok, Sinusoida, Prostokatny):

    y = []
    X1 = 0
    X2 = 0
    X3 = 0
    dt = 0.001

    A = [[0, 1, 0],
        [0, 0, 1],
        [-(k1 * k2) / (t0 * t2), -(t1 * k1 * k2 + 1) / (t0 * t2), -(t0 + t2) / (t0 * t2)]]

    B = [0, 0, 1]

    C = [(k1 * k2) / (t0 * t2), (t1 * k1 * k2) / (t0 * t2), 0]

    u=[]

    t_x = []
    for i in range(int(t/dt)):
        t_x.append(i*dt)

    if(Skok==1):
          u = np.ones(len(t_x))
          u[0]=0

    if(Prostokatny==1):
        for i in range(len(t_x)):
            u.append(np.sign(np.sin(F*np.pi*2*i*dt)))

    if(Sinusoida==1):
        for i in range(len(t_x)):
            u.append(np.sin(F*np.pi*2*i*dt))

    for k in range(len(t_x)):
        XD1 = X2
        XD2 = X3
        XD3 = (A[2][0] * X1 + A[2][1] * X2 + A[2][2] * X3 + u[k])
        y.append(X1 * C[0] + X2 * C[1])

        X1 += XD1 * dt
        X2 += XD2 * dt
        X3 += XD3 * dt

    drawGraph(t_x, y, u)


def Stablinosc(k1,k2,t0,t1,t2):
    if(t0*t2>0 and t0+t2>0 and k1*k2*t1+1 > 0 and k1*k2>0 and k1*k2*(t0*t1+t1*t2-t0*t2)+t0+t2>0):
        window['-S_Text-'].update('Uklad Stabilny')
    else:
        window['-S_Text-'].update('Uklad Niestabilny')

layout = [
    [sg.Image('uklad.png')],
    [sg.Text("k1=", key="-W_K1-"),sg.InputText()],
    [sg.Text("k2="), sg.InputText()],
    [sg.Text("t0="), sg.InputText()],
    [sg.Text("t1="), sg.InputText()],
    [sg.Text("t2="), sg.InputText()],
    [sg.Text("Czas Symulacji T[s]="), sg.InputText()],
    [sg.Text("Częstotliwość [Hz]="), sg.InputText()],
    [sg.T("Dodatkowe uwagi: "), sg.Text("",key='-S_Text-')],
    [sg.T(" "), sg.Radio('Skok jednostkowy', "RADIO1", default=True, key="-INPUT-")],
    [sg.T(" "), sg.Radio('Sinusoida', "RADIO1", default=False, key="-INPUT2-")],
    [sg.T(" "), sg.Radio('Prostokatny', "RADIO1", default=False, key="-INPUT3-")],
    [sg.Button("Oblicz")]
]

window = sg.Window("Projekt", layout, margins=(100, 50))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break
    if event == "Oblicz":
        if(checkValues(values)):
            if (values["-INPUT-"]):
                values[7]=0;
            Obliczanie(float(values[1]), float(values[2]), float(values[3]), float(values[4]), float(values[5]), float(values[6]), float(values[7]), int(values["-INPUT-"]), int(values["-INPUT2-"]),int(values["-INPUT3-"]))

window.close()