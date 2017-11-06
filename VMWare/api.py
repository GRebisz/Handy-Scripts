from bottle import route, run, template, request, response

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
            return vmware.getStatus(path)

        @route('/vmware/info/<path:path>')
        def getInfo(path):
            return vmware.getInfo(path)

        @route('/vmware/on/<path:path>')
        def on(path):
            vmware.machineOn(path)
            return 'OK'

        @route('/vmware/off/<path:path>')
        def off(path):
            vmware.machineOff(path)
            return 'OK'

        @route('/vmware/snapshots/<path:path>')
        def snapshotCreate(path):
            if request.query["method"] == "get":
                return vmware.getSnapshots(path)
            if request.query["method"] == "create":
                return vmware.createSnapShot(path, request.query["nname"], request.query["desc"])
            if request.query["method"] == "delete":
                return vmware.deleteSnapShot(path, request.query["nname"])
            if request.query["method"] == "revert":
                return vmware.revertSnapShot(path, request.query["nname"])
            return "err"

        run(host='localhost', port=port)
