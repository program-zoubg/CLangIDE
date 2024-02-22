"""
LICENSE: GPL v3
Author: Program-zoubg
Copyright (c) CLangIDE 2024

██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗     ███████╗ ██████╗ ██╗   ██╗██████╗  ██████╗
██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║     ╚══███╔╝██╔═══██╗██║   ██║██╔══██╗██╔════╝
██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║█████╗ ███╔╝ ██║   ██║██║   ██║██████╔╝██║  ███╗
██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║╚════╝███╔╝  ██║   ██║██║   ██║██╔══██╗██║   ██║
██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║     ███████╗╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝

 ██████╗██╗      █████╗ ███╗   ██╗ ██████╗ ██╗██████╗ ███████╗
██╔════╝██║     ██╔══██╗████╗  ██║██╔════╝ ██║██╔══██╗██╔════╝
██║     ██║     ███████║██╔██╗ ██║██║  ███╗██║██║  ██║█████╗
██║     ██║     ██╔══██║██║╚██╗██║██║   ██║██║██║  ██║██╔══╝
╚██████╗███████╗██║  ██║██║ ╚████║╚██████╔╝██║██████╔╝███████╗
 ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═════╝ ╚══════╝
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QMessageBox, QAction, QStatusBar, QFileDialog, QInputDialog, QLineEdit
from PyQt5.Qsci import QsciScintilla, QsciLexerCPP
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap

with open('config/config.ini', 'r') as f:
    if f.read() == 'cpp':
        codetype = 'cpp'
    else:
        codetype = 'c'
filename = f"untitled.{codetype}"
IsSave = False


# Highlight of C/C++
class highlight(QsciLexerCPP):
    def __init__(self, parent):
        QsciLexerCPP.__init__(self, parent)
        font = QFont()
        font.setFamily('Consolas')
        font.setPointSize(12)
        self.setFont(font)
        self.setFont(QFont('Consolas', 12, italic=True), QsciLexerCPP.Comment)
        self.setFont(QFont('Consolas', 12, italic=True), QsciLexerCPP.CommentLine)
        self.setFont(QFont("Consolas", 12, weight=QFont.Bold), QsciLexerCPP.Keyword)


# Class of Main window
class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Global
        self.setWindowTitle("CLangIDE - " + filename)
        self.setGeometry(100, 100, 800, 600)
        self.center()
        icon = QIcon()
        icon.addPixmap(QPixmap("./bin/window.ico"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)

        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        # Editor
        self.editor = QsciScintilla(self)
        self.setCentralWidget(self.editor)
        lexer = highlight(self)
        self.editor.setLexer(lexer)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor('lightyellow'))
        self.editor.setIndentationsUseTabs(True)
        self.editor.setIndentationWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(True)
        self.editor.setTabWidth(4)
        self.editor.setMarginsFont(font)
        self.editor.setMarginLineNumbers(0, True)
        self.editor.setMarginWidth(0, '000')
        self.editor.setMarkerForegroundColor(QColor("white"), 0)
        self.editor.setEolMode(QsciScintilla.EolUnix)
        self.editor.setAutoIndent(True)
        self.editor.setUtf8(True)
        self.editor.textChanged.connect(self.Changed)

        # StatusBar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # Menu
        self.menu = self.menuBar()
        self.FileOperator = self.menu.addMenu("文件")
        self.TextOperator = self.menu.addMenu("编辑")
        self.RunOperator = self.menu.addMenu("运行")
        self.HelpOperator = self.menu.addMenu("帮助")
        # FileOperator
        self.NewAction = QAction("新建", self)
        self.NewAction.setStatusTip("新建一个源代码文件")
        self.NewAction.setShortcut("Ctrl+N")
        self.NewAction.triggered.connect(self.NewFile)
        self.FileOperator.addAction(self.NewAction)
        self.OpenAction = QAction("打开", self)
        self.OpenAction.setStatusTip("打开一个源代码文件")
        self.OpenAction.setShortcut("Ctrl+O")
        self.OpenAction.triggered.connect(self.OpenFile)
        self.FileOperator.addAction(self.OpenAction)
        self.SaveAction = QAction("保存", self)
        self.SaveAction.setStatusTip("保存源代码文件")
        self.SaveAction.setShortcut("Ctrl+S")
        self.SaveAction.triggered.connect(self.savefile)
        self.FileOperator.addAction(self.SaveAction)
        self.SavesAction = QAction("另存为", self)
        self.SavesAction.setStatusTip("另存为源代码文件")
        self.SavesAction.setShortcut("Ctrl+Shift+S")
        self.FileOperator.addAction(self.SavesAction)
        self.CloseAction = QAction("退出", self)
        self.CloseAction.setStatusTip("退出进程并关闭窗口")
        self.CloseAction.setShortcut("Ctrl+Q")
        self.CloseAction.triggered.connect(self.close)
        self.FileOperator.addAction(self.CloseAction)
        # TextOperator
        self.UndoAction = QAction("撤销", self)
        self.UndoAction.setStatusTip("撤销上一步操作")
        self.UndoAction.setShortcut("Ctrl+Z")
        self.UndoAction.triggered.connect(self.editor.undo)
        self.RedoAction = QAction("重做", self)
        self.RedoAction.setStatusTip("重做上一步操作")
        self.RedoAction.setShortcut("Ctrl+Shift+Z")
        self.RedoAction.triggered.connect(self.editor.redo)
        self.CutAction = QAction("剪切", self)
        self.CutAction.setStatusTip("剪切文本到其他地方")
        self.CutAction.setShortcut("Ctrl+X")
        self.CutAction.triggered.connect(self.editor.cut)
        self.CopyAction = QAction("复制", self)
        self.CopyAction.setStatusTip("复制文本到其他地方")
        self.CopyAction.setShortcut("Ctrl+C")
        self.CopyAction.triggered.connect(self.editor.copy)
        self.PAction = QAction("粘贴", self)
        self.PAction.setStatusTip("把剪贴板里的文本拷贝到此处")
        self.PAction.setShortcut("Ctrl+V")
        self.PAction.triggered.connect(self.editor.paste)
        self.AllAction = QAction("全选", self)
        self.AllAction.setStatusTip("全选文本内容")
        self.AllAction.setShortcut("Ctrl+A")
        self.AllAction.triggered.connect(self.editor.selectAll)
        self.TextOperator.addAction(self.UndoAction)
        self.TextOperator.addAction(self.RedoAction)
        self.TextOperator.addAction(self.CutAction)
        self.TextOperator.addAction(self.CopyAction)
        self.TextOperator.addAction(self.PAction)
        self.TextOperator.addAction(self.AllAction)
        # RunOperator
        self.CompileAction = QAction("编译", self)
        self.RunAction = QAction("运行", self)
        self.CompileAndRunAction = QAction("编译并运行", self)
        self.CompileAction.setShortcut("F5")
        self.RunAction.setShortcut("F10")
        self.CompileAndRunAction.setShortcut("F11")
        self.CompileAction.setStatusTip("编译源代码并生成可执行程序")
        self.RunAction.setStatusTip("运行可执行程序")
        self.CompileAndRunAction.setStatusTip("编译源代码生成可执行程序并运行")
        self.CompileAction.triggered.connect(self.compile_btn)
        self.RunAction.triggered.connect(self.run_btn)
        self.CompileAndRunAction.triggered.connect(self.CompileAndRun_btn)
        self.RunOperator.addAction(self.CompileAction)
        self.RunOperator.addAction(self.RunAction)
        self.RunOperator.addAction(self.CompileAndRunAction)
        # HelpOperator
        self.AboutAction = QAction("关于CLangIDE", self)
        self.AboutAction.setStatusTip("关于CLangIDE的更多信息")
        self.AboutAction.triggered.connect(self.about)
        self.HelpOperator.addAction(self.AboutAction)

    def Changed(self):
        global IsSave
        IsSave = False
        self.setWindowTitle("CLangIDE - " + filename + "*")

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        sizes = self.geometry()
        WindowLeft, WindowTop = int((screen.width() - sizes.width()) / 2), int((screen.height() - sizes.height()) * (1 - 0.618))  # It's purely a live job. It's the golden ratio.
        self.move(WindowLeft, WindowTop)

    def compile_btn(self):
        try:
            global filename
            self.savefile()
            os.system(f"bin\\MinGW\\bin\\g++.exe -o {filename}.exe {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Return error：\n{e}")

    def run_btn(self):
        try:
            global filename
            os.system(f'start cmd /C "{filename}.exe & pause"')
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Return error：\n{e}")

    def CompileAndRun_btn(self):
        try:
            self.compile_btn()
            self.run_btn()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Return error：\n{e}")

    def NewFile(self):
        try:
            global filename, codetype
            self.editor.setText("")
            filename = f"untitled.{codetype}"
            self.setWindowTitle("CLangIDE - " + filename + "*")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Return error：\n{e}")

    def savefile(self):
        try:
            global filename, codetype
            if f"untitled.{codetype}" == filename:
                filews = QMessageBox.question(self, "重命名", "是否重命名？",
                                                        QMessageBox.Yes | QMessageBox.No,
                                                        QMessageBox.Yes)
                if filews == QMessageBox.Yes:
                    filename, ok = QInputDialog.getText(self, "重命名", "请输入重命名标题：", QLineEdit.Normal, "title")
                    filename = filename+"."+codetype
            savefile = open(filename, 'w+', encoding='utf-8')
            will = self.editor.text()
            savefile.write(will)
            savefile.close()
            global IsSave
            IsSave = True
            self.setWindowTitle("CLangIDE - " + filename)
        except Exception as e:
            QMessageBox.about(self, "错误", f"发生错误：\n{e}")

    def OpenFile(self):
        try:
            global filename, IsSave
            filename, _buff = QFileDialog.getOpenFileName(self, '打开', './', '源代码 (*.*)')
            if filename:
                if not IsSave:
                    filews = QMessageBox.question(self, "未保存", "是否保存？",
                                                            QMessageBox.Yes | QMessageBox.No,
                                                            QMessageBox.Yes)
                    if filews == QMessageBox.Yes:
                        self.savefile()
                self.editor.setText("")
                with open(filename, 'r', encoding='utf-8') as obj:
                    for objs in obj.readlines():
                        self.editor.setText(self.editor.text() + objs)
                filename = filename.replace("/", "\\")
                self.setWindowTitle("CLangIDE - " + filename)
            IsSave = True
        except Exception as e:
            QMessageBox.about(self, "错误", f"发生错误：\n{e}")

    def about(self):
        ideversion = "1.0.0 2024.2 Release"
        QMessageBox.about(self, "关于CLangIDE",
                                    f"Copyright (c) 2024 CLangIDE\n\nC/C++ Core: MinGW-w64\nCLangIDE version: {ideversion}\nCompile Core: GCC\nOpen Source: Github - Program-zoubg/CLangIDE\nOpen Source LICENSE: GPL v3\n\nThank you!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())

