import logging
from kubernetes import client
from dataobject.k8smanifest import Pod
import json
logging.basicConfig(level=logging.INFO)

k8s_client = None


class Readk8s:

    @staticmethod
    def get_k8s_client(k8s_client):
        if k8s_client is None:
            # configuration = client.Configuration()
            # configuration.host = "localhost:8888"
            k8s_client = client.CoreV1Api()
            return k8s_client
        return k8s_client

    @staticmethod
    def read_log_file(ns):
        pod_list = Readk8s.get_k8s_client(k8s_client).list_namespaced_pod('orc-int')
        pod_array = {}
        for pod in pod_list.items:
            pod_object = Pod(pod)
            pod_array[pod_object.name] = json.dumps(pod_object)
        print(json.dumps(pod_array))
        return json.dumps(pod_array)
