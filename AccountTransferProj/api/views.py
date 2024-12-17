from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer
from decimal import Decimal
import csv
import uuid
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage


"get and delete accounts"
class AccountList(APIView):
    def get(self, request):
        # Fetch all accounts from the database
        accounts = Account.objects.all()

        # Serialize the account data
        serializer = AccountSerializer(accounts, many=True)

        # Return the serialized data as a response
        return Response(serializer.data)

    def delete(self, request):
        try:
            # Delete all accounts from the database
            Account.objects.all().delete()
            return Response({"message": "All accounts have been deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

"Get Account By Name"
class AccountByName(APIView):
    
    def get(self, request):
        # Get the name from query parameters
        name = request.query_params.get('name', None)

        if not name:
            return Response({"error": "Name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Search for the account using the 'Name' field
            account = Account.objects.get(Name=name)
        except Account.DoesNotExist:
            return Response({"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the account data
        serializer = AccountSerializer(account)
        return Response(serializer.data)


"add accounts from a csv file"
class ImportAccounts(APIView):
    parser_classes = [MultiPartParser, FormParser]  # To handle file uploads

    def post(self, request, *args, **kwargs):
        # Get the file from the request
        file = request.FILES.get('file')  # Assuming the file field in the request is named 'file'

        if not file:
            return Response({"error": "No file provided"}, status=400)

        # Save the file temporarily
        file_path = default_storage.save(f'temp/{file.name}', file)
        full_file_path = default_storage.path(file_path)

        try:
            self.import_accounts_from_csv(full_file_path)
            return Response({"message": "File imported successfully"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def import_accounts_from_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                account_id = row['ID']

                # Validate if the ID is a valid UUID
                if not self.is_valid_uuid(account_id):
                    raise ValueError(f"Skipping invalid UUID: {account_id}")
                    continue

                # Create Account objects using the data from the CSV file
                Account.objects.create(
                    ID=account_id,
                    Name=row['Name'],
                    Balance=row['Balance']
                )

    def is_valid_uuid(self, id_string):
        try:
            uuid.UUID(id_string)
            return True
        except ValueError:
            return False        

"Transfer Funds between accounts"
class TransferFunds(APIView):
    def post(self, request):
        # Get the sender and receiver account IDs and the amount to transfer from the request data
        sender_name = request.data.get('sender_name')
        receiver_name = request.data.get('receiver_name')
        amount = request.data.get('amount')

        if not sender_name or not receiver_name or not amount:
            return Response({"error": "Sender, receiver, and amount are required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender_account = Account.objects.get(Name=sender_name)
            receiver_account = Account.objects.get(Name=receiver_name)
        except Account.DoesNotExist:
            return Response({"error": "Sender or receiver account not found"}, status=status.HTTP_404_NOT_FOUND)

        if sender_account.Balance < Decimal(amount):
            return Response({"error": "Insufficient funds in sender's account"}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the transfer
        sender_account.Balance -= Decimal(amount)
        receiver_account.Balance += Decimal(amount)

        # Save the updated accounts
        sender_account.save()
        receiver_account.save()

        # Optionally, you can return the updated account details
        sender_serializer = AccountSerializer(sender_account)
        receiver_serializer = AccountSerializer(receiver_account)

        return Response({
            "message": "Transfer successful",
            
        })            