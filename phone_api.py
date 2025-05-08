import requests
import os


def get_phone_info(phone_number: str) -> dict:
    """Получение информации о номере через API"""
    API_KEY = os.getenv("f9e65f4c205178b518833e5c76f0e7c3")
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={phone_number}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'valid': data.get('valid', False),
            'number': data.get('international_format'),
            'country': data.get('country_name'),
            'operator': data.get('carrier'),
            'type': data.get('line_type')
        }
    except Exception as e:
        return {'error': f"API Error: {str(e)}"}