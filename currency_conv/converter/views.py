"""
Views for the converter API
"""
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
from rest_framework import status


class CurrencyConverterView(APIView):
    """View for currency conversion using Xe.com"""
    def get(self, request):
        """Convert one currency to another"""
        from_currency = request.query_params.get('from')
        to_currency = request.query_params.get('to')
        value = float(request.query_params.get('value', 1))

        try:
            url = f'https://www.xe.com/currencyconverter/convert/?Amount={value}&From={from_currency}&To={to_currency}'

            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                result_element = soup.find('p', class_='result__BigRate-sc-1bsijpp-1')

                if result_element:
                    result_text = result_element.get_text()
                    number = result_text.split(' ')[0]
                    result_number = round(float(number), 2)

                    result = {
                        "result": result_number
                    }

                    return Response(result)
                else:
                    return Response({"error": "Error when parsing the conversion result"}, status=400)
            else:
                return Response({"error": "Error when requesting to Xe.com"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

