from coreservices.kubernetes_client import kubernetes_api_client
from coreservices.service_utils import get_age
from dataobject.k8smanifest import KubernetesResourceObject
from kubernetes.client.rest import ApiException
import logging

logger = logging.getLogger(__name__)

core_v1_api_client = kubernetes_api_client.get_core_v1_api_client()
app_v1_api_client = kubernetes_api_client.get_app_v1_api_client()


def get_all_namespaces():
    ns_list = []
    ns_object_list = core_v1_api_client.list_namespace()
    for ns in ns_object_list.items:
        ns_list.append(KubernetesResourceObject(name=ns.metadata.name,
                                                age=get_age(ns.metadata.creation_timestamp)).__dict__)
    return ns_list


def get_namespace_by_name(ns_name):
    try:
        ns_object = core_v1_api_client.read_namespace(ns_name)
        return KubernetesResourceObject(name=ns_object.metadata.name,
                                        age=get_age(ns_object.metadata.creation_timestamp)).__dict__
    except ApiException as e:
        logger.info(msg=e.body)
        return e.body
