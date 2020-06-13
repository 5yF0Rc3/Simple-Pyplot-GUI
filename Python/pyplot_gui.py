# Import
import tkinter as tk 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import webbrowser
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyBboxPatch


#Dok: https://web.archive.org/web/20190511024508/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/button.html
# Dok for Vertical Legend and Markers: LaTex
# https://matplotlib.org/1.3.1/users/usetex.html?highlight=latex
# https://stackoverflow.com/questions/32012120/matplotlib-legend-vertical-rotation
# https://stackoverflow.com/questions/38002700/rotating-legend-or-adding-patch-to-axis-label-in-matplotlib


#To Do:
# Legend on/off
# host plot, only left possible
# symbols in labename? CB
# symbol in label size, bigger
# y label without spine and ticks


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        # -------------------------------
        # Create a new MainFrame
        self.menue_top = tk.Frame(root, width=700,height=300)
        self.menue_top.grid(row=0, column=0, sticky="nsew")
        self.menue_top.pack(side = "top", pady = 30, padx = 30)
        # Configure Column "3,9", min. size 
        self.menue_top.columnconfigure(3,minsize=10, weight = 1)
        self.menue_top.columnconfigure(9,minsize=30, weight = 1) 
        self.menue_top.columnconfigure(11,minsize=30) 
        self.menue_top.rowconfigure(0) #grid setting
        # -------------------------------
        # Create a new Frame, Bottom
        self.menue_bottom = tk.Frame(root, width=700,height=300)
#        self.menue_bottom.grid(row=0, column=0, sticky="nsew")
        self.menue_bottom.pack(side = "bottom")
        # -------------------------------
        # Create a new Frame, Right, inside Menue_top
        self.menue_option = tk.LabelFrame(self.menue_top, text="Option",pady = 4, padx = 4,)
#        self.menue_bottom.grid(row=0, column=0, sticky="nsew")
        self.menue_option.grid( row = 0, column = 13,rowspan=6, columnspan=2, sticky="n")
        # -------------------------------
        # Create a new Frame, data, inside Menue_top
        self.menue_func = tk.LabelFrame(self.menue_top, text="Data",pady = 4, padx = 4,)
#        self.menue_bottom.grid(row=0, column=0, sticky="nsew")
        self.menue_func.grid( row = 0, column = 8,rowspan=2, columnspan=3, sticky="n")
        # -------------------------------
        # Load variables and create all widgets
        self.load_variables()
        self.create_widgets()
        self.updater()



    def load_variables(self):

        self.data_dict = {"Kein Eintrag": 0}
        
        self.choosemarker = ['o', '.', 'x', '+', 'v', '^', '<', '>', 's', 'd']
        self.chooseline = [' ', 'solid', 'dashed', 'dashdot', 'dotted']
        self.choosecolor = ["black","green","blue","cyan","yellow","red","magenta"]
        self.chooseside = ["right","left"]

        # -------------------------------
        self.list_del_button = []
        # INPUT LISTS
        # List are 2-D, [i][0]: dropvar, [i][1]: dropmenu
        self.list_datax = []
        self.list_datay = []
        self.list_name = []
        self.list_marker = []
        self.list_line = []
        self.list_color = []
        self.list_side = []
        self.list_newaxis = []
        self.list_ylabel = []
        self.list_xlabel = []
        self.list_data_top = []
        self.list_hide_tick = []
        # -------------------------------
        self.plot_grid_bool = tk.IntVar()
        self.colorize_label_bool = tk.IntVar()
        self.legend_bool = tk.IntVar()
        self.var_y_dist = tk.DoubleVar()
        self.var_y_dist.set(0.08)
        self.var_m_size = tk.DoubleVar()
        self.var_m_size.set(5)
        self.var_fontsize = tk.DoubleVar()
        self.var_fontsize.set(12)
        # -------------------------------
        self.free_to_save = False
        self.rowcount = 8





    def create_widgets(self):
        print("create_widget")
        # Column label description
        # Top Buttons
        self.button_load_file = tk.Button(self.menue_func, text="Load .CSV File",
                                  command=self.load_file).grid(
                                  row = 0, column = 0,columnspan=1, sticky="we")
        self.button_new_Data = tk.Button(self.menue_func, text="New Data row",
                                  command=self.add_line).grid(
                                  row = 1, column = 0,columnspan=1, sticky="we")
        self.generate = tk.Button(self.menue_func, text="Generate Plot", fg="red",
                              command=self.gen_builder).grid(
                              row = 0, column = 1, rowspan=2, columnspan=1, sticky="nswe")
        self.save = tk.Button(self.menue_func, text="Save Plot",
                              command=self.save_fig).grid(
                              row = 0, column = 2, rowspan=2, columnspan=1, sticky="nswe")
        self.label_help = tk.Label(self.menue_top, text="Help / Bugs", fg="blue", cursor="hand2")
        self.label_help.grid(row = 0, column = 1, sticky="n")
        self.label_help.bind("<Button-1>", lambda e: self.callback("https://github.com/5yF0Rc3/Simple-Pyplot-GUI"))
        # -------------------------------
        # Options
        self.label_grid = tk.Label(self.menue_option, text="Plot Grid").grid(
                                   row = 0, column = 1, sticky="w")
        self.plot_grid = tk.Checkbutton(self.menue_option, variable=self.plot_grid_bool).grid(
                                   row = 0, column = 0, sticky="w")
        self.label_colorize_label = tk.Label(self.menue_option, text="Colorize Label").grid(
                                   row = 1, column = 1, sticky="w")
        self.colorize_label = tk.Checkbutton(self.menue_option, variable=self.colorize_label_bool).grid(
                                   row = 1, column = 0, sticky="w")
        self.label_show_legend = tk.Label(self.menue_option, text="Show Legend").grid(
                                   row = 2, column = 1, sticky="w")
        self.show_legend = tk.Checkbutton(self.menue_option, variable=self.legend_bool).grid(
                                   row = 2, column = 0, sticky="w")
        self.label_y_dist = tk.Label(self.menue_option, text="Distance of Y-axis").grid(
                                   row = 3, column = 1, sticky="n")
        self.y_dist = tk.Entry(self.menue_option,  textvariable=self.var_y_dist, width= 5).grid(
                                   row = 3, column = 0, sticky="w")
        self.label_msize = tk.Label(self.menue_option, text="Marker size").grid(
                                   row = 4, column = 1, sticky="n")
        self.m_size = tk.Entry(self.menue_option,  textvariable=self.var_m_size, width= 5).grid(
                                   row = 4, column = 0, sticky="w")
        self.label_font_size = tk.Label(self.menue_option, text="Font size").grid(
                                   row = 5, column = 1, sticky="n")
        self.font_size = tk.Entry(self.menue_option,  textvariable=self.var_fontsize, width= 5).grid(
                                   row = 5, column = 0, sticky="w")

        # -------------------------------
        self.label_hauptplot = tk.Label(self.menue_top, text="Mainplot", bg="#c3cade", width=23).grid(
                                   row = 1, column = 1, columnspan=9, sticky="n")
        # -------------------------------
        self.label_datax = tk.Label(self.menue_top, text="Data x",).grid(
                                   row = 2, column = 1, sticky="n")
        self.label_datay = tk.Label(self.menue_top, text="Data Y",).grid(
                                   row = 2, column = 2, sticky="n")
        self.label_name = tk.Label(self.menue_top, text="Name",).grid(
                                   row = 2, column = 3, sticky="n")
        self.label_marker = tk.Label(self.menue_top, text="Marker",).grid(
                                   row = 2, column = 4, sticky="n")
        self.label_line = tk.Label(self.menue_top, text="Linetyp",).grid(
                                   row = 2, column = 5, sticky="n")
        self.label_color = tk.Label(self.menue_top, text="Color",).grid(
                                   row = 2, column = 6, sticky="n")
        self.label_side = tk.Label(self.menue_top, text="Side",).grid(
                                   row = 2, column = 7, sticky="n")
        self.label_max_top = tk.Label(self.menue_top, text="Y-Axis limit",).grid(
                                   row = 2, column = 8, sticky="n")  
        #self.label_cb = tk.Label(self.menue_top, text="Side",).grid(
        #                           row = 2, column = 9, sticky="n")
        self.label_ylabel = tk.Label(self.menue_top, text="Axis Y-Label",).grid(
                                   row = 2, column = 10, sticky="n")
        self.label_xlabel = tk.Label(self.menue_top, text="Axis X-Label",).grid(
                                   row = 2, column = 11, sticky="n")
        # -------------------------------
        self.label_hauptplot = tk.Label(self.menue_top, text="Additional Data", bg="#c3cade", width=23).grid(
                                   row = 6, column = 1, columnspan=9, sticky="n")
        # -------------------------------
        self.a_label_datax = tk.Label(self.menue_top, text="Data x",).grid(
                                  row = 7, column = 1, sticky="n")
        self.a_label_datay = tk.Label(self.menue_top, text="Data Y",).grid(
                                  row = 7, column = 2, sticky="n")
        self.a_label_name = tk.Label(self.menue_top, text="Name",).grid(
                                  row = 7, column = 3, sticky="n")
        self.a_label_marker = tk.Label(self.menue_top, text="Marker",).grid(
                                  row = 7, column = 4, sticky="n")
        self.a_label_line = tk.Label(self.menue_top, text="Linetyp",).grid(
                                  row = 7, column = 5, sticky="n")
        self.a_label_color = tk.Label(self.menue_top, text="Color",).grid(
                                  row = 7, column = 6, sticky="n")
        self.a_label_side = tk.Label(self.menue_top, text="Side",).grid(
                                  row = 7, column = 7, sticky="n")
        self.label_max_top = tk.Label(self.menue_top, text="Y-Axis limit",).grid(
                                   row = 7, column = 8, sticky="n")
        self.a_label_cb = tk.Label(self.menue_top, text="New Y-Axis",).grid(
                                  row = 7, column = 9, sticky="n")
        self.a_label_ylabel = tk.Label(self.menue_top, text="Axis Y-Label",).grid(
                                  row = 7, column = 10, sticky="n")
        self.a_label_hideticks = tk.Label(self.menue_top, text="Hide Ticks",).grid(
                                  row = 7, column = 12, sticky="n")

        # -------------------------------
        # For list entry only !!!!
        self.list_del_button.append(tk.Button(self.menue_top, text="X", fg="red"))
        # - -
        # ACHTUNG REDUDANT IN UPDATE_DROPDOWN !!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.list_datax.append([])
        self.list_datax[0].append(tk.StringVar())
        try:
            self.list_datax[0][0].set(list(self.data_dict.keys())[0])
        except:
            self.list_datax[0][0].set("Kein Eintrag")
        self.list_datax[0].append(tk.OptionMenu(self.menue_top, self.list_datax[0][0],
                                                     *self.data_dict.keys(),
                                                     command=(lambda _, row=0: self.change_axis_x_name(row))))
        self.list_datax[0][1].config(width=10)
        self.list_datax[0][1].grid(row = 4, column = 1, sticky="n")
        # ACHTUNG REDUDANT IN UPDATE_DROPDOWN !!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.list_datay.append([])
        self.list_datay[0].append(tk.StringVar())
        try:
            self.list_datay[0][0].set(list(self.data_dict.keys())[0])
        except:
            self.list_datay[0][0].set("Kein Eintrag")
        self.list_datay[0].append(tk.OptionMenu(self.menue_top, self.list_datay[0][0],
                                                     *self.data_dict.keys(),
                                                     command=(lambda _, row=0: self.change_axis_y_name(row))))
        self.list_datay[0][1].config(width=10)
        self.list_datay[0][1].grid(row = 4, column = 2, sticky="n")
        # -
        self.list_name.append([])
        self.list_name[0].append(tk.StringVar())
        self.list_name[0].append(tk.Entry(self.menue_top, textvariable=self.list_name[0][0]))
        self.list_name[0][1].grid(row = 4, column = 3, sticky="n")
        # -
        self.list_marker.append([])
        self.list_marker[0].append(tk.StringVar())
        try:
            self.list_marker[0][0].set(self.choosemarker[0])
        except:
            self.list_marker[0][0].set("Kein Eintrag")
        self.list_marker[0].append(tk.OptionMenu(self.menue_top, self.list_marker[0][0],
                                                     *self.choosemarker))
        self.list_marker[0][1].config(width=2)
        self.list_marker[0][1].grid(row = 4, column = 4, sticky="n")
        # -
        self.list_line.append([])
        self.list_line[0].append(tk.StringVar())
        try:
            self.list_line[0][0].set(self.chooseline[0])
        except:
            self.list_line[0][0].set("Kein Eintrag")
        self.list_line[0].append(tk.OptionMenu(self.menue_top, self.list_line[0][0],
                                                     *self.chooseline))
        self.list_line[0][1].config(width=2)
        self.list_line[0][1].grid(row = 4, column = 5, sticky="n")
        # -
        self.list_color.append([])
        self.list_color[0].append(tk.StringVar())
        try:
            self.list_color[0][0].set(self.choosecolor[0])
        except:
            self.list_color[0][0].set("Kein Eintrag")
        self.list_color[0].append(tk.OptionMenu(self.menue_top, self.list_color[0][0],
                                                     *self.choosecolor))
        self.list_color[0][1].config(width=6)
        self.list_color[0][1].grid(row = 4, column = 6, sticky="n")
        # -
        self.list_side.append([])
        self.list_side[0].append(tk.StringVar())
        try:
            self.list_side[0][0].set(self.chooseside[1])
        except:
            self.list_side[0][0].set("Kein Eintrag")
        self.list_side[0].append(tk.OptionMenu(self.menue_top, self.list_side[0][0],
                                                     self.chooseside[1]))
        self.list_side[0][1].config(width=6)
        self.list_side[0][1].grid(row = 4, column = 7, sticky="n")
        # -
        self.list_data_top.append([])
        self.list_data_top[0].append(tk.StringVar())
        self.list_data_top[0][0].set("auto")
        self.list_data_top[0].append(tk.Entry(self.menue_top, textvariable=self.list_data_top[0][0], width= 5))
        self.list_data_top[0][1].grid(row = 4, column = 8, sticky="n")
        # -
        self.list_newaxis.append([])
        self.list_newaxis[0].append(tk.IntVar())
        self.list_newaxis[0][0].set(0)
        self.list_newaxis[0].append(tk.Checkbutton(self.menue_top, variable=self.list_newaxis[0][0],
                                                       command=lambda row=0: self.visible_change(row))) #command für ein/ausblenden Label 
        #self.list_newaxis[0][1].grid(row = 4, column = 9, sticky="n")
        # -
        self.list_ylabel.append([])
        self.list_ylabel[0].append(tk.StringVar())
        self.list_ylabel[0].append(tk.Entry(self.menue_top, textvariable=self.list_ylabel[0][0]))
        self.list_ylabel[0][1].grid(row = 4, column = 10, sticky="n")
        # -
        self.list_xlabel.append([])
        self.list_xlabel[0].append(tk.StringVar())
        self.list_xlabel[0].append(tk.Entry(self.menue_top, textvariable=self.list_xlabel[0][0]))
        self.list_xlabel[0][1].grid(row = 4, column = 11, sticky="n")
        # -
        self.list_hide_tick.append([])
        self.list_hide_tick[0].append(tk.IntVar())
        self.list_hide_tick[0][0].set(0)
        self.list_hide_tick[0].append(tk.Checkbutton(self.menue_top, variable=self.list_hide_tick[0][0]))
        #self.list_hide_tick[0][1].grid(row = self.rowcount, column = 12, sticky="n")

        # -------------------------------
        # First initial row
        self.add_line()
        # -------------------------------

        

    def updater(self):
        # updates the text Labels
#        print("updater")

        root.after(500, self.updater)


    def update_dropdown(self):
        # Creates the same Dropdowns again for the data_dict, DANGER - redudant!
        #!!!!!!!!!!!!!!!!!!!!!! ACHTUNG !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        try:
            self.list_datax[0][0].set(list(self.data_dict.keys())[0])
        except:
            self.list_datax[0][0].set("Kein Eintrag")
        self.list_datax[0][1] = tk.OptionMenu(self.menue_top, self.list_datax[0][0],
                                                     *self.data_dict.keys(),
                                                     command=(lambda _, row=0: self.change_axis_x_name(row)))
        self.list_datax[0][1].config(width=10)
        self.list_datax[0][1].grid(row = 4, column = 1, sticky="n")
        # -
        try:
            self.list_datay[0][0].set(list(self.data_dict.keys())[0])
        except:
            self.list_datay[0][0].set("Kein Eintrag")
        self.list_datay[0][1] = tk.OptionMenu(self.menue_top, self.list_datay[0][0],
                                                     *self.data_dict.keys(),
                                                     command=(lambda _, row=0: self.change_axis_y_name(row)))
        self.list_datay[0][1].config(width=10)
        self.list_datay[0][1].grid(row = 4, column = 2, sticky="n")
        # -
        for i in range(1, len(self.list_datay)):
            if self.list_datay[i][0].get() != "__XX__XX__":
                try:
                    self.list_datay[i][0].set(list(self.data_dict.keys())[0])
                except:
                    self.list_datay[i][0].set("Kein Eintrag")
                self.list_datay[i][1].grid_forget()
                self.list_datay[i][1] = tk.OptionMenu(self.menue_top, self.list_datay[i][0],
                                                         *self.data_dict.keys(),
                                                         command=(lambda _, row=i: self.change_axis_y_name(row)))
                self.list_datay[i][1].config(width=10)
                self.list_datay[i][1].grid(row = i + 7, column = 2, sticky="n")





    def add_line(self):
        #effective position of rows. pos [0] is fixed with data from mainplot
        cline = self.rowcount -7
        print("Add_line, cline:", cline)
        # -------------------------------
        # del Button
        self.list_del_button.append(tk.Button(self.menue_top, text="X", fg="red",
                                          command=lambda row=cline: self.del_row_line(row)))
        self.list_del_button[cline].grid(row = self.rowcount, column = 0, sticky="w")
        # -------------------------------
        # Input Lists
        # Steps: 1. Add new listentry, 2. [i][0]: Variable, 3. Setting to Choice, 4. [i][1]: Widget, 5. Grid
        # -
        #self.list_datax.append([])
        #self.list_datax[cline].append(tk.StringVar())
        #try:
        #    self.list_datax[cline][0].set(self.variablex[0])
        #except:
        #    self.list_datax[cline][0].set("Kein Eintrag")
        #self.list_datax[cline].append(tk.OptionMenu(self.menue_top, self.list_datax[cline][0],
        #                                             *self.variablex))
        #self.list_datax[cline][1].config(width=10)
        #self.list_datax[cline][1].grid(row = self.rowcount, column = 1, sticky="n")
        # -
        self.list_datay.append([])
        self.list_datay[cline].append(tk.StringVar())
        try:
            self.list_datay[cline][0].set(list(self.data_dict.keys())[0])
        except:
            self.list_datay[cline][0].set("Kein Eintrag")
        self.list_datay[cline].append(tk.OptionMenu(self.menue_top, self.list_datay[cline][0],
                                                     *self.data_dict.keys(),
                                                     command=(lambda _, row=cline: self.change_axis_y_name(row))))
        self.list_datay[cline][1].config(width=10)
        self.list_datay[cline][1].grid(row = self.rowcount, column = 2, sticky="n")
        # -
        self.list_name.append([])
        self.list_name[cline].append(tk.StringVar())
        self.list_name[cline].append(tk.Entry(self.menue_top, textvariable=self.list_name[cline][0]))
        self.list_name[cline][1].grid(row = self.rowcount, column = 3, sticky="n")
        # -
        self.list_marker.append([])
        self.list_marker[cline].append(tk.StringVar())
        try:
            self.list_marker[cline][0].set(self.choosemarker[0])
        except:
            self.list_marker[cline][0].set("Kein Eintrag")
        self.list_marker[cline].append(tk.OptionMenu(self.menue_top, self.list_marker[cline][0],
                                                     *self.choosemarker))
        self.list_marker[cline][1].config(width=2)
        self.list_marker[cline][1].grid(row = self.rowcount, column = 4, sticky="n")
        # -
        self.list_line.append([])
        self.list_line[cline].append(tk.StringVar())
        try:
            self.list_line[cline][0].set(self.chooseline[0])
        except:
            self.list_line[cline][0].set("Kein Eintrag")
        self.list_line[cline].append(tk.OptionMenu(self.menue_top, self.list_line[cline][0],
                                                     *self.chooseline))
        self.list_line[cline][1].config(width=2)
        self.list_line[cline][1].grid(row = self.rowcount, column = 5, sticky="n")
        # -
        self.list_color.append([])
        self.list_color[cline].append(tk.StringVar())
        try:
            self.list_color[cline][0].set(self.choosecolor[0])
        except:
            self.list_color[cline][0].set("Kein Eintrag")
        self.list_color[cline].append(tk.OptionMenu(self.menue_top, self.list_color[cline][0],
                                                     *self.choosecolor))
        self.list_color[cline][1].config(width=6)
        self.list_color[cline][1].grid(row = self.rowcount, column = 6, sticky="n")
        # -
        self.list_side.append([])
        self.list_side[cline].append(tk.StringVar())
        try:
            self.list_side[cline][0].set(self.chooseside[0])
        except:
            self.list_side[cline][0].set("Kein Eintrag")
        self.list_side[cline].append(tk.OptionMenu(self.menue_top, self.list_side[cline][0],
                                                     *self.chooseside))
        self.list_side[cline][1].config(width=6)
        self.list_side[cline][1].grid(row = self.rowcount, column = 7, sticky="n")
        # -
        self.list_data_top.append([])
        self.list_data_top[cline].append(tk.StringVar())
        self.list_data_top[cline][0].set("auto")
        self.list_data_top[cline].append(tk.Entry(self.menue_top, textvariable=self.list_data_top[cline][0], width= 5))
        self.list_data_top[cline][1].grid(row = self.rowcount, column = 8, sticky="n")
        # - 
        self.list_newaxis.append([])
        self.list_newaxis[cline].append(tk.IntVar())
        self.list_newaxis[cline][0].set(0)
        self.list_newaxis[cline].append(tk.Checkbutton(self.menue_top, variable=self.list_newaxis[cline][0],
                                                       command=lambda row=cline: self.visible_change(row))) #command für ein/ausblenden Label 
        self.list_newaxis[cline][1].grid(row = self.rowcount, column = 9, sticky="n")
        # -
        self.list_ylabel.append([])
        self.list_ylabel[cline].append(tk.StringVar())
        self.list_ylabel[cline].append(tk.Entry(self.menue_top, textvariable=self.list_ylabel[cline][0]))
        # self.list_ylabel[cline][1].grid(row = self.rowcount, column = 10, sticky="n")
        # -
        #self.list_xlabel.append([])
        #self.list_xlabel[cline].append(tk.StringVar())
        #self.list_xlabel[cline].append(tk.Entry(self.menue_top, textvariable=self.list_xlabel[cline][0]))
        #self.list_xlabel[cline][1].grid(row = self.rowcount, column = 11, sticky="n")
        # - 
        self.list_hide_tick.append([])
        self.list_hide_tick[cline].append(tk.IntVar())
        self.list_hide_tick[cline][0].set(0)
        self.list_hide_tick[cline].append(tk.Checkbutton(self.menue_top, variable=self.list_hide_tick[cline][0]))
        self.list_hide_tick[cline][1].grid(row = self.rowcount, column = 12, sticky="n")


        # -------------------------------

        self.rowcount += 1





    def load_file(self):
        """
        Load File, String name expectet at pos 0 !
        [name1] | [name2] |
        [int]   |  [int]  |
        [int]   |  [int]  | 
        """
        datapath = tk.filedialog.askopenfilename(title = "Select file",filetypes = (("Csv files","*.csv"),("all files","*.*")))

        try:
            with open(datapath, newline="") as csvfile:
                datareader = csv.reader(csvfile, dialect="excel")
                self.data_dict = {}
                data_list = []
                rowlist = []
                temp = []
                # saves the file into a list
                for row in datareader:
                    rowlist.append(row)
                # splits the data at ; for german files
                for i in range(len(rowlist)):    
                    temp.append(rowlist[i][0].strip().split(';', 50))
                # columns of data_list
                for i in range(len(temp[0])):
                    data_list.append([])
                # seperates the datas in row into colums, sorted for Empty, Float, String
                for i in range(len(temp)):
                    for j in range(len(temp[0])):
                        if temp[i][j] == "":
                            data_list[j].append(None)
                        else:
                            try:
                                data_list[j].append(float(temp[i][j]))
                            except:
                                data_list[j].append(temp[i][j])

            # into Dict
            for i in range(len(data_list)):
                # set datanames into name
                name = [data_list[i][0]]
                # deletes names from data
                data_list[i].pop(0)
                # append data to name key dict
                print(i, name, data_list[i])
                self.data_dict[name[0]] = data_list[i]
        except:
            print("Keine Datei geladen")
            return
        self.update_dropdown()




    def gen_builder(self):
        # takes all the data and calls gen_plot correct
        #pos 0 für host
        variablex = []
        variabley = []
        linetype   = []
        color = []
        marker = []
        name = []
        axislabelx = []
        axislabely = []
        newaxisy = []
        position = []
        data_top = []
        hidetick = []

        zwlist =[]

        print("DEBUG: gen_builder")

        for i in range(len(self.list_datax)):
            if self.list_datax[i][0].get() != "__XX__XX__":
                zwlist = self.data_dict[self.list_datax[i][0].get()]
#                zwlist = self.data_dict[self.list_datax[i][0].get()][i].strip("()")
#                zwlist = [int(s) for s in zwlist.split(',')]
                variablex.append(zwlist)
        for i in range(len(self.list_datay)):
            if self.list_datay[i][0].get() != "__XX__XX__":
                zwlist = self.data_dict[self.list_datay[i][0].get()]
#                zwlist = self.data_dict[self.list_datay[i][0].get()][i].strip("()")
#                zwlist = [int(s) for s in zwlist.split(',')]
                variabley.append(zwlist)
        for i in range(len(self.list_name)):
            if self.list_name[i][0].get() != "__XX__XX__":
                name.append(self.list_name[i][0].get())
        for i in range(len(self.list_marker)):
            if self.list_marker[i][0].get() != "__XX__XX__":
                marker.append(self.list_marker[i][0].get())
        for i in range(len(self.list_line)):
            if self.list_line[i][0].get() != "__XX__XX__":
                linetype.append(self.list_line[i][0].get())
        for i in range(len(self.list_color)):
            if self.list_color[i][0].get() != "__XX__XX__":
                color.append(self.list_color[i][0].get())
        for i in range(len(self.list_side)):
            if self.list_side[i][0].get() != "__XX__XX__":
                position.append(self.list_side[i][0].get())  
        for i in range(len(self.list_newaxis)):
            if self.list_newaxis[i][0].get() != 2:
                newaxisy.append(self.list_newaxis[i][0].get())
        for i in range(len(self.list_ylabel)):
            if self.list_ylabel[i][0].get() != "__XX__XX__":
                axislabely.append(self.list_ylabel[i][0].get())
        for i in range(len(self.list_xlabel)):
            if self.list_xlabel[i][0].get() != "__XX__XX__":
                axislabelx.append(self.list_xlabel[i][0].get())
        for i in range(len(self.list_data_top)):
            if self.list_data_top[i][0].get() != "__XX__XX__":
                data_top.append(self.list_data_top[i][0].get())
        for i in range(len(self.list_hide_tick)):
            if self.list_hide_tick[i][0].get() != 2:
                hidetick.append(self.list_hide_tick[i][0].get())

        self.gen_plot( variablex, variabley, linetype, color, marker, name,
                         axislabelx, axislabely, newaxisy, position, data_top, hidetick)



    def make_patch_spines_invisible(self, ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

            

    def gen_plot(self, variablex, variabley, linetype, color, marker, name,
                 axislabelx, axislabely, newaxisy, position, data_top, hidetick):
        """
        arguments:
        variablex = []
        variabley = []
        linetype   = []
        color = []
        marker = []
        name = []
        axislabelx = []
        axislabely = []
        newaxisy = []
        position = []
        data_top = []
        -------
        pos[0] for mainplot 
        """
        print("DEBUG: gen_plot")


        #-----variables--------

        y_axis_dist = self.var_y_dist.get()
        inc_r = 1
        inc_l = -y_axis_dist
        
        n_col = 1
        msize = self.var_m_size.get()
        fontsize = self.var_fontsize.get()

        #-----Hostplotting----------------------
        fig, host = plt.subplots(figsize=(20,5), dpi=100)
        #verkleinert die Bbox der Axes auf 0.75
        fig.subplots_adjust(left=0.25, right=0.75)

        tkw = dict(size=4, width=1.5, labelsize=fontsize)
        p1, = host.plot(variablex[0], variabley[0], ls=linetype[0], color=color[0],
                       marker=marker[0], ms=msize, label=name[0])
        host.minorticks_on()
        if self.plot_grid_bool.get() == 1:
            host.grid(True, which='major', ls='--')
#        host.grid(True, which='minor', ls='--')
        host.set_xlabel(axislabelx[0], fontsize=fontsize)
        host.set_ylabel(axislabely[0], fontsize=fontsize)
        an1 = host.annotate(self.get_symbol(marker[0]), xy=(0, 0), xycoords=host.yaxis.label, 
                           xytext=(0, -10), textcoords="offset points",
                           va="center", ha="left", rotation=90,
                           color=color[0], size=fontsize
                           )
        if self.colorize_label_bool.get():
            host.yaxis.label.set_color(p1.get_color())
            host.tick_params(axis='y', colors=p1.get_color(), **tkw)
        else:
            host.yaxis.label.set_color("black")
            host.tick_params(axis='y', colors="black", **tkw)
        host.tick_params(axis='x', **tkw)
        #host.set_xlim(left=0)
        #host.set_ylim(bottom=0)
        lines = [p1]
        
        #------Rest Y Axis----------------------
        for ix, i in enumerate(variabley):
            if ix != 0:
                # creates new axis, if not, the plot gets addet to host
                if newaxisy[ix] != 0:
                    # initialize more axis, with shared X axis of Host
                    par = host.twinx()
                    # set only the spine left or right and increase the space between axis
                    if position[ix] == 'right':
                        par.spines[position[ix]].set_position(("axes", inc_r))
                        inc_r += y_axis_dist
                    elif position[ix] == 'left':
                        par.spines[position[ix]].set_position(("axes", inc_l))
                        inc_l += -y_axis_dist
                    # make patch invisible and the spine visible. Also set the position of the tick and label
                    self.make_patch_spines_invisible(par)
                    par.spines[position[ix]].set_visible(True)
                    par.yaxis.set_label_position(position[ix])
                    par.yaxis.set_ticks_position(position[ix])

                    # hide Ticks
                    if hidetick[ix] != 0:
                        par.tick_params(
                            axis='y',          # changes apply to the x-axis
                            which='both',      # both major and minor ticks are affected
                            left=False,      
                            right=False,         
                            labelright=False,
                            labelleft=False,)
                        par.spines[position[ix]].set_visible(False)
                        # correct the distance for the next spine and this one
                        if position[ix] == 'right':
                            par.spines[position[ix]].set_position(("axes", inc_r -y_axis_dist -0.01))
                            inc_r += -y_axis_dist +0.02
                        elif position[ix] == 'left':
                            par.spines[position[ix]].set_position(("axes", inc_l +y_axis_dist + 0.01))
                            inc_l += y_axis_dist -0.02

                    # create plot
                    
                    p, = par.plot(variablex[0], variabley[ix], ls=linetype[ix], color=color[ix],
                                 marker=marker[ix], ms=msize, label=name[ix])
                    par.set_ylabel(axislabely[ix], fontsize=fontsize)




                    if self.colorize_label_bool.get():
                        par.yaxis.label.set_color(p.get_color())
                        par.tick_params(axis='y', colors=p.get_color(), **tkw)
                    else:
                        par.yaxis.label.set_color("black")
                        par.tick_params(axis='y', colors="black", **tkw)

                    an2 = par.annotate(self.get_symbol(marker[ix]), xy=(0, 0), xycoords=par.yaxis.label,
                                        xytext=(0, -10), textcoords="offset points",
                                        va="center", ha="left", rotation=90,
                                        color=color[ix], size=fontsize
                                        )

                    
                    par.set_ylim(bottom=0)
                    if data_top[ix] != "auto":
                        try:
                            par.set_ylim(top=float(data_top[ix]))
                        except:
                            print("cant set TOP! no Valid Float.")
                    lines.append(p)
                else:
                    #self.make_patch_spines_invisible(par)
                    #par.axis("off")
                    p, = host.plot(variablex[0], variabley[ix], ls=linetype[ix], color=color[ix],
                       marker=marker[ix], ms=msize, label=name[ix])
                    lines.append(p)
                    
                n_col += 1

        host.set_ylim(bottom=0)
        if data_top[0] != "auto":
            try:
                host.set_ylim(top=float(data_top[0]))
            except:
                print("cant set TOP! no Valid Float.")
        # show legend
        if self.legend_bool.get() == 1:
            host.legend(lines, [l.get_label() for l in lines], fontsize=fontsize, 
                        bbox_to_anchor=(0., 1.02, 1., .102), ncol=n_col, mode="expand", loc='best')


        #tkinter gui
        scatter = FigureCanvasTkAgg(fig, self.menue_bottom)
        scatter.get_tk_widget().grid(row = 0, column = 0, sticky="n")

        self.free_to_save = True

        #plt.show() # plt.close(fig=None) für das schliessen des alten fensters
        




    def get_symbol(self, marker):
        # \u for unicode
        symbol_dict = {'o':'\u25CF',
                        'd':'\u29EB',
                        's':'\\blacksquare',
                        '+':'\\plus',
                        'x':'\\times',
                        '.':'\\bullet',
                        '<':'\\blacktriangleleft',
                        '>':'\\blacktriangleright',
                        'v':'\\blacktriangledown',
                        '^':'\\blacktriangle'}
        

        symbol = symbol_dict[marker]
        #symbol = "blacktriangleleft"
        return "$"+symbol+"$"



    def save_fig(self):
        if self.free_to_save:
            datapath = tk.filedialog.asksaveasfilename(title = "Save as",filetypes = (("PNG files","*.png"),("all files","*.*")))
            if not datapath:
                print("no path")
                return
            plt.savefig(datapath, dpi=100, bbox_inches="tight")
            #plt.savefig(datapath, dpi=100)
        else:     
            print("Error, cant save fig, not yet constructed")
    

    def callback(self,url):
        #open URL
        webbrowser.open_new(url)    


    def visible_change(self, row):
        print("visible_change, ",self.list_newaxis[row][0].get())
        if self.list_newaxis[row][0].get() == 0:
            self.list_ylabel[row][1].grid_forget()
        else:
            self.list_ylabel[row][1].grid(row = (row + 7), column = 10, sticky="n")


    def change_axis_x_name(self, row):
        # Change the Names and Axis automatic from data
        print("CHANGED TO ",row)
        self.list_xlabel[row][0].set(self.list_datax[row][0].get())


    def change_axis_y_name(self, row):
        # Change the Names and Axis automatic from data
        print("CHANGED TO ",row)
        self.list_ylabel[row][0].set(self.list_datay[row][0].get())
        self.list_name[row][0].set(self.list_datay[row][0].get())
         
        
    def del_row_line(self, row):
        print("del_row_line, row", row)
        for i in range(len(self.list_datax)): 
            print("dataX ",i, ": ", self.list_datax[i][0].get())

        self.list_del_button[row].grid_forget()

#        self.list_datax[row][1].grid_forget()
#        self.list_datax[row][0].set("__XX__XX__")

        self.list_datay[row][1].grid_forget()
        self.list_datay[row][0].set("__XX__XX__")

        self.list_name[row][1].grid_forget()
        self.list_name[row][0].set("__XX__XX__")

        self.list_marker[row][1].grid_forget()
        self.list_marker[row][0].set("__XX__XX__")

        self.list_line[row][1].grid_forget()
        self.list_line[row][0].set("__XX__XX__")

        self.list_color[row][1].grid_forget()
        self.list_color[row][0].set("__XX__XX__")

        self.list_side[row][1].grid_forget()
        self.list_side[row][0].set("__XX__XX__")

        self.list_newaxis[row][1].grid_forget()
        self.list_newaxis[row][0].set(2)

        self.list_ylabel[row][1].grid_forget()
        self.list_ylabel[row][0].set("__XX__XX__")

        self.list_data_top[row][1].grid_forget()
        self.list_data_top[row][0].set("__XX__XX__")

        self.list_hide_tick[row][1].grid_forget()
        self.list_hide_tick[row][0].set(2)



#        self.list_xlabel[row][1].grid_forget()
#        self.list_xlabel.pop(row)















root = tk.Tk()

app = Application(master=root)
app.title = "gui"
root.mainloop()

print("mainloop out, Exit")
