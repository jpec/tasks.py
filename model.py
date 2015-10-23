# model.py
# Data model for tasks application.
# Author: Julien Pecqueur (julien@peclu.net)
# License: GPL

import sqlite3
import datetime
from config import DB, DEBUG

def debug(msg):
    if DEBUG:
        print(msg)

def today():
    n = datetime.datetime.now()
    return("{}-{}-{}".format(n.year, n.month, n.day))

def query(sql, args=None, commit=True):
    r = None
    db = sqlite3.connect(DB)
    c = db.cursor()
    debug(sql)
    if not args is None:
        debug(args)
        c.execute(sql, args)
    else:
        c.execute(sql)
    if commit:
        db.commit()
    if sql[0:6] == 'SELECT':
        r = c.fetchall()
    if sql[0:6] == 'INSERT':
        r = c.lastrowid
    db.close()
    return(r)

class Object():
    "Object"
    def __init__(self, oid=None, lb=None, fg='#000000', bg='#FFFFFF',
                 active=1, s='', i='', u='', d=''):
        self.__s = s
        self.__i = i
        self.__u = u
        self.__d = d
        if not oid is None:
            # existing object
            self.oid = int(oid)
            self.load()
        elif not lb is None:
            # new object
            self.lb = lb
            self.fg = fg
            self.bg = bg
            self.active = active
            self.new()
        else:
            # error
            return(None)
        debug((self.oid, self.lb))

    def load(self):
        d = query(self.__s, (self.oid, ))
        debug(d)
        for lb, fg, bg, active in d:
            self.lb = lb
            self.fg = fg
            self.bg = bg
            self.active = active

    def new(self):
        d = query(self.__i, (self.lb, self.fg, self.bg, self.active))
        self.oid = int(d)
        debug(d)

    def save(self):
        d = query(self.__u, (self.lb, self.fg, self.bg, self.active,
                             self.oid))
        debug(d)

    def delete(self):
        d = query(self.__d, (self.oid,))
        debug(d)

class Milestone(Object):
    "Milestone"
    def __init__(self, oid=None, lb=None, fg='#000000', bg='#FFFFFF',
                 active=1):
        s = "SELECT lb, fg, bg, active "\
            "FROM milestones "\
            "WHERE rowid=?"
        i = "INSERT INTO milestones(lb, fg, bg, active) "\
            "VALUES (?,?,?,?)"
        u = "UPDATE milestones "\
            "SET lb=?, fg=?, bg=?, active=? "\
            "WHERE rowid=?"
        d = "UPDATE milestones SET active=0 WHERE rowid=?"
        super().__init__(oid, lb, fg, bg, active, s, i, u, d)


class Team(Object):
    "Team"
    def __init__(self, oid=None, lb=None, fg='#000000', bg='#FFFFFF',
                 active=1):
        s = "SELECT lb, fg, bg, active "\
            "FROM teams "\
            "WHERE rowid=?"
        i = "INSERT INTO teams(lb, fg, bg, active) "\
            "VALUES (?,?,?,?)"
        u = "UPDATE teams "\
            "SET lb=?, fg=?, bg=?, active=? "\
            "WHERE rowid=?"
        d = "UPDATE teams SET active=0 WHERE rowid=?"
        super().__init__(oid, lb, fg, bg, active, s, i, u, d)

class Task():
    def __init__(self, oid=None, task=None, milestone=None, team=None,
                 active=1, done=0, urgent=0, date=today(),
                 updated=today(), evo=0):
        s = "SELECT task, milestone, active, done, urgent, team, "\
            "date, updated, evo "\
            "FROM tasks "\
            "WHERE rowid=?"
        i = "INSERT INTO tasks(task, milestone, active, done, "\
            "urgent, team, date, updated, evo) "\
            "VALUES (?,?,?,?,?,?,?,?,?)"
        u = "UPDATE tasks "\
            "SET task=?, milestone=?, active=?, done=?, urgent=?, "\
            "team=?, date=?, updated=?, evo=? "\
            "WHERE rowid=?"
        d = "UPDATE tasks SET active=0 WHERE rowid = ?"
        self.__s = s
        self.__i = i
        self.__u = u
        self.__d = d
        if not oid is None:
            # existing object
            self.oid = int(oid)
            self.load()
        elif not task is None:
            # new object
            self.task = task
            self.milestone = Milestone(oid=milestone)
            self.active = active
            self.done = done
            self.urgent = urgent
            self.team = Team(oid=team)
            self.date = date
            self.updated = updated
            self.evo = evo
            self.new()
        else:
            # error
            return(None)

    def load(self):
        d = query(self.__s, (self.oid, ))
        debug(d)
        for task, milestone, active, done, urgent, team, date, \
            updated, evo in d:
            self.task = task
            self.milestone = Milestone(oid=milestone)
            self.active = active
            self.done = done
            self.urgent = urgent
            self.team = Team(oid=team)
            self.date = date
            self.updated = updated
            self.evo = evo

    def new(self):
        d = query(self.__i, (self.task, self.milestone.oid, \
                             self.active, self.done, self.urgent, \
                             self.team.oid, self.date, self.updated, \
                             self.evo))
        self.oid = int(d)
        debug(d)

    def save(self):
        d = query(self.__u, (self.task, self.milestone.oid, self.active, \
                             self.done, self.urgent, self.team.oid, \
                             self.date, today(), self.evo, \
                             self.oid))
        debug(d)

    def set_milestone(self, oid):
        debug("set_milestone({})".format(oid))
        if not oid is None:
            self.milestone = Milestone(oid=oid)
            debug(self.milestone)

    def set_team(self, oid):
        debug("set_team({})".format(oid))
        if not oid is None:
            self.team = Team(oid=oid)
            debug(self.team)

    def delete(self):
        d = query(self.__d, (self.oid,))
        debug(d)

    def toggle_done(self):
        if self.done:
            self.done = 0
        else:
            self.done = 1
        self.save()

    def toggle_urgent(self):
        if self.urgent:
            self.urgent = 0
        else:
            self.urgent = 1
        self.save()

    def toggle_evo(self):
        if self.evo:
            self.evo = 0
        else:
            self.evo = 1
        self.save()

    def clone(self):
        new = Task(task=self.task, milestone=self.milestone.oid, \
                   team=self.team.oid, active=self.active, \
                   done=self.done, urgent=self.urgent, \
                   date=self.date, updated=today(), evo=self.evo)

def list_of_milestones():
    r = []
    q = query('SELECT rowid FROM milestones WHERE active=1 ORDER BY lb')
    for (oid,) in q:
        r.append(Milestone(oid=oid))
    return(r)

def list_of_teams():
    r = []
    q = query('SELECT rowid FROM teams WHERE active=1 ORDER BY lb')
    for (oid,) in q:
        r.append(Team(oid=oid))
    return(r)

def list_of_tasks():
    sql = 'SELECT t.rowid FROM tasks t, milestones m '\
          'WHERE t.milestone = m.oid AND t.active=1 '\
          'ORDER BY m.lb, t.task'
    r = []
    q = query(sql)
    for (oid,) in q:
        r.append(Task(oid=oid))
    return(r)
