# ui.py
# UI managment for tasks application.
# Author: Julien Pecqueur (julien@peclu.net)
# License: GPL

from bottle import template, redirect
import config, model

def process(request, mode, oid):
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


