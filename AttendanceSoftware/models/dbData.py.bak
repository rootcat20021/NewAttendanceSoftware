dbData = DAL('mysql://rootcat:a7133783@rootcat.mysql.pythonanywhere-services.com/rootcat$AttendanceDB')

#dbData.SSDates.drop()
#dbData.SSCounts.drop()
#dbData.CtnWWAttendance.drop()
#dbData.CtnAttendance.drop()
#dbData.Master.drop()
dbData.define_table(
    'SSDates',
    Field('GRNO'),
    Field('DATE','datetime'),
    Field('TYPE'),
    redefine=True
)


dbData.define_table(
    'CtnWWAttendance',
    Field('GRNO'),
    Field('DATE','datetime'),
    Field('Remarks'),
    Field('SSMarkingDate','datetime'),
    Field('SSMarked','boolean'),
    redefine=True,
    format = '%(GRNO)s'
)

dbData.define_table(
    'CtnAttendance',
    Field('GRNO'),
    Field('ENTRY','datetime'),
    Field('EXIT','datetime'),
    Field('SSDate','datetime'),
    Field('SSMarked','boolean'),
    redefine=True,
    format = '%(GRNO)s'
)

dbData.define_table(
    'SSCounts',
    Field('NewID'),
    Field('Name'),
    Field('Father_Husband_Name'),
    Field('status'),
    Field('Initiated_Status'),
    Field('Gender'),
    Field('B','integer'),
    Field('w','integer'),
    Field('V1','integer'),
    Field('V2','integer'),
    Field('V3','integer'),
    Field('V4','integer'),
    Field('Total','integer'),
    Field('TotalVisit','integer'),
    Field('NewNumbers'),
    redefine=True,
    format = '%(NewID)s'
)

dbData.define_table(
    'Master',
    Field('GRNO'),
    Field('CANTEEN'),
    Field('JATHA'),
    Field('VISIT_CANTEEN'),
    Field('SSCount','reference SSCounts'),
    Field('SSDates','list:reference SSDates'),
    Field('CtnAttendance','list:reference CtnAttendance'),
    Field('CtnWWAttendance','list:reference CtnWWAttendance'),
    redefine=True,
    format = '%(GRNO)s')
dbData.Master.GRNO.requires = IS_NOT_EMPTY('')
dbData.Master.CANTEEN.requires = IS_NOT_EMPTY()
dbData.Master.JATHA.requires = IS_NOT_EMPTY()
dbData.Master.VISIT_CANTEEN.requires = IS_NOT_EMPTY()
dbData.Master.VISIT_CANTEEN.requires = IS_IN_SET([1,2,3,4,5,6,'ADMIN','SHED','2-A','2-B'])
dbData.Master.CANTEEN.requires = IS_IN_SET([1,2,3,4,5,6,'ADMIN','SHED','2-A','2-B'])
