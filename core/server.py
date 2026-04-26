from LicensePlate import recognizeLicensePlateBuffer
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import json
import traceback
import numpy as np

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("Hello, World!", "utf-8"))

    @staticmethod
    def to_python(obj):
        if isinstance(obj, dict):
            return {k: RequestHandler.to_python(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [RequestHandler.to_python(x) for x in obj]       
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_, bool)):                       
            return bool(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        if isinstance(obj, (bytes, bytearray)):
            try:
                return obj.decode("utf-8")
            except Exception:
                return obj.hex()
        return obj

    def do_POST(self):
        try:
            ctype, pdict = cgi.parse_header(self.headers.get('Content-Type', ''))
            if ctype != 'multipart/form-data':
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status":"failed","message":"Cần multipart/form-data với field 'file'"}).encode("utf-8"))
                return

            content_len = int(self.headers.get('Content-Length', 0))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = content_len
            fields = cgi.parse_multipart(self.rfile, pdict)

            if 'file' not in fields:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"status":"failed","message":"Thiếu field 'file'"}).encode("utf-8"))
                return

            file_bytes = fields['file'][0]

            # ---- THAM SỐ TÙY CHỌN (tự mặc định nếu không gửi kèm) ----
            def _get(name, default=None):
                if name not in fields: return default
                return fields[name][0].decode('utf-8')

            def _get_bool(name, default=False):
                v = _get(name, None)
                if v is None: return default
                return v.strip().lower() in ('1','true','yes','on')

            def _get_float(name, default):
                v = _get(name, None)
                if v is None: return default
                try: return float(v)
                except: return default

            boxes = None
            boxes_json = _get('boxes', None)
            if boxes_json:
                try:
                    boxes = json.loads(boxes_json)
                except Exception:
                    boxes = None

            keep_hyphen = _get_bool('keep_hyphen', False)
            draw        = _get_bool('draw', True)
            detect_conf = _get_float('detect_conf', 0.3)

            # ---- GỌI PIPELINE: truyền bytes trực tiếp ----
            results = recognizeLicensePlateBuffer(file_bytes)

            # ---- Ảnh kết quả dạng base64 (optional) ----
            resp = {
                "status": "success",
                "results": results,
            }
            resp = RequestHandler.to_python(resp)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode("utf-8"))

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status":"failed",
                "message": str(e),
                "trace": traceback.format_exc()
            }, ensure_ascii=False).encode("utf-8"))

def start(host: str, port: int):
    httpd = HTTPServer((host, port), RequestHandler)
    print(f"RequestHandler starts at http://{host}:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
