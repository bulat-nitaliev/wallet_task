from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from wallet.models import Wallet, User
from wallet.serializers import WalletSerializer, OperationSerializer, UserCreateSerializer
import threading
import logging

logger = logging.getLogger(__name__)


class UserVievSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]
    serializer_class = UserCreateSerializer


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Wallet.objects.all()
    lookup_field = 'uuid'

    serializer_class = WalletSerializer
    # permission_classes = [permissions.IsAuthenticated,]

    @action(detail=True, methods=['post'], url_path='operation')
    def perform_operation(self, request, uuid=None):
        try:
            wallet = self.get_object()  
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            operation_type = serializer.validated_data['operation_type']
            amount = serializer.validated_data['amount']
            
            lock = threading.Lock()
            with lock:
                logger.info(f"{threading.current_thread().getName()} acquired the lock")
                
                if operation_type == 'DEPOSIT':
                    wallet.balance += amount
                elif operation_type == 'WITHDRAW' and wallet.balance >= amount:
                    wallet.balance -= amount
                else:
                    return Response({"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
                
                wallet.save(update_fields=['balance'])  
                logger.info(f"{threading.current_thread().getName()} released the lock")
            
            return Response(WalletSerializer(wallet).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
