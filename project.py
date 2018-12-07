#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 15:57:40 2018

@author: agni
"""

import sys
import re
import platform
import numpy as np
import notch

#import matplotlib
#matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import (QMainWindow, QApplication, QLineEdit, QRadioButton,
                             QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
                             QAction, QMessageBox, QFileDialog, QSizePolicy,
                             QLabel, QGridLayout, QWidget, QFrame, QGroupBox)
from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR, Qt

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self, parent=None) :
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Notch Sensitivity Analyser')
        self.widget = QWidget()
        self.button1 = QPushButton("Start")
        self.button1.clicked.connect(self.newWin)
        layout = QGridLayout()
        layout.addWidget(self.textGroup(),0,0,1,4)
        layout.addWidget(self.radioGroup(),1,1,1,2)
        layout.addWidget(self.button1,2,1,1,2)
        self.widget.setLayout(layout) 
        self.setCentralWidget(self.widget)  
    def newWin(self):
        global val
        if self.radio1.isChecked():
            val=0
        else:
            val=1
        self.nw = MainWindow1(self)
        self.nw.show()
    def test(self):
        return val
            
    def radioGroup(self):
        gb = QGroupBox("Units")
        self.radio1 = QRadioButton("&SI Units")
        self.radio2 = QRadioButton("&English Units")
        self.radio1.setChecked(True)
        hb = QHBoxLayout()
        hb.addWidget(self.radio1)
        hb.addWidget(self.radio2)
        gb.setLayout(hb)
        return gb
    def textGroup(self):
        gb = QGroupBox()
        self.label = QLabel()
        self.label.setText("<span style='font-size:12pt; font-weight:600;color:red;'\
                           >Welcome to Notch Sensitivity Analyser <i>(v0.1)</i></span>\
                           <span style='font-size:9pt; font-weight:400; color:red;'>\
                           <p><i>Copyright &copy; 2018 Agniprobho Mazumder, All Rights Reserved</i></p>\
                           <p><i>Python %s -- Qt %s -- PyQt %s on %s</i></p></span>"%(platform.python_version(),QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))
        self.label.setAlignment(Qt.AlignCenter)
        hb = QHBoxLayout()
        hb.addWidget(self.label)
        gb.setLayout(hb)
        return gb
    

class MainWindow1(QMainWindow) :
    
    def __init__(self, parent=None): 
        super(MainWindow1, self).__init__(parent) 

        ########################################################################
        # ADD MENU ITEMS
        ########################################################################
        
        # Create the File menu
        self.setWindowTitle('Notch Sensitivity (q)')
        self.menuFile = self.menuBar().addMenu("&File")
        self.actionSaveAs = QAction("&Save As", self)
        self.actionSaveAs.triggered.connect(self.saveas)
        self.actionQuit = QAction("&Quit", self)
        self.actionQuit.triggered.connect(self.close)
        self.menuFile.addActions([self.actionSaveAs, self.actionQuit])
        
        # Create the Help menu
        self.menuHelp = self.menuBar().addMenu("&Help")
        self.actionAbout = QAction("&About",self)
        self.actionAbout.triggered.connect(self.about)
        self.actionTut = QAction("&Help...",self)
        self.actionTut.triggered.connect(self.helpMe)
        self.menuHelp.addActions([self.actionAbout,self.actionTut])
        
        ########################################################################
        # CREATE CENTRAL WIDGET
        ########################################################################

        self.widget = QWidget()
        self.plot = MatplotlibCanvas()
        self.test_text = QLineEdit()
        
        self.win = MainWindow(self)
        if self.win.test()==0:
            self.edit2c = QLabel("MPa")
            self.edit3c = QLabel("mm") 
            self.xlabel='Notch Radius, r, mm'
        elif self.win.test()==1:
            self.edit2c = QLabel("ksi")
            self.edit3c = QLabel("in")
            self.xlabel='Notch Radius, r, in'
            
        self.edit1a = QLabel("Material: ")
        self.edit2a = QLabel("Ultimate Tensile Strength (Su): ")
        self.edit3a = QLabel("Notch Radius: ")
        self.edit4a = QLabel("Notch Sensitivity Factor (q): ")
        self.edit2b = QLineEdit("")
        self.edit3b = QLineEdit("")
        self.edit4b = QLineEdit("")
        
        self.edit2b.setDisabled(True)
        self.edit3b.setDisabled(True)
        self.edit4b.setDisabled(True)
        
        self.edit1b = QComboBox()
        self.edit1b.addItems(['Material dropdown','Comparison Chart','Quenched/Tempered Steel','Annealed Steel',
                              'Steel (input Su)','Aluminium Alloy 356.0 as cast',
                              'Aluminium Alloy 6061','Aluminium Alloy 7075'])
        
        self.button1 = QPushButton("OK")
        self.button2 = QPushButton("Cancel")
        
        # signals + slots ()
        self.button1.clicked.connect(self.update)
        self.button2.clicked.connect(self.clearup)
        
        separator1 = QFrame()
        separator2 = QFrame()
        separator1.setFrameShape(QFrame.HLine)
        separator1.setLineWidth(2)
        separator2.setFrameShape(QFrame.HLine)
        separator2.setLineWidth(2)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.edit1a,1,0)
        grid.addWidget(self.edit1b,1,1,1,2)
        grid.addWidget(separator1,2,0,1,3)
        grid.addWidget(self.edit2a,3,0)
        grid.addWidget(self.edit2b,3,1)
        grid.addWidget(self.edit2c,3,2)
        grid.addWidget(self.edit3a,4,0)
        grid.addWidget(self.edit3b,4,1)
        grid.addWidget(self.edit3c,4,2)
        grid.addWidget(separator2,5,0,1,3)
        grid.addWidget(self.edit4a,6,0)
        grid.addWidget(self.edit4b,6,1)
        
        layoutb = QHBoxLayout()
        layoutb.addWidget(self.button1)
        layoutb.addWidget(self.button2)
    
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(self.plot)
        layout.addLayout(grid)
        layout.addLayout(layoutb)
        
        
        self.widget.setLayout(layout) 
        self.setCentralWidget(self.widget) 
                
    def about(self):
        QMessageBox.about(self, 
            "About Notch Sensitivity Analyser",
            """<b>Notch Sensitivity Analyser</b>
               <p>Copyright &copy; 2018 Agniprobho Mazumder, All Rights Reserved.
               <p>Python %s -- Qt %s -- PyQt %s on %s""" %
            (platform.python_version(),
             QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))
        
    def helpMe(self):
        QMessageBox.about(self, 
            "Help Dialog",
            """<p>This window calculates notch sensitivity <b>q</b>. Type the value 
                of the <b>notch radius</b> to automatically calculate <b>q</b>, 
                depending on your choice of material type. Press OK to plot <b>q</b> 
                vs <b>notch radius</b> or get the <b>calculated value of q</b> and
                CANCEL to go back to the main window.
               <p><b><i>Plot Window</i></b> shows the notch sensitivity values as a 
                function of <b>notch radius</b> and <b>Su</b>
               <p><b><i>Su</i></b> is the Ultimate tensile strength. The default value 
                (for all materials) is loaded from the Materials library in the 
                code. For <b>Steel (input Su)</b>, user can input the Su value.
               <p><b><i>Comparison chart</i></b> shows the <b>q</b> vs <b>r</b> plot of all the materials in the library
               <p><b></i>Peterson's notch sensitivity criteria has been used for steel and Neuber's notch sensitivity
                criteria has been used for aluminium</i></b>""")
        
    def saveas(self):
        """Save plot as jpeg/png file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name= QFileDialog.getSaveFileName(self, "Save As","","PNG (*.png)",options=options)[0]
        self.plot.fig.savefig(name)

    def update(self):
        """Update the figure title.
        Evaluate the function and update the plot
        """
        self.plot.draw()
        
        func=str(self.edit1b.currentText())
        if self.win.test()==0:
            x=np.linspace(0,10,200)
        elif self.win.test()==1:
            x=np.linspace(0,0.40,200)
        
        pattern1=r'Steel'
        pattern2=r'Aluminium'
        pattern3=r'[\d]+'
        
        if (func!='Comparison Chart'):
            self.edit2b.setDisabled(False)
            self.edit3b.setDisabled(False)
            self.edit4b.setDisabled(False)
            if (func=='Quenched/Tempered Steel'):
                alpha = 0.0025
            elif (func=='Annealed Steel'):
                alpha = 0.01
            elif (func=='Steel (input Su)'):
                S = str(self.edit2b.text())
                if (self.win.test()==0):
                    S = str(float(S)/6.895)
                alpha = notch.alpha(eval(S))
            elif (func=='Aluminium Alloy 356.0 as cast'):
                rho = 0.08
            elif (func=='Aluminium Alloy 6061'):
                rho = 0.025
            elif (func=='Aluminium Alloy 7075'):
                rho = 0.015
            elif (func=='Material dropdown'):
                pass
            
            y1=[]
            if re.search(pattern1,func):
                Su=notch.su_s(alpha)
                if (self.win.test()==0):
                    Su = Su*6.895
                for i in range(len(x)):
                    y1.append(notch.nsp(alpha,x[i],self.win.test()))
                y=np.asarray(y1)
                if (re.search(pattern3,str(self.edit3b.text()))):
                    r=eval(str(self.edit3b.text()))
                    self.edit4b.setText(str(notch.nsp(alpha,r,self.win.test())))
            elif re.search(pattern2,func):
                Su=notch.su_a(rho)
                if (self.win.test()==0):
                    Su = Su*6.895
                for i in range(len(x)):
                    y1.append(notch.nsn(rho,x[i],self.win.test()))
                y=np.asarray(y1)
                if (re.search(pattern3,str(self.edit3b.text()))):
                    r=eval(str(self.edit3b.text()))
                    self.edit4b.setText(str(notch.nsn(rho,r,self.win.test())))
                
            self.edit2b.setText(str(Su))
            func1 = 'Steel (Su='+str(self.edit2b.text())+')'
            if (func!='Steel (input Su)'):
                self.plot.redraw(x,y,func, self.xlabel)
            elif (func=='Steel (input Su)'):
                self.plot.redraw(x,y,func1, self.xlabel)
            
        elif (func=='Comparison Chart'):
            self.edit2b.setText("")
            self.edit2b.setDisabled(True)
            self.edit3b.setText("")
            self.edit3b.setDisabled(True)
            self.edit4b.setText("")
            self.edit4b.setDisabled(True)
            self.plot.draw_comp(self.xlabel, self.win.test())
        
    def clearup(self):
        """
        close the window
        """
        self.close()    
                
                

class MatplotlibCanvas(FigureCanvas) :
    """ This is borrowed heavily from the matplotlib documentation;
        specifically, see:
        http://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """
    def __init__(self):
        
        # Initialize the figure and axes
        self.fig = Figure() 
        self.fig.subplots_adjust(bottom=0.2)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_xlim([0,10])
        self.axes.set_ylim([0,1])
        
    
        # Give it some default plot
        self.axes.set_title('Plot Window')
        self.axes.set_xlabel('Notch Radius, r') 
        self.axes.set_ylabel('Notch Sensitivity, q')
        self.axes.grid()
        
        # Now do the initialization of the super class
        FigureCanvas.__init__(self, self.fig)
        #self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
         
        
    def redraw(self, x, y, title, xlabel) :
        """ Redraw the figure with new x and y values.
        """
        # clear the old image (axes.hold is deprecated)
        self.fig.clf()
        self.fig.subplots_adjust(bottom=0.2)
        self.axes = self.fig.add_subplot(111)
        self.axes.clear()
        if re.search('mm',xlabel):
            self.axes.set_xlim([0,10])
        elif re.search('in',xlabel):
            self.axes.set_xlim([0,0.4])
        self.axes.set_ylim([0,1])
        self.axes.plot(x, y)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel('Notch Sensitivity, q') 
        self.axes.grid()
        self.draw()
          
    def draw_comp(self, xlabel, val):
        """
            Comparison plot
        """
        self.fig.clf()
        self.fig.subplots_adjust(bottom=0.2)
        self.axes = self.fig.add_subplot(111)
        if re.search('mm',xlabel):
            self.axes.set_xlim([0,10])
            x=np.linspace(0,10,200)
        elif re.search('in',xlabel):
            self.axes.set_xlim([0,0.4])
            x=np.linspace(0,0.40,200)
        self.axes.set_ylim([0,1])
        
        y1=[]
        y2=[]
        y3=[]
        y4=[]
        y5=[]
        for i in range(len(x)):
            y1.append(notch.nsp(0.0025,x[i],val))
            y2.append(notch.nsp(0.01,x[i],val))
            y3.append(notch.nsn(0.08,x[i],val))
            y4.append(notch.nsn(0.025,x[i],val))
            y5.append(notch.nsn(0.015,x[i],val))
        y_1=np.asarray(y1)
        y_2=np.asarray(y2)
        y_3=np.asarray(y3)
        y_4=np.asarray(y4)
        y_5=np.asarray(y5)
        self.axes.plot(x, y_1, 'r-', label='Quenched/Tempered Steel')
        self.axes.plot(x, y_2, 'k-', label='Annealed Steel')
        self.axes.plot(x, y_3, 'g-', label='Aluminium Alloy 356.0 as cast')
        self.axes.plot(x, y_4, 'b-', label='Aluminium Alloy 6061')
        self.axes.plot(x, y_5, 'y-', label='Aluminium Alloy 7075')
        self.axes.legend()
        self.axes.set_title('Comparison Chart')
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel('Notch Sensitivity, q')
        self.axes.grid()
        self.draw()
        
app = QApplication(sys.argv)
form = MainWindow()
form.show()
app.exec_()
