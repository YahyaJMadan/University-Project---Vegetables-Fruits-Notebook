from PyQt6.QtSql import QSqlQuery, QSqlDatabase

def database():
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName("VegetablesFruitsDatabase_NoteBook.db")

    if not connection.open():
        return False

    query = QSqlQuery()
    query.exec("""
            CREATE TABLE IF NOT EXISTS vegetables_and_fruits
                (vegetable_or_fruit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                Icon TEXT,
                name TEXT,
                type TEXT,
                link TEXT
                );
            """)

    query.exec("""
            CREATE TABLE IF NOT EXISTS alternative_names
                (alternative_name_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vegetable_or_fruit_id INTEGER,
                alternative_name TEXT,
                FOREIGN KEY (vegetable_or_fruit_id)
                REFERENCES vegetables_and_fruits(vegetable_or_fruit_id)
                );
            """)

    query.exec("""
            CREATE TABLE IF NOT EXISTS months
                (months_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vegetable_or_fruit_id INTEGER,
                month TEXT,
                FOREIGN KEY (vegetable_or_fruit_id)
                REFERENCES vegetables_and_fruits(vegetable_or_fruit_id)
                );
            """)

    query.exec("""
            CREATE TABLE IF NOT EXISTS nutritions
                (nutrition_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vegetable_or_fruit_id INTEGER,
                nutrition TEXT,
                FOREIGN KEY (vegetable_or_fruit_id)
                REFERENCES vegetables_and_fruits(vegetable_or_fruit_id)
                );
            """)

    query.exec("""
            CREATE TABLE IF NOT EXISTS plant_requirements
                (plant_requirements_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vegetable_or_fruit_id INTEGER,
                difficulty TEXT,
                quantity TEXT,
                stage TEXT,
                space FLOAT,
                water FLOAT,
                sun_endurance TEXT,
                soil_requirement TEXT,
                minimum_days_to_next_stage INTEGER,
                maximum_days_to_next_stage INTEGER,
                FOREIGN KEY (vegetable_or_fruit_id)
                REFERENCES vegetables_and_fruits(vegetable_or_fruit_id)
                );
            """)

    query.exec("""
            CREATE TABLE IF NOT EXISTS todolist
                (todolist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                description TEXT,
                status TEXT
                );
            """)

    return True

# Loading data to be used in the app.

def vegetables_and_fruits_load():
    query = QSqlQuery('SELECT * FROM vegetables_and_fruits')

    vegetables_and_fruits_list = []
    while query.next():
        row = [query.value(i) for i in range(5)]
        vegetables_and_fruits_list.append(row)

    return vegetables_and_fruits_list

def alternative_names_load(vegetable_or_fruit_id):
    query = QSqlQuery('SELECT * FROM alternative_names WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    alternative_names_list = []
    if query.exec():
        while query.next():
            row = [query.value(i) for i in range(3)]
            alternative_names_list.append(row)

    return alternative_names_list

def months_load(vegetable_or_fruit_id):
    query = QSqlQuery('SELECT * FROM months WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    months_list = []
    if query.exec():
        while query.next():
            row = [query.value(i) for i in range(3)]
            months_list.append(row)

    return months_list

def nutritions_load(vegetable_or_fruit_id):
    query = QSqlQuery('SELECT * FROM nutritions WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    nutrition_list = []
    if query.exec():
        while query.next():
            row = [query.value(i) for i in range(3)]
            nutrition_list.append(row)

    return nutrition_list

def plant_requirements_load(vegetable_or_fruit_id):
    query = QSqlQuery('SELECT * FROM plant_requirements WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    plant_requirements_list = []
    if query.exec():
        while query.next():
            row = [query.value(i) for i in range(11)]
            plant_requirements_list.append(row)

    return plant_requirements_list

def todolist_load():
    query = QSqlQuery('SELECT * FROM todolist')

    todolist_list = []
    while query.next():
        row = [query.value(i) for i in range(4)]
        todolist_list.append(row)

    return todolist_list

# Input data into the database.

def vegetables_and_fruits_input(icon, name, type, link):
    query = QSqlQuery()
    query.prepare('''INSERT INTO vegetables_and_fruits
                    (icon, name, type, link) VALUES (?, ?, ?, ?)
                    ''')
    query.addBindValue(icon)
    query.addBindValue(name)
    query.addBindValue(type)
    query.addBindValue(link)

    query.exec()

    return query.lastInsertId()

def alternative_names_input(vegetable_or_fruit_id, alternative_name):
    query = QSqlQuery()
    query.prepare('''INSERT INTO alternative_names
                    (vegetable_or_fruit_id, alternative_name) VALUES (?, ?)
                    ''')
    query.addBindValue(vegetable_or_fruit_id)
    query.addBindValue(alternative_name)

    return query.exec()

def months_input(vegetable_or_fruit_id, month):
    query = QSqlQuery()
    query.prepare('''INSERT INTO months
                    (vegetable_or_fruit_id, month) VALUES (?, ?)
                    ''')
    query.addBindValue(vegetable_or_fruit_id)
    query.addBindValue(month)

    return query.exec()

def nutritions_input(vegetable_or_fruit_id, nutrition):
    query = QSqlQuery()
    query.prepare('''INSERT INTO nutritions
                    (vegetable_or_fruit_id, nutrition) VALUES (?, ?)
                    ''')
    query.addBindValue(vegetable_or_fruit_id)
    query.addBindValue(nutrition)

    return query.exec()

def plant_requirements_input(vegetable_or_fruit_id, difficulty, quantity, stage, space, water, sun_endurance, soil_requirement, minimum_days_to_next_stage, maximum_days_to_next_stage):
    query = QSqlQuery()
    query.prepare('''INSERT INTO plant_requirements
                    (vegetable_or_fruit_id, difficulty, quantity, stage, space, water, sun_endurance, soil_requirement, minimum_days_to_next_stage, maximum_days_to_next_stage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''')
    query.addBindValue(vegetable_or_fruit_id)
    query.addBindValue(difficulty)
    query.addBindValue(quantity)
    query.addBindValue(stage)
    query.addBindValue(space)
    query.addBindValue(water)
    query.addBindValue(sun_endurance)
    query.addBindValue(soil_requirement)
    query.addBindValue(minimum_days_to_next_stage)
    query.addBindValue(maximum_days_to_next_stage)

    return query.exec()

def todolist_input(type, description, status):
    query = QSqlQuery()
    query.prepare('''INSERT INTO todolist
                    (type, description, status) VALUES (?, ?, ?)
                    ''')
    query.addBindValue(type)
    query.addBindValue(description)
    query.addBindValue(status)

    return query.exec()

# Updates the data in the database.

def vegetables_and_fruits_update(vegetable_or_fruit_id, icon, type, name, link):
    query = QSqlQuery()
    query.prepare('''UPDATE vegetables_and_fruits
                    SET icon = ?, type = ?, name = ?, link = ?
                    WHERE vegetable_or_fruit_id = ?
                    ''')
    query.addBindValue(icon)
    query.addBindValue(type)
    query.addBindValue(name)
    query.addBindValue(link)
    query.addBindValue(vegetable_or_fruit_id)

    return query.exec()

def alternative_names_update(alternative_name_id, alternative_name):
    query = QSqlQuery()
    query.prepare('''UPDATE alternative_names
                    SET alternative_name = ?
                    WHERE alternative_name = ?
                    ''')
    query.addBindValue(alternative_name)
    query.addBindValue(alternative_name_id)

    return query.exec()

def months_update(month_id, month):
    query = QSqlQuery()
    query.prepare('''UPDATE months
                    SET month = ?
                    WHERE month_id = ?
                    ''')
    query.addBindValue(month)
    query.addBindValue(month_id)

    return query.exec()

def nutritions_update(nutrition_id, nutrition):
    query = QSqlQuery()
    query.prepare('''UPDATE nutritions
                    SET nutrition = ?
                    WHERE nutrition_id = ?
                    ''')
    query.addBindValue(nutrition)
    query.addBindValue(nutrition_id)

    return query.exec()

def plants_requirements_update(plants_requirements_id, difficulty, quantity, stage, space, water, sun_endurance, soil_requirement, minimum_days_to_next_stage, maximum_days_to_next_stage):
    query = QSqlQuery()
    query.prepare('''UPDATE plants_requirements
                    SET difficulty = ?, quantity = ?, stage = ?, space = ?, water = ?, sun_endurance = ?, soil_requirement = ?, minimum_days_to_next_stage = ?, maximum_days_to_next_stage = ?
                    WHERE plants_requirements_id = ?
                    ''')
    query.addBindValue(difficulty)
    query.addBindValue(quantity)
    query.addBindValue(stage)
    query.addBindValue(space)
    query.addBindValue(water)
    query.addBindValue(sun_endurance)
    query.addBindValue(soil_requirement)
    query.addBindValue(minimum_days_to_next_stage)
    query.addBindValue(maximum_days_to_next_stage)
    query.addBindValue(plants_requirements_id)

    return query.exec()

def todolist_update(todolist_id, type, status):
    query = QSqlQuery()
    query.prepare('''UPDATE todolist
                    SET type = ?, status = ?
                    WHERE todolist_id = ?
                    ''')
    query.addBindValue(type)
    query.addBindValue(status)
    query.addBindValue(todolist_id)

    return query.exec()

# Deletes data from the database.

def vegetables_and_fruits_delete(vegetable_or_fruit_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM vegetables_and_fruits WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    return query.exec()

def alternative_names_delete(vegetable_or_fruit_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM alternative_names WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    return query.exec()

def months_delete(vegetable_or_fruit_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM months WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    return query.exec()

def nutritions_delete(vegetable_or_fruit_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM nutritions WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    return query.exec()

def plants_requirements_delete(vegetable_or_fruit_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM plant_requirements WHERE vegetable_or_fruit_id = ?')
    query.addBindValue(vegetable_or_fruit_id)

    return query.exec()

def todolist_delete(todolist_id):
    query = QSqlQuery()
    query.prepare('DELETE FROM todolist WHERE todolist_id = ?')
    query.addBindValue(todolist_id)

    return query.exec()
