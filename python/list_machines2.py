import os
output=os.popen("virsh list --all").readlines()
def list_machines(vm_list=None):
    machines=dict()
    if input:
        vm_list=vm_list[2:]
        machine_line_splitted = [ machine_string.split() for machine_string in vm_list]
        for machine_string in machine_line_splitted:
            if bool(machine_string):
                vm_name=machine_string[1]
                machine_status = ''.join(machine_string[2:])
                machines[vm_name]=dict()
                machines[vm_name]['status']=machine_status
    return machines

def list_interfaces(machine):
    output=os.popen("virsh domiflist %s" % ( machine) ).readlines()
    interfaces_list=output[2:]
    interfaces = list()
    interfaces = [ interface_line.split() for interface_line in interfaces_list]
    port_list = [[interfaces[x][0],interfaces[x][1],interfaces[x][4]] for x in range(len(interfaces)) if bool(interfaces[x])]
    return port_list


machines=list_machines(output)
for machine in machines.keys():
    interface = list_interfaces(machine)
    machines[machine]['network']=interface

for machine in machines:
    print("%-20s is %-5s with " % (machine,machines[machine]['status']) , end='')
    for port in machines[machine]['network']:
        print("[ network device %s %s and mac %s ] " % (port[0],port[1],port[2]),end='')
    print()
