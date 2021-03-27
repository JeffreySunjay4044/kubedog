class Deployment:
    def __init__(deployment, name, namespace):
        deployment.name = name
        deployment.namespace = namespace

class Service:
    def __init__(service, name, namespace, deployment):
        service.name = name
        service.namespace = namespace
        service.deployment = deployment

class Ingress:
    pass

class DepTree:
    def __init__(self, service, deploymenr, ingress):
        self.service = Service
        self.deploymenr = Deployment
        self.ingress = Ingress

class Namespace:
  def __init__(self, name, data):
    self.name = name
    self.depTrees = data

class Pod:
  def __init__(self, pod_data):
    self.name = pod_data.metadata.name
    self.status = pod_data.status.phase
    self.pod_ip = pod_data.status.pod_ip
    self.host_ip = pod_data.status.host_ip
      
    

