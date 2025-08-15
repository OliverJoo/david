import csv
import os
import struct
from typing import List, Dict, Any, Optional

DATA_DIR = 'data_source'
RESULT_DIR = 'result'

INVENTORY_CSV = os.path.join(DATA_DIR, 'Mars_Base_Inventory_List.csv')
DANGER_CSV = os.path.join(RESULT_DIR, 'Mars_Base_Inventory_danger.csv')
BINARY_FILE = os.path.join(RESULT_DIR, 'Mars_Base_Inventory_List.bin')

def ensure_dir(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print(f'[에러] 디렉터리 생성 실패({path}): {e}')

def safe_float(s: Any, default: float = 0.0) -> float:
    try:
        if s is None:
            return default
        if isinstance(s, (int, float)):
            return float(s)
        s2 = str(s).strip()
        if s2 == '':
            return default
        return float(s2)
    except Exception:
        return default

def safe_int(s: Any, default: int = 0) -> int:
    try:
        if s is None:
            return default
        if isinstance(s, (int, float)):
            return int(s)
        s2 = str(s).strip()
        if s2 == '':
            return default
        return int(float(s2))
    except Exception:
        return default

def normalize_header(header: List[str]) -> List[str]:
    norm = []
    for h in header:
        h2 = (h or '').strip().lower()
        norm.append(h2)
    return norm

def read_inventory_csv(path: str) -> List[Dict[str, Any]]:
    """CSV 파일을 읽어 리스트[dict]로 반환한다.
    - 다양한 헤더명 매핑 지원
    - 값 타입 오류/빈 값/부족한 컬럼 방어
    - BOM/공백 라인 처리
    """
    items: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        print(f'[경고] 파일이 존재하지 않습니다: {path}')
        return items

    # 컬럼명 후보 매핑
    name_keys = {'name', 'substance', 'item', 'material'}
    qty_keys = {'quantity', 'qty', 'count', 'weight (g/cm³)'}
    flamm_keys = {'flammability', 'flammability_index', 'flammability idx', 'flammability score'}

    try:
        with open(path, 'r', encoding='utf-8-sig', newline='') as f:
            # *.csv 는 자체 줄 처리가 되므로, newline='' 옵션으로서 자동 개행 변환이 섞여 빈줄 추가되는 문제를 방지
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                print('[경고] CSV 헤더가 비어있습니다.')
                return items
            header_norm = normalize_header(header)

            # 열 인덱스 탐색
            def find_idx(candidates: set[str]) -> Optional[int]:
                for i, h in enumerate(header_norm):
                    if h in candidates:
                        return i
                return None

            idx_name = find_idx(name_keys)
            idx_qty = find_idx(qty_keys)
            idx_fi = find_idx(flamm_keys)

            # 헤더 명이 예상 외일 경우, 기본 위치 추정: 0:name, 1:qty, 4 or 2:flammability
            # 제공 파일 스키마: Substance, Weight (g/cm³), Specific Gravity, Strength, Flammability
            if idx_name is None:
                idx_name = 0 if len(header_norm) > 0 else None
            if idx_qty is None:
                # 제공 스키마의 'Weight (g/cm³)'는 수량이 아님. 수량 불명 시 0 처리.
                idx_qty = None
            if idx_fi is None:
                # 제공 스키마에서 Flammability는 마지막 컬럼₩    Å¸¸¸¸``Å⁄⁄¸¸¸⁄¸
                if 'flammability' in header_norm:
                    idx_fi = header_norm.index('flammability')
                elif len(header_norm) >= 5:
                    idx_fi = 4
                elif len(header_norm) >= 3:
                    idx_fi = 2

            for row in reader:
                if not row or all((c is None or str(c).strip() == '') for c in row):
                    continue
                try:
                    name = (row[idx_name].strip() if (idx_name is not None and len(row) > idx_name) else 'UNKNOWN') or 'UNKNOWN'
                except Exception:
                    name = 'UNKNOWN'

                quantity = 0
                if idx_qty is not None and len(row) > idx_qty:
                    quantity = safe_int(row[idx_qty], 0)

                fi = 0.0
                if idx_fi is not None and len(row) > idx_fi:
                    fi = safe_float(row[idx_fi], 0.0)

                items.append({
                    'name': name,
                    'quantity': quantity,
                    'flammability_index': fi,
                })
    except OSError as e:
        print(f'[에러] CSV 읽기 실패: {e}')
    except csv.Error as e:
        print(f'[에러] CSV 파싱 실패: {e}')
    return items

def print_items(items: List[Dict[str, Any]], title: str = '') -> None:
    if title:
        print(title)
    if not items:
        print('[정보] 출력할 항목이 없습니다.')
        return
    for it in items:
        name = it.get('name', 'UNKNOWN')
        qty = safe_int(it.get('quantity', 0), 0)
        fi = safe_float(it.get('flammability_index', 0.0), 0.0)
        print(f'이름: {name}, 수량: {qty}, 인화성지수: {fi:.3f}')

def sort_by_flammability_desc(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(items, key=lambda x: safe_float(x.get('flammability_index', 0.0), 0.0), reverse=True)

def filter_dangerous(items: List[Dict[str, Any]], threshold: float = 0.7) -> List[Dict[str, Any]]:
    return [it for it in items if safe_float(it.get('flammability_index', 0.0), 0.0) >= threshold]

def save_danger_csv(items: List[Dict[str, Any]], path: str) -> bool:
    ensure_dir(os.path.dirname(path))
    try:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'quantity', 'flammability_index'])
            for it in items:
                writer.writerow([
                    it.get('name', 'UNKNOWN'),
                    safe_int(it.get('quantity', 0), 0),
                    f'{safe_float(it.get("flammability_index", 0.0), 0.0):.3f}',
                ])
        print(f'[정보] 위험 목록 CSV 저장 완료: {path}')
        return True
    except OSError as e:
        print(f'[에러] 위험 CSV 저장 실패: {e}')
        return False

def save_sorted_to_binary(items: List[Dict[str, Any]], path: str) -> bool:
    ensure_dir(os.path.dirname(path))
    try:
        with open(path, 'wb') as f:
            # struct.pack format
            # <: 리틀 엔디안(Little Endian) 바이트 순서 지정
            # i: 4바이트 부호있는 정수(signed integer)
            # I: 4바이트 부호없는 정수(unsigned integer)
            # d: 8바이트 배정밀도 부동소수점(double precision float)
            f.write(struct.pack('<I', len(items))) # 전체 아이템 개수를 파일 시작 부분에 저장 목적
            for it in items:
                name_b = (it.get('name', 'UNKNOWN') or 'UNKNOWN').encode('utf-8')
                qty = safe_int(it.get('quantity', 0), 0)
                fi = safe_float(it.get('flammability_index', 0.0), 0.0)
                f.write(struct.pack('<I', len(name_b)))
                f.write(name_b)
                f.write(struct.pack('<id', qty, fi))
        print(f'[정보] 이진 파일 저장 완료: {path}')
        return True
    except OSError as e:
        print(f'[에러] 이진 파일 저장 실패: {e}')
        return False

def read_binary_inventory(path: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if not os.path.exists(path):
        print(f'[경고] 이진 파일이 없습니다: {path}')
        return items
    try:
        with open(path, 'rb') as f:
            hdr = f.read(4)
            if len(hdr) < 4:
                print('[경고] 이진 파일 손상(헤더 부족).')
                return items
            n = struct.unpack('<I', hdr)[0]
            for _ in range(n):
                nb = f.read(4)
                if len(nb) < 4:
                    print('[경고] 이진 파일 손상(이름 길이).')
                    break
                nlen = struct.unpack('<I', nb)[0]
                name_bytes = f.read(nlen)
                if len(name_bytes) < nlen:
                    print('[경고] 이진 파일 손상(이름 본문).')
                    break
                rest = f.read(12)
                if len(rest) < 12:
                    print('[경고] 이진 파일 손상(값 본문).')
                    break
                qty, fi = struct.unpack('<id', rest)
                items.append({'name': name_bytes.decode('utf-8', errors='replace'),
                              'quantity': qty,
                              'flammability_index': fi})
    except OSError as e:
        print(f'[에러] 이진 파일 읽기 실패: {e}')
    return items

def explain_text_vs_binary() -> str:
    return '\n'.join([
        '- 텍스트: 사람이 읽기 쉬움, 이식성 높음, 크기 큼, 파싱 비용 존재.',
        '- 이진: 사람이 읽기 어려움, 크기 작고 I/O 빠름, 엔디안/버전 호환 주의.',
        '- 장애 내성: 텍스트는 라인 단위 복구 용이, 이진은 오프셋 손상 시 연쇄 오류.',
        '- 정밀도: 텍스트는 포맷/파싱 오차 가능, 이진은 원값 보존에 유리(본래 이진 표현을 그대로 보존하므로 변환 오차가 없음).',
    ])

def main() -> None:
    while True:
        print('\n[Mars 기지 적재물 관리]')
        items = read_inventory_csv(INVENTORY_CSV)
        print_items(items, title='--- 전체 인벤토리 ---')

        sorted_items = sort_by_flammability_desc(items)
        print_items(sorted_items, title='\n--- 인화성 내림차순 정렬 ---')

        dangerous = filter_dangerous(sorted_items, 0.7)
        print_items(dangerous, title='\n--- 위험(인화성≥0.700) 항목 ---')

        save_danger_csv(dangerous, DANGER_CSV)

        if sorted_items:
            if save_sorted_to_binary(sorted_items, BINARY_FILE):
                loaded = read_binary_inventory(BINARY_FILE)
                print_items(loaded, title='\n--- 이진 파일 재로딩 결과 ---')

        # print('\n--- 텍스트 vs 이진 ---')
        # print(explain_text_vs_binary())

        cmd = input('\n계속 진행하려면 y, 종료하려면 q: ').strip().lower()
        if cmd == 'q':
            print('종료합니다.')
            break

if __name__ == '__main__':
    main()
