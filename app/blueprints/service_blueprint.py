from flask import Blueprint
from flask.wrappers import Response

from coreservices.svc_service import get_all_svc, get_all_svc_from
from utils.service_utils import get_json_list


service_bp =  Blueprint('service_blueprint',__name__)

@service_bp.route('/get/services', methods=['GET'])
def get_svc_from_all_ns():
    """
    This API fetches list of all services from all-namespaces in the cluster
    :return HTTP Response with list of services:
    """
    svc_list = get_all_svc()
    svc_list_json = get_json_list(svc_list)
    return Response(response=svc_list_json, status=200, mimetype='application/json')


@service_bp.route('/get/services/<namespace>', methods=['GET'])
def get_all_svc_from_ns(namespace):
    """
    This API fetches list of services from given namespace in the cluster
    :param namespace:
    :return HTTP Response with list of services:
    """
    svc_list = get_all_svc_from(namespace)
    svc_list_json = get_json_list(svc_list)
    return Response(response=svc_list_json, status=200, mimetype='application/json')