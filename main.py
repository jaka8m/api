from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from helpers.proxy_checker import process_proxy

from jinja2 import Environment, FileSystemLoader

app = FastAPI()

env = Environment(loader=FileSystemLoader("templates"))

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    template = env.get_template("index.html")
    return template.render()

@app.get("/checker", response_class=HTMLResponse) # Tambahkan endpoint ini
async def random_ip_page(request: Request):
    template = env.get_template("checker.html")
    return template.render()

@app.get("/check")
async def check_proxy_url_endpoint(
    request: Request,
    ip: str = Query(..., description="Alamat IP proxy dengan format IP:PORT")
):
    if ":" not in ip:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Parameter 'ip' harus dalam format IP:PORT."
            },
        )

    ip_address, port_str = ip.split(":", 1)

    try:
        port_number = int(port_str)
        status_str, message, country_code, asn, country_name, country_flag, http_protocol, org_name, connection_time, latitude, longitude, colo = process_proxy(ip_address, port_number)

        if status_str == "Active":
            response_data = {
                "ip": ip_address,
                "port": port_number,
                "status": "ACTIVE",
                "isp": org_name,
                "countryCode": country_code,
                "country": f"{country_name} {country_flag}",
                "asn": asn,
                "colo": colo,
                "httpProtocol": http_protocol,
                "delay": f"{round(connection_time)} ms",
                "latitude": latitude,
                "longitude": longitude,
                "colo": colo,
            }
        else:
            response_data = {
                "ip": ip_address,
                "port": port_number,
                "status": "DEAD",
                "asn": asn,
            }

        return response_data

    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Port harus berupa angka."})
    except Exception as e:
        error_message = f"Terjadi kesalahan server saat memproses proxy {ip}: {e}"
        print(error_message)
        return JSONResponse(status_code=500, content={"error": error_message})
