#
# Copyright (c) 2015 Autodesk Inc.
# All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import logging
import os

from jinja2 import Environment, FileSystemLoader
from ochopod.bindings.ec2.kubernetes import Pod
from ochopod.core.fsm import diagnostic
from ochopod.core.utils import merge, retry, shell
from ochopod.models.piped import Actor as Piped
from ochopod.models.reactive import Actor as Reactive
from os.path import join, dirname

logger = logging.getLogger('ochopod')


if __name__ == '__main__':

    #
    # - load our pod configuration settings
    # - this little json payload is packaged by the deployment tool
    # - is it passed down to the container as the $pod environment variable
    #
    cfg = json.loads(os.environ['pod'])

    class Model(Reactive):

        damper = 15.0

        sequential = True

        depends_on = ['zookeeper']

    class Strategy(Piped):

        cwd = '/opt/kafka_2.9.2-0.8.2.1'

        strict = True

        def can_configure(self, cluster):

            #
            # - we want a 3+ zk ensemble in our namespace
            # - if the assert blows up the pod will attempt to re-configure later on
            #
            assert len(cluster.dependencies['zookeeper']) >= 3, '3+ zookeeper ensemble required'

        def configure(self, cluster):

            #
            # - look our broker index up
            # - this index is required in the configuration
            #
            pod = cluster.pods[cluster.key]
            assert '9092' in pod['ports'], 'kafka container not exposing 9092 ?'

            #
            # - render the server.properties file
            # - the bulk of the broker settings come from our pod configuration
            # - it is hardcoded to use our mounted /var/lib/kafka directory for the log files
            #
            env = Environment(loader=FileSystemLoader(join(dirname(__file__), 'templates')))
            template = env.get_template('server.properties')
            index = cluster.seq + 1
            mapping = \
                {
                    'id':       index,
                    'host':     pod['ip'],
                    'port':     9092,
                    'settings': cfg['broker'],
                    'zk':       cluster.grep('zookeeper', 2181)
                }

            logger.debug('starting broker #%d' % index)

            with open('%s/config/server.properties' % self.cwd, 'wb') as f:
                f.write(template.render(mapping))

            return 'bin/kafka-server-start.sh config/server.properties', {}


    Pod().boot(Strategy, model=Model)