import json
from pysphere import VIServer
class VMWare():
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.sserver = VIServer()
        self.sserver.connect(self.server, self.username, self.password)

    #GETS ALL SHARED VMS

    def getRegistered(self):
        return self.sserver.get_registered_vms(None, None, None, None)

    #SPECIFIC VM GETTER
    #NOT RECOMMENDED
    def getByName(self, name):
        try:
            return self.sserver.get_vm_by_name(name)
        except:
            return None
    #RECOMMENDED - Get from getRegistered method
    def getByPath(self, path):
        try:
            return self.sserver.get_vm_by_path(path)
        except:
            return None

    #PROPERTIES AND VARIABLES
    #TODO: check this works for windows!?
    def getEnvVar(self, name):
        try:
            machine = self.sserver.get_vm_by_name(name)
            return machine.get_environment_variables()
        except:
            return None

    def getStatus(self, name):
        try:
            machine = self.sserver.get_vm_by_path(name)
            return machine.get_status()
        except:
            return None

    def getInfo(self, name):
        try:
            machine = self.sserver.get_vm_by_path(name)
            x = machine.get_properties()
            stat = machine.get_status()
            ip = ""
            if "ip_address" in x:
                ip = x["ip_address"]
            ret = {
                "ip": ip,
                "status": stat,
                "memory": x["memory_mb"],
                "guest_full_name": x["guest_full_name"]
            }
            print ret
            #print x
            return ret
        except Exception as e:
            print e
            return None

    #POWER SETTINGS

    def machineOn(self, name):
        machine = self.sserver.get_vm_by_name(name)
        machine.power_on()

    def machineOff(self, name):
        machine = self.sserver.get_vm_by_name(name)
        machine.power_off()

    #Snapshots

    def getSnapshots(self, name):
        machine = self.sserver.get_vm_by_name(name)
        arr = []
        for snapshot in machine.get_snapshots():
            name = snapshot.get_name()
            desc = snapshot.get_description()
            create = snapshot.get_create_time()
            state = snapshot.get_state()
            path = snapshot.get_path()
            arr.append({
                "name": name,
                "desc": desc,
                "create": create,
                "state": state,
                "path": path
                #"parent": parent,
                #"children": children
            })
        return json.dumps(arr)

    def createSnapShot(self, name, snap, desc):
        machine = self.sserver.get_vm_by_name(name)
        machine.create_snapshot(snap, description=desc)
        return "OK"

    def deleteSnapShot(self, name, snap):
        machine = self.sserver.get_vm_by_name(name)
        machine.delete_snapshot_by_path(snap)
        return "OK"

    def revertSnapShot(self, name, snap):
        machine = self.sserver.get_vm_by_name(name)
        machine.revert_to_path(snap)
        return "OK"
