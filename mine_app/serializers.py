from rest_framework import serializers


class NewTrxsSerializer(serializers.Serializer):
    sender = serializers.CharField(required=True)
    recipient = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)

    class Meta:
        fields = '__all__'


class NodesSerializer(serializers.Serializer):
    nodes = serializers.ListField(child=serializers.CharField(required=True))

    class Meta:
        fields = '__all__'
