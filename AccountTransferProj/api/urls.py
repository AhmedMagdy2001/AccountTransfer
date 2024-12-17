from django.urls import path
from .views import AccountList,ImportAccounts,AccountByName,TransferFunds

urlpatterns = [
    path('accounts/', AccountList.as_view(), name='accounts-list'),
    path('account/', AccountByName.as_view(), name='account'),\
    path('transfer-funds/', TransferFunds.as_view(), name='transfer-funds'),
    path('upload-csv/', ImportAccounts.as_view(), name='upload_csv'),
]