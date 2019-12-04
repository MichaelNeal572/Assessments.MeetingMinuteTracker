import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from SupportClasses import dashboard, databaseconnector, MeetingTypeSelection, MeetingItemSelection

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

		self.dash = DashboardW()
		self.itemselector = ItemSelectorW()
		self.typeselector = TypeSelectorW()
		self.messageDisplay = MessageW()

		self.connect_buttons()

	##Button Connections##
	def connect_buttons(self):
		self.dash.ui.btnNewMeeting.clicked.connect(self.dashboard_to_meeting_type)

		self.typeselector.ui.btnCancel.clicked.connect(self.meeting_type_to_dashboard)
		self.typeselector.ui.btnOK.clicked.connect(self.meeting_type_to_meeting_item)
		
		self.itemselector.ui.btnCancel.clicked.connect(self.meeting_item_to_dashboard)
	######################

	##Window Transitions#
	def show_dashboard(self):
		self.dash.window.show()

	def dashboard_to_meeting_type(self):
		self.dash.window.close()
		self.typeselector.window.show()

	def meeting_type_to_meeting_item(self):
		self.typeselector.window.close()
		self.itemselector.window.show()

	def meeting_type_to_dashboard(self):
		self.typeselector.window.close()
		self.dash.window.show()

	def meeting_item_to_dashboard(self):
		self.itemselector.window.close()
		self.dash.window.show()

	#####################

	##Database Interaction##
	def populate_meeting_types(self):
		pass

	def populate_available_meeting_items(self):
		pass
	########################

def main():
	app = QtWidgets.QApplication(sys.argv)
	controller = Controller()
	controller.show_dashboard()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()