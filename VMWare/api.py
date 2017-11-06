from bottle import route, run, template, request, response

def getname(path, vmware):
    p = vmware.getByPath(path)
    props = p.get_properties()
    return props["name"]

class API():

    def __init__(self, vmware, port):
        self.port = port
        @route('/hello/<name>')
        def index(name):
            return template('<b>Hello {{name}}</b>!', name=name)

        @route('/vmware/getRegistered')
        def getRegistered():
            return vmware.getRegistered()

        @route('/vmware/getStatus/<path:path>')
        def getStatus(path):
            name = getname(path, vmware)
            return vmware.getStatus(path)

        @route('/vmware/info/<path:path>')
        def getInfo(path):
            name = getname(path, vmware)
            return vmware.getInfo(path)

        @route('/vmware/on/<path:path>')
        def on(path):
            name = getname(path, vmware)
            vmware.machineOn(name)
            return 'OK'

        @route('/vmware/off/<path:path>')
        def off(path):
            name = getname(path, vmware)
            vmware.machineOff(name)
            return 'OK'

        @route('/vmware/snapshots/<path:path>')
        def snapshotCreate(path):
            name = getname(path, vmware)
            if request.query["method"] == "get":
                return vmware.getSnapshots(name)
            if request.query["method"] == "create":
                return vmware.createSnapShot(name, request.query["nname"], request.query["desc"])
            if request.query["method"] == "delete":
                return vmware.deleteSnapShot(name, request.query["nname"])
            if request.query["method"] == "revert":
                return vmware.revertSnapShot(name, request.query["nname"])
            return "err"

        run(host='localhost', port=port)
