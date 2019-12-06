import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from SupportClasses import dashboard, databaseconnector, MeetingTypeSelection, MeetingItemSelection, MeetingNumberSelection

class Memory:
	def __init__(self):
		self.meeting = {
			"prefix":"",
			"latestNumber":0,
			"currentNumber":0
		}
		self.operation = "New"

	def set_operation(self, stringIn):
		self.operation = stringIn
	
	def get_operation(self):
		return self.operation

	def set_meeting_prefix(self, stringIn):
		self.meeting["prefix"] = stringIn

	def get_meeting_prefix(self):
		return self.meeting["prefix"]

	def set_meeting_latestNumber(self, intIn):
		self.meeting["latestNumber"] = intIn
		self.set_meeting_currentNumber = intIn+1

	def get_meeting_latestNumber(self):
		return self.meeting["latestNumber"]

	def set_meeting_currentNumber(self, intIn):
		self.meeting["latestNumber"] = intIn

	def get_meeting_currentNumber(self):
		return self.meeting["latestNumber"]

class DashboardW:
    def __init__(self):
        self.window = dashboard.QtWidgets.QMainWindow()
        self.ui = dashboard.Ui_MainWindow()
        self.ui.setupUi(self.window)

class ItemSelectorW:
    def __init__(self):
        self.window = MeetingItemSelection.QtWidgets.QMainWindow()
        self.ui = MeetingItemSelection.Ui_MainWindow()
        self.ui.setupUi(self.window)

class NumberSelectorW:
    def __init__(self):
        self.window = MeetingNumberSelection.QtWidgets.QMainWindow()
        self.ui = MeetingNumberSelection.Ui_MainWindow()
        self.ui.setupUi(self.window)

class TypeSelectorW:
    def __init__(self):
        self.window = MeetingTypeSelection.QtWidgets.QMainWindow()
        self.ui = MeetingTypeSelection.Ui_MainWindow()
        self.ui.setupUi(self.window)

class MessageW:
    def __init__(self):
        self.window = QtWidgets.QMessageBox()

    def showMessage(self, message, details = "", type = ""):
        self.window.setWindowTitle("");
        self.window.setText(message);
        self.window.setDetailedText(details);
        if type=="Warning":
            self.window.setIcon(QtWidgets.QMessageBox.Warning)
        elif type=="Information":
            self.window.setIcon(QtWidgets.QMessageBox.Information)
        elif type =="Critical":
            self.window.setIcon(QtWidgets.QMessageBox.Critical)
        self.window.show()

class Controller:
	def __init__(self):
		self.dbc = databaseconnector.DatabaseConnector()

		self.memory = Memory()

		self.dash = DashboardW()
		self.itemselector = ItemSelectorW()
		self.typeselector = TypeSelectorW()
		self.messageDisplay = MessageW()
		self.numberselector = NumberSelectorW()

		self.connect_buttons()

	##Button Connections##
	def connect_buttons(self):
		self.dash.ui.btnNewMeeting.clicked.connect(lambda : self.dashboard_to_meeting_type("New"))
		self.dash.ui.btnEditMeeting.clicked.connect(lambda : self.dashboard_to_meeting_type("Edit"))

		self.typeselector.ui.btnCancel.clicked.connect(self.meeting_type_to_dashboard)
		self.typeselector.ui.btnOK.clicked.connect(self.meeting_type_to_x)
		
		self.itemselector.ui.btnCancel.clicked.connect(self.meeting_item_to_dashboard)
		self.itemselector.ui.btnAdd.clicked.connect(self.select_item)
		self.itemselector.ui.btnRemove.clicked.connect(self.deselect_item)
		self.itemselector.ui.btnReset.clicked.connect(self.reset_items)

		self.numberselector.ui.btnCancel.clicked.connect(self.meeting_number_to_dashboard)

	######################

	##Window Transitions#
	def show_dashboard(self):
		self.dash.window.show()

	def dashboard_to_meeting_type(self, option = "New"):
		self.memory.set_operation(option)
		self.dash.window.close()
		self.typeselector.window.show()
		self.populate_meeting_types()

	def meeting_type_to_x(self):
		res = self.dbc.get_meeting_prefix_by_type(self.typeselector.ui.cmbMeetingTypes.currentText())
		if res["status"]=="Success":
			self.memory.set_meeting_prefix(res["result"])
			if(self.memory.get_operation=="New"):
				self.typeselector.window.close()
				self.itemselector.window.show()
				self.populate_available_meeting_items()
			elif(self.memory.get_operation=="Edit"):
				self.typeselector.window.close()
				self.numberselector.window.show()
				self.populate_meeting_numbers()
		else:
			pass

	def meeting_type_to_dashboard(self):
		self.typeselector.window.close()
		self.dash.window.show()

	def meeting_item_to_dashboard(self):
		self.itemselector.window.close()
		self.dash.window.show()

	def meeting_number_to_dashboard(self):
		self.numberselector.window.close()
		self.dash.window.show()

	#####################

	##Window Component Setup##
	def populate_meeting_numbers(self):
		res = self.dbc.get_meetings_by_type(self.memory.get_meeting_prefix())
		if res["status"]=="No Records":
			pass
		elif res["status"]=="Success":
			
		else:
			pass

	def populate_meeting_types(self):
		res = self.dbc.get_meeting_types()
		if res["status"]=="Success":
			self.typeselector.ui.cmbMeetingTypes.clear()
			self.typeselector.ui.cmbMeetingTypes.addItems(res["result"])
		else:
			pass
		
	def populate_available_meeting_items(self):
		res = self.dbc.get_last_meeting_by_type(self.memory.get_meeting_prefix())
		if res["status"]=="Success":
			self.memory.set_meeting_latestNumber(res["result"])
			print(self.memory.get_meeting_prefix(), self.memory.get_meeting_latestNumber())
			res2 = self.dbc.get_meeting_items_by_last_meeting(self.memory.get_meeting_prefix(), self.memory.get_meeting_latestNumber())
			if res2["status"]=="Success":
				self.itemselector.ui.lstAvailable.addItems(res2["result"])
			else:
				pass
		else:
			pass

	def select_item(self):
		if self.itemselector.ui.lstAvailable.currentItem() != None:
			self.itemselector.ui.lstSelected.addItems([self.itemselector.ui.lstAvailable.currentItem().text()])
			items = self.itemselector.ui.lstAvailable.selectedItems()
			for item in items:
				self.itemselector.ui.lstAvailable.takeItem(self.itemselector.ui.lstAvailable.row(item))
			listWidget = self.itemselector.ui.lstSelected
			print(f" Selected: {[str(listWidget.item(i).text()) for i in range(listWidget.count())]}")

	def deselect_item(self):
		if self.itemselector.ui.lstSelected.currentItem() != None:
			self.itemselector.ui.lstAvailable.addItems([self.itemselector.ui.lstSelected.currentItem().text()])
			items = self.itemselector.ui.lstSelected.selectedItems()
			for item in items:
				self.itemselector.ui.lstSelected.takeItem(self.itemselector.ui.lstSelected.row(item))
			listWidget = self.itemselector.ui.lstAvailable
			print(f" Deselected:{[str(listWidget.item(i).text()) for i in range(listWidget.count())]}")

	def reset_items(self):
		self.itemselector.ui.lstSelected.clear()
		self.itemselector.ui.lstSelected.clear()
		self.populate_available_meeting_items()

		
	########################

def main():
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.show_dashboard()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()