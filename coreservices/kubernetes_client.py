from kubernetes import config, client

class KubernetesClient:

    kube_config = None
    core_v1_api_client = None
    app_v1_api_client = None

    def __init__(self):
        self.config_loader()

    @staticmethod
    def get_core_v1_api_client():
        if KubernetesClient.core_v1_api_client is None:
            KubernetesClient.core_v1_api_client = client.CoreV1Api()
        return KubernetesClient.core_v1_api_client

    @staticmethod
    def get_app_v1_api_client():
        if KubernetesClient.app_v1_api_client is None:
            KubernetesClient.app_v1_api_client = client.ApiClient()
        return KubernetesClient.app_v1_api_client

    @staticmethod
    def config_loader():
        if KubernetesClient.kube_config is None:
            KubernetesClient.kube_config = client.Configuration()
            KubernetesClient.kube_config.host = "192.168.64.2"
            KubernetesClient.kube_config.cert_file = "/Users/karavichandran/.minikube/profiles/minikube/client.crt"
            KubernetesClient.kube_config.key_file = "/Users/karavichandran/.minikube/profiles/minikube/client.key"
            config.load_kube_config()

kubernetes_api_client = KubernetesClient()