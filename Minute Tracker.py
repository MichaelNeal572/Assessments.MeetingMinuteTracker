import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from SupportClasses import dashboard, databaseconnector, MeetingTypeSelection, MeetingItemSelection, MeetingNumberSelection, MeetingItemEditor

class Memory:
	def __init__(self):
		self.meeting = {
			"prefix":"",
			"latestNumber":0,
			"currentNumber":0
		}
		self.operation = "New"

		self.meetingItems = []

	def set_meetingItems(self, lstIn):
		self.operation = lstIn
	
	def get_meetingItems(self):
		return self.operation

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
		self.set_meeting_currentNumber(intIn+1)

	def get_meeting_latestNumber(self):
		return self.meeting["latestNumber"]

	def set_meeting_currentNumber(self, intIn):
		self.meeting["currentNumber"] = intIn

	def get_meeting_currentNumber(self):
		return self.meeting["currentNumber"]

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

class ItemEditorW:
    def __init__(self):
        self.window = MeetingItemEditor.QtWidgets.QMainWindow()
        self.ui = MeetingItemEditor.Ui_MainWindow()
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
		self.itemeditor = ItemEditorW()

		self.connect_buttons()

	##Button Connections##
	def connect_buttons(self):
		self.dash.ui.btnNewMeeting.clicked.connect(lambda : self.dashboard_to_meeting_type("New"))
		self.dash.ui.btnEditMeeting.clicked.connect(lambda : self.dashboard_to_meeting_type("Edit"))
		self.dash.ui.btnExit.clicked.connect(self.exit_program)

		self.typeselector.ui.btnCancel.clicked.connect(self.meeting_type_to_dashboard)
		self.typeselector.ui.btnOK.clicked.connect(self.meeting_type_to_x)
		
		self.itemselector.ui.btnCancel.clicked.connect(self.meeting_item_to_dashboard)
		self.itemselector.ui.btnAdd.clicked.connect(self.select_item)
		self.itemselector.ui.btnRemove.clicked.connect(self.deselect_item)
		self.itemselector.ui.btnReset.clicked.connect(self.populate_available_meeting_items)
		self.itemselector.ui.btnOK.clicked.connect(self.meeting_item_to_item_editor)

		self.numberselector.ui.btnCancel.clicked.connect(self.meeting_number_to_dashboard)
		self.numberselector.ui.btnOK.clicked.connect(self.number_selector_to_item_editor)

		self.itemeditor.ui.btnSaveQuit.clicked.connect(self.editor_to_dashboard)
		self.itemeditor.ui.btnClear.clicked.connect(self.item_editor_clear_fields)
		self.itemeditor.ui.btnUpdate.clicked.connect(self.update_selected_item)
		self.itemeditor.ui.tblItem.clicked.connect(self.item_editor_populate_fields)

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
			if(self.memory.get_operation()=="New"):
				self.typeselector.window.close()
				self.itemselector.window.show()
				self.populate_available_meeting_items()
			elif(self.memory.get_operation()=="Edit"):
				self.typeselector.window.close()
				self.numberselector.window.show()
				self.populate_meeting_numbers()
		else:
			self.messageDisplay.showMessage(message = "Error connecting to database", details =res["result"] , type ="Critical")
			self.meeting_type_to_dashboard()

	def meeting_type_to_dashboard(self):
		self.typeselector.window.close()
		self.dash.window.show()

	def meeting_item_to_dashboard(self):
		self.itemselector.window.close()
		self.dash.window.show()

	def editor_to_dashboard(self):
		self.itemeditor.window.close()
		self.dash.window.show()

	def meeting_number_to_dashboard(self):
		self.numberselector.window.close()
		self.dash.window.show()

	def meeting_item_to_item_editor(self):
		listWidget = self.itemselector.ui.lstSelected
		self.memory.set_meetingItems([str(listWidget.item(i).text()) for i in range(listWidget.count())])
		self.setup_new_meeting()
		self.itemselector.window.close()
		self.itemeditor.window.show()
		self.refresh_table()

	def number_selector_to_item_editor(self):
		self.memory.set_meeting_currentNumber(int(self.numberselector.ui.cmbMeetingNumbers.currentText()))
		self.numberselector.window.close()
		self.itemeditor.window.show()
		self.refresh_table()

	def exit_program(self):
		sys.exit()

	#####################

	##Window Component Setup##
	def refresh_table(self):
		table = self.itemeditor.ui.tblItem
		res = self.dbc.get_all_meeting_items_by_meeting(self.memory.get_meeting_prefix(), self.memory.get_meeting_currentNumber())
		if res["status"]=="Success":
			for i in range(table.rowCount())[::-1]:
				table.removeRow(i)

			for record in res["result"]:
				nextRow = table.rowCount()
				table.insertRow(nextRow)
				c=0
				try:
					for r in record:
						table.setItem(nextRow,c,QtWidgets.QTableWidgetItem(str(r)))
						c+=1
				except Exception as e:
					print(f"table exception: {str(e)}")
		else:
			self.messageDisplay.showMessage(message = "Error connecting to database", details =res["result"] , type ="Critical")

	def setup_new_meeting(self):
		res = self.dbc.insert_meeting(self.memory.get_meeting_prefix(), self.memory.get_meeting_currentNumber())
		if res["status"]=="Success":
			res2 = self.dbc.insert_meeting_item_statuses(self.memory.get_meetingItems(), self.memory.get_meeting_prefix(), self.memory.get_meeting_currentNumber())
			if res2["status"]=="Error":
				self.messageDisplay.showMessage(message = "Error populating meeting items", details =res2["result"] , type ="Critical")
		else:
			self.messageDisplay.showMessage(message = "Error creating meeting", details =res["result"] , type ="Critical")

	def update_selected_item(self):
		item = self.itemeditor.ui.txtItem.text()
		actions = self.itemeditor.ui.txtActions.text()
		person = self.itemeditor.ui.txtPerson.text()
		prefix = self.memory.get_meeting_prefix()
		number = self.memory.get_meeting_currentNumber()
		res = self.dbc.update_meeting_item(item, prefix, number, actions, person)
		if res["status"]=="Success":
			self.refresh_table()
			self.messageDisplay.showMessage(message = "Success", details ="Meeting Item Successfully updated" , type ="Information")
		else:
			self.messageDisplay.showMessage(message = "Database Failure", details =res["result"] , type ="Warning")

	def item_editor_clear_fields(self):
		self.itemeditor.ui.txtItem.setText("")
		self.itemeditor.ui.txtActions.setText("")
		self.itemeditor.ui.txtPerson.setText("")

	def item_editor_populate_fields(self):
		table = self.itemeditor.ui.tblItem
		row = table.selectedIndexes()[-1].row()
		self.itemeditor.ui.txtItem.setText(table.item(row, 0).text())
		self.itemeditor.ui.txtActions.setText(table.item(row, 1).text())
		self.itemeditor.ui.txtPerson.setText(table.item(row, 2).text())

	def populate_meeting_numbers(self):
		res = self.dbc.get_meeting_numbers_by_type(self.memory.get_meeting_prefix())
		if res["status"]=="No Records":
			self.messageDisplay.showMessage(message = "There are no previous meetings of this type", details = "Please create a new meeting or contact administration for assistance" , type ="Critical")

		elif res["status"]=="Success":
			self.numberselector.ui.cmbMeetingNumbers.clear()
			self.numberselector.ui.cmbMeetingNumbers.addItems([str(i) for i in res["result"]])
		else:
			self.messageDisplay.showMessage(message = "Error connecting to database", details =res["result"] , type ="Critical")

	def populate_meeting_types(self):
		res = self.dbc.get_meeting_types()
		if res["status"]=="Success":
			self.typeselector.ui.cmbMeetingTypes.clear()
			self.typeselector.ui.cmbMeetingTypes.addItems(res["result"])
		else:
			self.messageDisplay.showMessage(message = "Error connecting to database", details =res["result"] , type ="Critical")
		
	def populate_available_meeting_items(self):
		res = self.dbc.get_last_meeting_by_type(self.memory.get_meeting_prefix())
		if res["status"]=="Success":
			self.memory.set_meeting_latestNumber(res["result"])
			res2 = self.dbc.get_meeting_items_by_last_meeting(self.memory.get_meeting_prefix(), self.memory.get_meeting_latestNumber())
			if res2["status"]=="Success":
				self.itemselector.ui.lstSelected.clear()
				self.itemselector.ui.lstSelected.clear()
				self.itemselector.ui.lstAvailable.addItems(res2["result"])
			else:
				self.messageDisplay.showMessage(message = "Error connecting to database", details =res["result"] , type ="Critical")
		else:
			self.messageDisplay.showMessage(message = "Error connecting to database", details =res["result"] , type ="Critical")

	def select_item(self):
		if self.itemselector.ui.lstAvailable.currentItem() != None:
			self.itemselector.ui.lstSelected.addItems([self.itemselector.ui.lstAvailable.currentItem().text()])
			items = self.itemselector.ui.lstAvailable.selectedItems()
			for item in items:
				self.itemselector.ui.lstAvailable.takeItem(self.itemselector.ui.lstAvailable.row(item))

	def deselect_item(self):
		if self.itemselector.ui.lstSelected.currentItem() != None:
			self.itemselector.ui.lstAvailable.addItems([self.itemselector.ui.lstSelected.currentItem().text()])
			items = self.itemselector.ui.lstSelected.selectedItems()
			for item in items:
				self.itemselector.ui.lstSelected.takeItem(self.itemselector.ui.lstSelected.row(item))

	########################

def main():
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.show_dashboard()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()