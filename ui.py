# ui.py
# UI managment for tasks application.
# Author: Julien Pecqueur (julien@peclu.net)
# License: GPL

from bottle import template, redirect
import config, model

def process(request, page, mode, oid):
    if page == 'tasks':
        return(tasks(request, mode, oid))
    if page in ['milestones', 'teams']:
        return(admin(request, page, mode, oid))
    return("(404)")


def tasks(request, mode, oid):
    if mode is None:
        return(template('tasks.html', t=None, d=model, c=config, \
                        m=mode))
    if mode in ['edit', 'delete', 'urgent', 'done', 'evo', 'clone'] \
       and not oid is None:
        task = model.Task(oid=oid)
        if not task is None and mode == 'edit':
            if not request.query.save == 'Save':
                return(template('tasks.html', t=task, d=model, \
                                c=config, m=mode))
            else:
                # sauvegarde tâche éditée
                task.task = request.query.task
                task.set_milestone(request.query.milestone)
                task.set_team(request.query.team)
                task.date = request.query.date
                task.urgent = request.query.urgent
                task.done = request.query.done
                task.evo = request.query.evo
                task.save()
        if not task is None and mode == 'delete':
            task.delete()
        if not task is None and mode == 'urgent':
            task.toggle_urgent()
        if not task is None and mode == 'done':
            task.toggle_done()
        if not task is None and mode == 'evo':
            task.toggle_evo()
        if not task is None and mode == 'clone':
            task.clone()
    if mode == 'new':
        if not request.query.save == 'Save':
            return(template('tasks.html', t=None, d=model,\
                            c=config, m=mode))
        else:
            # sauvegarde tâche éditée
            task = model.Task(task=request.query.task,\
                             milestone=request.query.milestone, \
                             team=request.query.team, \
                             done=request.query.done, \
                             urgent=request.query.urgent, \
                             date=request.query.date, \
                             evo=request.query.evo)
    redirect('/')

def admin(request, page, mode, oid):
    if mode is None:
        return(template('admin.html', page=page, t=None, d=model, c=config, m=mode))
    if mode in ['edit', 'delete', 'clone'] \
       and not oid is None:
        if page == 'teams':
            elt = model.Team(oid=oid)
        if page == 'milestones':
            elt = model.Milestone(oid=oid)
        if not elt is None and mode == 'edit':
            if not request.query.save == 'Save':
                return(template('admin.html', page=page, t=elt, d=model, c=config, m=mode))
            else:
                elt.lb = request.query.lb
                elt.fg = request.query.fg
                elt.bg = request.query.bg
                elt.active = request.query.active
                elt.save()
        if not elt is None and mode == 'delete':
            elt.delete()
        if not elt is None and mode == 'clone':
            elt.clone()
    if mode == 'new':
        if not request.query.save == 'Save':
            return(template('admin.html', page=page, t=None, d=model, c=config, m=mode))
        else:
            if page == 'teams':
                elt = model.Team(lb=request.query.lb, fg=request.query.fg, bg=request.query.bg, active=request.query.active)
            if page == 'milestones':
                elt = model.Milestone(lb=request.query.lb, fg=request.query.fg, bg=request.query.bg, active=request.query.active)
    redirect('/')
