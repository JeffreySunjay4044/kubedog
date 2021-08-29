from flask import Blueprint
from flask.wrappers import Response

from coreservices.namespace_service import get_all_namespaces, get_namespace_by_name
from dataobject.k8smanifest import KubernetesResourceObject
from utils.service_utils import get_json_list, get_json

namespace_bp = Blueprint('namespace_blueprint',__name__)

@namespace_bp.route('/get/namespaces', methods=['GET'])
def get_namespaces():
    """
    This API fetches the list of all namespaces in the cluster along with its age
    :return HTTP Response with list of all-namespaces in the cluster:
    """
    ns_list = get_all_namespaces()
    ns_list_json = get_json_list(ns_list)
    return Response(response=ns_list_json, status=200, mimetype='application/json')


@namespace_bp.route('/get/namespace/<name>', methods=['GET'])
def get_namespace(name):
    """
    This API fetches the namespace with given name along with its age. If the namespace does not exist, response with
    message: 'namespace not found' and status: '404' is returned
    :param name: Name of the namespace
    :return HTTP Response with details of given namespace:
    """
    ns_object = get_namespace_by_name(name)
    response_body = None
    if isinstance(ns_object, KubernetesResourceObject):
        status_code = 200
        response_body = get_json(ns_object)
    else:
        response_body = "There is no namespace in the given name"
        status_code = 404
    return Response(response=response_body, status=status_code, mimetype='application/json')