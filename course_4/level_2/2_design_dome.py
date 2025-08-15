import math
import sys

CM_TO_M = 0.01
MARS_GRAVITY_RATIO = 0.38  # 화성 중력 비율 (지구 대비 약 0.38배)
DENSITY_G_CM3 = {
    "glass": 2.4,
    "aluminum": 2.7,
    "carbon_steel": 7.85
}
MATERIAL_KO = {
    "glass": "유리",
    "aluminum": "알루미늄",
    "carbon_steel": "탄소강"
}

def sphere_area(diameter: float) -> float:
    """전체 구의 겉넓이 (m²)"""
    radius = diameter / 2.0
    return 2.0 * math.pi * (radius ** 2) # 반구체 계산
    # return 4.0 * math.pi * (radius ** 2) # 구체 전체 계산


def sphere_weight(diameter: float, material: str, thickness_cm: float) -> float:
    """반구 돔 무게(kg): 표면적 x 두께 x 밀도 -> 질량, 화성 중력 반영"""
    area_m2 = sphere_area(diameter)
    thickness_m = thickness_cm * CM_TO_M
    volume_m3 = area_m2 * thickness_m
    # 밀도 변환: (g/cm³) → (kg/m³)  (1 g/cm³ = 1000 kg/m³)
    density_kg_m3 = DENSITY_G_CM3[material] * 1000
    mass_kg = area_m2 * thickness_m * density_kg_m3
    mars_weight_kg = mass_kg * MARS_GRAVITY_RATIO
    return mars_weight_kg

def input_material() -> str:
    """재질 입력과 검증"""
    valid_materials = set(DENSITY_G_CM3.keys())
    while True:
        mat = input("재질(glass/aluminum/carbon_steel): ").strip().lower()
        if mat in valid_materials:
            return mat
        print("올바른 재질(glass/aluminum/carbon_steel) 중 하나를 입력하세요.")

def input_float(prompt: str, min_value: float = 0.001) -> float:
    """float 입력과 검증"""
    while True:
        value_str = input(prompt).strip()
        try:
            value = float(value_str)
            if value >= min_value:
                return value
            print(f"{min_value} 이상의 숫자를 입력하세요.")
        except ValueError:
            print("숫자를 입력하세요.")

def input_yes_no(prompt: str) -> bool:
    """종료 여부 입력"""
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        elif answer in {"n", "no"}:
            return False
        else:
            print("y 또는 n 으로 답변하세요.")

def main():
    print("="*50)
    print("반구체 돔 표면적/무게 계산기 (화성 중력 반영)")
    print("="*50)
    while True:
        try:
            material = input_material()
            diameter = input_float("돔의 지름(m): ", min_value=0.001)
            thickness_cm = input_float("쉘 두께(cm, 기본: 1): ", min_value=0.001)
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            sys.exit(0)
        except Exception as e:
            print(f"예상치 못한 오류: {e}")
            continue

        try:
            area = sphere_area(diameter)
            weight = sphere_weight(diameter, material, thickness_cm)

            print(f"재질 ⇒ {MATERIAL_KO[material]}, "
                  f"지름 ⇒ {int(diameter)}, "
                  f"두께 ⇒ {int(thickness_cm)}, "
                  f"면적 ⇒ {area:.3f}, "
                  f"무게 ⇒ {weight:.3f} kg\n")
        except Exception as e:
            print(f"계산 오류: {e}")

        # 반복 여부
        if not input_yes_no("계속 계산하시겠습니까?"):
            print("프로그램을 종료합니다.")
            break

if __name__ == "__main__":
    main()