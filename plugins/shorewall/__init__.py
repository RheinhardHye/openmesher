import logging, interfaces, os
from StringIO import StringIO
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, ChoiceLoader


class Shorewall(interfaces.IOpenMesherConfigPlugin):
    def __init__(self):
        env = Environment(loader=ChoiceLoader([
                FileSystemLoader('~/.openmesher/'),
                FileSystemLoader('%s/plugins/' %(os.getcwd())),
            ]))
        self._files = {}
        self._interfaces_template = env.get_template('shorewall/interfaces.conf')
        self._rules_template = env.get_template('shorewall/rules.conf')
    
    def process(self, mesh, cliargs=None):
        logging.debug('Generating Shorewall config...')
        self._files = {}
        for router in mesh.links:
            self._files[router] = {}
            interfaces = StringIO()
            rules = StringIO()
            
            self._files[router]['/shorewall/interfaces.mesh'] = self._interfaces_template.render(links = mesh.links[router], zone='vpn')
            self._files[router]['/shorewall/rules.mesh'] = self._rules_template.render(links= mesh.links[router])
            
        return True
    
    def files(self):
        """ Return a dictionary of routers containing a dictionary of filenames and contents """
        return self._files

