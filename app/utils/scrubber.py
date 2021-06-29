import os
import yaml
import json
import crayons
import logging
import shutil
from builtins import FileExistsError


logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(" IngressGatewayCreator ")


class IngressGatewayCreator:

    @staticmethod
    def clone_default_ingress(clone_context):
        # Clone the deployment
        IngressGatewayCreator.clone_deployment_object(clone_context)

        # Clone the deployment's HPA
        IngressGatewayCreator.clone_hpa_object(clone_context)

    @staticmethod
    def clone_deployment_object(deployment, namespace, deployment_name):
        # Clone the object deployment as a dic
        cloned_dict = IngressGatewayCreator.clone_k8s_object(deployment)
        # Save the deployment template in the output dir
        return IngressGatewayCreator.save_clone_as_yaml(cloned_dict, namespace, deployment_name)

    @staticmethod
    def clone_k8s_object(k8s_object):
        # Manipilate in the dict level, not k8s api, but from the fetched raw object
        # https://github.com/kubernetes-client/python/issues/574#issuecomment-405400414
        cloned_obj = json.loads(k8s_object.data)

        cloned_obj['status'] = None

        # Scrub by removing the "null" and "None" values
        cloned_obj = IngressGatewayCreator.scrub_dict(cloned_obj)

        # Patch the metadata with the name and labels adjusted

        return cloned_obj

    # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-strings-from-a-dict/59959570#59959570
    @staticmethod
    def scrub_dict(d):
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = IngressGatewayCreator.scrub_dict(v)
            if isinstance(v, list):
                v = IngressGatewayCreator.scrub_list(v)
            if not v in (u'', None, {}):
                new_dict[k] = v
        return new_dict

    # https://stackoverflow.com/questions/12118695/efficient-way-to-remove-keys-with-empty-strings-from-a-dict/59959570#59959570
    @staticmethod
    def scrub_list(d):
        scrubbed_list = []
        for i in d:
            if isinstance(i, dict):
                i = IngressGatewayCreator.scrub_dict(i)
            scrubbed_list.append(i)
        return scrubbed_list

    @staticmethod
    def get_yaml_for_dep(ns, dep):
        with open('/Users/sujeffrish/yaml/' + ns+'/'+ dep + '-deployment.yaml') as f:
            data = yaml.safe_load(f)
        return data

    @staticmethod
    def save_clone_as_yaml(k8s_object, namespace, deployment_name):
        try:
            os.makedirs("/Users/sujeffrish/yaml/" + namespace)
        except FileExistsError:
            LOGGER.debug("Dir already exists %s", "/Users/sujeffrish/yaml")

        full_file_path = os.path.join("/Users/sujeffrish/yaml/" + namespace, deployment_name + '-' + "deployment" + '.yaml')

        try:
            with open(full_file_path, 'w') as yaml_file:
                yaml.dump(k8s_object, yaml_file, default_flow_style=False)
        except Exception as file_write_exception:
            return file_write_exception
        LOGGER.info(crayons.yellow("Saved %s '%s' at %s: \n%s"), "deployment", deployment_name, full_file_path,
                    k8s_object)
        return full_file_path

    @staticmethod
    def get_from_json():
        with open('/Users/sujeffrish/metadata/latest-backup.json') as f:
            data = json.load(f)
        return data

    @staticmethod
    def save_clone_as_json(k8s_object):
        try:
            # Just try to create if it doesn't exist
            os.makedirs("/Users/sujeffrish/metadata")

        except FileExistsError:
            LOGGER.debug("Dir already exists %s", "/Users/sujeffrish/metadata")

        full_file_path = os.path.join("/Users/sujeffrish/metadata", "latest-backup" + '.json')
        json_object = json.dumps(k8s_object, indent=4)

        # Writing to sample.json
        try:
            with open(full_file_path, "w") as outfile:
                outfile.write(json_object)
        except Exception as json_exception:
            return json_exception
        return True

    @staticmethod
    def delete_directory():
        shutil.rmtree("/Users/sujeffrish/yaml");
        shutil.rmtree("/Users/sujeffrish/metadata");

# try:
#     k8s_clone_name = "http2-ingressgateway"
#     hostname = "my-nlb-awesome.a.company.com"
#     nats = ["123.345.678.11", "333.444.222.111", "33.221.444.23"]
#     manifest_dir = "out/clones"
#
#     context = IngressGatewayContext(manifest_dir, k8s_clone_name, hostname, nats, "nlb")
#
#     IngressGatewayCreator.clone_default_ingress(context)
#
# except Exception as err:
#   print("ERROR: {}".format(err))
