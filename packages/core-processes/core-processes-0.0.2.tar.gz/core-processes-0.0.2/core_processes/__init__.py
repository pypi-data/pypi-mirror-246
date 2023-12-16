from process_bigraph import process_registry
from core_processes.cobra_process import CobraProcess
from core_processes.copasi_process import CopasiProcess
from core_processes.smoldyn_process import SmoldynProcess
from core_processes.tellurium_process import TelluriumProcess, TelluriumStep


# register processes
process_registry.register('cobra', CobraProcess)
process_registry.register('copasi', CopasiProcess)
process_registry.register('smoldyn_process', SmoldynProcess)
process_registry.register('tellurium_step', TelluriumStep)
process_registry.register('tellurium_process', TelluriumProcess)
