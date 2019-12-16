# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

#@auth.requires_login()
def admin():
    msg = "wow"
    return dict(msg=msg)

def update():
    import os
    response.subtitle = "Upload excel file "
    from gluon.sqlhtml import form_factory
    FormUploadMaster=form_factory(SQLField('Master_xls','upload',uploadfolder='temporary'),SQLField('RunNow','string',default='No',requires=IS_IN_SET(['Yes','No'])),formname='MASTER')
    if FormUploadMaster.accepts(request.vars,session,formname='MASTER'):
        request.flash='Received: %s'%request.vars.Master_xls
        path = os.path.join(request.folder,'private','Master_xls.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.Master_xls.file,open(path, 'wb'))
        from datetime import timedelta as timed
        scheduler.queue_task('uploaddata_Master',
            start_time=request.now + timed(seconds=30),
            timeout = 6000)

    FormUploadSSDates=form_factory(SQLField('SSAttendanceDates_xls','upload',uploadfolder='temporary'), SQLField('RunNow','string',default='No',requires=IS_IN_SET(['Yes','No'])),formname='SSATTENDANCE')
    if FormUploadSSDates.accepts(request.vars,session,formname='SSATTENDANCE'):
        request.flash='Received: %s' % request.vars.SSAttendanceDates_xls
        path = os.path.join(request.folder,'private','SSAttendanceDates_xls.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.SSAttendanceDates_xls.file,open(path, 'wb'))
        from datetime import timedelta as timed
        scheduler.queue_task('uploaddata_SSAttendance',
            start_time=request.now + timed(seconds=30),
            timeout = 6000)

    FormUploadSSCount=form_factory(SQLField('SSAttendanceCount_xls','upload',uploadfolder='temporary'),formname='SSATTENDANCECOUNT')
    if FormUploadSSCount.accepts(request.vars,session,formname='SSATTENDANCECOUNT'):
        request.flash='Received: %s'%request.vars.SSAttendanceCount_xls
        path = os.path.join(request.folder,'private','SSAttendanceCount_xls.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.SSAttendanceCount_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_SSAttendanceCount'))

    FormSSPreVisitParshadList=form_factory(SQLField('SSPreVisitParshadList_xls','upload',uploadfolder='temporary'), formname='SSPREVISITPARSHAD')
    if FormSSPreVisitParshadList.accepts(request.vars,session,formname='SSPREVISITPARSHAD'):
        request.flash='Received: %s'%request.vars.SSPreVisitParshadList_xls
        path = os.path.join(request.folder,'private','SSPreVisitParshadList.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.SSPreVisitParshadList_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_SSPreVisitParshadList'))

    FormSSPostVisitParshadList=form_factory(SQLField('SSPostVisitParshadList_xls','upload',uploadfolder='temporary'), formname='SSPOSTVISITPARSHAD')
    if FormSSPostVisitParshadList.accepts(request.vars,session,formname='SSPOSTVISITPARSHAD'):
        request.flash='Received: %s'%request.vars.SSPostVisitParshadList_xls
        path = os.path.join(request.folder,'private','SSPostVisitParshadList.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.SSPostVisitParshadList_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_SSPostVisitParshadList'))

    FormUploadCanteenAttendance=form_factory(SQLField('CTNAttendance_xls','upload',uploadfolder='temporary'),formname='CTNATTENDANCE')
    if FormUploadCanteenAttendance.accepts(request.vars,session,formname='CTNATTENDANCE'):
        request.flash='Received: %s'%request.vars.CTNAttendance_xls
        path = os.path.join(request.folder,'private','CTNATtendance.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.CTNAttendance_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_CTNAttendance'))

    FormUploadCanteenWWAttendance=form_factory(SQLField('CTNWWAttendance_xls','upload',uploadfolder='temporary'), formname='CTNWWATTENDANCE')
    if FormUploadCanteenAttendance.accepts(request.vars,session,formname='CTNWWATTENDANCE'):
        request.flash='Received: %s'%request.vars.CTNWWAttendance_xls
        path = os.path.join(request.folder,'private','CTNWWATtendance.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.CTNWWAttendance_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_CTNWWAttendance'))

    return dict(FormUploadCanteenAttendance=FormUploadCanteenAttendance,FormUploadCanteenWWAttendance=FormUploadCanteenWWAttendance,FormUploadSSDates=FormUploadSSDates,FormUploadSSCount=FormUploadSSCount,FormUploadMaster=FormUploadMaster,FormSSPreVisitParshadList=FormSSPreVisitParshadList,FormSSPostVisitParshadList=FormSSPostVisitParshadList)
