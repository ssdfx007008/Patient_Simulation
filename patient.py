import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import QThread,SIGNAL
import time


class Patient(QThread):
    # the operation list contains all the buttons we  needed in the main window
    # the index will be saved by order, the value will be recorded in states
    # states[0]=HR
    # states[1]=BPH
    # states[2]=BPL
    # states[3]=RR
    # states[4]=SatsPercentage
    # states[5]=SatsDescription

    # next_states[] passes all the states available to the main GUI
    # then it creates a dynamic table for the buttons
    # after specify all the available next states it should connect all the available signals to the next state functions


    def __init__(self,parent):
        super(Patient, self).__init__()
        self.parent=parent
        # when initializing the patient thread, we need to start the thread from the main thread, which is just before displaying the main GUI
        self.connect(parent,SIGNAL("Initialize patient"),self.start)

    def run(self):
        print("Initializing patient")
        self.states=[]
        self.states.append(130)
        self.states.append(85)
        self.states.append(52)
        self.states.append(29)
        self.states.append(89)
        self.states.append( "RA")
        self.next_states=[]
        self.On_state_changed()
        self.GSW_Prehospital()


        # every time the patient state changed, there will be a signal generated to tell the main gui
        # to read the states again and generate a new state display, then a new button list

    def On_state_changed(self):
        print("\r\n\r\nState Changed")
        self.emit(SIGNAL("patient_state_changed"))

    def GSW_Prehospital(self):
        print("GSW_Prehospital")
        self.states[0] = 130
        self.states[1] = 85
        self.states[2] = 52
        self.states[3] = 29
        self.states[4] = 89
        self.states[5] = "RA"
        self.On_state_changed()
        start=time.time()
        a=0
        while time.time()-start < 3 :
            a=a+1
        self.Initial_Trauma_Bay()

    def Initial_Trauma_Bay(self):
        print("Initializing TraumaBay")
        self.states[0] = 134
        self.states[1] = 89
        self.states[2] = 50
        self.states[3] = 30
        self.states[4] = 90
        self.states[5] = "NRB"
        self.next_states=[]
        self.next_states.append("Needle decompression")
        self.connect(self.parent, SIGNAL("Needle decompression"), self.Needle_Decompression)
        self.next_states.append("Place Chest Tube")
        self.connect(self.parent, SIGNAL("Place Chest Tube"), self.Chest_tube_placed)
        self.new_thread = No_chest_tube_300s_timer()
        self.connect(self.new_thread, SIGNAL("No_chest_tube_placed_300s()"), self.No_chest_tube_300s)
        # the timer permission gives the right for the timer to change the state, if 0 then the timer is not allowed to change the patient state
        self.timer_permission = 1
        self.new_thread.start()
        self.On_state_changed()


    def Needle_Decompression(self):
        self.states[0] = 88
        self.states[1] = 108
        self.states[2] = 54
        self.states[3] = 12
        self.states[4] = 98
        self.states[5] = "NRB"
        self.new_thread = No_chest_tube_300s_timer()
        self.connect(self.new_thread, SIGNAL("No_chest_tube_placed_300s()"), self.No_chest_tube_300s)
        self.new_thread.start()
        self.next_states=[]
        self.next_states.append("Place Chest Tube")
        self.connect(self.parent,SIGNAL("Place Chest Tube"),self.Chest_tube_placed)
        self.On_state_changed()

    def Chest_tube_placed(self):
        print("Chest_tube_placed")
        self.states[0] = 87
        self.states[1] = 108
        self.states[2] = 54
        self.states[3] = 12
        self.states[4] = 98
        self.states[5] = "NRB"
        self.timer_permission=0
        self.next_states=[]
        self.On_state_changed()
        self.emit(SIGNAL("Patient Cured"))


    def No_chest_tube_300s(self):
        print("No_chest_tube_300s")
        self.states[0] = 160
        self.states[1] = 55
        self.states[2] = 20
        self.states[3] = 40
        self.states[4] = 82
        self.states[5] = "NRB/No Chest Tube placed for 300s"
        self.new_thread = No_chest_tube_placed_180s_timer(self)
        self.new_thread.start()
        self.connect(self.new_thread, SIGNAL("No_chest_tube_placed"), self.No_chest_tube_placed)
        self.connect(self.parent, SIGNAL("Chest_tube_placed"), self.Chest_tube_placed)
        self.next_states=[]
        self.next_states.append("place chest tube")
        self.On_state_changed()

    def No_chest_tube_placed(self):
        if self.timer_permission==1:
            print("No_chest_tube_placed")
            self.states[0] = 0
            self.states[1] = 0
            self.states[2] = 0
            self.states[3] = 0
            self.states[4] = 0
            self.states[5] = "No_chest_tube_placed/Died"
            self.On_state_changed()


class No_chest_tube_placed_180s_timer(QtCore.QThread):
    def __initial__(self, parent):
        super(No_chest_tube_placed_180s_timer, self).__init__()

    def run(self):
        print("in thread for 180 timer\n")
        start = time.time()
        a = 0
        while (time.time() - start < 3.6):
            a = a + 1
        self.emit(QtCore.SIGNAL("No_chest_tube_placed"))




class No_chest_tube_300s_timer(QtCore.QThread):
    def __init__(self):
        super(No_chest_tube_300s_timer, self).__init__()
    def run(self):
        print("in thread for 300 timer\n")
        start=time.time()
        a=0
        while(time.time()-start<6.0):
            a=a+1
        print("timer stopped\n")
        self.emit(QtCore.SIGNAL("No_chest_tube_placed_300s()"))



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Patient(app)

    sys.exit(app.exec_())
