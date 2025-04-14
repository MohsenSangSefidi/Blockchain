from django.urls import path
from .views import (FullChainView, NewTrxsView, MineView, RegisterNodeView, ConsensusView)

urlpatterns = [
    path('full-chain', FullChainView.as_view(), name='full-chain'),
    path('new-trxs', NewTrxsView.as_view(), name='new-trxs'),
    path('mine-block', MineView.as_view(), name='mine-block'),
    path('register-nodes', RegisterNodeView.as_view(), name='register-nodes'),
    path('consensus', ConsensusView.as_view(), name='consensus'),
]
