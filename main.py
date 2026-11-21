def get_valid_number(prompt: str, min_val: int, max_val: int) -> int:
    """공백 제거, 빈 입력, 숫자 변환 실패, 범위 이탈을 검증해 유효한 정수를 반환합니다."""
    while True:
        raw_input = input(prompt).strip()

        if not raw_input:
            print("잘못된 입력입니다. 빈 값은 입력할 수 없습니다.")
            continue

        try:
            number = int(raw_input)
        except ValueError:
            print(f"잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")
            continue

        if not (min_val <= number <= max_val):
            print(f"잘못된 입력입니다. {min_val}-{max_val} 사이의 숫자를 입력하세요.")
            continue

        return number


def print_menu() -> None:
    """메인 메뉴 화면을 출력합니다."""
    print("\n=== 나만의 영화 퀴즈 게임 ===")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")


def main() -> None:
    """프로그램 메인 루프입니다."""
    try:
        while True:
            print_menu()
            choice = get_valid_number("선택: ", 1, 5)

            if choice == 1:
                print("[안내] 퀴즈 풀기 기능 준비 중입니다.")
            elif choice == 2:
                print("[안내] 퀴즈 추가 기능 준비 중입니다.")
            elif choice == 3:
                print("[안내] 퀴즈 목록 기능 준비 중입니다.")
            elif choice == 4:
                print("[안내] 점수 확인 기능 준비 중입니다.")
            elif choice == 5:
                print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
                break
    except (KeyboardInterrupt, EOFError):
        print("\n[안내] 종료 신호가 감지되어 프로그램을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()