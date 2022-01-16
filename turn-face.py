#!/usr/bin/env python
import sys
from Tkinter import *
from Tkinter import END, Label, Entry, StringVar, W, E, Menu, N, S, IntVar, Radiobutton, Text, Scrollbar, SEL, Frame, \
    Button
from tkFileDialog import *
from SimpleDialog import *
from ConfigParser import *
from decimal import *
import tkMessageBox
import os

version = '1.0.0'
IN_AXIS = os.environ.has_key("AXIS_PROGRESS_BAR")


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, width=700, height=400, bd=1)
        self.g_code = Text(self, width=30, height=30, bd=3)
        self.cp = ConfigParser()
        self.home_var = IntVar()
        self.safe_var = StringVar()
        self.end_z_var = StringVar()
        self.start_z_var = StringVar()
        self.spindle_rpm_var = StringVar()
        self.feedrate_var = StringVar()
        self.unit_var = IntVar()
        self.depth_of_final_cut_var = StringVar()
        self.blank_od_var = StringVar()
        self.final_od_var = StringVar()
        self.depth_of_cat_var = StringVar()
        self.grid()
        self.create_menu()
        self.create_widgets()
        self.load_preferences()
        self.nc_dir = ""

    def create_menu(self):
        # Create the Menu base
        menu_var = Menu(self)
        # Add the Menu
        self.master.config(menu=menu_var)
        # Create our File menu
        file_menu = Menu(menu_var)
        # Add our Menu to the Base Menu
        menu_var.add_cascade(label='File', menu=file_menu)
        # Add items to the menu
        file_menu.add_command(label='New', command=self.clear_text_box)
        file_menu.add_command(label='Open', command=self.simple)
        file_menu.add_separator()
        file_menu.add_command(label='Quit', command=self.quit)

        edit_menu = Menu(menu_var)
        menu_var.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Copy', command=self.copy_clipboard)
        edit_menu.add_command(label='Select All', command=self.select_all_text)
        edit_menu.add_command(label='Delete All', command=self.clear_text_box)
        edit_menu.add_separator()
        edit_menu.add_command(label='Save Preferences', command=self.save_preferences)
        edit_menu.add_command(label='Load Preferences', command=self.load_preferences)

        help_menu = Menu(menu_var)
        menu_var.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Help Info', command=self.help_info)
        help_menu.add_command(label='About', command=self.help_about)

    def create_widgets(self):

        sp1 = Label(self)
        sp1.grid(row=0)

        st1 = Label(self, text='Blank Outside Diameter ')
        st1.grid(row=1, column=0, sticky=E)
        blank_od = Entry(self, width=10, textvariable=self.blank_od_var)
        blank_od.grid(row=1, column=1, sticky=W)
        blank_od.focus_set()

        st2 = Label(self, text='Internal Diameter ')
        st2.grid(row=2, column=0, sticky=E)
        final_od = Entry(self, width=10, textvariable=self.final_od_var)
        final_od.grid(row=2, column=1, sticky=W)

        st6 = Label(self, text='Depth of Each Cut ')
        st6.grid(row=3, column=0, sticky=E)
        depth_of_cut = Entry(self, width=10, textvariable=self.depth_of_cat_var)
        depth_of_cut.grid(row=3, column=1, sticky=W)

        st5 = Label(self, text='Depth of final Cut ')
        st5.grid(row=4, column=0, sticky=E)
        depth_of_final_cut = Entry(self, width=10, textvariable=self.depth_of_final_cut_var)
        depth_of_final_cut.grid(row=4, column=1, sticky=W)

        st4 = Label(self, text='Feedrate ')
        st4.grid(row=1, column=2, sticky=E)
        feed_rate = Entry(self, width=10, textvariable=self.feedrate_var)
        feed_rate.grid(row=1, column=3, sticky=W)

        st4a = Label(self, text='M3 Spindle RPM ')
        st4a.grid(row=2, column=2, sticky=E)
        spindle_rpm = Entry(self, width=10, textvariable=self.spindle_rpm_var)
        spindle_rpm.grid(row=2, column=3, sticky=W)

        st4a = Label(self, text='Start Z position ')
        st4a.grid(row=3, column=2, sticky=E)
        start_z = Entry(self, width=10, textvariable=self.start_z_var)
        start_z.grid(row=3, column=3, sticky=W)

        st4a = Label(self, text='End Z position ')
        st4a.grid(row=4, column=2, sticky=E)
        end_z = Entry(self, width=10, textvariable=self.end_z_var)
        end_z.grid(row=4, column=3, sticky=W)

        st10 = Label(self, text='Retract distance ')
        st10.grid(row=5, column=0, sticky=E)
        safe = Entry(self, width=10, textvariable=self.safe_var)
        safe.grid(row=5, column=1, sticky=W)

        spacer3 = Label(self, text='')
        spacer3.grid(row=6, column=0, columnspan=4)

        self.g_code.grid(row=7, column=0, columnspan=5, sticky=E + W + N + S)
        tb_scroll = Scrollbar(self, command=self.g_code.yview)
        tb_scroll.grid(row=7, column=5, sticky=N + S + W)
        self.g_code.configure(yscrollcommand=tb_scroll.set)

        sp4 = Label(self)
        sp4.grid(row=8)

        st8 = Label(self, text='Units')
        st8.grid(row=0, column=5)
        unit_options = [('Inch', 1), ('MM', 2)]
        for text, value in unit_options:
            Radiobutton(self, text=text, value=value, variable=self.unit_var, indicatoron=0, width=6, ) \
                .grid(row=value, column=5)
        self.unit_var.set(1)

        st9 = Label(self, text='X0-Y0')
        st9.grid(row=3, column=5)
        home_options = [('Left-Rear', 4), ('Left-Front', 5)]
        for text, value in home_options:
            Radiobutton(self, text=text, value=value, variable=self.home_var, indicatoron=0, width=11, ) \
                .grid(row=value, column=5)
        self.home_var.set(4)

        gen_button = Button(self, text='Generate G-Code', command=self.gen_code)
        gen_button.grid(row=8, column=0)

        copy_button = Button(self, text='Select All & Copy', command=self.select_copy)
        copy_button.grid(row=8, column=1)

        write_button = Button(self, text='Write to File', command=self.write_to_file)
        write_button.grid(row=8, column=2)

        if IN_AXIS:
            to_axis = Button(self, text='Write to AXIS and Quit', command=self.write_to_axis)
            to_axis.grid(row=8, column=3)

            quit_button = Button(self, text='Quit', command=self.quit_from_axis)
            quit_button.grid(row=8, column=5, sticky=E)
        else:
            quit_button = Button(self, text='Quit', command=self.quit)
            quit_button.grid(row=8, column=5, sticky=E)

    def quit_from_axis(self):
        sys.stdout.write("M2 (Turn-face.py Aborted)")
        self.quit()

    def write_to_axis(self):
        sys.stdout.write(self.g_code.get(0.0, END))
        self.quit()

    def gen_code(self):
        """ Generate the G-Code turning face"""

        # Define Lathe mode, work with Diameter (not Radius)
        self.g_code.insert(END, '%\n')
        self.g_code.insert(END, '(1000)\n')
        self.g_code.insert(END, 'G7\n')
        self.g_code.insert(END, 'G18\n')
        self.g_code.insert(END, 'G90\n')
        self.g_code.insert(END, 'G21\n\n')

        start_od = self.float_to_decimal(self.blank_od_var.get())
        end_od = self.float_to_decimal(self.final_od_var.get())
        cut_depth = self.float_to_decimal(self.depth_of_cat_var.get())
        final_cut_depth = self.float_to_decimal(self.depth_of_final_cut_var.get())
        start_z = self.float_to_decimal(self.start_z_var.get())
        end_z = self.float_to_decimal(self.end_z_var.get())
        feed_rate = self.float_to_decimal(self.feedrate_var.get())
        retract = self.float_to_decimal(self.safe_var.get())
        loop_count = int((start_z - end_z - 2 * final_cut_depth) / cut_depth)

        self.g_code.insert(END, 'G0 X%.4f z%.4f\n' % (start_od + 4, start_z + 4))

        work_end_z = end_z + 2 * final_cut_depth
        z_position = start_z

        self.g_code.insert(END, 'G1 X%.4f Z%.4f F%4f\n' % (start_od + retract, start_z + retract, feed_rate))

        for i in range(loop_count):
            z_position -= cut_depth
            # prepare for next cut
            self.g_code.insert(END, 'G1 Z%.4f F%4f\n' % (z_position, feed_rate))
            # work
            self.g_code.insert(END, 'X%.4f\n' % end_od)
            # retract
            self.g_code.insert(END, 'Z%.4f\n' % (z_position + retract))
            # Rapid to beginning of the work
            self.g_code.insert(END, 'G0 X%.4f\n' % (start_od + retract))

        # Final cycles
        # pre finish
        self.g_code.insert(END, '\n(Pre Finish cut)\n')
        z_position = end_z + final_cut_depth
        self.g_code.insert(END, 'G1 Z%.4f F%4f\n' % (z_position, feed_rate / 2))
        # work
        self.g_code.insert(END, 'X%.4f\n' % end_od)
        # retract
        self.g_code.insert(END, 'Z%.4f\n' % (z_position + retract))
        # Rapid to start OD
        self.g_code.insert(END, 'G0 X%.4f\n' % (start_od + retract))

        # final cut
        self.g_code.insert(END, '\n(Finish cut)\n')
        z_position = end_z
        self.g_code.insert(END, 'G1 Z%.4f F%4f\n' % (z_position, feed_rate / 2))
        # work
        self.g_code.insert(END, 'X%.4f\n' % end_od)
        # retract
        self.g_code.insert(END, 'Z%.4f\n' % (z_position + retract))
        # Rapid to start OD
        self.g_code.insert(END, 'G0 X%.4f\n' % (start_od + retract))
        # Rapid to beginning of the work
        self.g_code.insert(END, 'G0 X%.4f Z%.4f\n' % (start_od + retract, start_z + retract))

        self.g_code.insert(END, '\n')

        # Generate the G-Codes
        if len(self.spindle_rpm_var.get()) > 0:
            self.g_code.insert(END, 'S%i ' % (self.float_to_decimal(self.spindle_rpm_var.get())))
            self.g_code.insert(END, 'M3 ')
        if len(self.feedrate_var.get()) > 0:
            self.g_code.insert(END, 'F%s\n' % (self.feedrate_var.get()))

        if len(self.spindle_rpm_var.get()) > 0:
            self.g_code.insert(END, 'M5\n')
        self.g_code.insert(END, '\nM2 (End of File)\n')
        self.g_code.insert(END, '%')

    @staticmethod
    def float_to_decimal(s):  # Float To Decimal
        """
        Returns a decimal with 4 place precision
        valid inputs are any fraction, whole number space fraction
        or decimal string. The input must be a string!
        """
        s = s.strip(' ')  # remove any leading and trailing spaces
        d = Decimal  # Save typing
        p = d('0.0001')  # Set the precision wanted
        if ' ' in s:  # if it is a whole number with a fraction
            w, f = s.split(' ', 1)
            w = w.strip(' ')  # make sure there are no extra spaces
            f = f.strip(' ')
            n, d = f.split('/', 1)
            return d(d(n) / d(d) + d(w)).quantize(p)
        elif '/' in s:  # if it is just a fraction
            n, d = s.split('/', 1)
            return d(d(n) / d(d)).quantize(p)
        return d(s).quantize(p)  # if it is a decimal number already

    def get_ini_data(self, file_name, section_name, option_name, default=''):
        """
        Returns the data in the file, section, option if it exists
        of an .ini type file created with ConfigParser.write()
        If the file is not found or a section or an option is not found
        returns an exception
        """
        try:
            self.cp.readfp(open(file_name, 'r'))
            try:
                self.cp.has_section(section_name)
                try:
                    ini_data = self.cp.get(section_name, option_name)
                except:
                    ini_data = default
            except:
                ini_data = default
        except:
            ini_data = default
        return ini_data

    def write_ini_data(self, file_name, section_name, option_name, option_data):
        """
        Pass the file name, section name, option name and option data
        When complete returns 'success'
        """
        cp = ConfigParser()
        try:
            fn = open(file_name, 'a')
        except IOError:
            fn = open(file_name, 'w')
        if not self.cp.has_section(section_name):
            self.cp.add_section(section_name)
        cp.set(section_name, option_name, option_data)
        cp.write(fn)
        fn.close()

    @staticmethod
    def get_directory():
        dir_name = askdirectory(initialdir='/home', title='Please select a directory')
        if len(dir_name) > 0:
            return dir_name

    def copy_clipboard(self):
        self.g_code.clipboard_clear()
        self.g_code.clipboard_append(self.g_code.get(0.0, END))

    def write_to_file(self):
        new_file_name = asksaveasfile(initialdir=self.nc_dir, mode='w', master=self.master, title='Create NC File',
                                      defaultextension='.ngc')
        self.nc_dir = os.path.dirname(new_file_name.name)
        new_file_name.write(self.g_code.get(0.0, END))
        new_file_name.close()

    def load_preferences(self):
        self.nc_dir = self.get_ini_data('turn_face.ini', 'Directories', 'NcFiles', os.path.expanduser("~"))
        self.feedrate_var.set(self.get_ini_data('turn_face.ini', 'LatheParameters', 'Feedrate', '100'))
        self.depth_of_cat_var.set(self.get_ini_data('turn_face.ini', 'LatheParameters', 'DepthOfCut', '0.1'))
        self.spindle_rpm_var.set(self.get_ini_data('turn_face.ini', 'LatheParameters', 'SpindleRPM', '2500'))
        self.unit_var.set(int(self.get_ini_data('turn_face.ini', 'LatheParameters', 'UnitVar', '2')))
        self.home_var.set(int(self.get_ini_data('turn_face.ini', 'LatheParameters', 'HomeVar', '4')))
        self.safe_var.set(self.get_ini_data('turn_face.ini', 'LatheParameters', 'SafeZ', '1.0'))
        self.blank_od_var.set(self.get_ini_data('turn_face.ini', 'Part', 'X0'))
        self.final_od_var.set(self.get_ini_data('turn_face.ini', 'Part', 'X1'))
        self.depth_of_final_cut_var.set(self.get_ini_data('turn_face.ini', 'LatheParameters', 'DepthOfFinalCut'))
        self.start_z_var.set(self.get_ini_data('turn_face.ini', 'LatheParameters', 'StartZ'))
        self.end_z_var.set(self.get_ini_data('turn_face.ini', 'Part', 'EndZ'))

    def save_preferences(self):
        def set_pref(section_name, option_name, option_data):
            if not self.cp.has_section(section_name):
                self.cp.add_section(section_name)
            self.cp.set(section_name, option_name, option_data)

        self.cp = ConfigParser()
        fn = open('turn_face.ini', 'w')
        set_pref('Directories', 'NcFiles', self.nc_dir)
        set_pref('LatheParameters', 'Feedrate', self.feedrate_var.get())
        set_pref('LatheParameters', 'DepthOfCut', self.depth_of_cat_var.get())
        set_pref('LatheParameters', 'SpindleRPM', self.spindle_rpm_var.get())
        set_pref('LatheParameters', 'UnitVar', self.unit_var.get())
        set_pref('LatheParameters', 'HomeVar', self.home_var.get())
        set_pref('LatheParameters', 'SafeZ', self.safe_var.get())
        set_pref('LatheParameters', 'StartZ', self.start_z_var.get())
        set_pref('Part', 'EndZ', self.end_z_var.get())
        set_pref('LatheParameters', 'DepthOfFinalCut', self.depth_of_final_cut_var.get())
        set_pref('Part', 'X0', self.blank_od_var.get())
        set_pref('Part', 'X1', self.final_od_var.get())
        self.cp.write(fn)
        fn.close()

    @staticmethod
    def simple():
        tkMessageBox.showinfo('Feature', 'Sorry this Feature has\nnot been programmed yet.')

    def clear_text_box(self):
        self.g_code.delete(1.0, END)

    def select_all_text(self):
        self.g_code.tag_add(SEL, '1.0', END)

    def select_copy(self):
        self.select_all_text()
        self.copy_clipboard()

    def help_info(self):
        SimpleDialog(self,
                     text='Required fields are:\n'
                          'Part Width & Length,\n'
                          'Amount to Remove,\n'
                          'and Feedrate\n'
                          'Fractions can be entered in most fields',
                     buttons=['Ok'],
                     default=0,
                     title='User Info').go()

    @staticmethod
    def help_about():
        tkMessageBox.showinfo('Help About', 'Programmed by\n'
                                            'Alex Tenenbaum\n'
                                            'Version ' + version)


app = Application()
app.master.title('Turning OD G-Code Generator Version ' + version)
app.mainloop()
