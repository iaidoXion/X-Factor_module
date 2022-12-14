import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
def plug_in(data, classification, itemType) :
    DL = []
    RD = []
    CNM = itemType
    for c in range(len(data.computer_id)):
        if classification == 'os' :
            DL.append(data.os_platform[c])
        elif classification == 'operating_system' :
            DL.append(data.operating_system[c])
        elif classification == 'virtual' :
            DL.append(data.is_virtual[c])
        elif classification == 'asset' :
            DL.append(data.chassis_type[c])
        elif classification == 'installed_applications' :
            for d in data.installed_applications_name[c].replace('"', '').replace('{', '').replace('}', '').split(',') :
                DL.append(d)
        elif classification == 'listen_port_count_change' :
            DL.append(data.listenPortCountChange[c])
        elif classification == 'established_port_count_change' :
            DL.append(data.establishedPortCountChange[c])
        elif classification == 'running_service' :
            for d in data.running_service[c] :
                DL.append(d)
        elif classification == 'drive_usage_size_exceeded' :
            DL.append(data.drive[c])
        elif classification == 'ram_usage_size_exceeded' :
            DL.append(data.ram[c])
        elif classification == 'cpu_usage_size_exceeded' :
            DL.append(data.cpu[c])
        elif classification == 'last_reboot_exceeded' :
            DL.append(data.last_reboot[c])
        elif classification == 'group_ram_usage_exceeded' :
            if data.ram[c] == '95Risk' :
                DL.append(data.ip_group[c])
        elif classification == 'group_cpu_usage_exceeded' :
            if data.cpu[c] == '95Risk':
                DL.append(data.ip_group[c])
        elif classification == 'group_listen_port_count_change' :
            if data.listenport_count[c] == 'Yes':
                DL.append(data.ip_group[c])
        elif classification == 'group_established_port_count_change' :
            if data.establishedport_count[c] == 'Yes':
                DL.append(data.ip_group[c])
        elif classification == 'group_running_service_count_exceeded' :
            if data.running_service_count[c] == 'Yes':
                DL.append(data.ip_group[c])
        elif classification == 'group_last_reboot' :
            if data.last_reboot[c] == 'Yes':
                DL.append(data.ip_group[c])
        elif classification == 'group_drive_usage_size_exceeded' :
            if data.drive[c] == '99Risk':
                DL.append(data.ip_group[c])
        elif classification == 'group_server_count' :
            DL.append(data.ip_group[c])

    DF = pd.DataFrame(DL, columns=[CNM])
    DFG = DF.groupby([CNM]).size().reset_index(name='counts')
    DFGS = DFG.sort_values(by="counts", ascending=False)

    if classification == 'os' :
        statistics_unique = classification + '_' + DFGS.OP
        item = DFGS.OP
    if classification == 'operating_system' :
        statistics_unique = classification + '_' + DFGS.OS
        item = DFGS.OS
    elif classification == 'virtual':
        statistics_unique = classification + '_' + DFG.IV
        item = DFGS.IV
    elif classification == 'asset':
        statistics_unique = classification+'_'+DFGS.CT
        item = DFGS.CT
    elif classification == 'installed_applications':
        statistics_unique = classification+'_'+DFGS.IANM
        item = DFGS.IANM
    elif classification == 'listen_port_count_change':
        statistics_unique = classification+'_'+ DFGS.LPC
        item = DFGS.LPC
    elif classification == 'established_port_count_change':
        statistics_unique = classification + '_' + DFGS.EPC
        item = DFGS.EPC
    elif classification == 'running_service':
        statistics_unique = classification + '_' + DFGS.RSNM
        item = DFGS.RSNM
    elif classification == 'drive_usage_size_exceeded':
        statistics_unique = classification + '_' + DFGS.DUS
        item = DFGS.DUS
    elif classification == 'ram_usage_size_exceeded':
        statistics_unique = classification + '_' + DFGS.RUS
        item = DFGS.RUS
    elif classification == 'cpu_usage_size_exceeded':
        statistics_unique = classification + '_' + DFGS.CPU
        item = DFGS.CPU
    elif classification == 'last_reboot_exceeded':
        statistics_unique = classification + '_' + DFGS.LRB
        item = DFGS.LRB
    elif classification == 'group_ram_usage_exceeded' or classification == 'group_cpu_usage_exceeded' or classification == 'group_listen_port_count_change' or classification == 'group_established_port_count_change' or classification  == 'group_running_service_count_exceeded' or classification == 'group_last_reboot' or classification == 'group_drive_usage_size_exceeded':
        statistics_unique = classification + '_' + DFGS.ip_group
        item = DFGS.ip_group


    elif classification == 'group_server_count':
        statistics_unique = classification + '_' + DFGS.ip_group
        item = DFGS.ip_group


    item_count = DFG.counts

    for DFC in range(len(DFGS)) :
        RD.append([statistics_unique[DFC], classification, item[DFC], item_count[DFC]])
    return RD

