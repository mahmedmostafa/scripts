#This script has been made in order to fix a problem with virtual machines not starting
#Because the storage admins re-zoned the storage and changed the ports.
#That lead to machines being either in shutoff state or in error state when --hard rebooted.
#The error string in nova-compute 
#ERROR oslo_messaging.rpc.server NoFibreChannelVolumeDeviceFound: Unable to find a Fibre Channel volume device
# Coming from https://github.com/openstack/os-brick/blob/newton-eol/os_brick/initiator/connectors/fibre_channel.py#L115

import pymysql.cursors
import json

# Please note that the script needs some manual changes at this stage. Do not use it just yet and please 
# Always consult me before using it 
connection = pymysql.connect(host='<ip>', user='nova', password='<password>', db='nova', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor,autocommit=True)
#Replace this with the new target wwn
new_target_wwn = ["500507680C254A70","500507680C264A70","500507680C354A70","500507680C364A70","500507680C554A70","500507680C564A70","500507680C254B0B","500507680C264B0B","500507680C354B0B","500507680C364B0B","500507680C554B0B","500507680C564B0B"]

try:
    with connection.cursor() as cursor:
        sql = "SELECT connection_info from block_device_mapping"
        cursor.execute(sql)
        results = cursor.fetchall()
        old_ports = ["500507680C224B0B", "500507680C324B0B", "500507680C224A70", "500507680C324A70"] # Replace this with the old ports 
        for result in results:
                #connection_info = json.loads(string(result))
                if(result['connection_info']):
                        connection_info=json.loads(result['connection_info'])
                        if(connection_info):
                                controllers = len(connection_info['connector']['wwpns'])
                                print("Check mark 0")
                                if ( controllers == 2 ):
                                        print("Checkmark 1")
                                        controller0 = connection_info['connector']['wwpns'][0]
                                        controller1 = connection_info['connector']['wwpns'][1]
                                        print("Current target_wwn list %s " % connection_info['data']['target_wwn'])
                                        for item in old_ports:
                                                if ( item in connection_info['data']['target_wwn'] ):
                                                        volume_id = connection_info['data']['volume_id']
                                                        connection_info['data']['target_wwn'] = new_target_wwn
                                                        connection_info['data']['initiator_target_map'][controller1] = new_target_wwn
                                                        connection_info['data']['initiator_target_map'][controller0] = new_target_wwn
                                                        update_connection_info = json.dumps(connection_info,ensure_ascii=False)
                                                        update_sql = "UPDATE block_device_mapping set connection_info='%s' where volume_id='%s'" % (update_connection_info, volume_id)
                                                        print("Got a match on volume %s on port %s , Updating nova's database" % ( volume_id, item ) )
                                                        cursor.execute(update_sql)
                                                        break # We have found a port we do not need to loop again
finally:
    connection.close()