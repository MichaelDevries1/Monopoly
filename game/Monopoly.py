import tkinter as tk
from tkinter import ttk


class DEVWINDOW(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.windowWidth = 300
        self.windowHeight = 500
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        self.winlocationleft = 7 * (self.screenWidth / 10) - (self.windowWidth / 10)
        self.winlocationtop = (self.screenHeight / 3) - (self.windowHeight / 3)

        self.title('Dev Options')
        self.geometry('%dx%d+%d+%d' % (self.windowWidth,
                                       self.windowHeight,
                                       self.winlocationleft,
                                       self.winlocationtop))
        self.dice1lable = ttk.Label(self, text='Set Dice 1 Value').grid(row=0, column=0)
        self.dice1val = int()
        self.dice1Entry = ttk.Entry(self, textvariable=self.dice1val).grid(row=0, column=1, columnspan=2)
        ttk.Button(self, text='Close', command=self.destroy).grid(row=1, column=2)


class MONOPOLY(tk.Tk):
    def __init__(self):
        super().__init__()

        self.windowWidth = 500
        self.windowHeight = 500
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()

        self.winlocationleft = (self.screenwidth / 10) - (self.windowWidth / 10)
        self.winlocationtop = (self.screenheight / 3) - (self.windowHeight / 3)

        self.title('Monopoly')
        self.geometry('%dx%d+%d+%d' % (self.windowWidth,
                                       self.windowHeight,
                                       self.winlocationleft,
                                       self.winlocationtop))

        ttk.Button(self, text='Open Dev window', command=self.open_dev_window()).pack(expand=True)

    def dice1test(self, devWindow):
        dice1value = devWindow.get()
        self.dice1 = ttk.Label(self, text=str(dice1value))

    def open_dev_window(self):
        devWindow = tk.Toplevel()
        devWindow.title('Dev Options')
        devWindow.windowWidth = 300
        devWindow.windowHeight = 500
        devWindow.screenWidth = self.winfo_screenwidth()
        devWindow.screenHeight = self.winfo_screenheight()

        devWindow.winlocationleft = 7 * (devWindow.screenWidth / 10) - (devWindow.windowWidth / 10)
        devWindow.winlocationtop = (devWindow.screenHeight / 3) - (devWindow.windowHeight / 3)

        devWindow.geometry('%dx%d+%d+%d' % (devWindow.windowWidth,
                                            devWindow.windowHeight,
                                            devWindow.winlocationleft,
                                            devWindow.winlocationtop))
        devWindow.dice1lable = ttk.Label(devWindow, text='Set Dice 1 Value').grid(row=0, column=0)
        devWindow.dice1val = int()
        devWindow.dice1Entry = ttk.Entry(devWindow, textvariable=devWindow.dice1val).grid(row=0, column=1, columnspan=2)
        ttk.Button(devWindow, text='Close', command=devWindow.destroy).grid(row=1, column=2)


if __name__ == '__main__':
    root = MONOPOLY()
    root.mainloop()
