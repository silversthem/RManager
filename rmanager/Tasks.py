from time import time

class Tasks:
    def __init__(self,user,db):
        self.user     = user
        self.database = db
    # Static
    @staticmethod
    def task():
        return {"name":"","description":"","tags":"","deadline":""}
    @staticmethod
    def format(sql_tuple):
        pass
    # Task Related
    def add(self,form): # Adds a new task
        task_data = Tasks.task()
        for k in task_data:
            if form.get(k) is None: # Parameter missing
                return False
            task_data[k] = form.get(k)
        teams = ' ' # @TODO
        # Tags handling @TODO
        # Adding task
        cursor = self.database.cursor()
        cursor.execute('INSERT INTO Task VALUES (NULL,?,?,?,?,?,?,?,?,?)', \
            (teams,self.user.id,time(),task_data["name"],task_data["description"],task_data["tags"], \
                0,task_data.get("ordered_steps",0),task_data["deadline"]))
        task_id = cursor.lastrowid
        self.database.commit()
        # Adding steps
        steps_len = form.get('steps-n')
        for i in range(1,int(steps_len)+1):
            self.add_step(task_id,i,form.get('step'+str(i)+'_text'),form.get('step'+str(i)+'_tags'))
        return True
    def get(self,task_id,**options): # Returns a task
        cursor = self.database.cursor()
        return cursor.execute('SELECT * FROM Task WHERE id = ' + str(int(task_id)))
    def update_task(self,task,update): # Changes something in an existing task
        pass
    def update_task_state(self,task): # Updates task state by reading task steps states
        pass
    def count(self): # Total amount of tasks
        pass
    def get_multiple(self,start,end,**options): # Returns multiple tasks
        cursor = self.database.cursor()
        # @TODO Constraints
        r = cursor.execute('SELECT * FROM Task ORDER BY creation_date DESC LIMIT ? OFFSET ?',(end,start))
        if options.get('as_dict') == True: # Converting each entry to a key/value pair
            tasks_dicts = []
            for task in r:
                v = {"id":task[0],"date":task[3],"desc":task[5],"name":task[4]}
                if options.get('with_steps') == True:
                    v['steps'] = self.get_task_steps(task[0],as_dict=True)
                tasks_dicts.append(v)
            return tasks_dicts
        else:
            return r
    # Task State related
    # @TODO
    # Task Step related
    def add_step(self,task_id,n,text,tags): # Adds a new task step
        cursor = self.database.cursor()
        # @TODO : Step deadline
        cursor.execute('INSERT INTO Task_Step VALUES (NULL,?,?,?,?,?,?,?,?)',(task_id,self.user.id,time(),text,tags,0,n,0))
        self.database.commit()
    def update_step(self,task,step,update):
        pass
    def get_task_steps(self,task,**options):
        cursor = self.database.cursor()
        r = cursor.execute('SELECT * FROM Task_Step WHERE task_id = ' + str(int(task)))
        if options.get('as_dict') == True: # Converting each entry to a key/value pair
            step_dicts = []
            for step in r:
                v = {"id":step[0],"task_id":step[1],"date":step[3],"desc":step[4]}
                step_dicts.append(v)
            return step_dicts
        else:
            return r
    # Task Step State related
    # @TODO
