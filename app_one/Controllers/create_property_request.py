from odoo import http
from odoo.http import request
import json


class CreatePropertyRequest(http.Controller):
    @http.route('/v1/properties', type='http', auth='public',methods=['POST'],csrf=False)

    def create_property_request(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        res=request.env['property'].sudo().create(vals)
        print(res)


    @http.route('/v1/properties/<int:property_id>', type='http', auth='public',methods=['PUT'],csrf=False)
    def create_property_request(self,property_id):
        try:
           property_id=request.env['property'].sudo().search([('id','=',property_id)])
           if not property_id:
            return request.make_json_response({"message":"Property does not exist"},status=404)

           args = request.httprequest.data.decode()
           vals = json.loads(args)
           property_id.write(vals)
           print(property_id.post_code)
           return request.make_json_response({"message": "Property updated successfully"},status=200)
        except Exception as error:
            return request.make_json_response({"message":str(error)},status=500)













