import json

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status

from .serializers import (NewTrxsSerializer, NodesSerializer)

from blockchain import instance, node_id


class MineView(APIView):
    def get(self, request, *args, **kwargs):
        last_block = instance.last_block
        proof = instance.proof_of_work(last_block['proof'])
        previous_hash = instance.hash(last_block)

        instance.new_transactions(sender="0", recipient=node_id, amount=50)

        block = instance.new_block(proof, previous_hash)

        response = {
            'massage': 'New Block Forged',
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }

        return JsonResponse(response, status=status.HTTP_200_OK)


# Add New Transaction
class NewTrxsView(APIView):
    def post(self, request, *args, **kwargs):
        # Validating Data
        serializer = NewTrxsSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Store Information
        sender = serializer.validated_data['sender']
        recipient = serializer.validated_data['recipient']
        amount = serializer.validated_data['amount']

        # Mine Block
        block = instance.new_transactions(sender, recipient, amount)

        # Create Response
        response = {
            'massage': f'Will be added to block {block}'
        }

        return JsonResponse(response, safe=False)


# Return The Full Chain
class FullChainView(APIView):
    def get(self, request, *args, **kwargs):
        # Store Information To Response
        res = {
            'chain': instance.chain,
            'length': len(instance.chain),
        }

        return JsonResponse(res, status=status.HTTP_200_OK)


# Register Node
class RegisterNodeView(APIView):
    def post(self, request, *args, **kwargs):
        # Validating Data
        serializer = NodesSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Store Node Address
        nodes = list(serializer.validated_data['nodes'])

        # Add Nodes
        for node in nodes:
            instance.register_node(node)

        # Set Response
        response = {
            'massage': 'nodes add',
            'nodes': list(instance.nodes)
        }

        return JsonResponse(response, status=status.HTTP_201_CREATED)


# Resolve Conflicts
class ConsensusView(APIView):
    def get(self, request, *args, **kwargs):
        # Replace The Chain
        replace = instance.resolve_conflicts()

        # Check Response
        if replace:
            response = {
                'massage': 'Consensus replaced',
                'new_chain': instance.chain
            }
        else:
            response = {
                'massage': 'Consensus not replaced',
            }

        return JsonResponse(response, status=status.HTTP_200_OK)
