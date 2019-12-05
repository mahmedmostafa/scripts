#!/bin/python
#Written by Alex
#TODO
# Enable CLI arguments for all of the required information [DONE]
# Enable DryRun options [DONE]
# Enable set delete to yes by default [DONE]
# Enable jump hosts
# Enable multi backends ( not really accute now )
import argparse
from cinderclient import client as cinderclient
from novaclient import client as novaclient
import paramiko
import base64
import os
import time 


def check_backend(ssh_client, volume_id):
    _command_string = "lsvdiskhostmap volume-%s" % volume_id 
    out, err = ssh_client.exec_command(_command_string)[1:]
    output_string = out.read()
    mapped_host = ""
    if len(output_string) > 0: #It's connected
        mapped_host = output_string.split()[-5:-4]
    return mapped_host

def unmap_backend(ssh_client, host_id, volume_id):
    _command_string = "rmvdiskhostmap -host %s volume-%s" % (host_id, volume_id)
    out, err = ssh_client.exec_command(_command_string)[1:] #This ont does not return an output :/ so we have to check again ? not sure
    output_string = out.read()
    return output_string

def force_detach(cinder_client, volume):
    cinder_client.volumes.reset_state(volume, "available", attach_status="detached") #we gonna set the volume to active and detached

def delete_volume(cinder_client, volume):
     cinder_client.volumes.force_delete(volume)

def do_remove():
    while True:
        answer = raw_input("Should I remove ? (y/n): ")
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            print("What was that")


parser = argparse.ArgumentParser(prog='cleanup.py', usage='%(prog)s [options]', description="Cleanup \
all stuck cinder volumes that has attachment to non existant nova server")

parser.add_argument('--dryrun', help='dru run', choices=['enable'])
parser.add_argument('--delete', help='delete the volumes after unmapping them', choices=['yes'])
parser.add_argument('--os-username', help='OpenStack Username')
parser.add_argument('--os-password', help='OpenStack password')
parser.add_argument('--os-project-name', help='OpenStack project name')
parser.add_argument('--os-auth-urlv3', help='OpenStack authentication url for api version 3')
parser.add_argument('--os-auth-urlv2', help='OpenStack authentication url for api version 2')
parser.add_argument('--svc-username', required=True, help='FC SVC storage username')
parser.add_argument('--svc-password', required=True, help='FC SVC storage password')
parser.add_argument('--svc-ip', required=True, help='FC SVC storage ip')

args = parser.parse_args()
OS_USER_NAME = os.environ.get('OS_USERNAME',args.os_username)
OS_PASSWORD = os.environ.get('OS_PASSWORD',args.os_password)
OS_PROJECT_NAME = os.environ.get('OS_PROJECT_NAME',args.os_project_name)
OS_AUTH_URLV3 = os.environ.get('OS_AUTH_URL',args.os_auth_urlv3)
OS_AUTH_URLV2 = os.environ.get('OS_AUTH_URL',args.os_auth_urlv2)

SVC_HOST = args.svc_ip
SVC_USERNAME = args.svc_username
SVC_PASSWORD = args.svc_password

if not(OS_USER_NAME) or not(OS_PASSWORD) or not(OS_PROJECT_NAME) or not(OS_AUTH_URLV3):
    parser.print_help()
    exit(-1)


cinder = cinderclient.Client('2', OS_USER_NAME, OS_PASSWORD, OS_PROJECT_NAME, OS_AUTH_URLV3)
nova = novaclient.Client('2', OS_USER_NAME, OS_PASSWORD, OS_PROJECT_NAME, OS_AUTH_URLV2)

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(SVC_HOST, username=SVC_USERNAME, password=SVC_PASSWORD)


volumes = cinder.volumes.findall()
all_servers = nova.servers.list(search_opts={'all_tenants' : 1 }) #We have to do this early because this api does not support findall like cinder

for volume in volumes:
    state = volume.status
    servers = []
    for attachment in volume.attachments:
        servers.append(attachment['server_id'])
        
    for server in servers: #This is ugly but will refactor later
        found = False 
        for instance in all_servers:
            if str(instance.id) == str(server): #then the server exists, do nothing
                found = True 
        if found == False: #Now we have to take action and 1) check the volume in the backend 2) Remove the volume from cinder
            mapped_host  = check_backend(ssh_client,volume.id)
            if len(mapped_host) > 0 : #We have a host
                print("Volume %s is %s and has attachment to non existant server %s is mapped to host %s"  % 
                (volume.id, state, server, mapped_host) )
                if not(args.dryrun): #Only unmap and delete if this is not a dryrun
                    output = unmap_backend(ssh_client,mapped_host,volume.id)
                    print("Volume has been unmapped %s " % output)
                    force_detach(cinder, volume)
                    print("Sleeping 3 seconds")
                    time.sleep(3)
                    if not(args.delete):
                        if do_remove() == True:
                            delete_volume(cinder, volume)
                    else:
                        delete_volume(cinder, volume)

            else:
                #The volume has attachment to non existent server, but it does't have a mapping to a host
                #we should just go ahead and reset this volume now
                print("Volume %s has attachment to non existent server %s but it's not mapped to any host" %
                (volume.id, server))
                if not(args.dryrun):
                    force_detach(cinder, volume)
                    print("Sleeping 3 seconds")
                    time.sleep(3)
                    if not(args.delete):
                        if do_remove() == True:
                            delete_volume(cinder, volume)
                    else:
                        delete_volume(cinder, volume)
        else: #If we found a volume that is attached to an instance we need to make sure that it's not in any other state but detached
            if state != "in-use":
                print("This volume %s is attached to %s but it's in %s state" % 
                ( volume.id, server, state ) )
                #We should only report this for now
        
