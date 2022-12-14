from datetime import datetime, timedelta
import psycopg2
import json

def plug_in(data, cycle) :
    try :
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['HOST']
        DBPORT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PORT']
        DBNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['NAME']
        DBUNM = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['USER']
        DBPWD = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['PWD']
        MSLT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['MSL']
        DSLT = SETTING['CORE']['Tanium']['OUTPUT']['DB']['PS']['TNM']['DSL']
        if cycle == 'minutely' :
            TNM = MSLT
            insertDate = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        elif cycle == 'daily' :
            TNM = DSLT
            yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
            insertDate = yesterday + " 23:59:59"

        insertConn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        insertCur = insertConn.cursor()
        if cycle == 'minutely':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    computer_id, computer_name, ipv_address, chassis_type, os_platform, operating_system, is_virtual, last_reboot,
                    driveUsage, ramUsage, cpuUsage, listenPortCountChange, establishedPortCountChange,
                    running_service_count, online, asset_list_statistics_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, '""" + insertDate + """'
                )
                ON CONFLICT (computer_id)
                DO UPDATE SET
                    computer_name = excluded.computer_name, 
                    ipv_address = excluded.ipv_address, 
                    chassis_type = excluded.chassis_type, 
                    os_platform = excluded.os_platform,
                    operating_system = excluded.operating_system,
                    is_virtual = excluded.is_virtual, 
                    last_reboot = excluded.last_reboot, 
                    driveUsage = excluded.driveUsage,
                    ramUsage = excluded.ramUsage,
                    cpuUsage = excluded.cpuUsage,
                    listenPortCountChange = excluded.listenPortCountChange,
                    establishedPortCountChange = excluded.establishedPortCountChange,
                    running_service_count = excluded.running_service_count,
                    online = excluded.online,
                    asset_list_statistics_collection_date = '""" + insertDate + """'                                                                
            """
        elif cycle == 'daily':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    computer_id, computer_name, ipv_address, chassis_type, os_platform, operating_system, is_virtual, last_reboot,
                    driveUsage, ramUsage, cpuUsage, listenPortCountChange, establishedPortCountChange,
                    running_service_count, online, asset_list_statistics_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, '""" + insertDate + """'
                )
            """
        datalen = len(data.computer_id)
        for i in range(datalen):
            CI = data.computer_id[i]
            CN = data.computer_name[i]
            IP = data.ipv_address[i]
            CT = data.chassis_type[i]
            OP = data.os_platform[i]
            OS = data.operating_system[i]
            IV = data.is_virtual[i]
            LR = data.last_reboot[i]
            DUS = data.driveUsage[i]
            RUS = data.ramUsage[i]
            CPUUS = data.cpuUsage[i]
            LPC = data.listenPortCountChange[i]
            EPC = data.establishedPortCountChange[i]
            RSC = data.running_service_count[i]
            OL = data.online[i]
            dataList = CI, CN, IP, CT, OP, OS, IV, LR, DUS, RUS, CPUUS, LPC, EPC, RSC, OL
            insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
    except ConnectionError as e:
        print(e)
