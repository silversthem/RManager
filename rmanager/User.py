class User:
    def __init__(self,session,db): # Creates a user if possible
        self.session = session
        self.db      = db
        self.logged_on = False if not self.has_session() \
        else self.load(self.session['user_name'],self.session['user_password'])
    # State related
    def has_session(self): # Checks for a valid session
        return ('user_name' in self.session and 'user_password' in self.session)
    def login(self,username,pw): # Tries to connect an user
        if self.logged_on: # Already connected
            return True
        self.logged_on = self.load(username,pw) # Trying to connect
        if self.logged_on: # Trying to connect user infos
            # Creating session
            self.session['user_name']     = username
            self.session['user_password'] = pw
            return True
        else:
            return False
    def logout(self): # Disconnects a user
        if self.has_session():
            session.pop('user_name',None)
            session.pop('user_password',None)
    # Database related
    def load(self,name,pw): # Loads user from database if possible
        cursor = self.db.cursor()
        row = cursor.execute('SELECT * FROM User WHERE name = ? and password = ?',(name,pw)).fetchone()
        if row is not None: # Got a row
            u_id,teams,name,mail,password,rights = row
            teams = [k if k == 'all' else int(k) for k in teams.split(' ')]
            # Author parameters
            self.id       = u_id
            self.teams    = teams
            self.name     = name
            self.mail     = mail
            self.password = password
            self.rights   = int(rights)
            return True
        else: # Unable to authentify user
            return False
    # App related
    def has_permission(self,min_rights,whitelist_teams = None): # If user has permission
        if whitelist_teams is None: # Rights issue
            return min_rights <= self.rights
        else: # Rights and whitelist
            pass # @TODO team rights
    def get_rights(self): # Returns all things user can do to build options menu
        return
    def get_teams(self): # Returns all teams a user belongs to
        if 'all' in self.teams: # All teams
            return User.get_all_teams()
        else: # Fetching team names
            teams = []
            cursor = self.db.cursor()
            for team_id in self.teams:
                r = cursor.execute('SELECT * FROM Team WHERE id = ?',(team_id))
                if r is not None:
                    teams.append({"id":r[0],"name":r[1]})
            return teams
    def get_all_teams(self): # Returns all teams
        cursor = self.db.cursor()
        rows = cursor.execute('SELECT * FROM Team')
        return [{"id":r[0],"name":r[1]} for r in rows]
