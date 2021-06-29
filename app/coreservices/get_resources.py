from coreservices.kubernetes_client import kubernetes_api_client

core_v1_api_client = kubernetes_api_client.get_core_v1_api_client()
app_v1_api_client = kubernetes_api_client.get_app_v1_api_client()

def get_all_namespaces():
    ns_list = []
    ns_object_list = core_v1_api_client.list_namespace()
    for ns in ns_object_list.items:
        ns_list.append(ns.metadata.name)
    return ns_list

