from coreservices.kubernetes_client import kubernetes_api_client
from coreservices.service_utils import get_age
from dataobject.k8smanifest import KubernetesResourceObject
from kubernetes.client.rest import ApiException
import logging

logger = logging.getLogger(__name__)

core_v1_api_client = kubernetes_api_client.get_core_v1_api_client()
app_v1_api_client = kubernetes_api_client.get_app_v1_api_client()


def get_all_deployments():
    dep_list = []
    dep_object_list = app_v1_api_client.list_deployment_for_all_namespaces()
    for dep in dep_object_list.items:
        dep_list.append(KubernetesResourceObject(name=dep.metadata.name, age=get_age(dep.metadata.creation_timestamp),
                                                 namespace=dep.metadata.namespace).__dict__)
    return dep_list


def get_deployments_from(namespace):
    try:
        dep_list = []
        dep_object_list = app_v1_api_client.list_namespaced_deployment(namespace=namespace)
        for dep in dep_object_list.items:
            dep_list.append(
                KubernetesResourceObject(name=dep.metadata.name, age=get_age(dep.metadata.creation_timestamp),
                                         namespace=dep.metadata.namespace).__dict__)
    except ApiException as e:
        logger.info(e.body)
        return e.body
    return dep_list
