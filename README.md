## Ochonetes

### Overview

You need to setup & run quick a bunch of [**Kafka**](http://kafka.apache.org/) brokers ? You are afraid of setting the
underlying [**Zookeeper**](https://zookeeper.apache.org/) ensemble ? You love
[**Kubernetes**](https://github.com/GoogleCloudPlatform/kubernetes) ?

Good news, you can easily leverage [**Ochonetes**](https://github.com/autodesk-cloud/ochonetes) and get everything
running in no time !

### How does it work ?

We propose two simple containers that will do all the magic for you. You can look at the code in the ```images/```
folder. We basically have a [**Zookeeper**](https://zookeeper.apache.org/) container that will self-cluster into an
ensemble and a [**Kafka**](http://kafka.apache.org/) container which relies on that ensemble.

How do they know about each other ? Go look at [**Ochopod**](https://github.com/autodesk-cloud/ochopod) for details
about that magical process. What you want is to deploy these two guys in the same clustering _scope_ and they will
find each other. I said it was easy right ?

If you are curious try deploying less than 3 [**Zookeeper**](https://zookeeper.apache.org/) containers. The
[**Kafka**](http://kafka.apache.org/) containers will then boot but refuse to configure until this condition is met.

Please note I included a fairly simple [**Kafka**](http://kafka.apache.org/) container which will use a local
```/var/lib/kafka``` to store its logs. Feel free to mount something or even allocate a volume on the fly.

### Do it !

#### Step 1 : install K8S on AWS with the portal running

Easy, look at the **README** in [**Ochonetes**](https://github.com/autodesk-cloud/ochonetes) if you are wondering what
I am talking about.

#### Step 2 : deploy your two tiers

Let us CURL a bit. If have a specific broker configuration in mind first edit ```kafka.yml``` and specify your
own settings.

You want 4 brokers ? No problemo, do the following:

```
$ curl -X POST -H "X-Shell:deploy zk -p 3 -n test" -F "zk=@zookeeper.yml" http://<PROXY NODE IP>:9000/shell
$ curl -X POST -H "X-Shell:deploy kafka -p 4 -n test" -F "kafka=@kafka.yml" http://<PROXY NODE IP>:9000/shell
```

Wait a bit, peek into the web-console and you should see your brokers. For instance:

```
> grep test.kafka
<test.kafka> -> 100% replies (4 pods total) ->
cluster        |  pod IP       |  process  |  state
               |               |           |
test.kafka #1  |  10.244.2.8   |  running  |  leader
test.kafka #2  |  10.244.2.9   |  running  |  follower
test.kafka #3  |  10.244.2.10  |  running  |  follower
test.kafka #4  |  10.244.1.8   |  running  |  follower
```

#### Step 3 : enjoy

Your brokers are now functional. Note their IP and use them from any other pod on port TCP 9092. When you are tired
playing with them you can tear the whole thing down in one shot :

```
$ curl -X POST -H "X-Shell:kill test.kafka test.zookeeper" http://<PROXY NODE IP>:9000/shell
```

### Support

Contact autodesk.cloud.opensource@autodesk.com for more information about this project.

### License

© 2015 Autodesk Inc.
All rights reserved

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.