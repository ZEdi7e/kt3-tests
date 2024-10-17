import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        # set headers, authorisation etc

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, data=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True

        # log part
        pprint.pprint(f'{request_type} example')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        pprint.pprint(response.text)
        pprint.pprint(response.json())
        pprint.pprint('**********')
        return response

    def get(self, endpoint, endpoint_id, expected_error=False):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json()

    def post(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body)
        return response.json()['message']

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json()['message']


BASE_URL_PETSTORE = 'https://petstore.swagger.io/'
base_request = BaseRequest(BASE_URL_PETSTORE)

new_user_data = {
    "id": 1,
    "username": "danMark",
    "firstName": "Dan",
    "lastName": "Mark",
    "email": "dan@example.com",
    "password": "password",
    "phone": "1234567890",
    "userStatus": 1
}
created_user = base_request.post('user', '', new_user_data)
pprint.pprint(created_user)

user_info = base_request.get('user', 'danMark')
pprint.pprint(user_info)

assert user_info['username'] == new_user_data['username']

updated_user_data = {
    "id": 1,
    "username": "danMark_updated",
    "firstName": "Dan",
    "lastName": "Mark Updated",
    "email": "dan_updated@example.com",
    "password": "newpassword",
    "phone": "9876543210",
    "userStatus": 1
}
updated_user = base_request.post('user', 'danMark', updated_user_data)
pprint.pprint(updated_user)

user_info = base_request.get('user', 'danMark_updated')
assert user_info['username'] == updated_user_data['username']

deleted_user = base_request.delete('user', 'danMark_updated')
pprint.pprint(deleted_user)

user_info_after_delete = base_request.get('user', 'danMark_updated', expected_error=True)
assert 'User not found' in user_info_after_delete['message']

new_order_data = {
    "id": 1,
    "petId": 1,
    "quantity": 1,
    "shipDate": "2024-10-14T18:30:00.000Z",
    "status": "placed",
    "complete": True
}
created_order = base_request.post('store/order', '', new_order_data)
pprint.pprint(created_order)

order_info = base_request.get('store/order', 1)
pprint.pprint(order_info)

assert order_info['status'] == 'placed'

deleted_order = base_request.delete('store/order', 1)
pprint.pprint(deleted_order)

order_info_after_delete = base_request.get('store/order', 1, expected_error=True)
assert 'Order not found' in order_info_after_delete['message']

inventory_info = base_request.get('store', 'inventory')
pprint.pprint(inventory_info)