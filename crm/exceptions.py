from rest_framework.exceptions import APIException


class FilterNotExist(APIException):
    status_code = 400
    default_detail = "Le(s) filtre(s) n'existe(nt) pas"
    default_code = "filter_not_exist"
