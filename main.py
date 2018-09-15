#!/usr/bin/python

#import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrintPreviewDialog
from PyQt5.QtGui import QColor, QTextCursor, QBrush, QTextCharFormat
from PyQt5.Qsci import *

import sys

#import ui
from MainWindow import *
from AboutDialog import *

# expanduser for finding users home directory
from os.path import expanduser


# jedi for autocomplete
import jedi

# re for finding text
from PyQt5.QtCore import QRegExp

import re


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget.hide()

        # FileMenu
        self.ui.actionNew.triggered.connect(self.New)
        self.ui.actionOpen.triggered.connect(self.openfiledialog)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_As.triggered.connect(self.saveas)
        self.ui.actionQuit.triggered.connect(self.quit)

        # Edit Menu
        self.ui.actionFind.triggered.connect(self.find)
        
        #used in Finding strings
        self.ui.checkBox.clicked.connect(self.regexp)
        self.ui.checkBox_2.clicked.connect(self.casesens)
        self.ui.checkBox_3.clicked.connect(self.wholeword)

        # View Menu
        self.ui.actionWordwrap.triggered.connect(self.wordwrap)
        self.ui.actionShow_line_numbers.triggered.connect(self.linenum)
        self.ui.actionChange_Font.triggered.connect(self.fontchange)
        self.ui.actionchange_font_color.triggered.connect(self.changefontcolor)

        # Help Menu
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionAbout_Qt.triggered.connect(self.about_qt)

        # For Syntax highlighting
        self.ui.actionNormal.triggered.connect(self.normal)
        self.ui.actionBash.triggered.connect(self.bash)
        self.ui.actionBatch.triggered.connect(self.batch)
        self.ui.actionC.triggered.connect(self.cpp)
        self.ui.actionC_2.triggered.connect(self.cpp)
        self.ui.actionC_3.triggered.connect(self.cs)
        self.ui.actionCoffeeScript.triggered.connect(self.cofScript)
        self.ui.actionCSS.triggered.connect(self.css)
        self.ui.actionCmake.triggered.connect(self.cmake)
        self.ui.actionD.triggered.connect(self.D)
        self.ui.actionFortan.triggered.connect(self.Fortran)
        self.ui.actionHTML.triggered.connect(self.HTML)
        self.ui.actionJSON.triggered.connect(self.JSON)
        self.ui.actionLua.triggered.connect(self.Lua)
        self.ui.actionMakeFIle.triggered.connect(self.makefile)
        self.ui.actionMarkDown.triggered.connect(self.markdown)
        self.ui.actionMat.triggered.connect(self.mat)
        self.ui.actionPascal.triggered.connect(self.Pascal)
        self.ui.actionPerl.triggered.connect(self.Perl)
        self.ui.actionPython.triggered.connect(self.python)
        self.ui.actionRuby.triggered.connect(self.Ruby)
        self.ui.actionSQL.triggered.connect(self.sql)
        self.ui.actionTeX.triggered.connect(self.tex)
        self.ui.actionXML.triggered.connect(self.XML)
        self.ui.actionYAML.triggered.connect(self.YAML)

        # for text editor customization
        self.texteditor()

#-------------------------------Syntax Highlighting----------------------------------#

    def normal(self):
        language = None
        self.syntaxhighlight(language)

    def bash(self):
        language = "Bash"
        self.syntaxhighlight(language)

    def batch(self):
        language = "Batch"
        self.syntaxhighlight(language)

    def cpp(self):
        language = "C++"
        self.syntaxhighlight(language)

    def cs(self):
        language = "C#"
        self.syntaxhighlight(language)

    def cofScript(self):
        language = "CoffeeScript"
        self.syntaxhighlight(language)

    def css(self):
        language = "CSS"
        self.syntaxhighlight(language)

    def cmake(self):
        language = "CMake"
        self.syntaxhighlight(language)

    def D(self):
        language = "D"
        self.syntaxhighlight(language)

    def Fortran(self):
        language = "Fortran"
        self.syntaxhighlight(language)

    def HTML(self):
        language = "HTML"
        self.syntaxhighlight(language)

    def JSON(self):
        language = "JSOn"
        self.syntaxhighlight(language)

    def Lua(self):
        language = "Lua"
        self.syntaxhighlight(language)

    def makefile(self):
        language = "Makefile"
        self.syntaxhighlight(language)

    def markdown(self):
        language = "Markdown"
        self.syntaxhighlight(language)

    def mat(self):
        language = "Matlab"
        self.syntaxhighlight(language)

    def Pascal(self):
        language = "Pascal"
        self.syntaxhighlight(language)

    def Perl(self):
        language = "Perl"
        self.syntaxhighlight(language)

    def python(self):
        language = "Python"
        self.syntaxhighlight(language)

    def Ruby(self):
        language = "Ruby"
        self.syntaxhighlight(language)

    def sql(self):
        language = "SQL"
        self.syntaxhighlight(language)

    def tex(self):
        language = "TeX"
        self.syntaxhighlight(language)

    def YAML(self):
        language = "YAML"
        self.syntaxhighlight(language)

    def XML(self):
        language = "XML"
        self.syntaxhighlight(language)


#-----------------------------------------Syntax Highghting---------------------------#

    def texteditor(self):  # Text Editor customization
        self.path = None
        self.openfile = None
        self.ui.textEdit.setIndentationsUseTabs(True)
        self.ui.textEdit.setAutoIndent(True)
        self.ui.textEdit.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.ui.textEdit.setAutoCompletionThreshold(1)
        self.ui.textEdit.setAutoCompletionCaseSensitivity(False)
        self.ui.textEdit.setBraceMatching(1)
        if self.ui.actionWordwrap.isChecked():
            self.ui.textEdit.setWrapMode(QsciScintilla.WrapWord)

        self.fileToLanguage = {
            '': None,
            'txt': None,
            'sh': 'Bash',
            'bat': 'Batch',
            'coffee': 'CoffeeScript',
            'c': 'C++',
            'cpp': 'C++',
            'cxx': 'C++',
            'h': 'C++',
            'hpp': 'C++',
            'hxx': 'C++',
            'cs': 'C#',
            'css': 'CSS',
            'd': 'D',
            'f': 'Fortran',
            'html': 'HTML',
            'java': 'Java',
            'js': 'JavaScript',
            'json': 'JSON',
            'lua': 'Lua',
            'md': 'Markdown',
            'mlx': 'Matlab',
            'pas': 'Pascal',
            'pl': 'Perl',
            'py': 'Python',
            'rb': 'Ruby',
            'sql': 'SQL',
            'yaml': 'YAML',
            'xml': 'XML'
        }

    def New(self):  # Opens New Window
        self.new = MainWindow()
        self.new.show()

    def find(self):#opens find widget
        self.ui.widget.show()
        self.re = False
        self.cs = False
        self.wo = False

        searchtext = self.ui.lineEdit.text()
        self.ui.pushButton.clicked.connect(self.hidefind)
        self.ui.pushButton_2.clicked.connect(self.search)

    def hidefind(self):#closes the find widget
        self.ui.widget.hide()

    #used in finding strings
    
    def regexp(self):
        if self.ui.checkBox.isChecked():
            self.re = True
        else:
            self.re = False

    def casesens(self):
        if self.ui.checkBox_2.isChecked():
            self.cs = True
        else:
            self.cs = False

    def wholeword(self):
        if self.ui.checkBox_3.isChecked():
            self.wo = True
        else:
            self.wo = False

    def search(self):#for finding the strings
        searchtext = self.ui.lineEdit.text()

        self.ui.textEdit.findFirst(
            searchtext, self.re, self.cs, self.wo, False)

    def hidestatbar(self): #hides the statusBar
        self.statusBar.hide()


    def linenum(self):  # Sets Line Number
        if self.ui.actionShow_line_numbers.isChecked():
            self.ui.textEdit.setMarginType(1, QsciScintilla.NumberMargin)
            self.ui.textEdit.setMarginWidth(1, "0000")
        else:
            self.ui.textEdit.setMarginWidth(1, "")

    def about(self):
        AboutDialog().exec_()

    def about_qt(self):
        a = QMessageBox().aboutQt(self)

    def wordwrap(self):  # Word Wrap
        if self.ui.actionWordwrap.isChecked():
            self.ui.textEdit.setWrapMode(QsciScintilla.WrapWord)
        else:
            self.ui.textEdit.setWrapMode(QsciScintilla.WrapNone)

    def openfiledialog(self):  # open file
        home = expanduser('~')
        self.path = QFileDialog.getOpenFileName(self, "Open File", home)[0]
        if self.path:
            self.openfile = open(self.path, 'r')
            text = self.openfile.read()
            self.ui.textEdit.setText(str(text))
            extension = self.path.split('.')[-1]
            if extension in self.fileToLanguage:
                language = self.fileToLanguage.get(extension)
                self.syntaxhighlight(language)
            else:
                self.syntaxhighlight(None)

    def save(self):  # save file
        if self.path is None:
            return self.saveas()
        if self.path:
            text = self.ui.textEdit.text()
            savefile = open(self.path, 'w')
            savefile.write(str(text))

    def saveas(self):  # Save as file
        home = expanduser('~')

        self.path = QFileDialog().getSaveFileName(self, "Save File", home)[0]
        if self.path:
            savefile = open(self.path, 'w')
            text = self.ui.textEdit.text()
            savefile.write(str(text))

    def closeEvent(self, events):
        text = self.ui.textEdit.text()
        if text == "":
            a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                       QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
            if a == QMessageBox().Yes:
                events.accept()
            else:
                events.ignore()
        else:
            if self.path is None:
                a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit", QMessageBox(
                ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                if a == QMessageBox().Yes:
                    self.saveas()
                    events.accept()
                elif a == QMessageBox().No:
                    events.accept()
                else:
                    events.ignore()
            else:
                f = open(self.path, 'r')
                filetext = f.read()
                if filetext == text:
                    a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                               QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
                    if a == QMessageBox().Yes:
                        events.accept()
                    else:
                        events.ignore()
                else:
                    a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit", QMessageBox(
                    ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                    if a == QMessageBox().Yes:
                        self.save()
                        events.accept()
                    elif a == QMessageBox().No:
                        events.accept()
                    else:
                        events.ignore()

    def quit(self):
        text = self.ui.textEdit.text()
        if text == "":
            a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                       QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
            if a == QMessageBox().Yes:
                sys.exit()
            else:
                pass
        else:
            if self.path is None:
                a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit", QMessageBox(
                ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                if a == QMessageBox().Yes:
                    self.saveas()
                    sys.exit()
                elif a == QMessageBox().No:
                    sys.exit()
                else:
                    pass
            else:
                f = open(self.path, 'r')
                filetext = f.read()
                if filetext == text:
                    a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                               QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
                    if a == QMessageBox().Yes:
                        events.accept()
                else:
                    a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit", QMessageBox(
                    ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                    if a == QMessageBox().Yes:
                        self.save()
                        sys.exit()
                    elif a == QMessageBox().No:
                        sys.exit()
                    else:
                        pass

    def syntaxhighlight(self, lexer):
        self.languageToLexer = {
            None: None,
            'Bash': QsciLexerBash,
            'Batch': QsciLexerBatch,
            'CMake': QsciLexerCMake,
            'CoffeeScript': QsciLexerCoffeeScript,
            'C++': QsciLexerCPP,
            'C#': QsciLexerCSharp,
            'CSS': QsciLexerCSS,
            'D': QsciLexerD,
            'Fortran': QsciLexerFortran,
            'HTML': QsciLexerHTML,
            'Java': QsciLexerJava,
            'JavaScript': QsciLexerJavaScript,
            'JSON': QsciLexerJSON,
            'Lua': QsciLexerLua,
            'Makefile': QsciLexerMakefile,
            'Markdown': QsciLexerMarkdown,
            'Matlab': QsciLexerMatlab,
            'Pascal': QsciLexerPascal,
            'Perl': QsciLexerPerl,
            'Python': QsciLexerPython,
            'Ruby': QsciLexerRuby,
            'SQL': QsciLexerSQL,
            'TeX': QsciLexerTeX,
            'YAML': QsciLexerYAML,
            'XML': QsciLexerXML
        }

        lang = self.languageToLexer.get(lexer)
        self.lexer = lang(self)
        self.ui.textEdit.setLexer(self.lexer)
        if lexer == "Python":
            self.autocomplete()

    def autocomplete(self):
        self.api = QsciAPIs(self.lexer)

        source = self.ui.textEdit.text()
        line = 1
        column = 0
        path = ""
        script = jedi.Script(source, line, column, path)
        complete = script.completions()
        l = []

        for i in complete:
            l.append(i.name)
        for i in l:
            self.api.add(i)

        self.api.prepare()

    def fontchange(self):
        changefont, i = QFontDialog().getFont()
        if i:
            self.ui.textEdit.setFont(changefont)

    def changefontcolor(self):
        color = QColorDialog().getColor()
        if color.isValid:
            self.ui.textEdit.setColor(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
