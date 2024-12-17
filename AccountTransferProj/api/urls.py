from django.urls import path
from .views import AccountList,ImportAccounts,AccountByName,TransferFunds,dashboard,menu

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/', AccountList.as_view(), name='accounts-list'),
    path('account/', AccountByName.as_view(), name='account'),\
    path('transfer-funds/', TransferFunds.as_view(), name='transfer-funds'),
    path('import-accounts/', ImportAccounts.as_view(), name='import-accounts'),
]