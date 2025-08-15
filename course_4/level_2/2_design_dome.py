import math
from typing import Tuple, Dict, Any

LAST_RESULT: Dict[str, Any] = {
    'material': None,
    'diameter': None,
    'thickness': None,
    'area': None,
    'weight_kg_mars': None,
}

DENSITY_G_CM3 = {
    'glass': 2.4,
    'aluminum': 2.7,
    'carbon_steel': 7.85,
}

MARS_G_RATIO = 0.38
GRAM_TO_KG = 0.001
CM_TO_M = 0.01

class DomeInputError(ValueError):
    pass

def is_number_str(s: str) -> bool:
    if s is None:
        return False
    s = s.strip()
    if s == '':
        return False
    # 음수/소수 허용
    if s[0] in '+-':
        s2 = s[1:]
    else:
        s2 = s
    return s2.replace('.', '', 1).isdigit()

def validate_inputs(material: str, diameter_m: float, thickness_cm: float) -> None:
    if material not in DENSITY_G_CM3:
        raise DomeInputError(f'허용되지 않은 재질: {material}')
    if not (isinstance(diameter_m, (int, float)) and diameter_m > 0):
        raise DomeInputError('지름은 양의 실수여야 합니다.')
    if not (isinstance(thickness_cm, (int, float)) and thickness_cm > 0):
        raise DomeInputError('두께는 양의 실수여야 합니다.')

def hemisphere_curved_area(radius_m: float) -> float:
    return 2.0 * math.pi * (radius_m ** 2)

def shell_volume_cm3(radius_m: float, thickness_cm: float) -> float:
    area_m2 = hemisphere_curved_area(radius_m)
    thickness_m = thickness_cm * CM_TO_M
    volume_m3 = area_m2 * thickness_m
    return volume_m3 * (100.0 ** 3)

def sphere_area(diameter: float, material: str, thickness: float = 1.0) -> Tuple[float, float]:
    validate_inputs(material, diameter, thickness)
    r_m = diameter / 2.0
    area_m2 = hemisphere_curved_area(r_m)

    density = DENSITY_G_CM3[material]
    vol_cm3 = shell_volume_cm3(r_m, thickness)
    mass_kg = density * vol_cm3 * GRAM_TO_KG
    weight_kg_on_mars = mass_kg * MARS_G_RATIO

    LAST_RESULT.update({
        'material': material,
        'diameter': diameter,
        'thickness': thickness,
        'area': area_m2,
        'weight_kg_mars': weight_kg_on_mars,
    })
    return area_m2, weight_kg_on_mars

def format_material_korean(material: str) -> str:
    return {'glass': '유리', 'aluminum': '알루미늄', 'carbon_steel': '탄소강'}.get(material, material)

def prompt_loop() -> None:
    while True:
        print('\n[Mars 돔 구조물 설계]')
        try:
            mat_in = input('재질(glass|aluminum|carbon_steel): ').strip().lower()
            dia_in = input('지름(m): ').strip()
            thk_in = input('두께(cm, 기본=1): ').strip()

            if not is_number_str(dia_in):
                raise DomeInputError('지름은 숫자여야 합니다.')
            diameter = float(dia_in)

            thickness = 1.0
            if thk_in:
                if not is_number_str(thk_in):
                    raise DomeInputError('두께는 숫자여야 합니다.')
                thickness = float(thk_in)

            area_m2, weight_kg_mars = sphere_area(diameter, mat_in, thickness)

            dia_out = int(diameter) if float(diameter).is_integer() else diameter
            thk_out = int(thickness) if float(thickness).is_integer() else thickness
            print(f"재질 ⇒ {format_material_korean(mat_in)}, 지름 ⇒ {dia_out}, 두께 ⇒ {thk_out}, "
                  f"면적 ⇒ {area_m2:.3f}, 무게 ⇒ {weight_kg_mars:.3f} kg")

        except DomeInputError as e:
            print(f'[입력오류] {e}')
        except Exception as e:
            print(f'[에러] 예기치 못한 오류: {e}')

        cmd = input('계속(y) / 종료(q): ').strip().lower()
        if cmd == 'q':
            print('종료합니다.')
            break

if __name__ == '__main__':
    prompt_loop()
