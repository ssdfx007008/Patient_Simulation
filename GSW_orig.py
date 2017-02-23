import sys
from PyQt4 import  QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QThread,SIGNAL

from patient import Patient

class GSW(QtGui.QWidget):


    def __init__(self):
        super(GSW,self).__init__()
        self.patient=Patient(self)
        self.initUI()

    # the GUI contains two major layout, patient_states and operation_options
    # the main thread here is the GUI
    # the second thread is the patient
    # we grab all the data we have from the second thread and display it on GUI(main thread)
    # the GUI interact with second thread using signals
    def initUI(self):
        self.mainlayout=QtGui.QVBoxLayout()
        self.patient_states=QtGui.QBoxLayout(0x1)
        self.mainlayout.addLayout(self.patient_states)
        self.add_States_to_layout()
        self.operation_options=QtGui.QBoxLayout(0x1)
        self.mainlayout.addLayout(self.operation_options)
        self.setLayout(self.mainlayout)
        self.setWindowTitle('GSW')
        self.connect(self.patient,SIGNAL("patient_state_changed"),self.State_changed)
        self.connect(self.patient,SIGNAL("Patient Cured"),self.Patient_Cured)
        self.emit(SIGNAL("Initialize patient"))
        self.show()

    def State_changed(self):
        print("show changed states on GUI")
        self.add_Button_to_layout()
        self.set_States_to_layout()


    def set_States_to_layout(self):
        print("start set_States_to_layout")
        self.HR.setPlainText("HR"+"\r\n"+str(self.patient.states[0]))
        self.BPH.setPlainText("BPH"+"\r\n"+str(self.patient.states[1]))
        self.BPL.setPlainText("BPL"+"\r\n"+str(self.patient.states[2]))
        self.RR.setPlainText("RR"+"\r\n"+str(self.patient.states[3]))
        self.SatsPercentage.setPlainText("SatsPercentage"+"\r\n"+str(self.patient.states[4]))
        self.SatsDescription.setPlainText("SatsDescription"+"\r\n"+str(self.patient.states[5]))
        print("finished set_States_to_layout")


    def add_States_to_layout(self):
        print("start add_States_to_layout")
        self.HR = QtGui.QPlainTextEdit("HR")
        self.BPH = QtGui.QPlainTextEdit("BPH")
        self.BPL = QtGui.QPlainTextEdit("BPL")
        self.RR = QtGui.QPlainTextEdit("RR")
        self.SatsPercentage = QtGui.QPlainTextEdit("SatsPercentage")
        self.SatsDescription = QtGui.QPlainTextEdit("SatsDescription")
        self.patient_states.addWidget(self.HR )
        self.patient_states.addWidget(self.BPH)
        self.patient_states.addWidget(self.BPL)
        self.patient_states.addWidget(self.RR)
        self.patient_states.addWidget(self.SatsPercentage)
        self.patient_states.addWidget(self.SatsDescription)

    def add_Button_to_layout(self):
        i=0
        print("starting  loop of adding buttons")
        for i in reversed(range(self.operation_options.count())):
            self.operation_options.itemAt(i).widget().setParent(None)
        if self.patient.next_states!=[] :
            for name in self.patient.next_states:
                print("adding Buttons")
                new_buttons=QtGui.QPushButton(name)
                self.operation_options.addWidget(new_buttons)
                new_buttons.clicked.connect(self.button_clicked)
        print("finished adding")

    def button_clicked(self):
        self.emit(SIGNAL(self.sender().text()))

    def Patient_Cured(self):
        reply = QtGui.QMessageBox.question(self, 'Message',"Patient is cured")
        self.past_treatment.setText(self.past_treatment.toPlainText()+"\r\n"+self.sender().text())
        self.mainlayout.patientstate.adjustSize()

        
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    ex = GSW()
    sys.exit(app.exec_())
