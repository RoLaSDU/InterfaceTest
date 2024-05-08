import sys
import subprocess  # Import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtCore import QCoreApplication


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.processes = [QProcess(self) for _ in range(6)]  # To keep track of running processes
        self.init_ui()
        
        #excecuted when clicking on the close icon
        QCoreApplication.instance().aboutToQuit.connect(self.kill_all_commands)

    def init_ui(self):
        vbox = QVBoxLayout()

        self.output_windows = [QTextEdit() for _ in range(6)]
        self.buttons = [QPushButton(f'Button {i+1}') for i in range(6)]
        self.kill_buttons = [QPushButton(f'Kill {i+1}') for i in range(6)]

        self.buttons[0].setText("Start\nGazebo")
        self.kill_buttons[0].setText("Kill\nGazebo")

        self.buttons[1].setText("Start\nMavRos")
        self.kill_buttons[1].setText("Kill\nMavRos")

        self.buttons[2].setText("Start\nOffboard\nControl")
        self.kill_buttons[2].setText("Kill\nOffboard\nControl")

        self.buttons[3].setText("Start\nVRPN\nto\nROS2")
        self.kill_buttons[3].setText("Kill\nVRPN\nto\nROS2")

        self.buttons[4].setText("Start\nTCP\nEndpoint\n(Unity)")
        self.kill_buttons[4].setText("Kill\nTCP\nEndpoint\n(Unity)")
        
        self.buttons[5].setText("Start\nWindwall\nTest")
        self.kill_buttons[5].setText("Kill\nWindwall\nTest")


        for i in range(6):
            self.buttons[i].clicked.connect(lambda _, i=i: self.execute_command(i))
            self.buttons[i].setMinimumSize(100, 150)  # Set a minimum size for the buttons
            font = self.buttons[i].font()
            font.setPointSize(18)  # Set font size to 18 points
            self.buttons[i].setFont(font)

            self.kill_buttons[i].clicked.connect(lambda _, i=i: self.kill_command(i))
            self.kill_buttons[i].setMinimumSize(100, 150)  # Set a minimum size for the kill buttons
            self.kill_buttons[i].setFont(font)

            self.processes[i].readyReadStandardOutput.connect(lambda i=i: self.read_output(i))
            self.processes[i].readyReadStandardError.connect(lambda i=i: self.read_error(i))

        top_half = QHBoxLayout()
        for output_window in self.output_windows:
            top_half.addWidget(output_window)

        bottom_half = QVBoxLayout()
        button_row = QHBoxLayout()
        kill_button_row = QHBoxLayout()

        for button in self.buttons:
            button_row.addWidget(button)

        for kill_button in self.kill_buttons:
            kill_button_row.addWidget(kill_button)

        bottom_half.addLayout(button_row)
        bottom_half.addLayout(kill_button_row)

        splitter = QSplitter(Qt.Vertical)
        vbox.addWidget(splitter)

        top_widget = QWidget()
        top_widget.setLayout(top_half)
        splitter.addWidget(top_widget)

        bottom_widget = QWidget()
        bottom_widget.setLayout(bottom_half)
        splitter.addWidget(bottom_widget)

        splitter.setSizes([2000, self.height()])  # Adjust this line to set the splitter position

        self.setLayout(vbox)

    #Put each of the scripts into it's own wrapper, so they get killed correctly TODO: Find a better method?
    def execute_command(self, i):
        match i:
            case 0:
                program = "python"
                arguments = ["wrapper.py", "./startGazebo_wrap.sh"]
                self.processes[i].start(program, arguments)
            case 1:
                program = "python"
                arguments = ["wrapper2.py", "./startMavROS_wrap.sh"]
                self.processes[i].start(program, arguments)
            case 2:
                program = "python"
                arguments = ["wrapper3.py", "./startOffboardCtrl_wrap.sh"]
                self.processes[i].start(program, arguments)
            case 3:
                program = "python"
                arguments = ["wrapper4.py", "./startVRPN_wrap.sh"]
                self.processes[i].start(program, arguments)
            case 4:
                program = "python"
                arguments = ["wrapper5.py", "./startTCP_Endpoint_wrap.sh"]
                self.processes[i].start(program, arguments)
            case 5:
                program = "python"
                arguments = ["wrapper6.py", "./startWindwallTest.sh"]
                self.processes[i].start(program, arguments)
            case _:
                self.output_windows[i].append(f'You pressed button {i + 1}')

    def kill_command(self, i):
        if self.processes[i] is not None and self.processes[i].state() == QProcess.Running:
            pid = self.processes[i].processId()
            command = f'/bin/pkill -INT -g {pid}'  # Specify the full path to pkill
            subprocess.run(command, shell=True)  # Use subprocess to run the command
            self.output_windows[i].append('Sent SIGINT to process group')

    def read_output(self, i):
        output = self.processes[i].readAllStandardOutput().data().decode()
        self.output_windows[i].append(output)

    def read_error(self, i):
        error = self.processes[i].readAllStandardError().data().decode()
        self.output_windows[i].append(error)

    def kill_all_commands(self):
        for i in range(5):
            self.kill_command(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.showMaximized()
    sys.exit(app.exec_())
