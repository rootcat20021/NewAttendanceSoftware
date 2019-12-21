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
        path = os.path.join(request.folder,'private','CTNAttendance.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.CTNAttendance_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_CTNAttendance'))

    FormUploadCanteenWWAttendance=form_factory(SQLField('CTNWWAttendance_xls','upload',uploadfolder='temporary'), formname='CTNWWATTENDANCE')
    if FormUploadCanteenWWAttendance.accepts(request.vars,session,formname='CTNWWATTENDANCE'):
        request.flash='Received: %s'%request.vars.CTNWWAttendance_xls
        path = os.path.join(request.folder,'private','CTNWWATtendance.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.CTNWWAttendance_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_CTNWWAttendance'))

    return dict(FormUploadCanteenAttendance=FormUploadCanteenAttendance,FormUploadCanteenWWAttendance=FormUploadCanteenWWAttendance,FormUploadSSDates=FormUploadSSDates,FormUploadSSCount=FormUploadSSCount,FormUploadMaster=FormUploadMaster,FormSSPreVisitParshadList=FormSSPreVisitParshadList,FormSSPostVisitParshadList=FormSSPostVisitParshadList)

def uploaddata_CTNAttendance():
    import pandas as pd
    import os
    import datetime as dt
    path = os.path.join(request.folder,'private','CTNAttendance.xlsx')
    pathlog = os.path.join(request.folder,'private','log_upload_CTNAttendance')
    logf = open(pathlog,'w')
    df = pd.read_excel(path)
    #First check data sanity
    #Critical errors:
    #5. Columns missing
    #6. Invalid Date time format
    #1. Check for GRNO repetition with overlapping dates
    #2. Check for out datetime less than in datetime
    #3. Check for out_datetime-in_datetime > 48 hrs
    #4. Check for in_datetime is in future
    #Non-critical errors:
    #1. Check for in_datetime in distant past
    #2. GRNO not in master
    #3. GRNO repetition for different date . Uploading many days at once
    Critical_Errors = pd.DataFrame(columns = ['Line No.','Error','List________________________________________________________________'])
    if not all(elem in ['GRNO','InDate','InTime','OutDate','OutTime'] for elem in df.columns):
        Critical_Errors.loc['HEADER_MISSING'] = [1,"Uploaded sheet must have these columns","GRNO,InDate,InTime,OutDate,OutTime"]
        return dict(Critical_Errors=Critical_Errors.to_html(index=False,justify='center',col_space=500))

    df['GRNO'] = df.apply(lambda row: row['GRNO'].upper(), axis=1)
 

    logf.write(df.to_string())
    logf.write("\n")
    logf.write(df.dtypes.to_string())
    logf.write("\n")
    if not df.dtypes.at['InDate'] == 'datetime64[ns]':
        Critical_Errors.loc[len(Critical_Errors.index)] = [1,"FORMAT MISMATCH","InDate format mismatch"]
    if not df.dtypes.at['OutDate'] == 'datetime64[ns]':
        Critical_Errors.loc[len(Critical_Errors.index)] = [1,"FORMAT MISMATCH","OutDate format mismatch"]
    if len(Critical_Errors.index)>0:
        return dict(Critical_Errors=Critical_Errors.to_html())

    df['InTime'] = pd.Series(map(lambda x:dt.timedelta(hours=x.hour,minutes=x.minute),df['InTime']))
    df['InDateTime'] = df.apply(lambda x:x.InDate + x.InTime,axis=1)
    df['OutTime'] = pd.Series(map(lambda x:dt.timedelta(hours=x.hour,minutes=x.minute),df['OutTime']))
    df['OutDateTime'] = df.apply(lambda x:x.OutDate + x.OutTime,axis=1)
    logf.write(df.to_string())
    logf.write("\n")
    for row in df.iterrows():
        logf.write("All GRNO with same date entry\n")
        logf.write(df[(df['GRNO']==row[1]['GRNO']) & (df['InDate']==row[1]['InDate'])].to_string())
        logf.write("\n")
        if len(row[1]['GRNO']) != 12:
            logf.write(str(len(row[1]['GRNO'])) + "\n")
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"GRNO is incomplete",row[1]['GRNO']]
        if len(df[(df['GRNO']==row[1]['GRNO']) & (df['InDate']==row[1]['InDate'])].index) > 1:
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"OVERLAPPING DATES",row[1]['GRNO'] + " has overlapping InDates " + row[1]['InDate'].strftime("%d-%b-%y")]
        if len(df[(df['GRNO']==row[1]['GRNO']) & (df['OutDate']==row[1]['OutDate'])].index) > 1:
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"OVERLAPPING DATES",row[1]['GRNO'] + " has overlapping OutDate " + row[1]['OutDate'].strftime("%d-%b-%y")]
        if row[1]['InDateTime'] >= row[1]['OutDateTime']:
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"EXIT BEFORE ENTRY",row[1]['GRNO'] + " In " + row[1]['InDateTime'].strftime("%d-%b %H:%M") + " Out " + row[1]['OutDateTime'].strftime("%d-%b %H:%M")]
        if (row[1]['OutDateTime'] - row[1]['InDateTime']) >= dt.timedelta(hours=48):
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"ATTENDANCE FOR MORE THAN ONE DAY",row[1]['GRNO'] + " In " + row[1]['InDateTime'].strftime("%d-%b %H:%M") + " Out " + row[1]['OutDateTime'].strftime("%d-%b %H:%M")]

    if len(Critical_Errors.index)>0:
        logf.close()
        return dict(Critical_Errors=Critical_Errors.to_html(index=False,justify='center',col_space=500))
    

    for row in df.iterrows():
        dbData.CtnAttendance.insert(GRNO=row[1]['GRNO'],ENTRY=row[1]['InDateTime'],EXIT=row[1]['OutDateTime'])

    logf.close()
    return("Upload Successful")
