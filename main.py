from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/cek_kuota', methods=['GET'])
def cek_kuota():
    msisdn = request.args.get('msisdn')
    if not msisdn:
        return jsonify({'status': 'error', 'message': 'Parameter "msisdn" is required'}), 400

    api_url = f"https://apigw.kmsp-store.com/sidompul/v4/cek_kuota?msisdn={msisdn}&isJSON=true"
    headers = {
        'Authorization': 'Basic c2lkb21wdWxhcGk6YXBpZ3drbXNw',
        'X-API-Key': '60ef29aa-a648-4668-90ae-20951ef90c55',
        'X-App-Version': '4.0.0',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return jsonify({'status': 'success', 'msisdn': msisdn, 'data': data}), 200

    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, 'status_code', 500)
        error_details = getattr(e.response, 'text', str(e))
        return jsonify({
            'status': 'error',
            'message': f"Failed to fetch data from XL API. Status: {status_code}",
            'details': error_details
        }), status_code
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Internal server error while checking XL package.',
            'details': str(e)
        }), 500

# supaya Vercel bisa kenali app Flask
app = app
