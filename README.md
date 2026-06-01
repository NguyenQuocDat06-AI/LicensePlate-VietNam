# 🚗 LicensePlate-VietNam

> Hệ thống nhận diện và đọc biển số xe Việt Nam sử dụng YOLOv5 và OpenCV.

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
  - [Chạy Server (HTTP API)](#chạy-server-http-api)
  - [Test trực tiếp với ảnh](#test-trực-tiếp-với-ảnh)
  - [Gọi API bằng cURL](#gọi-api-bằng-curl)
- [API Reference](#-api-reference)
- [Pipeline xử lý](#-pipeline-xử-lý)
- [Mô hình YOLO](#-mô-hình-yolo)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)

---

## 📖 Giới thiệu

**LicensePlate-VietNam** là một hệ thống hoàn chỉnh để **phát hiện** và **nhận diện ký tự** trên biển số xe Việt Nam. Hệ thống hỗ trợ cả biển số **1 dòng** và **2 dòng** (phổ biến ở xe máy), sử dụng 2 mô hình YOLOv5 chuyên biệt kết hợp với các kỹ thuật xử lý ảnh bằng OpenCV.

### ✨ Tính năng chính

- 🔍 **Phát hiện biển số** — Xác định vị trí biển số trong ảnh bằng YOLOv5
- 🔤 **Nhận diện ký tự (OCR)** — Đọc từng ký tự trên biển số bằng mô hình YOLO riêng
- 📐 **Chỉnh nghiêng tự động** — Deskew & perspective transform để chuẩn hóa góc chụp
- 🌐 **HTTP API** — Cung cấp REST API đơn giản để tích hợp vào các hệ thống khác
- 🏍️ **Hỗ trợ biển số 2 dòng** — Xử lý cả biển số xe ô tô (1 dòng) và xe máy (2 dòng)

---

## 🏗 Kiến trúc hệ thống

```
Ảnh đầu vào
    │
    ▼
┌──────────────────────┐
│  YOLOv5 LP Detector  │  ← Phát hiện vùng chứa biển số
│  (LP_detector.pt)    │
└──────────┬───────────┘
           │  Crop vùng biển số
           ▼
┌──────────────────────┐
│  Deskew & Normalize  │  ← Chỉnh nghiêng + Perspective Transform
│  (OpenCV)            │
└──────────┬───────────┘
           │  Ảnh biển số đã chuẩn hóa
           ▼
┌──────────────────────┐
│  YOLOv5 LP OCR       │  ← Nhận diện từng ký tự
│  (LP_ocr.pt)         │
└──────────┬───────────┘
           │  Sắp xếp ký tự theo vị trí
           ▼
┌──────────────────────┐
│  Ghép chuỗi biển số  │  ← Phân loại 1 dòng / 2 dòng
└──────────────────────┘
           │
           ▼
    Kết quả: "29A1-12345"
```

---

## 📂 Cấu trúc dự án

```
LicensePlate-VietNam/
├── Makefile                    # Makefile gốc (proxy sang core/)
├── README.md
├── package-lock.json
└── core/                       # Mã nguồn chính
    ├── Makefile                # Build & run commands
    ├── __init__.py             # Metadata (tên, phiên bản)
    ├── __main__.py             # Entry point — khởi chạy HTTP server
    ├── server.py               # HTTP server xử lý API requests
    ├── test.py                 # Script test nhận diện từ file ảnh
    ├── requirements.txt        # Python dependencies
    └── LicensePlate/           # Module nhận diện chính
        ├── __init__.py         # Pipeline: detect → normalize → OCR
        ├── yolo.py             # Load 2 mô hình YOLOv5
        ├── model/              # Trọng số mô hình (pretrained)
        │   ├── LP_detector.pt      # YOLOv5 — phát hiện biển số (~40MB)
        │   ├── LP_detector_nano_61.pt  # Phiên bản nano (~3.6MB)
        │   ├── LP_ocr.pt              # YOLOv5 — OCR ký tự (~40MB)
        │   └── LP_ocr_nano_62.pt       # Phiên bản nano (~3.8MB)
        ├── function/           # Các hàm tiện ích
        │   ├── helper.py           # Đọc & ghép ký tự biển số
        │   └── utils_rotate.py     # Chỉnh nghiêng (deskew), đổi contrast
        └── yolov5/             # YOLOv5 (git submodule)
```

---

## 💻 Yêu cầu hệ thống

| Thành phần | Yêu cầu                  |
| ---------- | ------------------------ |
| Python     | >= 3.8                   |
| Git        | Có hỗ trợ submodule      |
| RAM        | >= 4GB (khuyến nghị 8GB) |
| GPU        | Tùy chọn (hỗ trợ CUDA)  |

### Thư viện chính

- **PyTorch** & **Torchvision** — Deep learning framework
- **OpenCV** (`opencv-python`) — Xử lý ảnh
- **Ultralytics** — YOLOv5 framework
- **Pillow** — Đọc/ghi ảnh
- **NumPy** — Tính toán ma trận

---

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone --recursive https://github.com/NguyenQuocDat06-AI/LicensePlate-VietNam.git
cd LicensePlate-VietNam
```

> **Lưu ý:** Cờ `--recursive` là bắt buộc để tải submodule `yolov5`.

### 2. Khởi tạo môi trường

```bash
make init
```

Lệnh này sẽ tự động:
1. Cập nhật git submodule (YOLOv5)
2. Tạo Python virtual environment (`venv`)
3. Cài đặt tất cả dependencies từ `requirements.txt`
4. Cài đặt dependencies của YOLOv5

### Cài đặt thủ công (nếu cần)

```bash
cd core
git submodule update --init --recursive
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r ./LicensePlate/yolov5/requirements.txt
```

---

## 🔧 Sử dụng

### Chạy Server (HTTP API)

```bash
make run
```

Server sẽ khởi động tại `http://0.0.0.0:9049`.

### Test trực tiếp với ảnh

```bash
make test
```

Hoặc chạy thủ công với ảnh tùy chọn:

```bash
cd core
source venv/bin/activate
python test.py -i /đường/dẫn/tới/ảnh.jpg
```

### Gọi API bằng cURL

```bash
# Gửi ảnh để nhận diện biển số
curl -X POST -F "file=@/đường/dẫn/tới/ảnh.jpg" http://localhost:9049
```

---

## 📡 API Reference

### `POST /`

Nhận diện biển số xe từ ảnh.

**Request:**

| Tham số   | Kiểu            | Bắt buộc | Mô tả                         |
| --------- | ---------------- | -------- | ------------------------------ |
| `file`    | `multipart/file` | ✅       | File ảnh chứa biển số xe       |

**Response thành công** (`200 OK`):

```json
{
  "status": "success",
  "results": [
    {
      "x": 120,
      "y": 80,
      "w": 200,
      "h": 60,
      "text": "29A1-12345"
    }
  ]
}
```

| Trường     | Mô tả                                        |
| ---------- | --------------------------------------------- |
| `x`, `y`   | Tọa độ góc trên-trái của vùng biển số (px)   |
| `w`, `h`   | Chiều rộng và chiều cao vùng biển số (px)     |
| `text`     | Chuỗi ký tự biển số đã nhận diện             |

**Response lỗi** (`400 / 500`):

```json
{
  "status": "failed",
  "message": "Mô tả lỗi"
}
```

---

## ⚙ Pipeline xử lý

Pipeline nhận diện biển số gồm các bước sau:

### 1. Phát hiện biển số (License Plate Detection)

- Sử dụng **YOLOv5** với trọng số `LP_detector.pt`
- Input: ảnh gốc (kích thước 640px)
- Output: danh sách bounding box `[xmin, ymin, xmax, ymax]`

### 2. Chỉnh nghiêng (Deskew)

- Áp dụng **CLAHE** để tăng contrast (tùy chọn)
- Phát hiện đường thẳng bằng **Hough Transform**
- Tính góc nghiêng và xoay ảnh để chuẩn hóa

### 3. Chuẩn hóa biển số (Normalize Plate)

- Tách kênh màu **R, G, B** và nhị phân hóa (Otsu threshold)
- Tìm **tứ giác** bao quanh biển số từ contours
- Chấm điểm tứ giác dựa trên tỉ lệ `w/h` (1.0 – 7.0)
- Thực hiện **4-Point Perspective Transform** để trải phẳng biển số
- Tỉ lệ mặc định: `190/140` (chuẩn biển xe máy Việt Nam)

### 4. Nhận diện ký tự (OCR)

- Sử dụng **YOLOv5** với trọng số `LP_ocr.pt` (confidence ≥ 0.60)
- Phát hiện từng ký tự riêng lẻ trên biển số
- Phân loại biển số **1 dòng** hoặc **2 dòng** dựa trên vị trí y trung bình

### 5. Ghép chuỗi kết quả

- **Biển 1 dòng**: sắp xếp ký tự theo tọa độ x từ trái sang phải
- **Biển 2 dòng**: tách thành 2 hàng → sắp xếp từng hàng → nối bằng dấu `-`
- Kết quả dạng: `29A1-12345`

---

## 🧠 Mô hình YOLO

Dự án sử dụng 2 mô hình YOLOv5 đã được huấn luyện:

| Mô hình                  | Mục đích              | Kích thước  | Ghi chú            |
| ------------------------- | --------------------- | ----------- | ------------------- |
| `LP_detector.pt`          | Phát hiện biển số     | ~40 MB      | Mô hình chính      |
| `LP_detector_nano_61.pt`  | Phát hiện biển số     | ~3.6 MB     | Phiên bản nhẹ       |
| `LP_ocr.pt`               | Nhận diện ký tự (OCR) | ~40 MB      | Mô hình chính      |
| `LP_ocr_nano_62.pt`       | Nhận diện ký tự (OCR) | ~3.8 MB     | Phiên bản nhẹ       |

> 💡 Phiên bản **nano** phù hợp cho thiết bị edge / nhúng với tài nguyên hạn chế.

---

## 🛠 Công nghệ sử dụng

| Công nghệ         | Vai trò                                       |
| ------------------ | --------------------------------------------- |
| **YOLOv5**         | Object detection & character recognition      |
| **PyTorch**        | Deep learning framework                       |
| **OpenCV**         | Xử lý ảnh, perspective transform, deskew      |
| **Pillow**         | Đọc ảnh từ buffer (bytes → numpy)             |
| **Python `http.server`** | HTTP server tích hợp sẵn (không cần framework) |

---

## 📄 License

Dự án này được phát triển cho mục đích nghiên cứu và học tập.

---

<p align="center">
  Được phát triển bởi <a href="https://github.com/NguyenQuocDat06-AI">NguyenQuocDat06-AI</a>
</p>