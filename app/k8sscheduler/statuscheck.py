import logging,time
from kubernetes import client
from utils.scrubber import IngressGatewayCreator
logging.basicConfig(level=logging.INFO)

k8s_core_api = None

class StatusCheck:

    @staticmethod
    def get_k8scoreapi():
        if k8s_core_api is None:
            return client.CoreV1Api()
        return k8s_core_api

    @staticmethod
    def get_pods(dep, ns):
        k8s_client= StatusCheck.get_k8scoreapi()
        return k8s_client.list_namespaced_pod("orc")

    @staticmethod
    def status_check_pod(dep, ns):
        k8s_client= StatusCheck.get_k8scoreapi()
        k8s_client.read_namespaced_pod_status(dep, ns)

    @staticmethod
    def check_pod_status(ns, dep):
        client.AppsV1Api().read_namespaced_deployment_status(dep, ns)

    @staticmethod
    def status_check(loaded_json):
        timeout=180
        status_check_json = {}
        api=client.AppsV1Api()
        for ns in loaded_json.keys():
            if status_check_json.get(ns) is None:
                status_check_json[ns] = {}
            ns_dep = loaded_json.get(ns)
            for dep in ns_dep.keys():
                if status_check_json.get(ns).get(dep) is None:
                    status_check_json[ns][dep] = {}
                start = time.time()
                while time.time() - start < timeout:
                    time.sleep(30)
                    response = api.read_namespaced_deployment_status(dep, ns)
                    s = response.status
                    if (s.updated_replicas == response.spec.replicas and
                            s.replicas == response.spec.replicas and
                            s.available_replicas == response.spec.replicas and
                            s.observed_generation >= response.metadata.generation):
                            status_check_json[ns][dep] = "success"
                            return True
                    else:
                        print('[updated_replicas:{s.updated_replicas},replicas:{s.replicas}'
                              ',available_replicas:{s.available_replicas},observed_generation:{s.observed_generation}] waiting...')
                status_check_json[ns][dep] = "timeout"
                raise RuntimeError('Waiting timeout for deployment {dep}')    
        return status_check_json

        # pods = StatusCheck.get_pods(dep, ns)
        # k8s_client.read_namespaced_pod_status()