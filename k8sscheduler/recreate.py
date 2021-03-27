import logging
from kubernetes import client
from utils.scrubber import IngressGatewayCreator
from k8sscheduler.statuscheck import StatusCheck
logging.basicConfig(level=logging.INFO)

k8s_client = None


class RecreateFiles:

    @staticmethod
    def get_k8s_client(k8s_client):
        if k8s_client is None:
            k8s_client = client.AppsV1Api()
            return k8s_client
        return k8s_client

    @staticmethod
    def load_from_file(ns, dep):
        return IngressGatewayCreator.get_yaml_for_dep(ns, dep)

    @staticmethod
    def recreate_from_backup():
        loaded_json = IngressGatewayCreator.get_from_json()
        for ns in loaded_json.keys():
            ns_dep = loaded_json.get(ns)
            for dep in ns_dep.keys():
                dep_body = RecreateFiles.load_from_file(ns, dep)
                # making the resourceversion to empty string
                dep_body.get('metadata')['resourceVersion'] = ''
                RecreateFiles.get_k8s_client(k8s_client).create_namespaced_deployment(ns, dep_body)
        return StatusCheck.status_check(loaded_json)

    @staticmethod
    def clear_backedup_files():
        IngressGatewayCreator.delete_directory()
