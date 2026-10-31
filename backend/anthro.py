"""
WARISAN.AI - Clinical Antropometric Calculation Module
Standar Antropometri Anak Kemenkes RI No. 2 Tahun 2020 & WHO Child Growth Standards.

Fitur:
- Perhitungan z-score deterministik untuk BB/U, TB/U (PB/U), dan BB/TB (BB/PB).
- Pembedaan baku antara Panjang Badan (PB / Recumbent Length untuk usia < 24 bulan)
  dan Tinggi Badan (TB / Standing Height untuk usia >= 24 bulan) beserta konversi koreksi 0.7 cm.
- Deteksi tren pertumbuhan kunjungan berturut-turut (penurunan BB > 10% & BB stagnan 2 siklus).
- Validasi rentang biologis WHO dan sanitasi data balita.
"""

import math
import html
import re
from typing import Dict, Any, Optional, Tuple, List

# ==============================================================================
# TABEL REFERENSI WHO CHILD GROWTH STANDARDS (0 - 60 BULAN)
# Format: [Median, -3SD, -2SD, -1SD, +1SD, +2SD, +3SD]
# ==============================================================================

# Berat Badan menurut Umur (BB/U) - Laki-laki (kg)
BBU_L = {
    0:  [3.3, 2.1, 2.5, 2.9, 3.9, 4.4, 5.0],
    1:  [4.5, 2.9, 3.4, 3.9, 5.1, 5.8, 6.6],
    2:  [5.6, 3.8, 4.3, 4.9, 6.3, 7.1, 8.0],
    3:  [6.4, 4.4, 5.0, 5.7, 7.2, 8.0, 9.0],
    4:  [7.0, 4.9, 5.6, 6.2, 7.8, 8.7, 9.7],
    5:  [7.5, 5.3, 6.0, 6.7, 8.4, 9.3, 10.4],
    6:  [7.9, 5.7, 6.4, 7.1, 8.8, 9.8, 10.9],
    7:  [8.3, 5.9, 6.7, 7.4, 9.2, 10.3, 11.4],
    8:  [8.6, 6.2, 7.0, 7.7, 9.6, 10.7, 11.9],
    9:  [8.9, 6.4, 7.2, 8.0, 9.9, 11.0, 12.3],
    10: [9.2, 6.6, 7.5, 8.2, 10.2, 11.4, 12.7],
    11: [9.4, 6.8, 7.7, 8.4, 10.5, 11.7, 13.0],
    12: [9.6, 6.9, 7.8, 8.6, 10.8, 12.0, 13.3],
    13: [9.9, 7.1, 8.0, 8.8, 11.0, 12.3, 13.7],
    14: [10.1, 7.2, 8.2, 9.0, 11.3, 12.6, 14.0],
    15: [10.3, 7.4, 8.4, 9.2, 11.5, 12.8, 14.3],
    16: [10.5, 7.5, 8.5, 9.4, 11.7, 13.1, 14.6],
    17: [10.7, 7.7, 8.7, 9.6, 11.9, 13.3, 14.8],
    18: [10.9, 7.8, 8.8, 9.8, 12.1, 13.5, 15.1],
    19: [11.1, 7.9, 9.0, 9.9, 12.3, 13.7, 15.3],
    20: [11.3, 8.1, 9.1, 10.1, 12.5, 14.0, 15.6],
    21: [11.5, 8.2, 9.3, 10.3, 12.7, 14.2, 15.8],
    22: [11.8, 8.4, 9.5, 10.5, 13.0, 14.5, 16.2],
    23: [12.0, 8.6, 9.7, 10.7, 13.2, 14.8, 16.5],
    24: [12.2, 8.6, 9.7, 10.8, 13.6, 15.3, 17.1],
    25: [12.4, 8.8, 9.9, 11.0, 13.9, 15.5, 17.4],
    26: [12.5, 8.9, 10.0, 11.1, 14.0, 15.7, 17.6],
    27: [12.7, 9.0, 10.2, 11.3, 14.2, 15.9, 17.8],
    28: [12.9, 9.2, 10.4, 11.5, 14.4, 16.2, 18.1],
    29: [13.1, 9.3, 10.5, 11.7, 14.7, 16.4, 18.4],
    30: [13.3, 9.4, 10.7, 11.8, 14.9, 16.7, 18.7],
    31: [13.5, 9.6, 10.8, 12.0, 15.1, 16.9, 19.0],
    32: [13.7, 9.7, 11.0, 12.2, 15.3, 17.1, 19.2],
    33: [13.8, 9.8, 11.1, 12.3, 15.5, 17.4, 19.5],
    34: [14.0, 9.9, 11.3, 12.5, 15.7, 17.6, 19.7],
    35: [14.2, 10.1, 11.4, 12.7, 15.9, 17.8, 20.0],
    36: [14.3, 10.2, 11.5, 12.8, 16.1, 18.1, 20.3],
    38: [14.7, 10.4, 11.8, 13.1, 16.5, 18.5, 20.8],
    40: [15.1, 10.7, 12.1, 13.4, 16.9, 19.0, 21.4],
    42: [15.5, 10.9, 12.4, 13.8, 17.3, 19.5, 21.9],
    44: [15.8, 11.2, 12.7, 14.1, 17.7, 19.9, 22.4],
    46: [16.2, 11.4, 13.0, 14.4, 18.1, 20.4, 23.0],
    48: [16.6, 11.7, 13.3, 14.7, 18.5, 20.9, 23.5],
    50: [17.0, 11.9, 13.5, 15.0, 19.0, 21.4, 24.1],
    52: [17.4, 12.2, 13.8, 15.4, 19.4, 21.9, 24.7],
    54: [17.8, 12.4, 14.1, 15.7, 19.9, 22.4, 25.3],
    56: [18.2, 12.7, 14.4, 16.0, 20.3, 22.9, 25.9],
    58: [18.6, 12.9, 14.7, 16.4, 20.8, 23.5, 26.5],
    60: [19.1, 13.2, 15.0, 16.8, 21.2, 24.0, 27.1]
}

# Berat Badan menurut Umur (BB/U) - Perempuan (kg)
BBU_P = {
    0:  [3.2, 2.0, 2.4, 2.8, 3.7, 4.2, 4.8],
    1:  [4.2, 2.7, 3.2, 3.6, 4.8, 5.5, 6.2],
    2:  [5.1, 3.4, 3.9, 4.5, 5.8, 6.6, 7.5],
    3:  [5.8, 4.0, 4.5, 5.2, 6.6, 7.5, 8.5],
    4:  [6.4, 4.4, 5.0, 5.7, 7.3, 8.2, 9.3],
    5:  [6.9, 4.8, 5.5, 6.1, 7.8, 8.8, 10.0],
    6:  [7.3, 5.1, 5.7, 6.5, 8.2, 9.3, 10.6],
    7:  [7.6, 5.3, 6.0, 6.8, 8.6, 9.8, 11.1],
    8:  [7.9, 5.6, 6.3, 7.0, 9.0, 10.2, 11.6],
    9:  [8.2, 5.7, 6.5, 7.3, 9.3, 10.6, 12.0],
    10: [8.5, 5.9, 6.7, 7.5, 9.6, 10.9, 12.4],
    11: [8.7, 6.1, 6.9, 7.7, 9.9, 11.2, 12.8],
    12: [8.9, 6.2, 7.0, 7.9, 10.1, 11.5, 13.1],
    13: [9.2, 6.4, 7.2, 8.1, 10.4, 11.8, 13.5],
    14: [9.4, 6.5, 7.4, 8.3, 10.6, 12.1, 13.8],
    15: [9.6, 6.7, 7.6, 8.5, 10.9, 12.4, 14.1],
    16: [9.8, 6.8, 7.7, 8.7, 11.1, 12.6, 14.4],
    17: [10.0, 7.0, 7.9, 8.9, 11.4, 12.9, 14.7],
    18: [10.2, 7.1, 8.1, 9.1, 11.6, 13.2, 15.1],
    19: [10.4, 7.2, 8.2, 9.3, 11.8, 13.5, 15.4],
    20: [10.6, 7.4, 8.4, 9.5, 12.1, 13.7, 15.7],
    21: [10.9, 7.5, 8.6, 9.7, 12.3, 14.0, 16.0],
    22: [11.1, 7.7, 8.7, 9.9, 12.5, 14.3, 16.4],
    23: [11.3, 7.8, 8.9, 10.1, 12.8, 14.6, 16.7],
    24: [11.5, 7.8, 8.9, 10.2, 13.2, 15.1, 17.3],
    25: [11.7, 8.0, 9.1, 10.4, 13.4, 15.4, 17.6],
    26: [11.9, 8.1, 9.3, 10.6, 13.7, 15.7, 17.9],
    27: [12.1, 8.3, 9.4, 10.7, 13.9, 15.9, 18.2],
    28: [12.3, 8.4, 9.6, 10.9, 14.1, 16.2, 18.6],
    29: [12.5, 8.6, 9.8, 11.1, 14.4, 16.4, 18.8],
    30: [12.7, 8.7, 9.9, 11.3, 14.6, 16.7, 19.2],
    31: [12.9, 8.8, 10.1, 11.5, 14.9, 17.0, 19.5],
    32: [13.1, 9.0, 10.3, 11.7, 15.1, 17.3, 19.8],
    33: [13.3, 9.1, 10.4, 11.8, 15.3, 17.5, 20.1],
    34: [13.5, 9.2, 10.6, 12.0, 15.6, 17.8, 20.4],
    35: [13.7, 9.4, 10.7, 12.2, 15.8, 18.1, 20.8],
    36: [13.9, 9.5, 10.9, 12.4, 16.1, 18.4, 21.1],
    38: [14.3, 9.8, 11.2, 12.7, 16.5, 18.9, 21.8],
    40: [14.7, 10.1, 11.5, 13.1, 17.0, 19.4, 22.4],
    42: [15.1, 10.4, 11.8, 13.5, 17.5, 20.0, 23.1],
    44: [15.5, 10.7, 12.2, 13.8, 17.9, 20.5, 23.7],
    46: [15.9, 10.9, 12.5, 14.2, 18.4, 21.1, 24.4],
    48: [16.4, 11.2, 12.8, 14.6, 18.9, 21.7, 25.1],
    50: [16.8, 11.5, 13.2, 15.0, 19.4, 22.3, 25.8],
    52: [17.3, 11.8, 13.5, 15.3, 19.9, 22.9, 26.6],
    54: [17.7, 12.1, 13.9, 15.7, 20.5, 23.6, 27.4],
    56: [18.2, 12.4, 14.2, 16.1, 21.0, 24.2, 28.2],
    58: [18.7, 12.7, 14.6, 16.5, 21.6, 24.9, 29.0],
    60: [19.2, 13.0, 14.9, 16.9, 22.2, 25.6, 29.9]
}

# Panjang/Tinggi menurut Umur (TB/U) - Laki-laki (cm)
# Catatan WHO: 0-23 bln = Panjang Badan (PB terlentang), 24-60 bln = Tinggi Badan (TB berdiri)
TBU_L = {
    0:  [49.9, 44.2, 46.1, 47.9, 51.8, 53.7, 55.6],
    1:  [54.7, 48.9, 50.8, 52.8, 56.7, 58.6, 60.6],
    2:  [58.4, 52.4, 54.4, 56.4, 60.4, 62.4, 64.4],
    3:  [61.4, 55.3, 57.3, 59.4, 63.5, 65.5, 67.6],
    4:  [63.9, 57.6, 59.7, 61.8, 66.0, 68.0, 70.1],
    5:  [65.9, 59.6, 61.7, 63.8, 68.0, 70.1, 72.2],
    6:  [67.6, 61.2, 63.3, 65.5, 69.8, 71.9, 74.0],
    7:  [69.2, 62.7, 64.8, 67.0, 71.3, 73.5, 75.7],
    8:  [70.6, 64.0, 66.2, 68.4, 72.8, 75.0, 77.2],
    9:  [72.0, 65.2, 67.5, 69.7, 74.2, 76.5, 78.7],
    10: [73.3, 66.4, 68.7, 71.0, 75.6, 77.9, 80.1],
    11: [74.5, 67.6, 69.9, 72.2, 76.9, 79.2, 81.5],
    12: [75.7, 68.6, 71.0, 73.4, 78.0, 80.5, 82.9],
    13: [76.9, 69.6, 72.1, 74.5, 79.2, 81.7, 84.2],
    14: [78.0, 70.6, 73.1, 75.6, 80.3, 82.9, 85.4],
    15: [79.1, 71.6, 74.1, 76.6, 81.4, 84.0, 86.6],
    16: [80.2, 72.5, 75.0, 77.6, 82.4, 85.1, 87.8],
    17: [81.2, 73.4, 76.0, 78.6, 83.4, 86.2, 88.9],
    18: [82.3, 74.2, 76.9, 79.6, 84.4, 87.2, 90.0],
    19: [83.2, 75.1, 77.7, 80.5, 85.4, 88.2, 91.1],
    20: [84.2, 75.9, 78.6, 81.4, 86.4, 89.2, 92.1],
    21: [85.1, 76.8, 79.5, 82.3, 87.3, 90.2, 93.2],
    22: [86.0, 77.6, 80.3, 83.1, 88.2, 91.2, 94.2],
    23: [86.9, 78.4, 81.1, 84.0, 89.2, 92.2, 95.2],
    24: [87.8, 78.0, 81.0, 84.1, 91.3, 94.4, 97.5],
    25: [88.8, 78.6, 81.7, 84.9, 92.4, 95.6, 98.8],
    26: [89.8, 79.3, 82.5, 85.7, 93.4, 96.6, 99.9],
    27: [90.9, 79.9, 83.2, 86.5, 94.5, 97.8, 101.1],
    28: [91.9, 80.5, 83.8, 87.2, 95.5, 98.9, 102.3],
    29: [92.9, 81.1, 84.5, 87.9, 96.6, 100.0, 103.5],
    30: [93.9, 81.7, 85.1, 88.6, 97.6, 101.1, 104.6],
    31: [94.8, 82.3, 85.7, 89.3, 98.6, 102.1, 105.8],
    32: [95.8, 82.8, 86.3, 89.9, 99.6, 103.1, 106.9],
    33: [96.7, 83.4, 86.9, 90.5, 100.6, 104.2, 108.0],
    34: [97.7, 83.9, 87.5, 91.1, 101.6, 105.2, 109.1],
    35: [98.6, 84.4, 88.1, 91.7, 102.5, 106.1, 110.2],
    36: [99.5, 85.0, 88.7, 92.4, 103.5, 107.2, 111.3],
    38: [101.2, 86.1, 89.9, 93.6, 105.4, 109.2, 113.4],
    40: [103.0, 87.1, 90.9, 94.8, 107.2, 111.2, 115.5],
    42: [104.6, 88.2, 92.0, 96.0, 109.0, 113.1, 117.5],
    44: [106.2, 89.2, 93.1, 97.1, 110.8, 115.0, 119.5],
    46: [107.8, 90.2, 94.1, 98.2, 112.5, 116.9, 121.5],
    48: [109.4, 91.2, 95.1, 99.3, 114.2, 118.7, 123.4],
    50: [110.9, 92.2, 96.1, 100.3, 115.9, 120.5, 125.3],
    52: [112.4, 93.1, 97.1, 101.3, 117.5, 122.3, 127.1],
    54: [113.9, 94.1, 98.1, 102.3, 119.1, 124.0, 129.0],
    56: [115.4, 95.0, 99.0, 103.3, 120.7, 125.8, 130.8],
    58: [116.8, 95.9, 100.0, 104.2, 122.2, 127.5, 132.6],
    60: [118.3, 96.9, 101.0, 105.2, 123.7, 129.2, 134.5]
}

# Panjang/Tinggi menurut Umur (TB/U) - Perempuan (cm)
TBU_P = {
    0:  [49.1, 43.6, 45.4, 47.3, 51.0, 52.9, 54.7],
    1:  [53.7, 47.8, 49.8, 51.7, 55.6, 57.6, 59.5],
    2:  [57.1, 51.0, 53.0, 55.0, 59.1, 61.1, 63.2],
    3:  [59.8, 53.5, 55.6, 57.7, 61.9, 64.0, 66.1],
    4:  [62.1, 55.6, 57.8, 59.9, 64.3, 66.4, 68.6],
    5:  [64.0, 57.4, 59.6, 61.8, 66.2, 68.5, 70.7],
    6:  [65.7, 58.9, 61.2, 63.5, 68.0, 70.3, 72.5],
    7:  [67.3, 60.3, 62.7, 65.0, 69.6, 71.9, 74.3],
    8:  [68.7, 61.7, 64.0, 66.4, 71.0, 73.5, 75.9],
    9:  [70.1, 62.9, 65.3, 67.7, 72.4, 74.9, 77.4],
    10: [71.5, 64.1, 66.5, 69.0, 73.8, 76.4, 78.9],
    11: [72.8, 65.2, 67.7, 70.3, 75.3, 77.8, 80.4],
    12: [74.0, 66.3, 68.9, 71.4, 76.6, 79.2, 81.7],
    13: [75.2, 67.3, 70.0, 72.6, 77.8, 80.5, 83.1],
    14: [76.4, 68.3, 71.0, 73.7, 79.1, 81.7, 84.4],
    15: [77.5, 69.3, 72.0, 74.8, 80.2, 82.9, 85.7],
    16: [78.6, 70.3, 73.0, 75.8, 81.3, 84.2, 87.0],
    17: [79.7, 71.2, 74.0, 76.8, 82.4, 85.3, 88.2],
    18: [80.7, 72.0, 74.9, 77.8, 83.6, 86.5, 89.4],
    19: [81.7, 73.0, 75.8, 78.8, 84.6, 87.6, 90.6],
    20: [82.7, 73.7, 76.7, 79.7, 85.7, 88.7, 91.7],
    21: [83.7, 74.5, 77.5, 80.6, 86.7, 89.8, 92.9],
    22: [84.6, 75.2, 78.4, 81.5, 87.7, 90.8, 94.0],
    23: [85.5, 76.0, 79.2, 82.3, 88.7, 91.9, 95.0],
    24: [86.5, 76.0, 79.3, 82.5, 89.9, 93.1, 96.3],
    25: [87.5, 76.8, 80.0, 83.3, 90.8, 94.1, 97.3],
    26: [88.4, 77.5, 80.8, 84.1, 91.7, 95.1, 98.4],
    27: [89.3, 78.1, 81.5, 84.9, 92.6, 96.0, 99.4],
    28: [90.2, 78.8, 82.2, 85.7, 93.5, 97.0, 100.4],
    29: [91.1, 79.5, 82.9, 86.4, 94.4, 97.9, 101.4],
    30: [91.9, 80.1, 83.6, 87.1, 95.2, 98.8, 102.3],
    31: [92.7, 80.7, 84.3, 87.9, 96.1, 99.7, 103.3],
    32: [93.5, 81.3, 84.9, 88.6, 96.9, 100.5, 104.2],
    33: [94.3, 81.9, 85.6, 89.3, 97.7, 101.4, 105.1],
    34: [95.0, 82.5, 86.2, 90.0, 98.5, 102.2, 106.0],
    35: [95.8, 83.1, 86.8, 90.7, 99.3, 103.1, 106.9],
    36: [96.5, 83.6, 87.4, 91.4, 100.1, 103.9, 107.8],
    38: [98.0, 84.8, 88.6, 92.7, 101.6, 105.5, 109.5],
    40: [99.5, 85.9, 89.8, 94.0, 103.1, 107.1, 111.2],
    42: [100.9, 87.0, 91.0, 95.3, 104.6, 108.7, 112.9],
    44: [102.3, 88.0, 92.2, 96.5, 106.0, 110.2, 114.5],
    46: [103.7, 89.1, 93.3, 97.8, 107.4, 111.7, 116.1],
    48: [105.0, 90.1, 94.4, 99.0, 108.9, 113.3, 117.7],
    50: [106.3, 91.1, 95.5, 100.2, 110.3, 114.7, 119.2],
    52: [107.6, 92.1, 96.6, 101.4, 111.6, 116.2, 120.8],
    54: [108.9, 93.1, 97.6, 102.5, 113.0, 117.7, 122.3],
    56: [110.1, 94.0, 98.7, 103.7, 114.3, 119.1, 123.8],
    58: [111.3, 95.0, 99.7, 104.8, 115.6, 120.5, 125.3],
    60: [112.5, 95.9, 100.7, 105.9, 116.9, 121.9, 126.8]
}

# Berat Badan menurut Panjang/Tinggi Badan (BB/TB - WFL & WFH)
# Nilai acuan per interval 1 cm
BBTB_L = {
    45: [2.4, 1.9, 2.0, 2.2, 2.6, 2.9, 3.2],
    50: [3.3, 2.6, 2.8, 3.0, 3.7, 4.0, 4.5],
    55: [4.5, 3.6, 3.8, 4.1, 4.9, 5.4, 6.0],
    60: [6.0, 4.7, 5.1, 5.5, 6.5, 7.1, 7.8],
    65: [7.4, 5.9, 6.3, 6.8, 8.0, 8.7, 9.5],
    70: [8.6, 6.9, 7.4, 7.9, 9.3, 10.1, 11.0],
    75: [9.6, 7.7, 8.2, 8.8, 10.4, 11.3, 12.3],
    80: [10.4, 8.4, 9.0, 9.6, 11.4, 12.4, 13.6],
    85: [11.3, 9.2, 9.7, 10.4, 12.4, 13.6, 15.0],
    90: [12.4, 10.1, 10.7, 11.5, 13.7, 15.0, 16.6],
    95: [13.7, 11.2, 11.9, 12.7, 15.2, 16.7, 18.5],
    100: [15.1, 12.3, 13.1, 14.0, 16.7, 18.5, 20.6],
    105: [16.5, 13.5, 14.4, 15.4, 18.4, 20.4, 22.8],
    110: [18.0, 14.7, 15.7, 16.8, 20.2, 22.5, 25.1],
    115: [19.7, 16.0, 17.1, 18.3, 22.1, 24.7, 27.7],
    120: [21.5, 17.4, 18.6, 20.0, 24.2, 27.1, 30.5]
}

BBTB_P = {
    45: [2.5, 1.9, 2.1, 2.3, 2.7, 3.0, 3.3],
    50: [3.4, 2.6, 2.8, 3.1, 3.7, 4.1, 4.5],
    55: [4.5, 3.5, 3.8, 4.1, 4.9, 5.4, 6.0],
    60: [5.8, 4.5, 4.9, 5.3, 6.3, 7.0, 7.7],
    65: [7.0, 5.5, 6.0, 6.5, 7.7, 8.4, 9.3],
    70: [8.2, 6.5, 7.0, 7.6, 8.9, 9.7, 10.7],
    75: [9.1, 7.3, 7.8, 8.4, 10.0, 10.9, 12.0],
    80: [10.1, 8.1, 8.6, 9.3, 11.1, 12.1, 13.3],
    85: [11.1, 8.9, 9.5, 10.2, 12.2, 13.4, 14.8],
    90: [12.2, 9.8, 10.5, 11.3, 13.5, 14.9, 16.6],
    95: [13.5, 10.9, 11.6, 12.5, 15.0, 16.6, 18.5],
    100: [14.9, 12.0, 12.8, 13.8, 16.6, 18.4, 20.6],
    105: [16.4, 13.2, 14.1, 15.2, 18.3, 20.4, 22.9],
    110: [18.1, 14.5, 15.5, 16.7, 20.2, 22.6, 25.5],
    115: [19.9, 15.9, 17.0, 18.4, 22.3, 25.1, 28.4],
    120: [21.8, 17.3, 18.6, 20.1, 24.6, 27.8, 31.6]
}


# ==============================================================================
# FUNGSI INTERPOLASI & KALKULASI Z-SCORE DETERMINISTIK
# ==============================================================================

def get_nearest_ref(key: float, table: Dict[int, List[float]]) -> List[float]:
    """Cari titik referensi terdekat atau interpolasi 2 titik."""
    keys = sorted(table.keys())
    if key <= keys[0]:
        return table[keys[0]]
    if key >= keys[-1]:
        return table[keys[-1]]
    
    # Linear interpolation between nearest two keys
    for i in range(len(keys) - 1):
        k1, k2 = keys[i], keys[i + 1]
        if k1 <= key <= k2:
            f = (key - k1) / (k2 - k1)
            r1, r2 = table[k1], table[k2]
            return [r1[j] + f * (r2[j] - r1[j]) for j in range(7)]
    return table[keys[0]]


def calculate_z_score(val: float, ref: List[float]) -> float:
    """
    Hitung z-score standar deviasi WHO:
    ref format: [Median, -3SD, -2SD, -1SD, +1SD, +2SD, +3SD]
    """
    median = ref[0]
    sd_m3  = ref[1]
    sd_m2  = ref[2]
    sd_m1  = ref[3]
    sd_p1  = ref[4]
    sd_p2  = ref[5]
    sd_p3  = ref[6]

    if val == median:
        return 0.0

    if val > median:
        if val <= sd_p1:
            step = (sd_p1 - median)
            return (val - median) / step if step > 0 else 0.0
        elif val <= sd_p2:
            step = (sd_p2 - sd_p1)
            return 1.0 + ((val - sd_p1) / step) if step > 0 else 1.0
        elif val <= sd_p3:
            step = (sd_p3 - sd_p2)
            return 2.0 + ((val - sd_p2) / step) if step > 0 else 2.0
        else:
            step = (sd_p3 - sd_p2)
            return 3.0 + ((val - sd_p3) / step) if step > 0 else 3.0
    else:
        if val >= sd_m1:
            step = (median - sd_m1)
            return -((median - val) / step) if step > 0 else 0.0
        elif val >= sd_m2:
            step = (sd_m1 - sd_m2)
            return -(1.0 + ((sd_m1 - val) / step)) if step > 0 else -1.0
        elif val >= sd_m3:
            step = (sd_m2 - sd_m3)
            return -(2.0 + ((sd_m2 - val) / step)) if step > 0 else -2.0
        else:
            step = (sd_m2 - sd_m3)
            return -(3.0 + ((sd_m3 - val) / step)) if step > 0 else -3.0


# ==============================================================================
# KLASIFIKASI STATUS GIZI (PERMENKES NO. 2/2020)
# ==============================================================================

def classify_bbu(z: float) -> Dict[str, Any]:
    if z <= -3.0:
        return {"label": "Gizi Buruk", "code": "SEVERELY_UNDERWEIGHT", "is_crit": True, "is_warn": False}
    elif z <= -2.0:
        return {"label": "Gizi Kurang", "code": "UNDERWEIGHT", "is_crit": False, "is_warn": True}
    elif z <= 1.0:
        return {"label": "Gizi Baik", "code": "NORMAL_WEIGHT", "is_crit": False, "is_warn": False}
    else:
        return {"label": "Berisiko Gizi Lebih", "code": "RISK_OVERWEIGHT", "is_crit": False, "is_warn": True}


def classify_tbu(z: float) -> Dict[str, Any]:
    if z <= -3.0:
        return {"label": "Sangat Pendek (Stunting Akut)", "code": "SEVERELY_STUNTED", "is_crit": True, "is_warn": False}
    elif z <= -2.0:
        return {"label": "Pendek (Stunted)", "code": "STUNTED", "is_crit": False, "is_warn": True}
    elif z <= 3.0:
        return {"label": "Normal", "code": "NORMAL_HEIGHT", "is_crit": False, "is_warn": False}
    else:
        return {"label": "Tinggi", "code": "TALL", "is_crit": False, "is_warn": False}


def classify_bbtb(z: float) -> Dict[str, Any]:
    if z <= -3.0:
        return {"label": "Gizi Buruk (Wasting Akut)", "code": "SEVERELY_WASTED", "is_crit": True, "is_warn": False}
    elif z <= -2.0:
        return {"label": "Gizi Kurang (Wasted)", "code": "WASTED", "is_crit": False, "is_warn": True}
    elif z <= 1.0:
        return {"label": "Gizi Baik (Normal)", "code": "NORMAL_WASTING", "is_crit": False, "is_warn": False}
    elif z <= 2.0:
        return {"label": "Berisiko Gizi Lebih", "code": "RISK_OVERWEIGHT", "is_crit": False, "is_warn": False}
    elif z <= 3.0:
        return {"label": "Gizi Lebih (Overweight)", "code": "OVERWEIGHT", "is_crit": False, "is_warn": True}
    else:
        return {"label": "Obesitas", "code": "OBESE", "is_crit": True, "is_warn": False}


# ==============================================================================
# DETEKSI TREN PERTUMBUHAN KUNJUNGAN BERTURUT-TURUT
# Dipindahkan ke kode sesuai instruksi mentor!
# ==============================================================================

def analyze_growth_trend(
    bb_curr: float,
    bb_prev: Optional[float] = None,
    tb_curr: Optional[float] = None,
    tb_prev: Optional[float] = None
) -> Dict[str, Any]:
    """
    Evaluasi tren pertumbuhan antara 2 kunjungan berurutan:
    - Penurunan BB > 10% (Acute weight loss / risiko malnutrisi akut)
    - Kenaikan BB stagnan/tidak naik (T2/2T KMS)
    """
    if bb_prev is None or bb_prev <= 0:
        return {
            "has_trend_data": False,
            "bb_diff": 0.0,
            "bb_pct_change": 0.0,
            "is_acute_drop": False,
            "is_stagnant": False,
            "trend_label": "Data kunjungan sebelumnya tidak tersedia"
        }

    bb_diff = bb_curr - bb_prev
    pct_change = (bb_diff / bb_prev) * 100.0

    # Penurunan berat badan > 10%
    is_acute_drop = pct_change <= -10.0

    # Stagnan (berat sama atau turun sedikit)
    is_stagnant = bb_diff <= 0.05 and not is_acute_drop

    if is_acute_drop:
        label = f"Penurunan BB Akut ({pct_change:.1f}% dari bulan lalu)"
    elif is_stagnant:
        label = "Berat Badan Stagnan / Tidak Naik (KMS 2T)"
    elif bb_diff > 0:
        label = f"Kenaikan Positif (+{bb_diff:.2f} kg)"
    else:
        label = f"Fluktuasi Kecil ({bb_diff:.2f} kg)"

    return {
        "has_trend_data": True,
        "bb_diff": round(bb_diff, 2),
        "bb_pct_change": round(pct_change, 1),
        "is_acute_drop": is_acute_drop,
        "is_stagnant": is_stagnant,
        "trend_label": label
    }


# ==============================================================================
# PIPELINE ANALISIS LENGKAP ANAK
# ==============================================================================

def sanitize_name(name: str) -> str:
    """Sanitasi nama balita terhadap input malicious/HTML."""
    clean = html.escape(name.strip())
    # Hapus karakter berlebih non-alphanumeric & spasi standar
    clean = re.sub(r'[^a-zA-Z0-9\s\.\,\'\-]', '', clean)
    return clean[:60] if clean else "Balita"


def anonymize_name(name: str) -> str:
    """Sensor nama untuk privasi data (UU PDP No. 27/2022)."""
    parts = name.split()
    if not parts:
        return "Ananda ****"
    if len(parts) == 1:
        p = parts[0]
        return f"{p[:2]}****" if len(p) > 2 else f"{p}****"
    return f"{parts[0]} {parts[1][0]}.****"


def validate_biometric_bounds(usia: int, bb: float, tb: float) -> List[str]:
    """Validasi biologis rentang WHO untuk deteksi data anomali / Parity Validator."""
    errors = []
    if not (0 <= usia <= 60):
        errors.append(f"Usia ({usia} bln) di luar rentang acuan balita 0-60 bulan")
    if not (1.5 <= bb <= 35.0):
        errors.append(f"Berat badan ({bb} kg) di luar rentang biologis aman (1.5-35 kg)")
    if not (40.0 <= tb <= 130.0):
        errors.append(f"Tinggi/panjang badan ({tb} cm) di luar rentang standar (40-130 cm)")
    return errors


def evaluate_child(
    nama: str,
    usia_bulan: int,
    bb: float,
    tb: float,
    jk: str,
    cara_ukur: Optional[str] = None, # 'terlentang' atau 'berdiri'
    bb_prev: Optional[float] = None,
    anonymize: bool = False
) -> Dict[str, Any]:
    """
    Evaluasi klinis lengkap per balita sesuai standar WHO / Kemenkes RI.
    """
    safe_name = sanitize_name(nama)
    display_name = anonymize_name(safe_name) if anonymize else safe_name
    jk = 'L' if str(jk).strip().upper().startswith('L') else 'P'
    
    # Validasi biologis
    parity_warnings = validate_biometric_bounds(usia_bulan, bb, tb)

    # 1. Konversi Panjang Badan vs Tinggi Badan (Instruksi Mentor):
    # Standar WHO:
    # < 24 bulan: baku adalah Panjang Badan (PB / Terlentang).
    # >= 24 bulan: baku adalah Tinggi Badan (TB / Berdiri).
    # Jika cara ukur tidak sesuai baku usia, koreksi konversi 0.7 cm dilakukan.
    tb_adjusted = tb
    conversion_note = None

    if usia_bulan < 24:
        # Standar seharusnya PB (terlentang)
        if cara_ukur == 'berdiri':
            # Jika anak < 24 bulan diukur berdiri, PB = TB + 0.7 cm
            tb_adjusted = tb + 0.7
            conversion_note = "Koreksi +0.7 cm (diukur berdiri pada usia <24 bln)"
    else:
        # Standar seharusnya TB (berdiri)
        if cara_ukur == 'terlentang':
            # Jika anak >= 24 bulan diukur terlentang, TB = PB - 0.7 cm
            tb_adjusted = tb - 0.7
            conversion_note = "Koreksi -0.7 cm (diukur terlentang pada usia >=24 bln)"

    # Lookup Tabel WHO
    table_bbu = BBU_L if jk == 'L' else BBU_P
    table_tbu = TBU_L if jk == 'L' else TBU_P
    table_bbtb = BBTB_L if jk == 'L' else BBTB_P

    ref_bbu = get_nearest_ref(float(usia_bulan), table_bbu)
    ref_tbu = get_nearest_ref(float(usia_bulan), table_tbu)
    ref_bbtb = get_nearest_ref(float(round(tb_adjusted)), table_bbtb)

    # Z-scores
    z_bbu = calculate_z_score(bb, ref_bbu)
    z_tbu = calculate_z_score(tb_adjusted, ref_tbu)
    z_bbtb = calculate_z_score(bb, ref_bbtb)

    # Klasifikasi
    status_bbu = classify_bbu(z_bbu)
    status_tbu = classify_tbu(z_tbu)
    status_bbtb = classify_bbtb(z_bbtb)

    # Tren Pertumbuhan Kunjungan Berturut-turut
    trend = analyze_growth_trend(bb_curr=bb, bb_prev=bb_prev)

    # Penentuan Triase Risiko Terpadu
    # Prioritas Tinggi: zBBTB < -3 (wasting akut), zTBU < -3 (stunting berat), zBBU < -3, ATAU BB drop >10%
    # Perlu Pemantauan: zTBU < -2, zBBU < -2, zBBTB < -2, ATAU BB stagnan
    if (z_bbtb < -3.0 or z_tbu < -3.0 or z_bbu < -3.0 or trend["is_acute_drop"] or z_bbtb > 3.0):
        risk_level = "TINGGI"
        risk_label = "Rujukan Prioritas Puskesmas"
    elif (z_tbu < -2.0 or z_bbu < -2.0 or z_bbtb < -2.0 or trend["is_stagnant"] or z_bbtb > 2.0):
        risk_level = "SEDANG"
        risk_label = "Perlu Pemantauan Khusus"
    else:
        risk_level = "AMAN"
        risk_label = "Gizi Baik (Normal)"

    return {
        "nama": display_name,
        "nama_asli": safe_name,
        "usia_bulan": usia_bulan,
        "bb": bb,
        "tb": tb,
        "tb_adjusted": round(tb_adjusted, 1),
        "jk": jk,
        "jk_label": "Laki-laki" if jk == 'L' else "Perempuan",
        "cara_ukur": cara_ukur or ("terlentang" if usia_bulan < 24 else "berdiri"),
        "conversion_note": conversion_note,
        "z_bbu": round(z_bbu, 2),
        "z_tbu": round(z_tbu, 2),
        "z_bbtb": round(z_bbtb, 2),
        "status_bbu": status_bbu,
        "status_tbu": status_tbu,
        "status_bbtb": status_bbtb,
        "trend": trend,
        "risk_level": risk_level,
        "risk_label": risk_label,
        "parity_warnings": parity_warnings,
        "ref_bbu": ref_bbu,
        "ref_tbu": ref_tbu,
        "ref_bbtb": ref_bbtb
    }
