import logging

from kubernetes import client, config
from dataobject.k8smanifest import Deployment, DepTree
# from awss3 import S3
from utils.scrubber import IngressGatewayCreator

logging.basicConfig(level=logging.INFO)

# s3Obj = S3()
backed_up_obj ={}
loaded_obj = {}
k8s_client = None

class BackupDelete:

    @staticmethod
    def read_deployment_as_yaml(namespace, deployment_name):
        body = BackupDelete.get_deployments(BackupDelete.get_k8s_client(k8s_client), namespace=namespace, deployment_name=deployment_name, alNsFlag=False)
        return IngressGatewayCreator.clone_deployment_object(body, namespace, deployment_name)

    @staticmethod
    def get_k8s_client(k8s_client):
        if k8s_client is None:
            k8s_client = client.AppsV1Api()
            return k8s_client
        return k8s_client

    @staticmethod
    def delete_deployment(namespace, deployment):
        return BackupDelete.get_k8s_client(k8s_client).delete_namespaced_deployment(deployment, namespace)

    @staticmethod
    def delete_deployment_all(backed_up_obj):
        for ns in backed_up_obj.keys():
            delete_dep_ns = backed_up_obj.get(ns)
            for dep in delete_dep_ns.keys():
                BackupDelete.delete_deployment(ns, dep)
        return backed_up_obj

    @staticmethod
    def get_dep_map():
        return BackupDelete.get_tree_from_deployment(
            BackupDelete.get_deployments(BackupDelete.get_k8s_client(k8s_client), namespace="", deployment_name="", alNsFlag=True))

    @staticmethod
    def backup_existing_dep(map_ns_dep_tree, ns_dep, for_all_ns):
        for_all_dep = False
        if for_all_ns:
            for_all_dep = True
            ns_bucket_use = map_ns_dep_tree.keys()
        else:
            ns_bucket_use = ns_dep.keys()
        for ns in ns_bucket_use:
            map_dep_tree = map_ns_dep_tree.get(ns)
            ns_dep_use = map_dep_tree.keys() if for_all_dep else ns_dep.get(ns) if ns_dep.get(
                ns) is not None else map_dep_tree.keys()
            for dep in ns_dep_use:
                filePath = BackupDelete.read_deployment_as_yaml(ns, dep)
                if isinstance(filePath, str):
                    backed_up_obj[ns] = {} if backed_up_obj.get(ns) is None else backed_up_obj.get(ns)
                    backed_up_obj[ns][dep] = filePath
        #successfully saved in file

    @staticmethod
    def backup_and_delete(ns_dep, for_all_ns):
        map_ns_dep_tree = BackupDelete.get_dep_map()
        BackupDelete.backup_existing_dep(map_ns_dep_tree, ns_dep, for_all_ns)
        IngressGatewayCreator.save_clone_as_json(backed_up_obj)
        return BackupDelete.delete_deployment_all(backed_up_obj)

    @staticmethod
    def get_tree_from_deployment(result):
        nsWiseItems = {}
        for deployment in result.items:
            ns = deployment.metadata.namespace
            if nsWiseItems.get(ns) is None:
                nsWiseItems[ns] = {}
            deploymentName = deployment.metadata.name
            if nsWiseItems.get(ns).get(deploymentName) is None:
                nsWiseItems[ns][deploymentName] = {}
            k8sdepObj = Deployment(deploymentName, ns)
            nsWiseItems[ns][deploymentName] = DepTree(None, k8sdepObj, None)
        return nsWiseItems

    @staticmethod
    def get_deployments(k8sApiObject, namespace, deployment_name, alNsFlag):
        if (alNsFlag):
            return k8sApiObject.list_deployment_for_all_namespaces()
        return k8sApiObject.read_namespaced_deployment(deployment_name, namespace, _preload_content=False)

    @staticmethod
    def get_namespaces(k8sApiObject):
        return k8sApiObject.list_namespace()

    # @staticmethod
    # def save_to_s3(name, dep_body):
    #     s3Obj.__init__()