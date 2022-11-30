import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.backends.backend_tkagg as tkagg
import numpy as np
import pandas as pd
import os
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk


#Setting up plot style and pandas warning:
plt.style.use('ggplot')
pd.options.mode.chained_assignment = None

class AE_GUI(tk.Tk):

    def __init__(self):
        super().__init__()

        # Setting Default File options
        self.default_file_option = tk.StringVar()  # current subject
        self.default_file_option.set('')
        self.file_options = ['']

        self.curr_csv = None
        self.curr_ecg_time = None
        self.curr_ecg = None
        self.curr_peak = None

        #Setting up how to close application and setting up User Interface
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setup_UI()

    def setup_UI(self):
        self.title('HRV_app')

        # Adding attibutes to enable full screen:
        self.attributes('-fullscreen', False)
        self.fullScreenState = False
        self.bind('<F11>', self.toggleFullScreen)
        self.bind('<Escape>', self.quitFullScreen)

        # Defining Minimum Size of window to display screen width and height:
        self.minsize(int(self.winfo_screenwidth()/2),
                     int(self.winfo_screenheight()/2))

        # Defining Dropdown menu:
        self.menubar = tk.Menu(self)

        # Dropdown Menu for File:
        self.dropdown_file = tk.OptionMenu(
            self.menubar,
            self.default_file_option,
            *self.file_options
        )

        # Getting height and width of our DISPLAY:
        HEIGHT = self.winfo_screenheight()
        WIDTH = self.winfo_screenwidth()

        # Creating cavas to place all our widgets:
        self.canvas = tk.Canvas(self,
                                height=HEIGHT,
                                width=WIDTH,
                                bg='#999999')
        self.canvas.pack()


        #Dropdown menu:
        self.menubar = tk.Menu(self)
        self.dropdown_file = tk.Menu(self.menubar)
        self.dropdown_file.add_command(label='Select CSV',state=tk.NORMAL,command=self.upload_csv)
        self.dropdown_file.add_command(label='Quit',command=self.on_closing)
        self.menubar.add_cascade(label='File',menu=self.dropdown_file)
        self.config(menu=self.menubar)

        #Subject Label
        self.label_file = tk.Label(
            self,
            text='ECG File',
            font=('helvetica',12,'bold'),
            bd=2,bg='#d9d9d9'
        )
        self.label_file.place(
            relx=0.225, rely=0.915,
            relwidth=0.35,
            relheight=0.02
        )

        #Dropmenu for files:
        # self.dropmenu_file = tk.OptionMenu(
        #     self,self.default_file_option,
        #     *self.file_options)
        # self.dropmenu_file.place(
        #     relx=0.225, rely=0.94,
        #     relwidth=0.265,
        #     relheight=0.05
        # )

        self.dropmenu_file = ttk.Combobox(
            self,
            textvariable=self.default_file_option,
            font=('helvetica', 12, 'bold')
        )
        self.dropmenu_file.place(
            relx=0.225, rely=0.94,
            relwidth=0.265,
            relheight=0.05
        )
        self.dropmenu_file['state'] = 'readonly'

        self.button_plot = tk.Button(
            self,
            text='Plot',
            font=('helvetica', 12, 'bold'),
            state=tk.DISABLED,
            command=self.plot
        )
        self.button_plot.place(
            relx=0.495, rely=0.94,
            relwidth=0.08,
            relheight=0.05
        )

        # Saving Button
        self.label_save = tk.Label(
            self,
            text='Save and History',
            font=('helvetica', 12, 'bold'),
            bd=2, bg='#d9d9d9'
        )
        self.label_save.place(
            relx=0.585, rely=0.915,
            relwidth=0.405,
            relheight=0.02
        )

        self.button_save = tk.Button(
            self,
            text='Save',
            font=('helvetica', 12, 'bold'),
            state=tk.DISABLED,
            command=self.save_data
        )
        self.button_save.place(
            relx=0.585, rely=0.94,
            relwidth=0.105,
            relheight=0.05
        )

        #History Label:
        self.label_history = tk.Label(
            self,
            text = '',
            anchor='center',
            font = ('helvetica', 12, 'bold')
        )
        self.label_history.place(
            relx=0.70,rely=0.94,
            relwidth=0.29,
            relheight=0.05
        )

        #ECG figure
        self.fig_ecg,self.ax_ecg = plt.subplots(
            1,dpi=200,constrained_layout=True
        )
        self.ax_ecg.set_xticklabels([])
        self.ax_ecg.set_yticklabels([])
        self.ax_ecg.set_ylabel('ECG', fontsize=7)
        self.ecg_plot = self.ax_ecg.plot(picker=5)

        # Plot Widgets:
        self.canvas_plot = FigureCanvasTkAgg(self.fig_ecg, master=self.canvas)
        self.canvas_plot.get_tk_widget().place(
            relx=0.01, rely=0.01,
            relwidth=0.98,relheight=0.90)
        self.canvas_plot.mpl_connect('pick_event',self.onpick)

        self.label_toolbar = tk.Label(
            self,
            text='Plot Controls',
            font=('helvetica', 12, 'bold'),
            bd=2, bg='#d9d9d9'
        )
        self.label_toolbar.place(
            relx=0.01, rely=0.915,
            relwidth=0.205,#0.265
            relheight=0.02
        )

        self.toolbar = tkagg.NavigationToolbar2Tk(
            self.canvas_plot, self, pack_toolbar=False
        )
        self.toolbar.update()
        self.toolbar.place(
            relx=0.01, rely=0.94,
            relwidth=0.205,
            relheight=0.05
        )

    def quitFullScreen(self,event):
        #Function to quit full screen by pressing ESC
        self.fullScreenState = False
        self.attributes('-fullscreen',self.fullScreenState)

    def toggleFullScreen(self,event):
        #Function to toggle fullscreen by pressing F11
        self.fullScreenState = not self.fullScreenState
        self.attributes('-fullscreen',self.fullScreenState)

    def on_closing(self):
        self.quit()
        self.destroy()

    def upload_csv(self):
        #Function to load CSV(s)

        #Getting directory where ecg is located:
        self.dir_csv = filedialog.askdirectory()

        if not(os.path.isdir(self.dir_csv)):
            self.label_history.config(
                text="' %s ' does not exist! \nPlease select another directory where your ECG data is"%(self.dir_csv)
            )
            self.label_history.update()
            return

        #File names of ECG CSVs
        self.fileNames_csv = [
            os.path.splitext(f)[0] for f in os.listdir(self.dir_csv)
            if os.path.splitext(f)[1] in ['.csv']
        ]

        #File Paths of ECG CSVs
        self.filePaths_csv = [
            os.path.join(self.dir_csv,f) for f in os.listdir(self.dir_csv)
            if os.path.splitext(f)[1] in ['.csv']
        ]

        #Dictionary where ECG is stored
        self.ecg = {}

        self.label_history.config(text='Loading ECG data...')
        self.label_history.update()

        # self.dropmenu_file['menu'].delete(0, 'end')

        #Storing ECG data:
        for n,p in zip(self.fileNames_csv,self.filePaths_csv):
            self.ecg[n] = {}
            self.ecg[n]['path'] = p
            self.ecg[n]['ecg'] = pd.read_csv(p)

            # self.dropmenu_file['menu'].add_command(label=n,command=tk._setit(self.default_file_option,n))
            # self.default_file_option.set(self.fileNames_csv[0])

        self.dropmenu_file['values'] = self.fileNames_csv
        self.default_file_option.set(self.fileNames_csv[0])
        self.dropmenu_file.set(self.fileNames_csv[0])

        self.label_history.config(text='Loaded ECG data!')
        self.label_history.update()

        self.button_plot['state'] = tk.NORMAL
        self.button_save['state'] = tk.NORMAL

    def plot(self):

        #Function to plot data
        self.ax_ecg.clear()
        self.ax_ecg.set_ylabel('ECG',fontsize=12)
        self.ax_ecg.set_xlabel('Time (s)',fontsize=12)

        file_csv = self.default_file_option.get()

        if self.curr_csv is None:
            self.curr_csv = file_csv
            self.curr_ecg_time = self.ecg[file_csv]['ecg']['time_stamp']
            self.curr_ecg = self.ecg[file_csv]['ecg']['clean_ecg']
            self.curr_peak = self.ecg[file_csv]['ecg']['peaks']

        else:
            if self.curr_csv != file_csv:
                self.curr_csv = file_csv
                self.curr_ecg_time = self.ecg[file_csv]['ecg']['time_stamp']
                self.curr_ecg = self.ecg[file_csv]['ecg']['clean_ecg']
                self.curr_peak = self.ecg[file_csv]['ecg']['peaks']

        self.ecg_plot = self.ax_ecg.plot(
            self.curr_ecg_time,self.curr_ecg,
            'k-o',
            markersize=2,linewidth=1,
            picker=5
        )
        self.peaks_plot = self.ax_ecg.plot(
            self.curr_ecg_time[self.curr_peak],self.curr_ecg[self.curr_peak],
            ms=10,marker=matplotlib.markers.CARETDOWN,
            color='r',linestyle='None'
        )


        self.canvas_plot.draw()
        self.update()

        self.label_history.config(text="Plotted ' %s ' ECG"%self.curr_csv)
        self.label_history.update()


    def onpick(self, event):

        if event.artist == self.ecg_plot[0]:
            xdata = event.artist.get_xdata()
            ydata = event.artist.get_ydata()
            ind = event.ind
            points = tuple(zip(xdata[ind], ydata[ind]))

            if not(self.curr_csv is None):

                bool_index = (self.curr_ecg_time == points[0][0]).values

                bool_index = np.where(bool_index == True)[0]

                if self.curr_peak[bool_index].values == True:
                    self.curr_peak[bool_index] = False

                else:
                    self.curr_peak[bool_index] = True

                self.peaks_plot[0].set_xdata(
                    self.curr_ecg_time[self.curr_peak]
                )
                self.peaks_plot[0].set_ydata(
                    self.curr_ecg[self.curr_peak]
                )
                self.canvas_plot.draw()
                self.canvas_plot.flush_events()
                self.update()

    def save_data(self):
        #Function to save data
        self.label_history.config(text='Saving %s ECG Data...'%self.curr_csv)
        self.label_history.update()

        save_path = self.ecg[self.curr_csv]['path']

        self.ecg[self.curr_csv]['ecg']['peaks'] = self.curr_peak

        self.ecg[self.curr_csv]['ecg'].to_csv(save_path,index=False)

        self.label_history.config(text='Saved %s ECG Data!' % self.curr_csv)
        self.label_history.update()


            # Getting Subject and Stimulation
            # sub = self.default_sub_option.get()
            # stim = self.default_stim_option.get()
            #
            # if (self.plot_type == 'clean') and not (self.data[sub][stim].peaks is None):
            #     bool_index = (self.data[sub][stim].clean_ecg.ecg_timestamp == points[0][0]).values
            #     bool_index = np.where(bool_index == True)[0]
            #
            #     if self.data[sub][stim].peaks[bool_index] == True:
            #         self.data[sub][stim].peaks[bool_index] = False
            #     else:
            #         self.data[sub][stim].peaks[bool_index] = True
            #
            #     self.data[sub][stim].plot_clean_data()



#Creating GUI class to start and initialize main loop:
root = AE_GUI()
root.update()
root.mainloop()