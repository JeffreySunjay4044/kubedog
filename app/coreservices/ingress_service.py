from coreservices.kubernetes_client import kubernetes_api_client
from coreservices.service_utils import get_age
from dataobject.k8smanifest import KubernetesResourceObject
from kubernetes.client.rest import ApiException
import logging

logger = logging.getLogger(__name__)

extensions_v1_beta1_api_client = kubernetes_api_client.get_extensions_v1_beta1_api_client()


def get_all_ingress():
    ing_list = []
    ing_object_list = extensions_v1_beta1_api_client.list_ingress_for_all_namespaces()
    for ing in ing_object_list.items:
        ing_list.append(KubernetesResourceObject(name=ing.metadata.name, namespace=ing.metadata.namespace,
                                                 age=get_age(ing.metadata.creation_timestamp)).__dict__)
    return ing_list


def get_all_ingress_from(namespace):
    ing_list = []
    ing_object_list = extensions_v1_beta1_api_client.list_namespaced_ingress(namespace=namespace)
    for ing in ing_object_list.items:
        ing_list.append(KubernetesResourceObject(name=ing.metadata.name, namespace=ing.metadata.namespace,
                                                 age=get_age(ing.metadata.creation_timestamp)).__dict__)
    return ing_list
