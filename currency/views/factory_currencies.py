import json

from currency.models.currency_models import Currency
from currency.serializers.currency_serializers import RootCurrencySerializer
from rest_framework import generics, status
from rest_framework.response import Response


class FactoryCurrency(generics.CreateAPIView):
    permission_classes = []
    
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = RootCurrencySerializer

    def create(self, *args, **kwargs):
        file = open("currency/assets/factory/currencies.json", encoding="utf8")
        contents = json.load(file)
        success_index = 0
        for index, content in enumerate(contents.items()):
            if not Currency.objects.filter(code=content[0]).exists():
                serializer = self.get_serializer(data=content[1])
                serializer.is_valid(raise_exception=True)
                serializer.save(create_uid=self.request.user.id)
                success_index = index + 1
            else:
                continue
        msg = (
            f"Factory {success_index} currencies successfully."
            if success_index > 0
            else "Factory currencies are already inserted into the currencies table."
        )
        message = {"success": True, "message": msg}
        return Response(message, status=status.HTTP_201_CREATED)
