import sqlite3

# Creating database
db = sqlite3.connect('db.sqlite')

# User can be parts of teams
# Tasks can whitelist people from certain teams
# A task with a team value of all means everyone
# A user with a team value of all means accepted everywhere
db.execute('''
    CREATE TABLE Team(
        id   integer PRIMARY KEY AUTOINCREMENT,
        name varchar(64)
    )
''')
db.commit()

# User have different rights
# All above rank grants you powers from previous ranks
# Rights in task steps and tasks also go for related comments
# 0 - Not a user
# 1 - Can change state of task steps if team whitelisted
# 2 - Can create steps in tasks if team whitelisted and alter own created steps
# 3 - Can alter steps in tasks modified last by 1, 2 and 3 users
# 5 - Can create tasks for own team and everyone
# 6 - Can manage users in own team and rank them until 5th rank
# 7 - Can create tasks for other teams and is team whitelisted everywhere
# 8 - Can alter tasks from other users
# 9 - Can manage teams and rank users until 8th rank
# 10 - God lvl : Can rank other users until 10th rank and no user can undo your actions
#                (Except other gods). No god user is advised.
db.execute('''
    CREATE TABLE User(
        id       integer PRIMARY KEY AUTOINCREMENT,
        teams    varchar(128),
        name     varchar(64),
        mail     varchar(128),
        password varchar(256),
        rights   integer
    )
''')
db.commit()

# Task and Task_Step Tags are stored in a separate table for better recognition
# Few tags are preferable and recognition goes a long way assuring that
# Ideally this table will be fed before usage with a list of domain specific words
db.execute('''
    CREATE TABLE Tag(
        id   integer PRIMARY KEY AUTOINCREMENT,
        name varchar(64)
    )
''')
db.commit()

# A Task is linked to a collection of Task_Step
# The state of all steps defines the state of the task
# steps ordered is a boolean defining wether steps will be in a specific order or not
db.execute('''
    CREATE TABLE Task(
        id            integer PRIMARY KEY AUTOINCREMENT,
        teams         varchar(128),
        creator_id    integer,
        creation_date integer,
        name          varchar(128),
        description   varchar(256),
        tags          varchar(128),
        state         integer,
        steps_ordered integer,
        deadline      integer,
        FOREIGN KEY(creator_id) REFERENCES User(id)
    )
''')
db.commit()

# Task Step (and Tasks) can have different states
# 0 - IDLE
# 1 - Done
# 2 - Paused
# 3 - Failed (deadline over)
db.execute('''
    CREATE TABLE Task_Step(
        id            integer PRIMARY KEY AUTOINCREMENT,
        task_id       integer,
        creator_id    integer,
        creation_date integer,
        description   varchar(64),
        tags          varchar(128),
        state         integer,
        step_n        integer,
        deadline      integer,
        FOREIGN KEY(task_id) REFERENCES Task(id)
    )
''')
db.commit()

# Modification of Task_Step by a user
# All Modification are stored so everything can go in reverse if needed
db.execute('''
    CREATE TABLE Task_Step_State(
        id            integer PRIMARY KEY AUTOINCREMENT,
        task_step_id  integer,
        user_id       integer,
        creation_date integer,
        comment       varchar(256),
        state         integer,
        FOREIGN KEY(task_step_id) REFERENCES Task_Step(id),
        FOREIGN KEY(user_id)      REFERENCES User(id)
    )
''')
db.commit()

# Comments on Tasks left by users team whitelisted
db.execute('''
    CREATE TABLE Task_Comment(
        id            integer PRIMARY KEY AUTOINCREMENT,
        task_id       integer,
        user_id       integer,
        creation_date integer,
        comment       varchar(256),
        FOREIGN KEY(task_id) REFERENCES Task(id),
        FOREIGN KEY(user_id) REFERENCES User(id)
    )
''')
db.commit()

# Comments on task steps steps left by users team whitelisted
# Saves at what state of the task the comment was made, for clearer posteriori understanding
db.execute('''
    CREATE TABLE Task_Step_Comment(
        id            integer PRIMARY KEY AUTOINCREMENT,
        task_step_id  integer,
        on_state_id   integer,
        user_id       integer,
        creation_date integer,
        comment       varchar(256),
        FOREIGN KEY(task_step_id) REFERENCES Task_Step(id),
        FOREIGN KEY(on_state_id)  REFERENCES Task_Step_State(id),
        FOREIGN KEY(user_id)      REFERENCES User(id)
    )
''')
db.commit()

# Creating a god user
db.execute('INSERT INTO User VALUES (NULL,"all","admin","@.com","password","10")')
db.commit()

# And so it begins !

db.close()
