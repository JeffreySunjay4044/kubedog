from coreservices.kubernetes_client import kubernetes_api_client
from coreservices.service_utils import get_age
from dataobject.k8smanifest import KubernetesResourceObject
from kubernetes.client.rest import ApiException
import logging

logger = logging.getLogger(__name__)

core_v1_api_client = kubernetes_api_client.get_core_v1_api_client()
app_v1_api_client = kubernetes_api_client.get_app_v1_api_client()


def get_all_daemon_sets():
    ds_list = []
    ds_object_list = app_v1_api_client.list_daemon_set_for_all_namespaces()
    for ds in ds_object_list.items:
        ds_list.append(KubernetesResourceObject(name=ds.metadata.name, age=get_age(ds.metadata.creation_timestamp),
                                                namespace=ds.metadata.namespace).__dict__)
    return ds_list


def get_daemon_sets_from(namespace):
    try:
        ds_list = []
        ds_object_list = app_v1_api_client.list_namespaced_daemon_set(namespace=namespace)
        for ds in ds_object_list.items:
            ds_list.append(
                KubernetesResourceObject(name=ds.metadata.name, age=get_age(ds.metadata.creation_timestamp),
                                         namespace=ds.metadata.namespace).__dict__)
    except ApiException as e:
        logger.info(e.body)
        return e.body
    return ds_list
