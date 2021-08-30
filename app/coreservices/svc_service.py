from coreservices.kubernetes_client import kubernetes_api_client
from utils.service_utils import get_age
from dataobject.k8smanifest import KubernetesResourceObject
from kubernetes.client.rest import ApiException
import logging

logger = logging.getLogger(__name__)

core_v1_api_client = kubernetes_api_client.get_core_v1_api_client()


def get_all_svc():
    svc_list = []
    svc_object_list = core_v1_api_client.list_service_for_all_namespaces()
    for svc in svc_object_list.items:
        svc_list.append(KubernetesResourceObject(name=svc.metadata.name, namespace=svc.metadata.namespace,
                                                 age=get_age(svc.metadata.creation_timestamp)))
    return svc_list


def get_all_svc_from(namespace):
    svc_list = []
    svc_object_list = core_v1_api_client.list_namespaced_service(namespace=namespace)
    for svc in svc_object_list.items:
        svc_list.append(KubernetesResourceObject(name=svc.metadata.name, namespace=svc.metadata.namespace,
                                                 age=get_age(svc.metadata.creation_timestamp)))
    return svc_list
