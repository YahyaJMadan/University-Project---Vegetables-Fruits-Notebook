import os
from PIL import Image

from PyQt6.QtCore import Qt, QSize, QDir
from PyQt6.QtGui import QIcon, QAction, QFont, QPixmap
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QMainWindow, QStackedLayout, QLabel, QCheckBox, QLineEdit, QGridLayout, QComboBox, QStatusBar, QFileDialog, \
    QListWidget, \
    QAbstractItemView, QToolBar, QMessageBox, QInputDialog

import databaseOriginal
from database import *


class Window(QMainWindow):
    def __init__(self):
        # Activating the loops for the app.
        super().__init__()
        self.editing_idVegFruit = None
        self.main_frame()
        self.main_menuBar()
        self.main_section()
        self.create_tables()
        self.edit_mode_VegFruit()
        self.edit_mode_todolist()
        self.load_table_VegFruit()
        self.load_table_todolist()
        self.populate_edit_mode_original_list()
        self.main_screen()
        self.main_layout()
        self.layout_switch_table_checkbox_clicked()

#Main Frame & Menu

    def main_frame(self):
        # The main settings of the window app.
        self.setWindowTitle("Vegetables & Fruits in Bahrain")
        self.resize(1600, 800)
        self.icon = "images/fruit.png"
        self.icon_toolbar = "images/arrow-turn-180-left.png"
        self.setWindowIcon(QIcon(self.icon))

    def main_menuBar(self):
        # Sets the menu to switch between two layouts, one with the main table for VEG&Fruit data and the other for todolist table.
        button_action = QAction(QIcon(self.icon), "&Vegetables and Fruits Table", self)
        button_action.setStatusTip("Switches to Vegetables & Fruits Table")
        button_action.triggered.connect(self.menubar_button_clicked1)
        button_action.setCheckable(True)

        button_action2 = QAction(QIcon(self.icon), "&Todolist Table", self)
        button_action2.setStatusTip("Switches to the Todolist Table")
        button_action2.triggered.connect(self.menubar_button_clicked2)
        button_action2.setCheckable(True)

        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

        toolbar_action = QAction(QIcon(self.icon_toolbar), "&Main Menu", self)
        toolbar_action.setStatusTip("Return to Main Menu")
        toolbar_action.triggered.connect(self.toolbar_action_clicked)
        self.toolbar.addAction(toolbar_action)
        self.toolbar.close()

        self.setStatusBar(QStatusBar(self))

        self.menubar = self.menuBar()
        self.menuBar().close()
        self.file_menu = self.menubar.addMenu("Switch Between Vegetables&Fruits and Todolist Pages")
        self.file_menu.addAction(button_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(button_action2)

        self.layout_switch_table_checkbox = QCheckBox("Switch Between Original And Notebook Tables", self)
        self.layout_switch_table_checkbox.toggled.connect(self.layout_switch_table_checkbox_clicked)

    # The two below methods connect to the two button actions to change the layout, and changes the main label of the table.
    def menubar_button_clicked1(self):
        if self.layout_switch_table_checkbox.isChecked():
            databaseOriginal.database_original()
        self.layout_tables.setCurrentWidget(self.layout_VegFruit)
        self.layout_button.setCurrentIndex(0)

    def menubar_button_clicked2(self):
        database()
        self.layout_tables.setCurrentWidget(self.layout_table_todolist)
        self.layout_button.setCurrentIndex(1)

    def toolbar_action_clicked(self):
        self.toolbar.close()
        self.menuBar().close()
        self.main_layout.setCurrentIndex(0)

    # The main section that is shown between the two layouts, it contains the label and the editing option for the table.
    def main_section(self):
        #Main label of the table, and it switches when the layout changes.
        self.label_table = QLabel("Vegetables & Fruits Table")
        self.label_table_todolist = QLabel("Vegetables & Fruits Todolist Table:")

        #Edit checkbox to show&hide the layouts for editing the table.
        self.layout_edit_checkbox = QCheckBox("Edit Mode", self)
        self.layout_edit_checkbox.toggled.connect(self.layout_edit_checkbox_toggle)

        self.layout_edit_checkbox_todolist = QCheckBox("Edit Mode", self)
        self.layout_edit_checkbox_todolist.toggled.connect(self.layout_edit_checkbox_toggle)

# Layouts

    def layout_switch_table_checkbox_clicked(self):
        if self.layout_switch_table_checkbox.isChecked():
            databaseOriginal.database_original()
            self.label_table.setText("Original Vegetables & Fruits Table:")
            self.original_table_on = True
            i = self.widget_VegFruit.indexOf(self.layout_VegFruit_edit)
            self.widget_VegFruit.takeAt(i)
            self.layout_VegFruit_edit.hide()
            self.set_VegFruit_edit_buttons_visible(False)
            self.table_VegFruit.setSortingEnabled(False)
            self.load_table_VegFruit()
            self.table_VegFruit.setSortingEnabled(True)
        else:
            database()
            self.label_table.setText("Notebook Vegetables & Fruits Table:")
            self.original_table_on = False
            self.temp_widget_4.insertWidget(0, self.layout_VegFruit_edit)
            self.layout_VegFruit_edit.show()
            self.table_VegFruit.setSortingEnabled(False)
            self.load_table_VegFruit()
            self.table_VegFruit.setSortingEnabled(True)

    # The method to show&hide the layouts for editing the table.
    def layout_edit_checkbox_toggle(self):
        # If statement that checks when the edit checkbox is activated to either show the layouts or hide them.
        if self.layout_edit_checkbox.isChecked():
            self.widget_VegFruit.addWidget(self.layout_VegFruit_edit_1, 0, 1)
            self.widget_VegFruit.addWidget(self.layout_VegFruit_edit_2, 0, 2)
            self.widget_VegFruit.addWidget(self.layout_VegFruit_edit_3, 1, 1, 1, 2)
            self.widget_VegFruit.addWidget(self.layout_VegFruit_edit_4, 2, 1, 1, 2)
            self.layout_VegFruit_edit_1.show()
            self.layout_VegFruit_edit_2.show()
            self.layout_VegFruit_edit_3.show()
            self.layout_VegFruit_edit_4.show()
        else:
            i = self.widget_VegFruit.indexOf(self.layout_VegFruit_edit_1)
            self.widget_VegFruit.takeAt(i)
            i = self.widget_VegFruit.indexOf(self.layout_VegFruit_edit_2)
            self.widget_VegFruit.takeAt(i)
            i = self.widget_VegFruit.indexOf(self.layout_VegFruit_edit_3)
            self.widget_VegFruit.takeAt(i)
            i = self.widget_VegFruit.indexOf(self.layout_VegFruit_edit_4)
            self.widget_VegFruit.takeAt(i)
            self.layout_VegFruit_edit_1.hide()
            self.layout_VegFruit_edit_2.hide()
            self.layout_VegFruit_edit_3.hide()
            self.layout_VegFruit_edit_4.hide()

        if self.layout_edit_checkbox_todolist.isChecked():
            self.widget_table_todolist.addWidget(self.layout_table_gridtodolist)
            self.layout_table_gridtodolist.show()
        else:
            i = self.widget_VegFruit.indexOf(self.layout_table_gridtodolist)
            self.widget_VegFruit.takeAt(i)
            self.layout_table_gridtodolist.hide()

# Main screen
    def main_screen(self):
        main_screen_image_temp = QPixmap("Images/Vegetables & Fruits Icon.png")
        main_screen_image = QLabel()
        main_screen_image.setPixmap(main_screen_image_temp)
        main_screen_image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_screen_label = QLabel("Vegetables &  Fruits Notebook")
        font = main_screen_label.font()
        font.setPointSize(30)
        main_screen_label.setFont(font)
        main_screen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_screen_label.setMargin(50)

        main_screen_button_1 = QPushButton("Vegetables && Fruits Notebook Table")
        main_screen_button_1.setFont(QFont('Times', 20))
        main_screen_button_1.setMinimumSize(500, 100)
        main_screen_button_1.clicked.connect(self.main_screen_button_1_clicked)

        main_screen_button_2 = QPushButton("Vegetables && Fruits Original Table")
        main_screen_button_2.setFont(QFont('Times', 20))
        main_screen_button_2.setMinimumSize(500, 100)
        main_screen_button_2.clicked.connect(self.main_screen_button_2_clicked)


        main_screen_button_3 = QPushButton("Todo-list Table", self)
        main_screen_button_3.setMinimumSize(500, 50)
        main_screen_button_3.setFont(QFont('Times', 15))
        main_screen_button_3.clicked.connect(self.main_screen_button_3_clicked)

        main_screen_widget = QGridLayout()
        main_screen_widget.addWidget(main_screen_image, 0, 0, 1, 2)
        main_screen_widget.addWidget(main_screen_label, 1, 0, 1, 2)
        main_screen_widget.addWidget(main_screen_button_1, 2, 0)
        main_screen_widget.addWidget(main_screen_button_2, 2, 1)
        main_screen_widget.addWidget(main_screen_button_3, 3, 0, 1, 2)
        main_screen_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_screen_widget.setSpacing(30)
        self.main_screen_layout = QWidget()
        self.main_screen_layout.setLayout(main_screen_widget)

    def main_screen_button_1_clicked(self):
        self.toolbar.setVisible(True)
        self.layout_switch_table_checkbox.setChecked(False)
        self.layout_button.setCurrentIndex(0)
        self.layout_tables.setCurrentIndex(0)
        self.main_layout.setCurrentIndex(1)
        self.toolbar.show()
        self.menuBar().show()

    def main_screen_button_2_clicked(self):
        self.toolbar.setVisible(True)
        self.layout_switch_table_checkbox.setChecked(True)
        self.layout_button.setCurrentIndex(0)
        self.layout_tables.setCurrentIndex(0)
        self.main_layout.setCurrentIndex(1)
        self.toolbar.show()
        self.menuBar().show()

    def main_screen_button_3_clicked(self):
        self.toolbar.setVisible(True)
        self.layout_button.setCurrentIndex(1)
        self.layout_tables.setCurrentIndex(1)
        self.main_layout.setCurrentIndex(1)
        self.toolbar.show()
        self.menuBar().show()

    # Main method that combines the layout and sets it to a main layout for the window.
    def main_layout(self):
        #Layout 1 for the VEG&Fruit table and its hidden/visible edit widgets.
        self.widget_VegFruit = QGridLayout()
        self.widget_VegFruit.addWidget(self.table_VegFruit, 0, 0, 3, 1)
        self.layout_VegFruit = QWidget()
        self.layout_VegFruit.setLayout(self.widget_VegFruit)
        self.widget_VegFruit.setColumnStretch(0, 1)

        # Layout 1 for the todolist table and its hidden/visible edit widgets.
        self.widget_table_todolist = QHBoxLayout()
        self.widget_table_todolist.addWidget(self.table_todolist)
        self.layout_table_todolist = QWidget()
        self.layout_table_todolist.setLayout(self.widget_table_todolist)
        self.widget_table_todolist.setStretch(0, 1)

        # Layout tables to combine the two tables into one stacked layout to be able to switch between the two layouts.
        self.layout_tables = QStackedLayout()
        self.layout_tables.addWidget(self.layout_VegFruit)
        self.layout_tables.addWidget(self.layout_table_todolist)
        self.layout_tables.setCurrentIndex(0)

        # Layout for the menus
        widget_VegFruit_menu = QHBoxLayout()
        widget_VegFruit_menu.addWidget(self.label_table)
        widget_VegFruit_menu.addWidget(self.layout_edit_checkbox)
        widget_VegFruit_menu.addWidget(self.layout_switch_table_checkbox)
        widget_VegFruit_menu.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_VegFruit_menu = QWidget()
        self.layout_VegFruit_menu.setLayout(widget_VegFruit_menu)

        widget_table_todolist_menu = QHBoxLayout()
        widget_table_todolist_menu.addWidget(self.label_table_todolist)
        widget_table_todolist_menu.addWidget(self.layout_edit_checkbox_todolist)
        widget_table_todolist_menu.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_table_todolist_menu = QWidget()
        self.layout_table_todolist_menu.setLayout(widget_table_todolist_menu)

        # Layout for the table label and the edit checkbox.
        self.layout_button = QStackedLayout()
        self.layout_button.addWidget(self.layout_VegFruit_menu)
        self.layout_button.addWidget(self.layout_table_todolist_menu)
        self.layout_button.setCurrentIndex(0)

        # Combines the last two layouts for a main layout that is set to show in the window.
        layout_widget = QVBoxLayout()
        layout_widget.addLayout(self.layout_button)
        layout_widget.addLayout(self.layout_tables, stretch = 1)
        layout = QWidget()
        layout.setLayout(layout_widget)

        self.main_layout = QStackedLayout()
        self.main_layout.addWidget(self.main_screen_layout)
        self.main_layout.addWidget(layout)
        self.main_layout.setCurrentIndex(0)
        final_layout = QWidget()
        final_layout.setLayout(self.main_layout)

        self.setCentralWidget(final_layout)

# Create & Load Tables
    # The method creates two tables for VEG&Fruit and todolist.
    def create_tables(self):
        self.table_VegFruit = QTableWidget()
        self.table_VegFruit.setColumnCount(22)
        self.table_VegFruit.setHorizontalHeaderLabels(["Icon", "Vegetable/Fruit ID", "Type", "Name", "Alternative Names ID", "Alternative Names", "Seasons ID", "Seasons", "Nutritions ID", "Nutrition",
                                                       "Plants Requirements ID", "Difficulty Growing", "Quantity", "Stage", "Space", "Water", "Sun Endurance", "Soil Requirement", "Minimum Days To Next Stage",
                                                       "Maximum Days To Next Stage", "Average Days To Next Stage", "Link"])
        self.table_VegFruit.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_VegFruit.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_VegFruit.setIconSize(QSize(48, 48))
        self.table_VegFruit.verticalHeader().setDefaultSectionSize(56)
        self.table_VegFruit.setSortingEnabled(True)
        self.table_VegFruit.setColumnHidden(1, True)
        self.table_VegFruit.setColumnHidden(4, True)
        self.table_VegFruit.setColumnHidden(6, True)
        self.table_VegFruit.setColumnHidden(8, True)
        self.table_VegFruit.setColumnHidden(10, True)
        self.table_VegFruit.setColumnHidden(12, True)
        self.table_VegFruit.setColumnHidden(13, True)
        self.table_VegFruit.setColumnHidden(14, True)
        self.table_VegFruit.setColumnHidden(15, True)
        self.table_VegFruit.setColumnHidden(16, True)
        self.table_VegFruit.setColumnHidden(17, True)
        self.table_VegFruit.setColumnHidden(18, True)
        self.table_VegFruit.setColumnHidden(19, True)
        self.table_VegFruit.setColumnHidden(20, True)

        self.table_todolist = QTableWidget()
        self.table_todolist.setColumnCount(4)
        self.table_todolist.setHorizontalHeaderLabels(["ID", "Type", "Description", "status"])
        self.table_todolist.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_todolist.setSortingEnabled(True)
        self.table_todolist.setColumnHidden(0, True)

    # The two below methods loads the data from the database into the VEG&Fruit and todolist tables.
    def load_table_VegFruit(self):
        # Loads the data from the vegetablesFruits database into their appropriate list.
        vegetables_or_fruits_id_list = []
        icons_list = []
        names_list = []
        types_list = []
        links_list = []
        vegetables_or_fruits_list = vegetables_and_fruits_load()
        for inside_list in vegetables_or_fruits_list:
            vegetables_or_fruits_id_list.append(inside_list[0])
            icons_list.append(inside_list[1])
            names_list.append(inside_list[2])
            types_list.append(inside_list[3])
            links_list.append(inside_list[4])

        # Goes through each ID for vegetables&fruits to take all its data and adds it to the table.
        table_list = []
        row = 0
        for vegetable_or_fruit_id in vegetables_or_fruits_id_list:
            icon = icons_list[row]
            name = names_list[row]
            type = types_list[row]
            link = links_list[row]

            alternative_names_temp = alternative_names_load(vegetable_or_fruit_id)
            alternative_names_list_id = []
            alternative_names_list = []
            alternative_names_id = ""
            alternative_names = ""
            if any(alternative_names_temp):
                for i in range(len(alternative_names_temp)):
                    alternative_names_list_id.append(alternative_names_temp[i][0])
                    alternative_names_list.append(alternative_names_temp[i][2])
                alternative_names_id = ", ".join(map(str, alternative_names_list_id))
                alternative_names = ", ".join(alternative_names_list)

            months_temp = months_load(vegetable_or_fruit_id)
            months_list_id = []
            months_list = []
            months_id = ""
            months = ""
            if any(months_temp):
                for i in range(len(months_temp)):
                    months_list_id.append(months_temp[i][0])
                    months_list.append(months_temp[i][2])
                months_id = ", ".join(map(str, months_list_id))
                months = ", ".join(months_list)

            nutritions_temp = nutritions_load(vegetable_or_fruit_id)
            nutritions_list_id = []
            nutritions_list = []
            nutritions_id = ""
            nutritions = ""
            if any(nutritions_temp):
                for i in range(len(nutritions_temp)):
                    nutritions_list_id.append(nutritions_temp[i][2])
                    nutritions_list.append(nutritions_temp[i][2])
                nutritions_id = ", ".join(map(str, nutritions_list_id))
                nutritions = ", ".join(nutritions_list)

            plant_requirements_temp = plant_requirements_load(vegetable_or_fruit_id)
            (plant_requirements_list_id, difficulty_list, quantity_list, stage_list, space_list, water_list, sun_endurance_list, soil_requirement_list,
            minimum_days_to_next_stage_list, maximum_days_to_next_stage_list, average_days_to_next_stage_list) = [], [], [], [], [], [], [], [], [], [], []
            (plant_requirements_id, difficulty, quantity, stage, space, water, sun_endurance, soil_requirement,
            minimum_days_to_next_stage, maximum_days_to_next_stage, average_days_to_next_stage) = "", "", "", "", "", "", "", "", "", "", ""

            if any(plant_requirements_temp):
                i = 0
                for i in range(len(plant_requirements_temp)):
                    plant_requirements_list_id.append(plant_requirements_temp[i][0])
                    difficulty_list.append(plant_requirements_temp[i][2])
                    quantity_list.append(plant_requirements_temp[i][3])
                    stage_list.append(plant_requirements_temp[i][4])
                    space_list.append(plant_requirements_temp[i][5])
                    water_list.append(plant_requirements_temp[i][6])
                    sun_endurance_list.append(plant_requirements_temp[i][7])
                    soil_requirement_list.append(plant_requirements_temp[i][8])
                    minimum_days_to_next_stage_list.append(plant_requirements_temp[i][9])
                    maximum_days_to_next_stage_list.append(plant_requirements_temp[i][10])
                    average = (plant_requirements_temp[i][9] + plant_requirements_temp[i][10]) / 2
                    average_days_to_next_stage_list.append(average)
                    plant_requirements_id = ", ".join(map(str, plant_requirements_list_id))
                    difficulty = ", ".join(difficulty_list)
                    quantity = ", ".join(map(str, quantity_list))
                    stage = ", ".join(stage_list)
                    space = ", ".join(map(str, space_list))
                    water = ", ".join(map(str, water_list))
                    sun_endurance = ", ".join(sun_endurance_list)
                    soil_requirement = ", ".join(soil_requirement_list)
                    minimum_days_to_next_stage = ", ".join(map(str, minimum_days_to_next_stage_list))
                    maximum_days_to_next_stage = ", ".join(map(str, maximum_days_to_next_stage_list))
                    average_days_to_next_stage = f" for {stage_list[i]} stage, ".join(map(str, average_days_to_next_stage_list))
                if any(average_days_to_next_stage):
                    average_days_to_next_stage += f" for {stage_list[i]} stage"

            table_list.append([icon, vegetable_or_fruit_id, type, name, alternative_names_id, alternative_names, months_id, months, nutritions_id, nutritions,
                               plant_requirements_id, difficulty, quantity, stage, space, water, sun_endurance, soil_requirement, minimum_days_to_next_stage,
                               maximum_days_to_next_stage, average_days_to_next_stage, link])
            row += 1

        # Sets the vegetables&fruits table to zero, then it goes through two loops to go through the nested list to add them in the table.
        # For the icon, it implements via a method that translates the path to an image.
        self.table_VegFruit.setRowCount(0)
        for row_idx, dataList in enumerate(table_list):
            self.table_VegFruit.insertRow(row_idx)
            for col_idx, data in enumerate(dataList):
                if col_idx == 0:
                    self.table_VegFruit.setItem(row_idx, col_idx, self.create_icon_table_item(str(data)))
                else:
                    self.table_VegFruit.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    def load_table_todolist(self):
        todolist_list = todolist_load()

        # Sets the todolist table to zero, then it goes through two loops of the list to add them in the table.
        self.table_todolist.setRowCount(0)
        for row_idx, dataList in enumerate(todolist_list):
            self.table_todolist.insertRow(row_idx)
            for col_idx, data in enumerate(dataList):
                self.table_todolist.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))

    # Turns the path of the icon to an icon to be used for the table.
    def create_icon_table_item(self, icon_path):
        item = QTableWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, icon_path)
        item.setToolTip(icon_path)

        icon = QIcon(icon_path)
        if icon_path and not icon.isNull():
            item.setIcon(icon)
        else:
            item.setText(icon_path)

        return item

    # Adds an icon to the table if there isn't a valid icon path.
    def icon_path_exists(self, icon_path):
        if not icon_path or icon_path.startswith("http"):
            return False

        if os.path.exists(icon_path):
            return True

        return os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), icon_path))

# Edit Widgets

# VegFruit edit widgets

    # Creates the widgets for the VegFruit table.
    def edit_mode_VegFruit(self):

        edit_mode_original_label = QLabel("Add Fruits or Vegetables from original table to this table:")
        self.edit_mode_original_list = QListWidget()
        self.edit_mode_original_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.edit_mode_original_list.setFixedSize(400, 200)
        self.edit_mode_original_list_confirmation = QPushButton("Click to print the list of the original database")
        self.edit_mode_original_list_confirmation.clicked.connect(self.edit_mode_original_list_confirmation_clicked)

        temp_widget_0 = QVBoxLayout()
        temp_widget_0.addWidget(self.edit_mode_original_list)
        temp_widget_0.addWidget(self.edit_mode_original_list_confirmation)
        temp_widget_0.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_VegFruit_edit_0 = QWidget()
        layout_VegFruit_edit_0.setLayout(temp_widget_0)

        temp_widget = QVBoxLayout()
        temp_widget.addWidget(edit_mode_original_label)
        temp_widget.addWidget(layout_VegFruit_edit_0)
        temp_widget.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_VegFruit_edit = QWidget()
        self.layout_VegFruit_edit.setLayout(temp_widget)

        label_name = QLabel("Add the name of the vegetable/fruit below:")
        self.edit_mode_name = QLineEdit()
        self.edit_mode_name.setPlaceholderText("name")

        widget_label = QVBoxLayout()
        widget_label.addWidget(label_name)
        widget_label.addWidget(self.edit_mode_name)
        layout_label = QWidget()
        layout_label.setLayout(widget_label)

        self.list_alternative_names = []
        self.list_alternative_names_temp = QListWidget()
        self.list_alternative_names_temp.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.list_alternative_names_temp.setFixedSize(400, 80)
        alternative_name_label = QLabel("Add an optional alternative names:")
        self.alternative_name_edit = QLineEdit()
        self.alternative_name_edit.setPlaceholderText("Alternative Name")
        self.alternative_name_edit_add_button = QPushButton("Add to the list")
        self.alternative_name_edit_add_button.clicked.connect(self.alternative_name_edit_add_button_clicked)
        self.alternative_name_edit_delete_button = QPushButton("Remove from the list")
        self.alternative_name_edit_delete_button.clicked.connect(self.alternative_name_edit_delete_button_clicked)
        temp_widget_1_0 = QVBoxLayout()
        temp_widget_1_0.addWidget(self.alternative_name_edit)
        temp_widget_1_0.addWidget(self.alternative_name_edit_add_button)
        temp_widget_1_0.addWidget(self.alternative_name_edit_delete_button)
        temp_widget_1_0.addWidget(self.list_alternative_names_temp)
        temp_widget_1_0.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_alternative_names = QWidget()
        layout_alternative_names.setLayout(temp_widget_1_0)

        # Icon widget to add the icon link.
        # Haitham edited/added here: the icon field can be filled by browse, manual typing
        label_icon = QLabel("Add the icon link for the vegetable/fruit below:")
        self.edit_mode_icon = QLineEdit()
        self.edit_mode_icon.setPlaceholderText("Icon link")
        self.edit_mode_icon.returnPressed.connect(self.refresh_selected_icon_from_field)
        self.edit_mode_icon.editingFinished.connect(self.refresh_selected_icon_from_field)
        self.edit_mode_icon_checkbox = QCheckBox("Ignore Warning When Adding Images With The Same Name")
        browse_icon_button = QPushButton("Select Image")
        browse_icon_button.clicked.connect(self.select_icon_image_clicked)
        temp_widget_1_1 = QVBoxLayout()
        temp_widget_1_1.addWidget(label_icon)
        temp_widget_1_1.addWidget(self.edit_mode_icon)
        temp_widget_1_1.addWidget(browse_icon_button)
        temp_widget_1_1.addWidget(self.edit_mode_icon_checkbox)
        temp_widget_1_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_icon = QWidget()
        layout_icon.setLayout(temp_widget_1_1)

        # link widget to add a link for more information the vegetable/fruit.
        label_link = QLabel("Add an optional link for more information on the vegetable/fruit below:")
        self.edit_mode_link = QLineEdit()
        self.edit_mode_link.setPlaceholderText("link")
        temp_widget_1_2 = QVBoxLayout()
        temp_widget_1_2.addWidget(label_link)
        temp_widget_1_2.addWidget(self.edit_mode_link)
        layout_link = QWidget()
        layout_link.setLayout(temp_widget_1_2)

        # Layout that contains all the widgets above and adds it to a widget so we can then add it to another layout as a widget.
        temp_widget_1 = QVBoxLayout()
        temp_widget_1.addWidget(layout_label)
        temp_widget_1.addWidget(layout_icon)
        temp_widget_1.addWidget(layout_link)
        temp_widget_1.addWidget(alternative_name_label)
        temp_widget_1.addWidget(layout_alternative_names)
        self.layout_VegFruit_edit_1 = QWidget()
        self.layout_VegFruit_edit_1.setLayout(temp_widget_1)

        # The two loops below create a list of checkBoxes in a grid layout for all the months/nutrition using a loop and adds it to a widget so we can then add it to another layout as a widget.
        row = 1
        column = 0
        list_months = 0
        label_months = QLabel("Choose the good months for the vegetable/fruit below:")
        months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.edit_mode_months = []
        temp_widget_2 = QGridLayout()
        for i in months_list:
            edit_mode_months_temp = QCheckBox(i)
            self.edit_mode_months.append(edit_mode_months_temp)
            temp_widget_2.addWidget(self.edit_mode_months[list_months], row, column)
            column +=1
            list_months += 1
            if column % 4 == 0:
                row += 1
                column = 0

        layout_months_gridBox = QWidget()
        layout_months_gridBox.setLayout(temp_widget_2)

        label_nutrition = QLabel("Add the nutritions:")
        self.list_nutrition = QListWidget()
        self.list_nutrition.addItems(["Carbohydrates", "Proteins", "Fats", "Vitamins", "Minerals", "Water"])
        self.list_nutrition.clicked.connect(self.nutrition_list_changed)
        self.list_nutrition.setFixedSize(400, 150)
        self.list_nutrition_label = QLabel("...")
        self.list_nutrition_label_item = []

        temp_widget_3 = QVBoxLayout()
        temp_widget_3.addWidget(self.list_nutrition)
        layout_nutrition = QWidget()
        layout_nutrition.setLayout(temp_widget_3)

        difficulty_label = QLabel("Choose difficulty of growing the fruit")
        self.difficulty_comboBox = QComboBox()
        self.difficulty_comboBox.addItems(["Easy", "Medium", "Hard"])

        temp_widget_3_1 = QVBoxLayout()
        temp_widget_3_1.addWidget(self.difficulty_comboBox)
        temp_widget_3.setAlignment(Qt.AlignmentFlag.AlignTop)
        temp_widget_3.setSpacing(5)
        layout_difficulty = QWidget()
        layout_difficulty.setLayout(temp_widget_3_1)

        # ComboBox to choose either vegetable or a fruit.
        type_label = QLabel("Choose the type:")
        self.type = QComboBox()
        self.type.addItems(["Vegetable", "Fruit"])

        # Button to add the data to the table
        confirmation_button_VegFruit = QPushButton("Add to the table list")
        confirmation_button_VegFruit.clicked.connect(self.confirmation_button_VegFruit_clicked)

        # Layout that contains all the rest widgets above and adds it to a widget so we can then add it to another layout as a widget.
        self.temp_widget_4 = QVBoxLayout()
        self.temp_widget_4.addWidget(type_label)
        self.temp_widget_4.addWidget(self.type)
        self.temp_widget_4.addWidget(difficulty_label)
        self.temp_widget_4.addWidget(layout_difficulty)
        self.temp_widget_4.addWidget(label_months)
        self.temp_widget_4.addWidget(layout_months_gridBox)
        self.temp_widget_4.addWidget(label_nutrition)
        self.temp_widget_4.addWidget(self.list_nutrition_label)
        self.temp_widget_4.addWidget(layout_nutrition)
        self.temp_widget_4.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.temp_widget_4.setSpacing(5)
        self.layout_VegFruit_edit_2 = QWidget()
        self.layout_VegFruit_edit_2.setLayout(self.temp_widget_4)

        temp_widget_4_1 = QVBoxLayout()
        temp_widget_4_1.addWidget(confirmation_button_VegFruit)
        temp_widget_4_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        temp_widget_4_1.setSpacing(5)
        self.layout_VegFruit_edit_3 = QWidget()
        self.layout_VegFruit_edit_3.setLayout(temp_widget_4_1)

        # Two buttons to either get the data from a row into the edit table or to delete the row.
        label_id = QLabel("Click a table to then get the data or delete row:")

        fill_button_VegFruit = QPushButton("Edit The Vegetable/Fruit Row")
        fill_button_VegFruit.clicked.connect(self.fill_button_VegFruit_clicked)

        # Haitham edited/added here: Save and Cancel appear after a row is loaded for editing.
        self.save_button_VegFruit = QPushButton("Save")
        self.save_button_VegFruit.clicked.connect(self.save_button_VegFruit_clicked)
        self.save_button_VegFruit.hide()

        self.cancel_button_VegFruit = QPushButton("Cancel")
        self.cancel_button_VegFruit.clicked.connect(self.cancel_button_VegFruit_clicked)
        self.cancel_button_VegFruit.hide()

        delete_button_VegFruit = QPushButton("Remove from the list")
        delete_button_VegFruit.clicked.connect(self.delete_button_VegFruit_clicked)

        # Layout that contains the above two buttons and adds it to a widget so we can then add it to another layout as a widget.
        temp_widget_5 = QVBoxLayout()
        temp_widget_5.addWidget(label_id)
        temp_widget_5.addWidget(fill_button_VegFruit)
        temp_widget_5.addWidget(self.save_button_VegFruit)
        temp_widget_5.addWidget(self.cancel_button_VegFruit)
        temp_widget_5.addWidget(delete_button_VegFruit)
        temp_widget_5.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_VegFruit_edit_4 = QWidget()
        self.layout_VegFruit_edit_4.setLayout(temp_widget_5)

    def populate_edit_mode_original_list(self):
        databaseOriginal.database_original()
        original_vegetables_and_fruits_list = databaseOriginal.vegetables_and_fruits_load()
        for i in range(len(original_vegetables_and_fruits_list)):
            item = original_vegetables_and_fruits_list[i][0]
            name = original_vegetables_and_fruits_list[i][2]
            self.edit_mode_original_list.addItem(f"ID: {str(item)}, Name: {name}")

        database()

    # Should take the data from the other database for the selected options and load them in the table.
    def edit_mode_original_list_confirmation_clicked(self):
        self.table_VegFruit.setSortingEnabled(False)
        items_list = []
        temp_list = self.edit_mode_original_list.selectedItems()
        if temp_list:
            for item in temp_list:
                string = item.text()
                new_item_list = string.split(", ")
                new_item = new_item_list[0]
                new_item = int(new_item[4:])
                items_list.append(new_item)
        else:
            return

        items_list = [int(i) for i in items_list]
        for vegetables_and_fruits_id in items_list:
            databaseOriginal.database_original()

            original_vegetables_and_fruits_list = databaseOriginal.vegetables_and_fruits_load_original(vegetables_and_fruits_id)
            original_months_list = databaseOriginal.months_load(vegetables_and_fruits_id)
            original_nutritions_list = databaseOriginal.nutritions_load(vegetables_and_fruits_id)
            original_alternative_names_list = databaseOriginal.alternative_names_load(vegetables_and_fruits_id)
            original_plant_requirements_list = databaseOriginal.plant_requirements_load(vegetables_and_fruits_id)

            database()

            for sublist in original_alternative_names_list:
                del sublist[0]
            for sublist in original_months_list:
                del sublist[0]
            for sublist in original_nutritions_list:
                del sublist[0]
            for sublist in original_plant_requirements_list:
                del sublist[0]

            # Add to the table
            original_vegetables_and_fruits_id = original_vegetables_and_fruits_list[0][0]
            icon = original_vegetables_and_fruits_list[0][1]
            name = original_vegetables_and_fruits_list[0][2]
            type = original_vegetables_and_fruits_list[0][3]
            link = original_vegetables_and_fruits_list[0][4]
            new_vegetables_and_fruits_id = vegetables_and_fruits_input(icon, name, type, link)

            alternative_names = ""
            alternative_names_list = []
            for i in range(len(original_alternative_names_list)):
                if original_vegetables_and_fruits_id == original_alternative_names_list[i][0]:
                    alternative_names_list.append(original_alternative_names_list[i][1])
                alternative_names = ", ".join(alternative_names_list)
            alternative_names_input(new_vegetables_and_fruits_id, alternative_names)

            months = ""
            months_list = []

            for i in range(len(original_months_list)):
                if original_vegetables_and_fruits_id == original_months_list[i][0]:
                    months_list.append(original_months_list[i][1])
                months = ", ".join(months_list)
            months_input(new_vegetables_and_fruits_id, months)

            nutritions = ""
            nutritions_list = []
            for i in range(len(original_nutritions_list)):
                if original_vegetables_and_fruits_id == original_nutritions_list[i][0]:
                    nutritions_list.append(original_nutritions_list[i][1])
                nutritions = ", ".join(nutritions_list)
            nutritions_input(new_vegetables_and_fruits_id, nutritions)

            (difficulty_list, quantity_list, stage_list, space_list, water_list, sun_endurance_list, soil_requirement_list,
            minimum_days_to_next_stage_list, maximum_days_to_next_stage_list, average_days_to_next_stage_list) = [], [], [], [], [], [], [], [], [], []
            (difficulty, quantity, stage, space, water, sun_endurance, soil_requirement,
            minimum_days_to_next_stage, maximum_days_to_next_stage, average_days_to_next_stage) = "", "", "", "", "", "", "", "", "", ""

            for i in range(len(original_plant_requirements_list)):
                difficulty_list.append(original_plant_requirements_list[i][1])
                quantity_list.append(original_plant_requirements_list[i][2])
                stage_list.append(original_plant_requirements_list[i][3])
                space_list.append(original_plant_requirements_list[i][4])
                water_list.append(original_plant_requirements_list[i][5])
                sun_endurance_list.append(original_plant_requirements_list[i][6])
                soil_requirement_list.append(original_plant_requirements_list[i][7])
                minimum_days_to_next_stage_list.append(original_plant_requirements_list[i][8])
                maximum_days_to_next_stage_list.append(original_plant_requirements_list[i][9])
                average = (original_plant_requirements_list[i][8] + original_plant_requirements_list[i][9]) / 2
                average_days_to_next_stage_list.append(average)
                difficulty = ", ".join(difficulty_list)
                quantity = ", ".join(map(str, quantity_list))
                stage = ", ".join(stage_list)
                space = ", ".join(map(str, space_list))
                water = ", ".join(map(str, water_list))
                sun_endurance = ", ".join(sun_endurance_list)
                soil_requirement = ", ".join(soil_requirement_list)
                minimum_days_to_next_stage = ", ".join(map(str, minimum_days_to_next_stage_list))
                maximum_days_to_next_stage = ", ".join(map(str, maximum_days_to_next_stage_list))
                average_days_to_next_stage = f" for {stage_list[i]} stage, ".join(map(str, average_days_to_next_stage_list))
                if any(average_days_to_next_stage):
                    average_days_to_next_stage += f" for {stage_list[i]} stage"
            plant_requirements_input(new_vegetables_and_fruits_id, difficulty, quantity, stage, space, water, sun_endurance, soil_requirement, minimum_days_to_next_stage, maximum_days_to_next_stage)

        self.load_table_VegFruit()
        self.table_VegFruit.setSortingEnabled(True)


    # Takes the input changes from the nutrition list to put it in a list that will be added to the database.
    def nutrition_list_changed(self): # s is a str
        value = self.list_nutrition.currentItem().text()
        if value not in self.list_nutrition_label_item:
            self.list_nutrition_label_item.append(value)
        else:
            self.list_nutrition_label_item.remove(value)

        if not self.list_nutrition_label_item:
            self.list_nutrition_label.setText("...")
        else:
            self.list_nutrition_label.setText(", ".join(self.list_nutrition_label_item))

    # Takes the click from the delete button for alternative names to remove them from the list that will be added to the database.
    def alternative_name_edit_delete_button_clicked(self, item):
        list_items = self.list_alternative_names_temp.selectedItems()
        if list_items:
            for item in list_items:
                self.list_alternative_names_temp.takeItem(self.list_alternative_names_temp.row(item))

    # Takes the click from the add button for alternative names to add them to the list that will be added to the database.
    def alternative_name_edit_add_button_clicked(self):
        item = self.alternative_name_edit.text()
        count = self.list_alternative_names_temp.count()
        for i in range(count):
            if item == self.list_alternative_names_temp.item(i).text():
                return # Add a popout message to inform that the alternative name already exists.
        if item:
            self.list_alternative_names_temp.addItem(item)

    # Sets the buttons for updating the tables visible
    def set_VegFruit_edit_buttons_visible(self, is_visible):
        self.save_button_VegFruit.setVisible(is_visible)
        self.cancel_button_VegFruit.setVisible(is_visible)

    # The button that opens your file to add an image path.
    def select_icon_image_clicked(self):
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select icon image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;All Files (*)"
        )

        if image_path:
            self.edit_mode_icon.setText(image_path)
            self.refresh_selected_icon_from_field()

    def save_image(self):
        image_path = self.edit_mode_icon.text()

        image_path_name = image_path.split("/")
        image_path_name = image_path_name[len(image_path_name)-1]
        image_path_name = image_path_name.split(".")
        image_path_name = image_path_name[0]

        if os.path.exists(f"Images/{image_path_name}.jpg") and self.edit_mode_icon_checkbox.isChecked() == False:
            image_new_name, ok = QInputDialog.getText(self, "Error, image name already exists!", "Write a new image nme or cancel to use the already existing image.", QLineEdit.EchoMode.Normal)
            print("Test1")
            if ok and image_new_name == image_path_name:
                print("Test2")
            elif ok and image_new_name:
                print("Test3")
                image = Image.open(image_path)
                image.save(f"images/{image_new_name}.jpg")
                self.icon_path = f"images/{image_new_name}.jpg"
            else:
                print("Test4")
                self.icon_path = f"images/{image_path_name}.jpg"
        elif os.path.exists(image_path):
            image = Image.open(image_path)
            image.save(f"images/{image_path_name}.jpg")
            self.icon_path = f"images/{image_path_name}.jpg"
        else:
            self.icon_path = "ERROR"
            return

    # Updates the table image and the path image in the editable widget.
    def refresh_selected_icon_from_field(self):
        row = self.table_VegFruit.currentRow()
        # Checks if a row isn't selected and if there is a row that is being edited to bring the id of the row.
        if row < 0 and self.editing_idVegFruit:
            row = self.find_VegFruit_row_by_id(self.editing_idVegFruit)

        if row >= 0:
            self.table_VegFruit.setItem(row, 0, self.create_icon_table_item(self.edit_mode_icon.text()))

    # Finds the vegetable id for the row.
    def find_VegFruit_row_by_id(self, idVegFruit):
        for row in range(self.table_VegFruit.rowCount()):
            id_item = self.table_VegFruit.item(row, 1)
            if id_item and id_item.text() == idVegFruit:
                return row

        return -1

    # Gets the data from the row in the table.
    def get_VegFruit_row_data(self, row):
        if row < 0:
            return []

        row_data = []
        for column in range(22):
            item = self.table_VegFruit.item(row, column)
            if item is None:
                row_data.append("")
            elif column == 0:
                row_data.append(item.data(Qt.ItemDataRole.UserRole) or item.text())
            else:
                row_data.append(item.text())

        return row_data

    # Takes the values from the months, alternative names and the some others to return for the database.
    def get_VegFruit_form_values(self):
        self.list_months = []
        for i in range(12):
            if self.edit_mode_months[i].isChecked():
                self.list_months.append(self.edit_mode_months[i].text())

        for i in range(self.list_alternative_names_temp.count()):
            self.list_alternative_names.append(self.list_alternative_names_temp.item(i).text())

        self.save_image()

        return {
            "icon": self.icon_path,
            "name": self.edit_mode_name.text(),
            "type": self.type.currentText(),
            "link": self.edit_mode_link.text(),
            "difficulty": self.difficulty_comboBox.currentText()
        }

    # Adds the data to the VEG&Fruit table.
    def confirmation_button_VegFruit_clicked(self):
        self.table_VegFruit.setSortingEnabled(False)
        values = self.get_VegFruit_form_values()

        # We set it as a variable to get the return value which is the last id added.
        vegetable_or_fruit_id = vegetables_and_fruits_input(values["icon"], values["name"], values["type"], values["link"])

        for value in self.list_alternative_names:
            alternative_names_input(vegetable_or_fruit_id, value)

        for value in self.list_months:
            months_input(vegetable_or_fruit_id, value)

        for value in self.list_nutrition_label_item:
            nutritions_input(vegetable_or_fruit_id, value)

        plant_requirements_input(vegetable_or_fruit_id, values["difficulty"], "test", "test", 1, 1, "test", "test", 1, 1)

        if self.original_table_on:
            name = values["name"]
            self.edit_mode_original_list.addItem(f"ID: {vegetable_or_fruit_id}, Name: {name}")

        self.load_table_VegFruit()
        self.table_VegFruit.setSortingEnabled(True)
        self.clear_VegFruit_form()
        self.set_VegFruit_edit_buttons_visible(False)
        self.editing_idVegFruit = None

    # Clears the info on the edit section fields when clicking the cancel button.
    def clear_VegFruit_form(self):
        self.edit_mode_name.setText("")
        self.list_nutrition_label_item.clear()
        self.list_alternative_names_temp.clear()
        self.list_alternative_names.clear()
        self.alternative_name_edit.clear()
        self.edit_mode_icon.clear()
        self.edit_mode_link.clear()
        self.list_nutrition_label.setText("...")
        self.list_nutrition_label_item.clear()
        self.type.setCurrentIndex(0)
        self.difficulty_comboBox.setCurrentIndex(0)

        for checkbox in self.edit_mode_months:
            checkbox.setChecked(False)

    # Fills the data to the edit section of the VEG&Fruit layout.
    def fill_button_VegFruit_clicked(self):
        item = self.table_VegFruit.currentRow()
        table_list = self.get_VegFruit_row_data(item)
        if not table_list:
            return

        vegetable_or_fruit_id = table_list[1]
        # Save the id to use it for later when the save button is clicked.
        self.editing_idVegFruit = vegetable_or_fruit_id

        self.edit_mode_icon.setText(table_list[0])
        self.type.setCurrentText(table_list[2])
        self.edit_mode_name.setText(table_list[3])
        self.difficulty_comboBox.setCurrentText(table_list[11])
        self.edit_mode_link.setText(table_list[21])

        alternative_name_string = table_list[5]
        alternative_name_list = alternative_name_string.split(", ")
        alternative_name_list = [word.capitalize() for word in alternative_name_list]
        self.list_alternative_names_temp.clear()
        if alternative_name_list != ['']:
            for i in alternative_name_list:
                self.list_alternative_names_temp.addItem(i)

        list_months_string = table_list[7]
        list_months = list_months_string.split(", ")
        list_months = [word.capitalize() for word in list_months]
        dont_uncheck2 = []
        for i in range(len(list_months)):
            for j in range(12):
                if list_months[i] == self.edit_mode_months[j].text():
                    self.edit_mode_months[j].setChecked(True)
                    dont_uncheck2.append(j)
                elif j not in dont_uncheck2:
                    self.edit_mode_months[j].setChecked(False)

        list_nutrition_string = table_list[9]
        self.list_nutrition_label_item.clear()
        if list_nutrition_string:
            list_nutrition = list_nutrition_string.split(", ")
            list_nutrition = [word.capitalize() for word in list_nutrition]
            self.list_nutrition_label.setText(", ".join(list_nutrition))
            for i in list_nutrition:
                self.list_nutrition_label_item.append(i)
        else:
            self.list_nutrition_label.setText("...")

        self.set_VegFruit_edit_buttons_visible(True)
        self.list_alternative_names.clear()

    def save_button_VegFruit_clicked(self):
        if not self.editing_idVegFruit:
            return
        self.table_VegFruit.setSortingEnabled(False)

        alternative_names_delete(self.editing_idVegFruit)
        months_delete(self.editing_idVegFruit)
        nutritions_delete(self.editing_idVegFruit)
        plants_requirements_delete(self.editing_idVegFruit)

        values = self.get_VegFruit_form_values()
        vegetables_and_fruits_update(
            self.editing_idVegFruit,
            values["icon"],
            values["type"],
            values["name"],
            values["link"]
        )

        for value in self.list_alternative_names:
            alternative_names_input(self.editing_idVegFruit, value)

        for value in self.list_months:
            months_input(self.editing_idVegFruit, value)

        for value in self.list_nutrition_label_item:
            nutritions_input(self.editing_idVegFruit, value)

        plant_requirements_input(self.editing_idVegFruit, values["difficulty"], "test", "test", 1, 1, "test", "test", 1, 1)

        self.editing_idVegFruit = None
        self.set_VegFruit_edit_buttons_visible(False)
        self.load_table_VegFruit()
        self.clear_VegFruit_form()
        self.table_VegFruit.setSortingEnabled(True)

    # Sets the id that was saved to zero. Cancels the editing and hides the two buttons.
    def cancel_button_VegFruit_clicked(self):
        self.table_VegFruit.setSortingEnabled(False)
        self.editing_idVegFruit = None
        self.set_VegFruit_edit_buttons_visible(False)
        self.clear_VegFruit_form()
        self.load_table_VegFruit()
        self.table_VegFruit.setSortingEnabled(True)

    # Deletes a row of data from the VEG&Fruit table.
    def delete_button_VegFruit_clicked(self):
        self.table_VegFruit.setSortingEnabled(False)
        current_row = self.table_VegFruit.currentRow()

        if current_row < 0:
            return

        indexes = self.table_VegFruit.selectionModel().selectedRows()
        vegetable_or_fruit_id_list = []
        for index in indexes:
            vegetable_or_fruit_id_list.append(index.row())

        if vegetable_or_fruit_id_list:
            for row in range(len(vegetable_or_fruit_id_list)):
                vegetable_or_fruit_id_list[row] = self.table_VegFruit.item(vegetable_or_fruit_id_list[row], 1).text()
                row += 1
        else:
            vegetable_or_fruit_id_list.append(self.table_VegFruit.item(current_row, 1).text())

        for vegetable_or_fruit_id in vegetable_or_fruit_id_list:
            vegetables_and_fruits_delete(vegetable_or_fruit_id)
            alternative_names_delete(vegetable_or_fruit_id)
            months_delete(vegetable_or_fruit_id)
            nutritions_delete(vegetable_or_fruit_id)
            plants_requirements_delete(vegetable_or_fruit_id)

        # If the deleted row is also the one is edited, it will cancel the edit stuff alongside it.
        if self.editing_idVegFruit in vegetable_or_fruit_id_list:
            self.editing_idVegFruit = None
            self.set_VegFruit_edit_buttons_visible(False)
            self.clear_VegFruit_form()

        if self.original_table_on:
            item = []
            for vegetable_or_fruit_id in vegetable_or_fruit_id_list:
                item.append(self.edit_mode_original_list.findItems(vegetable_or_fruit_id, Qt.MatchFlag.MatchContains))
            for i in item:
                self.edit_mode_original_list.takeItem(self.edit_mode_original_list.row(i[0]))

        self.load_table_VegFruit()
        self.table_VegFruit.setSortingEnabled(True)

# todolist edit widgets

    # Creates the widgets for the todolist table.
    def edit_mode_todolist(self):
        self.todolist_type = QComboBox()
        self.todolist_type.addItems(["Urgent", "Daily", "Weekly"])

        self.status = QComboBox()
        self.status.addItems(["Resolved", "Unresolved"])

        label_description = QLabel("Add the description of the vegetable/fruit todolist below:")
        self.edit_todolist_mode_description = QLineEdit()
        self.edit_todolist_mode_description.setPlaceholderText("Todolist Description")

        confirmation_button_todolist = QPushButton("Add To Todo-list")
        confirmation_button_todolist.clicked.connect(self.confirmation_button_todolist_clicked)

        widget_table_grid1 = QVBoxLayout()
        widget_table_grid1.addWidget(self.todolist_type)
        widget_table_grid1.addWidget(self.status)
        widget_table_grid1.addWidget(label_description)
        widget_table_grid1.addWidget(self.edit_todolist_mode_description)
        widget_table_grid1.addWidget(confirmation_button_todolist)
        widget_table_grid1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_table_gridtodolist1 = QWidget()
        layout_table_gridtodolist1.setLayout(widget_table_grid1)

        label_id = QLabel("Click a table to then update the status or delete it:")

        fill_button_todolist = QPushButton("Update Status")
        fill_button_todolist.clicked.connect(self.update_button_todolist_clicked)

        delete_button_todolist = QPushButton("Remove from the list")
        delete_button_todolist.clicked.connect(self.delete_button_todolist_clicked)

        widget_table_grid2 = QVBoxLayout()
        widget_table_grid2.addWidget(label_id)
        widget_table_grid2.addWidget(fill_button_todolist)
        widget_table_grid2.addWidget(delete_button_todolist)
        widget_table_grid2.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_table_gridtodolist2 = QWidget()
        layout_table_gridtodolist2.setLayout(widget_table_grid2)

        widget_table_grid = QVBoxLayout()
        widget_table_grid.addWidget(layout_table_gridtodolist1)
        widget_table_grid.addWidget(layout_table_gridtodolist2)
        self.layout_table_gridtodolist = QWidget()
        self.layout_table_gridtodolist.setLayout(widget_table_grid)

    # Adds the data to the todolist table.
    def confirmation_button_todolist_clicked(self):
        new_todolist_type = self.todolist_type.currentText()
        new_edit_todolist_mode_description = self.edit_todolist_mode_description.text()
        new_status = self.status.currentText()

        todolist_input(new_todolist_type, new_edit_todolist_mode_description, new_status)
        self.load_table_todolist()

    # Updates the status for the highlighted row of the todolist layout.
    def update_button_todolist_clicked(self):
        self.table_todolist.setSortingEnabled(False)
        current_row = self.table_todolist.currentRow()
        if current_row < 0:
            return

        new_todolist_type = self.todolist_type.currentText()
        new_status = self.status.currentText()
        item = self.table_todolist.currentRow()
        id = self.table_todolist.item(item, 0).text()
        todolist_update(id, new_todolist_type, new_status)
        self.load_table_todolist()
        self.table_todolist.setSortingEnabled(True)

    # Deletes a row of data from the todolist table.
    def delete_button_todolist_clicked(self):
        self.table_todolist.setSortingEnabled(False)
        current_row = self.table_todolist.currentRow()
        if current_row < 0:
            return

        indexes = self.table_todolist.selectionModel().selectedRows()
        todolist_id_list = []
        for index in indexes:
            todolist_id_list.append(index.row())

        if todolist_id_list:
            for row in range(len(todolist_id_list)):
                todolist_id_list[row] = self.table_todolist.item(todolist_id_list[row], 0).text()
                row += 1
        else:
            todolist_id_list.append(self.table_todolist.item(current_row, 0).text())

        for todolist_id in todolist_id_list:
            todolist_delete(todolist_id)

        self.load_table_todolist()
        self.table_todolist.setSortingEnabled(True)
