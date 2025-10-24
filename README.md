# MetaTrader5 - Trader Nelayan

Bot trading otomatis untuk MetaTrader5 yang membuat grid (jaring) order pending. Strategi "Nelayan" ini menempatkan multiple pending orders pada interval harga tertentu untuk menangkap pergerakan pasar.

## Persyaratan

- Python 3.11 atau lebih tinggi
- MetaTrader5 terminal terinstall di sistem
- Akun trading MetaTrader5 (demo atau real)
- Windows OS (MetaTrader5 API hanya mendukung Windows)

## Instalasi

### Menggunakan uv (Recommended)

1. Install uv jika belum terinstall:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone repository:
```bash
git clone https://github.com/fdjrr/mt5-trader-nelayan
cd mt5-trader-nelayan
```

3. Install dependencies:
```bash
uv sync
```

4. Jalankan aplikasi:
```bash
uv run main.py
```

### Menggunakan pip

1. Clone repository:
```bash
git clone https://github.com/fdjrr/mt5-trader-nelayan
cd mt5-trader-nelayan
```

2. Buat virtual environment (opsional tapi direkomendasikan):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:
```bash
python main.py
```

## Konfigurasi

Pastikan MetaTrader5 terminal sudah berjalan dan login ke akun trading sebelum menjalankan bot.

## Cara Penggunaan

1. Jalankan program:
```bash
python main.py
```

2. Masukkan konfigurasi yang diminta:
   - **Symbol**: Pasangan mata uang (contoh: EURUSD, GBPUSD)
   - **Order Type**: Tipe order (BUY atau SELL)
   - **Lot Size**: Ukuran lot untuk setiap order (contoh: 0.01)
   - **Point**: Jarak antar order dalam point
   - **Start Price**: Harga awal untuk grid
   - **End Price**: Harga akhir untuk grid

### Contoh Konfigurasi

```json
{
    "symbol": "XAUUSDc",
    "order_type": "BUY",
    "lot_size": 0.01,
    "point": 10,
    "start_price": 4100.0,
    "end_price": 4000.0,
    "magic": 234000,
    "deviation": 20
}
```

Bot akan membuat grid pending orders dari start price ke end price dengan interval sesuai point yang ditentukan.

## Fitur

- Otomatis menempatkan pending orders dalam bentuk grid
- Mendukung order BUY dan SELL
- Menggunakan BUY/SELL LIMIT dan STOP orders sesuai harga pasar
- Magic number untuk identifikasi order

## Peringatan

- Selalu test di akun demo terlebih dahulu
- Trading memiliki risiko, pastikan memahami strategi sebelum menggunakan di akun real
- Pastikan memiliki manajemen risiko yang baik
