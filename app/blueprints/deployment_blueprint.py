from flask import Blueprint
from flask.wrappers import Response

from coreservices.deployment_service import get_all_deployments, get_deployments_from
from utils.service_utils import get_json_list

deploy_bp = Blueprint('deployment_blueprint',__name__)


@deploy_bp.route('/get/deployments', methods=['GET'])
def get_deployments_from_all_ns():
    """
    This API fetches list of deployments from all-namespaces in the cluster
    :return HTTP Response with list of deployments:
    """
    dep_list = get_all_deployments()
    return Response(response=get_json_list(dep_list), status=200, mimetype='application/json')


@deploy_bp.route('/get/deployments/<namespace>', methods=['GET'])
def get_deployments_from_ns(namespace):
    """
    This API fetches list of deployments from all-namespaces in the cluster
    :param namespace: Name of the namespace
    :return HTTP Response with list of deployments:
    """
    dep_list = get_deployments_from(namespace)
    return Response(response=get_json_list(dep_list), status=200, mimetype='application/json')

