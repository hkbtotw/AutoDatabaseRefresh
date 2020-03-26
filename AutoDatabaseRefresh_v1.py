import pandas as pd   
import numpy as np
import pyodbc

filepath='C:/Users/70018928/Documents/Project2020/MAC/AuditLog_test.xlsx'

dfIn=pd.read_excel(filepath)

# Check length of the new data : output is number of rows in this new table
lengthIn=len(dfIn)
print(' Rows of new data ==> ',lengthIn)


dfCheck=dfIn.copy()

#print(' ==> ',dfIn)
def Write_data(df_input):
    df_write=df_input.replace([np.inf,-np.inf,np.nan],-999)
    #print(df_write.head())
    
    conn1 = pyodbc.connect('Driver={SQL Server Native Client 11.0};'
                        'Server=SBNDCBIDSCIDB01;'
                        'Database=TBL_ADS;'
                        'Trusted_Connection=yes;')
    cursor=conn1.cursor()

    print("Displaying records in database : FCT_POWER_BI_AUDIT_LOG_test")
    sql_select_query='select * from TBL_ADS.dbo.FCT_POWER_BI_AUDIT_LOG_test '
    print(" sql : ",sql_select_query)
    record = pd.read_sql(sql_select_query,conn1)
    record1=record.drop(columns=['ID'],axis=1)
    df_write.columns=['CREATIONDATE', 'USERID', 'OPERATION', 'AUDITDATA']

    dfOld=record1.iloc[-lengthIn:]
    print(' tail : ',dfOld)
    olddataIdList=dfOld['AUDITDATA'].values.tolist()
    #print(' list : ', olddataIdList)

    # Create WriteList by checking the rows of new AuditData, not the same as those in database
    # output : List of AuditData
    count=0
    notWriteList=[]
    for n in olddataIdList:
        business=dfCheck.loc[dfCheck['AuditData']==n,'AuditData'].tolist()
        #print(' --- ',business, ' :: ', n )
        if(len(business)>0):
            #print(count,' -- ',n)
            notWriteList.append(n)
        else:
            print('  no value  ')
        count+=1
    #print(' notWriteList: ',notWriteList, ' == ',len(notWriteList))

    # Write new data
    for index, row in df_write.iterrows():
        #print("index:",index,"; row:\n",row['AUDITDATA'])
        
        wList=[]
        for n in notWriteList:
            if(row['AUDITDATA']==n):
                wList.append(n)
        #print(' len : ',len(wList))

        if(len(wList)==0):
            print('--- write ---')
            cursor.execute("""INSERT INTO TBL_ADS.dbo.FCT_POWER_BI_AUDIT_LOG_test
            ([CREATIONDATE], [USERID], [OPERATION], [AUDITDATA])
            values(?,?,?,?)""", 
            row['CREATIONDATE'],
            row['USERID'],
            row['OPERATION'],        
            row['AUDITDATA'])
            conn1.commit()

    cursor.close()
    conn1.close()



    print('------------Complete WriteDB-------------')
   
Write_data(dfIn)