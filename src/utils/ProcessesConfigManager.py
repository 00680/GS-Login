from config.ConfigLoader import Config

class ProcessesConfigManager:
    @staticmethod
    def getProcesses():
        return Config.get('processes', {})

    @staticmethod
    def getProcessById(processId):
        procs = ProcessesConfigManager.getProcesses()
        return procs.get(processId)

    @staticmethod
    def addOrUpdateProcess(processData):
        procs = ProcessesConfigManager.getProcesses()
        path = processData.get('path')
        if not path:
            raise ValueError("Process data must contain a 'path' field.")
        procs[path] = processData
        Config.cfg['processes'] = procs
        Config.save()

    @staticmethod
    def deleteProcess(processId):
        procs = ProcessesConfigManager.getProcesses()
        if processId in procs:
            del procs[processId]
            Config.cfg['processes'] = procs
            Config.save()
