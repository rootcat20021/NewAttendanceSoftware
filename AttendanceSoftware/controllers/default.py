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

def myonupdate(form):
    print('update!')
    print(form.vars)

def update():
    import os
    import datetime as dt
    import pandas as pd
    import numpy as np
    SewadarTable = ''
    dict_GLOBAL_TIMINGS = dbData(dbData.GLOBAL_TIMINGS.id>0).select().as_dict()
    for key in dict_GLOBAL_TIMINGS.keys():
        dict_GLOBAL_TIMINGS = dict_GLOBAL_TIMINGS[key]

    pathlog = os.path.join(request.folder,'private','log_update')
    logf = open(pathlog,'w')
    response.subtitle = "Upload excel file "
    from gluon.sqlhtml import form_factory
    FormUploadMaster=form_factory(SQLField('Master_xls','upload',uploadfolder='temporary'),formname='MASTER')
    if FormUploadMaster.accepts(request.vars,session,formname='MASTER'):
        response.flash='Received: %s'%request.vars.Master_xls
        path = os.path.join(request.folder,'private','Master_xls.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.Master_xls.file,open(path, 'wb'))
        redirect(URL(r=request, f='uploaddata_Master'))

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
        path = os.path.join(request.folder,'private','SSCounts.xlsx')
        import shutil
        shutil.copyfileobj(request.vars.SSAttendanceCount_xls.file,open(path, 'wb'))
        #Then redirect to the next screen (or do the processing now)
        redirect(URL(r=request, f='uploaddata_SSCounts'))

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


    FormUpdateSewadar=form_factory(SQLField('Sewadar_ID'), formname='UPDATE_SEWADAR')
    if FormUpdateSewadar.accepts(request.vars,session,formname='UPDATE_SEWADAR'):
        GRNO = request.vars.Sewadar_ID
        request.flash='Requesting: %s'%request.vars.Sewadar_ID
        SewadarTable=SQLFORM.grid(dbData.CtnAttendance.GRNO==GRNO,user_signature=False)

    FormCreateDailyAttendanceReport=form_factory(SQLField('Date','datetime',default=dt.datetime.now(),requires=IS_NOT_EMPTY()),formname='FormCreateDailyAttendanceReport')
    if FormCreateDailyAttendanceReport.accepts(request.vars,session,formname='FormCreateDailyAttendanceReport'):
        Date = dt.datetime.strptime(request.vars.Date, "%Y-%m-%d %H:%M:%S")
        dpath = os.path.join(request.folder,'private','DailyAttendanceReport_' + Date.strftime("%d-%b-%y") +  '.xlsx')
        writer = pd.ExcelWriter(dpath)
        logf.write("\nGLOBAL_DICT\n")
        logf.write("\n-----------\n")
        logf.write(str(dict_GLOBAL_TIMINGS))
        logf.write("\n-----------\n")
        df_CtnDates = pd.DataFrame.from_dict(dbData((dbData.CtnAttendance.ENTRY < Date.replace(hour=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].minute,second=0)) & (dbData.CtnAttendance.EXIT > Date.replace(hour=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].minute,second=0))).select().as_dict(),orient='index')
        if len(df_CtnDates.index)==0:
            response.flash('No Canteen Attendance available for selected day')
            return (-1)

        df_Master = pd.DataFrame.from_dict(dbData(dbData.Master.id>0).select().as_dict(),orient='index')
        logf.write(df_CtnDates.to_string())
        logf.write("\n")
        logf.write(df_Master.to_string())
        df_merged_inner = pd.merge(how='left',left=df_CtnDates,right=df_Master,left_on='GRNO',right_on='GRNO')
        df_merged_inner.loc[:,'PRESENT'] = 1
        df_merged_inner['PRESENT'] = pd.Series(map(lambda x:1,df_merged_inner.index))
        logf.write("\n")
        logf.write(df_merged_inner.to_string())
        logf.write("\n")
        pivot_table = pd.pivot_table(df_merged_inner,values=['PRESENT'],index=['CANTEEN'],aggfunc=np.sum)
        pivot_table.to_excel(writer,sheet_name='ALL_CANTEEN_SUMMARY',startrow=2)
        df_SewaSchedule = pd.DataFrame.from_dict(dbData((dbData.SewaSchedule.DATE > Date.replace(hour=0,minute=0,second=0)) & (dbData.SewaSchedule.DATE < Date.replace(hour=0,minute=0,second=0) + dt.timedelta(hours=24))).select().as_dict(),orient='index')
        df_merged_left = pd.merge(how='left',left=df_SewaSchedule,right=df_merged_inner,left_on='CANTEEN',right_on='CANTEEN')
        logf.write("\n")
        logf.write(df_merged_left.to_string())
        df_merged_left['PRESENT_LAST_NIGHT_TO_TONIGHT'] = pd.Series(map(lambda en,ex: 1 if (en < Date.replace(hour=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].minute,second=0) - dt.timedelta(days=1)) and (ex > Date.replace(hour=dict_GLOBAL_TIMINGS['NIGHT_EXIT_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['NIGHT_EXIT_SAMPLE_POINT'].minute,second=0)) and (ex < Date.replace(hour=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].minute,second=0)) else 0,df_merged_left['ENTRY'],df_merged_left['EXIT']))
        df_merged_left['PRESENT_TODAY_MORNING_TO_TODAY_EVENING'] = pd.Series(map(lambda en,ex: 1 if (en > Date.replace(hour=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].minute,second=0) - dt.timedelta(days=1)) and (en < Date.replace(hour=dict_GLOBAL_TIMINGS['MORNING_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['MORNING_ENTRY_SAMPLE_POINT'].minute,second=0)) and (ex > Date.replace(hour=dict_GLOBAL_TIMINGS['EVENING_EXIT_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['EVENING_EXIT_SAMPLE_POINT'].minute,second=0)) and (ex < Date.replace(hour=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].minute,second=0)) else 0,df_merged_left['ENTRY'],df_merged_left['EXIT']))
        df_merged_left['PRESENT_TODAY_MORNING_TO_TOMORROW_MORNING'] = pd.Series(map(lambda en,ex: 1 if (en > Date.replace(hour=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['NIGHT_ENTRY_SAMPLE_POINT'].minute,second=0) - dt.timedelta(days=1)) and (en < Date.replace(hour=dict_GLOBAL_TIMINGS['MORNING_ENTRY_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['MORNING_ENTRY_SAMPLE_POINT'].minute,second=0)) and (ex > Date.replace(hour=dict_GLOBAL_TIMINGS['MORNING_EXIT_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['MORNING_EXIT_SAMPLE_POINT'].minute,second=0) + dt.timedelta(days=1)) else 0,df_merged_left['ENTRY'],df_merged_left['EXIT']))
        logf.write("\n")
        logf.write(df_merged_left.to_string())
        logf.close()
        pivot_table = pd.pivot_table(df_merged_left,values=['PRESENT_LAST_NIGHT_TO_TONIGHT'],index=['CANTEEN'],aggfunc=np.sum)
        pivot_table.to_excel(writer,sheet_name='TODAY_SUMMARY',startrow=2)
        pivot_table = pd.pivot_table(df_merged_left,values=['PRESENT_TODAY_MORNING_TO_TODAY_EVENING'],index=['CANTEEN'],aggfunc=np.sum)
        pivot_table.to_excel(writer,sheet_name='TODAY_SUMMARY',startrow=5)
        pivot_table = pd.pivot_table(df_merged_left,values=['PRESENT_TODAY_MORNING_TO_TOMORROW_MORNING'],index=['CANTEEN'],aggfunc=np.sum)
        pivot_table.to_excel(writer,sheet_name='TODAY_SUMMARY',startrow=9)

        writer.close()
        return response.stream(open(dpath,'rb'), chunk_size=10**6)

    FormCreateSSAttendanceForUpload=form_factory(SQLField('Date','datetime',default=dt.datetime.now(),requires=IS_NOT_EMPTY()),formname='FormCreateSSAttendanceForUpload')
    if FormCreateSSAttendanceForUpload.accepts(request.vars,session,formname='FormCreateSSAttendanceForUpload'):
        Date = dt.datetime.strptime(request.vars.Date, "%Y-%m-%d %H:%M:%S")
        dpath = os.path.join(request.folder,'private','DailySSAttendanceForUpload_' + Date.strftime("%d-%b-%y") +  '.csv')
        df_CtnDates = pd.DataFrame.from_dict(dbData((dbData.CtnAttendance.ENTRY < Date.replace(hour=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].minute,second=0)) & (dbData.CtnAttendance.EXIT > Date.replace(hour=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].hour,minute=dict_GLOBAL_TIMINGS['PRESENCE_SAMPLE_POINT'].minute,second=0))).select().as_dict(),orient='index')
        if len(df_CtnDates.index)==0:
            response.flash('No Canteen Attendance available for selected day')
            return (-1)
        df_Master = pd.DataFrame.from_dict(dbData(dbData.Master.id>0).select().as_dict(),orient='index')
        logf.write(df_CtnDates.to_string())
        logf.write("\n")
        logf.write(df_Master.to_string())
        df_Exempted24hr_Jathas = pd.DataFrame.from_dict(dbData((dbData.EXEMPTED24HR_JATHAS.id > 0)).select().as_dict(),orient='index')
        df_Exempted24hr_Canteens = pd.DataFrame.from_dict(dbData((dbData.EXEMPTED24HR_CANTEENS.id > 0)).select().as_dict(),orient='index')
        df_Exempted24hr_GRNO = pd.DataFrame.from_dict(dbData((dbData.EXEMPTED24HR_GRNO.id > 0)).select().as_dict(),orient='index')

        logf.write(df_CtnDates.to_string())
        logf.write("\n")

        df_merged_left = pd.merge(how='left',left=df_CtnDates,right=df_Master,left_on='GRNO',right_on='GRNO')
        df_merged_left = pd.merge(how='left',left=df_merged_left,right=df_Exempted24hr_Jathas,left_on='JATHA',right_on='JATHA')
        df_merged_left = pd.merge(how='left',left=df_merged_left,right=df_Exempted24hr_Canteens,left_on='CANTEEN',right_on='CANTEEN')
        df_merged_left = pd.merge(how='left',left=df_merged_left,right=df_Exempted24hr_GRNO,left_on='GRNO',right_on='GRNO')

        logf.write("\n------After all the megring-------\n")
        logf.write(df_merged_left.to_string())
        logf.write("\n")
        logf.write(df_Master.to_string())

        df_merged_left['PRESENT'] = pd.Series(map(lambda x,y,z,en,ex: 1 if (x==1) or (y==1) or (z==1) or (ex-en).total_seconds() > dict_GLOBAL_TIMINGS['MINIMUM_HOURS_24HR']*3600 else 0,df_merged_left['EXEMPTION_24HR_JATHA'],df_merged_left['EXEMPTION_24HR_CANTEEN'],df_merged_left['EXEMPTION_24HR_GRNO'],df_merged_left['ENTRY'],df_merged_left['EXIT']))
        df_PRESENT = df_merged_left.loc[df_merged_left['PRESENT']==1]
        df_PRESENT['TYPE'] = pd.Series(data=['D']*len(df_PRESENT.index),index=df_PRESENT.index)
        df_PRESENT['DATE'] = pd.Series(data=[dt.datetime.strftime(Date,"%Y-%b-%d")]*len(df_PRESENT.index),index=df_PRESENT.index)
        logf.write("\n------After deducing presence-------\n")
        logf.write(df_PRESENT.to_string())
        logf.write("\n")
        logf.write(df_PRESENT.to_string())

        df_PRESENT.to_csv(dpath,index=False,header=False,columns=['GRNO','TYPE','DATE'])

        return response.stream(open(dpath,'rb'), chunk_size=10**6,filename='SSUpload.csv',attachment=True)

    logf.close()
    return dict(FormUploadCanteenAttendance=FormUploadCanteenAttendance,FormCreateDailyAttendanceReport=FormCreateDailyAttendanceReport,FormCreateSSAttendanceForUpload=FormCreateSSAttendanceForUpload,FormUploadCanteenWWAttendance=FormUploadCanteenWWAttendance,FormUploadSSDates=FormUploadSSDates,FormUploadSSCount=FormUploadSSCount,FormUploadMaster=FormUploadMaster,FormSSPreVisitParshadList=FormSSPreVisitParshadList,FormSSPostVisitParshadList=FormSSPostVisitParshadList,FormUpdateSewadar=FormUpdateSewadar,SewadarTable=SewadarTable)

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
    Critical_Errors = pd.DataFrame(columns = ['Line No.','Error','List_________________________________________________________________________________'])
    if not all(elem in df.columns for elem in ['GRNO','InDate','InTime','OutDate','OutTime']):
        Critical_Errors.loc['HEADER_MISSING'] = [1,"Exp col GRNO,InDate,InTime,OutDate,OutTime",str(list(df.columns))]
        return dict(Critical_Errors=Critical_Errors.to_html(index=False,justify='center',col_space=10000),text_message=str(list(df.columns)))

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
        return dict(Critical_Errors=Critical_Errors.to_html(),text_message="Failed to load")

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
        if len(row[1]['GRNO']) != 6:
            logf.write(str(len(row[1]['GRNO'])) + "\n")
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"GRNO is incomplete",row[1]['GRNO']]
        if len(df[(df['GRNO']==row[1]['GRNO']) & (df['InDate']==row[1]['InDate'])].index) > 1:
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"OVERLAPPING DATES",row[1]['GRNO'] + " has overlapping InDates " + row[1]['InDate'].strftime("%d-%b-%y")]
        #if len(df[(df['GRNO']==row[1]['GRNO']) & (df['OutDate']==row[1]['OutDate'])].index) > 1:
        #    Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"OVERLAPPING DATES",row[1]['GRNO'] + " has overlapping OutDate " + row[1]['OutDate'].strftime("%d-%b-%y")]
        if row[1]['InDateTime'] >= row[1]['OutDateTime']:
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"EXIT BEFORE ENTRY",row[1]['GRNO'] + " In " + row[1]['InDateTime'].strftime("%d-%b %H:%M") + " Out " + row[1]['OutDateTime'].strftime("%d-%b %H:%M")]
        if (row[1]['OutDateTime'] - row[1]['InDateTime']) >= dt.timedelta(hours=48):
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"ATTENDANCE FOR MORE THAN ONE DAY",row[1]['GRNO'] + " In " + row[1]['InDateTime'].strftime("%d-%b %H:%M") + " Out " + row[1]['OutDateTime'].strftime("%d-%b %H:%M")]
        if not pd.isnull(row[1]['MAPPED DATE']):
            if row[1]['MAPPED DATE'].replace(hour=23,minute=59,second=59) < row[1]['InDateTime']:
                Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"MAPPED DATE BEFORE ENTRY",row[1]['GRNO'] + " has mapped date " + row[1]['MAPPED DATE'].strftime("%d-%b-%y") + " before entry date " + row[1]['InDate'].strftime("%d-%b-%y")]

    if len(Critical_Errors.index)>0:
        logf.close()
        return dict(Critical_Errors=Critical_Errors.to_html(index=False,justify='center',col_space=500),text_message="Failed to load")
    

    for row in df.iterrows():
        dbData.CtnAttendance.insert(GRNO="BH0011" + row[1]['GRNO'],ENTRY=row[1]['InDateTime'],EXIT=row[1]['OutDateTime'],SSTentativeMapping=row[1]['MAPPING DATE'])

    logf.close()
    return dict(Critical_Errors=Critical_Errors.to_html(),text_message="Loaded Successfully")

def uploaddata_CTNWWAttendance():
    import pandas as pd
    import os
    import datetime as dt
    path = os.path.join(request.folder,'private','CTNWWAttendance.xlsx')
    pathlog = os.path.join(request.folder,'private','log_upload_CTNWWAttendance')
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
    if not all(elem in ['GRNO','DATE','Remark'] for elem in df.columns):
        Critical_Errors.loc['HEADER_MISSING'] = [1,"Uploaded sheet must have these columns","GRNO,DATE,Remark"]
        return dict(Critical_Errors=Critical_Errors.to_html(index=False,justify='center',col_space=500))

    df['GRNO'] = df.apply(lambda row: row['GRNO'].upper(), axis=1)
 

    logf.write(df.to_string())
    logf.write("\n")
    logf.write(df.dtypes.to_string())
    logf.write("\n")
    if not df.dtypes.at['DATE'] == 'datetime64[ns]':
        Critical_Errors.loc[len(Critical_Errors.index)] = [1,"FORMAT MISMATCH","DATE format mismatch"]
    if len(Critical_Errors.index)>0:
        return dict(Critical_Errors=Critical_Errors.to_html())

    logf.write(df.to_string())
    logf.write("\n")
    for row in df.iterrows():
        logf.write("All GRNO with same date entry\n")
        logf.write(df[(df['GRNO']==row[1]['GRNO']) & (df['InDate']==row[1]['InDate'])].to_string())
        logf.write("\n")
        if len(row[1]['GRNO']) != 6:
            logf.write(str(len(row[1]['GRNO'])) + "\n")
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"GRNO is incomplete",row[1]['GRNO']]
        if len(df[(df['GRNO']==row[1]['GRNO']) & (df['DATE']==row[1]['DATE'])].index) > 1:
            Critical_Errors.loc[len(Critical_Errors.index)] = [row[0]+2,"OVERLAPPING DATES",row[1]['GRNO'] + " has overlapping DATE " + row[1]['DATE'].strftime("%d-%b-%y")]

    if len(Critical_Errors.index)>0:
        logf.close()
        return dict(Critical_Errors=Critical_Errors.to_html(index=False,justify='center',col_space=500))
    
    for row in df.iterrows():
        dbData.CtnWWAttendance.insert(GRNO="BH0011" + row[1]['GRNO'],DATE=row[1]['DATE'],Remark=row[1]['Remark'])

    logf.close()
    return dict(Critical_Errors=Critical_Errors.to_html())



def SewaDayCanteen(Date):
    return("1")

def uploaddata_Master():
    import os
    import re
    import pandas as pd
    path = os.path.join(request.folder,'private','Master_xls.xlsx')
    pathlog = os.path.join(request.folder,'private','log_uploadMaster')
    logf = open(pathlog,'w')
    Critical_Errors = pd.DataFrame(columns = ['Line No.','Error','List________________________________________________________________'])
    df_Master = None
    try:
        df_Master = pd.read_excel(path,sheet_name="Master",usecols=['GR ID','JATHA','CANTEEN','VISIT CANTEEN'])
    except:
        Critical_Errors.loc['MISSING_SHEET'] = [0,"MASTER SHEET MISSING","PLEASE MAKE SURE THAT UPLOADED WORKBOOK HAS A SHEET NAMED Master"]
        logf.close()
        return dict(Critical_Errors=Critical_Errors.to_html())


    MAPPING = {'GR ID':'GRNO','CANTEEN':'CANTEEN','JATHA':'JATHA','VISIT CANTEEN':'VISIT_CANTEEN'}
    dbData(dbData.Master.id>0).delete()
    for row in df_Master.iterrows():
        logf.write(str(row))
        row_dict = {}
        for col in row[1].keys():
            value = row[1][col]
            try:
                value = re.sub("\s*$","",value)
            except:
                pass

            try:
                value = value.upper()
            except:
                pass

            if MAPPING[col] == 'GRNO':
                if len(value) != 6:
                    Critical_Errors.loc['INCORRECT GRNO'] = [row[0],"INCORRECT GRNO",value]
                    return dict(Critical_Errors=Critical_Errors.to_html())
                else:
                    value = "BH0011" + value

            if MAPPING[col] == 'CANTEEN':
                value = str(value)
            if MAPPING[col] == 'VISIT_CANTEEN':
                value = str(value)

            row_dict[MAPPING[col]] = value

        dbData.Master.insert(**row_dict)

    response.flash = T("Entry Successful!")
    logf.close()
    return dict(Critical_Errors=Critical_Errors.to_html())

def uploaddata_SSCounts():
    import os
    import re
    import pandas as pd
    path = os.path.join(request.folder,'private','SSCounts.xlsx')
    pathlog = os.path.join(request.folder,'private','log_upload_SSCount')
    logf = open(pathlog,'w')
    Critical_Errors = pd.DataFrame(columns = ['Line No.','Error','List________________________________________________________________'])
    MAPPING = {}
    df_SSCounts = pd.read_excel(path,usecols=['NewID', 'Name', 'Father_Husband_Name', 'status', 'Initiated_Status', 'Gender', 'B', 'w', 'V1', 'V2', 'V3', 'V4', 'Total', 'TotalVisit','NewNumbers'])
    for col in df_SSCounts.columns:
        MAPPING[col] = col

    dbData(dbData.SSCounts.id>0).delete()
    for row in df_SSCounts.iterrows():
        logf.write(str(row))
        row_dict = {}
        for col in row[1].keys():
            value = row[1][col]
            try:
                value = re.sub("\s*$","",value)
            except:
                pass

            try:
                value = value.upper()
            except:
                pass

            row_dict[MAPPING[col]] = value

        dbData.SSCounts.insert(**row_dict)

    response.flash = T("Entry Successful!")
    logf.close()
    return dict(Critical_Errors=Critical_Errors.to_html())
