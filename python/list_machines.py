import os
output=os.popen("virsh list --all").readlines()
def list_machines(vm_list=None):
    machines=dict()
    if input:
        vm_list=vm_list[2:]
        for machine_string in vm_list:
            machine_line_splitted = machine_string.split()
            if len(machine_line_splitted) > 0:
                vm_name=machine_line_splitted[1]
                machine_status = ""
                for status in machine_line_splitted[2:]:
                    machine_status += status
                    machines[vm_name]=dict()
                    machines[vm_name]['status']=machine_status
    return machines

def list_interfaces(machine):
    output=os.popen("virsh domiflist %s" % ( machine) ).readlines()
    interfaces_list=output[2:]
    interfaces = list()
    for interface_line in interfaces_list:
        interface = interface_line.split()
        if len(interface) > 0: # we have a line, it's not an empty line
            interface_name=interface[0]
            interface_mac=interface[4]
            interfaces.append([interface_name,interface_mac])
        return interfaces


machines=list_machines(output)
for machine in machines.keys():
    interface = list_interfaces(machine)
    machines[machine]['network']=interface

for machine in machines:
    print("%-20s is %-5s with Network device %-5s and network mac %s" % (machine,machines[machine]['status'],
        machines[machine]['network'][0][0],machines[machine]['network'][0][1]))
