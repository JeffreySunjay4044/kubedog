from flask import Blueprint
from flask.wrappers import Response

from coreservices.ingress_service import get_all_ingress, get_all_ingress_from
from utils.service_utils import get_json_list

ingress_bp = Blueprint('ingress_blueprint',__name__)

@ingress_bp.route('/get/ingress', methods=['GET'])
def get_ing_from_all_ns():
    """
    This API fetches list of all ingress from all-namespaces in the cluster
    :return HTTP Response with list of services:
    """
    ing_list = get_all_ingress()
    ing_list_json = get_json_list(ing_list)
    return Response(response=ing_list_json, status=200, mimetype='application/json')


@ingress_bp.route('/get/ingress/<namespace>', methods=['GET'])
def get_ing_from_ns(namespace):
    """
    This API fetches list of all ingress from given namespaces in the cluster
    :return HTTP Response with list of services:
    """
    ing_list = get_all_ingress_from(namespace)
    ing_list_json = get_json_list(ing_list)
    return Response(response=ing_list_json, status=200, mimetype='application/json')