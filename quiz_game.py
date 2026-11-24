import json
from pathlib import Path

from quiz import Quiz, get_default_quizzes


class QuizGame:
    """퀴즈 게임의 전체 상태(퀴즈 목록, 최고 점수)와 파일 입출력을 관리하는 클래스입니다."""

    def __init__(self, state_path: str | Path | None = None) -> None:
        if state_path is None:
            self.state_file = Path(__file__).resolve().parent / "state.json"
        else:
            self.state_file = Path(state_path)

        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.load_state()

    def load_state(self) -> None:
        """state.json에서 데이터를 불러오고, 파일이 없거나 손상 시 기본 데이터로 복구합니다."""
        if not self.state_file.exists():
            print("[안내] 저장된 데이터 파일이 없어 기본 영화 퀴즈로 시작합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("JSON 최상위 구조는 객체(dict)여야 합니다.")

            raw_quizzes = data.get("quizzes")
            if not isinstance(raw_quizzes, list):
                raise ValueError("quizzes 필드는 리스트여야 합니다.")

            loaded_quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

            best_score = data.get("best_score")
            if best_score is not None and (isinstance(best_score, bool) or not isinstance(best_score, int)):
                raise ValueError("best_score 필드는 정수 또는 null이어야 합니다.")

            self.quizzes = loaded_quizzes
            self.best_score = best_score

            score_text = f"{self.best_score}점" if self.best_score is not None else "기록 없음"
            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")
        except (OSError, json.JSONDecodeError, ValueError, TypeError, KeyError):
            print("[안내] state.json 파일이 손상되었거나 읽을 수 없어 기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = get_default_quizzes()
            self.best_score = None
            self.save_state()

    def save_state(self) -> None:
        """현재 퀴즈 목록과 최고 점수를 state.json에 UTF-8로 저장합니다."""
        payload = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"[오류] state.json 저장 중 문제가 발생했습니다: {e}")

    @staticmethod
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

    @staticmethod
    def get_non_empty_text(prompt: str) -> str:
        """앞뒤 공백을 제거하고 빈 입력을 방어해 유효한 문자열을 반환합니다."""
        while True:
            text = input(prompt).strip()
            if not text:
                print("잘못된 입력입니다. 내용을 입력해 주세요.")
                continue
            return text

    def print_menu(self) -> None:
        """메인 메뉴 화면을 출력합니다."""
        print("\n=== 나만의 영화 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def play_quiz(self) -> None:
        """저장된 퀴즈를 출제하고 채점 결과 출력 및 최고 점수를 갱신·저장합니다."""
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        total = len(self.quizzes)
        correct_count = 0
        print(f"\n▶ 퀴즈를 시작합니다! (총 {total}문제)")

        for idx, quiz in enumerate(self.quizzes, start=1):
            quiz.display(idx)
            user_answer = self.get_valid_number("정답 입력 (1-4): ", 1, 4)

            if quiz.check_answer(user_answer):
                print("✓ 정답입니다!")
                correct_count += 1
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"✗ 오답입니다. 정답은 {quiz.answer}번({correct_text})입니다.")

        score = round((correct_count / total) * 100)
        print(f"\n결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save_state()
            print("★ 새로운 최고 점수입니다!")

    def add_quiz(self) -> None:
        """새로운 퀴즈(문제, 선택지 4개, 정답 번호)를 입력받아 추가하고 파일에 저장합니다."""
        print("\n★ 새로운 퀴즈를 추가합니다.")
        question = self.get_non_empty_text("문제를 입력하세요: ")

        choices: list[str] = []
        for i in range(1, 5):
            choice_text = self.get_non_empty_text(f"선택지 {i}: ")
            choices.append(choice_text)

        answer = self.get_valid_number("정답 번호 (1-4): ", 1, 4)
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("✓ 퀴즈가 추가되었습니다!")

    def show_quiz_list(self) -> None:
        """저장된 퀴즈 목록을 번호와 함께 출력합니다."""
        if not self.quizzes:
            print("\n[안내] 등록된 퀴즈가 없습니다.")
            return

        print(f"\n■ 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"[{idx}] {quiz.question}")

    def show_best_score(self) -> None:
        """현재까지 기록된 최고 점수를 출력합니다."""
        if self.best_score is None:
            print("\n[안내] 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요!")
            return

        print(f"\n★ 최고 점수: {self.best_score}점")

    def run(self) -> None:
        """프로그램 메인 루프를 실행합니다."""
        try:
            while True:
                self.print_menu()
                choice = self.get_valid_number("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.save_state()
                    print("프로그램을 종료합니다. 이용해주셔서 감사합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            self.save_state()
            print("\n[안내] 종료 신호가 감지되어 데이터를 저장한 뒤 안전하게 종료합니다.")