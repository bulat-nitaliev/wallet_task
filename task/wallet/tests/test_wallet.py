from rest_framework.test import APITestCase
from wallet.factories import UserFactory, WalletFactory
from rest_framework import status
from wallet.models import User, Wallet
from decimal import Decimal

class WalletTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = '/api/v1/wallets/'

    def test_retrieve_wallet(self):
        wallet = WalletFactory.create(user=self.user)

        data = {
            'user': wallet.user.pk, 
            'uuid': wallet.uuid, 
            'balance': round(wallet.balance,1)
         }

        response = self.client.get(self.url + f'{wallet.uuid}/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_not_wallet(self):
        uuid =  '3a687f77-defc-42c2-ab08-2ba85720504b'

        response = self.client.get(self.url + f'{uuid}/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
       

    def test_invalid_operation(self):
        wallet = WalletFactory.create(user=self.user)

        data = {
            'deposit': 'DEPOSIT' ,
            'amount': 1000
        }
        response = self.client.post(self.url + f'{wallet.uuid}/operation/', data=data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_error_valid_operation(self):
        wallet = WalletFactory.create(user=self.user)
        data = {
            'operation_type': 'DEPOSITDEPOSIT' ,
            'amount': 1000
        }
        response = self.client.post(self.url + f'{wallet.uuid}/operation/', data=data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        withdraw_data = {
            'operation_type': 'WITHDRAW' ,
            'amount': wallet.balance + 1
        }
        error_message = {"error": "Insufficient funds"}

        response_withdraw = self.client.post(self.url + f'{wallet.uuid}/operation/', data=withdraw_data, format='json')
        
        self.assertEqual(response_withdraw.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_withdraw.json(), error_message)


    def test_operation_deposit(self):
        wallet = WalletFactory.create(user=self.user)

        data = {
            'operation_type': 'DEPOSIT' ,
            'amount': 1000
        }

        response_data = {
            'user': wallet.user.pk, 
            'uuid': wallet.uuid, 
            'balance': round(wallet.balance,1) + data['amount']
         }

        response = self.client.post(self.url + f'{wallet.uuid}/operation/', data=data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), response_data)


    def test_operation_withdraw(self):
        wallet = WalletFactory.create(user=self.user)

        data = {
            'operation_type': 'WITHDRAW' ,
            'amount': wallet.balance
        }

        response_data = {
            'user': wallet.user.pk, 
            'uuid': wallet.uuid, 
            'balance': 0
         }

        response = self.client.post(self.url + f'{wallet.uuid}/operation/', data=data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), response_data)

    def test_retrieve_wallet_unauthorized(self):
        self.client.logout()
        wallet = WalletFactory.create(user=self.user)

        response = self.client.get(self.url + f'{wallet.uuid}/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wallet_operation_unauthorized(self):
        wallet = WalletFactory.create(user=self.user)
        self.client.logout()

        response = self.client.get(self.url + f'{wallet.uuid}/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

