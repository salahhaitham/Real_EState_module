import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request
import json




def handle_valid_response(data,status,pagination_info):

    responsebody={"message":"successful","data":data}
    if pagination_info:
        responsebody["pagination_info"]=pagination_info
    return request.make_json_response(responsebody,status=status)

def handle_Invalid_response(error,status):

    responsebody={"error":error}

    return request.make_json_response(responsebody,status=status)






class CreatePropertyRequest(http.Controller):

    @http.route('/v1/properties', type='http', auth='public',methods=['POST'],csrf=False)

    def create_property_request(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        try:
             res=request.env['property'].sudo().create(vals)
             return request.make_json_response(
                 {"message": "Property created successfully",
                        "id":res.id,
                         "name":res.name



                         }, status=200)


        except Exception as error:
            return request.make_json_response({str(error)}, status=404)


    @http.route('/v1/properties/<int:property_id>', type='http', auth='public',methods=['PUT'],csrf=False)
    def update_property_request(self,property_id):
        try:
           property_id=request.env['property'].sudo().search([('id','=',property_id)])
           if not property_id:
            return handle_Invalid_response("Property does not exist",status=404)

           args = request.httprequest.data.decode()
           vals = json.loads(args)
           property_id.write(vals)
           print(property_id.post_code)
           return request.make_json_response({"message": "Property updated successfully"},status=200)
        except Exception as error:
            return request.make_json_response({"message":str(error)},status=500)

    @http.route('/v1/properties/<int:property_id>', type='http', auth='public',methods=['GET'],csrf=False)
    def get_property_request(self,property_id):
        try:
           property_id=request.env['property'].sudo().search([('id','=',property_id)])
           if not property_id:
            return request.make_json_response({"message":"Property does not exist"},status=404)


           return request.make_json_response(
               {"message": "Property updated successfully",
                "id":property_id.id,
                "name": property_id.name,
                "post_code": property_id.post_code,
                "ref": property_id.ref,



                },
               status=200)

        except Exception as error:
            return request.make_json_response({"message":str(error)},status=500)


    @http.route('/v1/properties', type='http', auth='public',methods=['GET'],csrf=False)
    def get_All_property_request(self):
            try:
                params=parse_qs(request.httprequest.query_string.decode())
                search_domain=[]
                page=offset=None
                limit=3


                if params.get('page'):
                   page=int(params.get('page')[0])

                if params.get('limit'):
                    limit=int(params.get('limit')[0])

                if page:
                 offset=(page*limit)-limit

                if params.get('state'):
                   search_domain+=[('state','=',params['state'][0])]
                property_ids = request.env['property'].sudo().search(search_domain,offset=offset,order='id desc',limit=limit)
                property_count= request.env['property'].sudo().search_count(search_domain)
                print(property_ids)
                print(property_count)
                if not property_ids:
                    return request.make_json_response({"message": "Property does not exist"}, status=404)

                return handle_valid_response([
                    {

                     "id": property_id.id,
                     "name": property_id.name,
                     "post_code": property_id.post_code,
                     "ref": property_id.ref,

                     }for property_id in property_ids],pagination_info={
                               "page":page if page else 1,
                               "limit": limit ,
                               "pages": math.ceil(property_count/limit) if limit else 1,
                               "count":property_count

                             },
                               status=200)

            except Exception as error:
                return request.make_json_response({"message": str(error)}, status=500)













