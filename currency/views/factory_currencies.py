import json
import os

from currency.models.currency_models import Currency
from currency.serializers.currency_serializers import RootCurrencySerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response


class FactoryCurrency(ListCreateAPIView):
    permission_classes = []
    
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = RootCurrencySerializer
    
    def create(self, *args, **kwargs):
        try:
            # Construct the absolute file path
            file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "currencies.json"
            )
            with open(file_path, encoding="utf8") as file:
                contents = json.load(file)
        except FileNotFoundError:
            return Response({"success": False, "message": "File not found."}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({"success": False, "message": "Error decoding JSON file."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        success_index = 0
        for index, content in enumerate(contents.items()):
            if not Currency.objects.filter(code=content[0]).exists():
                serializer = self.get_serializer(data=content[1])
                serializer.is_valid(raise_exception=True)
                serializer.save(create_uid=self.request.user.id)
                success_index = index + 1

        msg = (
            f"Factory {success_index} currencies successfully."
            if success_index > 0
            else "Factory currencies are already inserted into the currencies table."
        )
        return Response({"success": True, "message": msg}, status=status.HTTP_200_OK)
