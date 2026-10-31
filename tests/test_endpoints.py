import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from backend.excel_handler import generate_posyandu_template_excel

# 1. Test Health
r1 = requests.get('http://127.0.0.1:3000/api/health')
print('1. Health Check:', r1.status_code, r1.json())

# 2. Test Excel Ingest
excel_data = generate_posyandu_template_excel()
r2 = requests.post(
    'http://127.0.0.1:3000/api/ingest/excel',
    files={'file': ('posyandu_sample.xlsx', excel_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
)
print('2. Excel Ingest:', r2.status_code)
d2 = r2.json()
print('   Status:', d2.get('status'))
print('   Extracted count:', d2.get('total_extracted'))
for item in d2.get('data', []):
    print(f"   * {item['nama']} ({item['jk']}, {item['usia']} bln): BB {item['bb']} kg, TB {item['tb']} cm -> {item['parity_status']}")

# 3. Test AI Counsel
payload = {
    'posyandu': 'Posyandu Melati RW 03',
    'periode': '2026-09',
    'balita_list': [
        {'nama': 'Andi Pratama', 'usia': 21, 'bb': 8.5, 'tb': 78.0, 'jk': 'L', 'bb_prev': 8.4},
        {'nama': 'Budi Santoso', 'usia': 16, 'bb': 7.1, 'tb': 70.0, 'jk': 'L', 'bb_prev': 8.0}
    ],
    'anonymize': False
}
r3 = requests.post('http://127.0.0.1:3000/api/ai/counsel', json=payload)
print('3. AI Counsel:', r3.status_code)
d3 = r3.json()
print('   Source:', d3.get('source'))
print('   Summary:', d3.get('summary'))
print('   Instructions:', d3.get('instructions'))

# 4. Test Offline Sync
r4 = requests.post('http://127.0.0.1:3000/api/sync', json={
    'posyandu': 'Posyandu Melati RW 03',
    'periode': '2026-09',
    'recorded_at': '2026-09-15T09:00:00Z',
    'balita_list': d3.get('analyzed_data', []),
    'summary': d3.get('summary', {}),
    'notes': 'Sync test from automated suite'
})
print('4. Offline Sync to Server:', r4.status_code, r4.json().get('message'))

# 5. Test Records History
r5 = requests.get('http://127.0.0.1:3000/api/records')
print('5. Historical Records count:', len(r5.json().get('records', [])))
