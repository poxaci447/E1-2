class Quiz:
    """개별 퀴즈 문제, 선택지, 정답을 관리하는 클래스입니다."""

    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, number: int | None = None) -> None:
        """퀴즈 문제와 1~4번 선택지를 화면에 출력합니다."""
        if number is not None:
            print(f"\n[문제 {number}]")
        print(self.question)
        for idx, choice in enumerate(self.choices, start=1):
            print(f"{idx}. {choice}")

    def check_answer(self, user_answer: int) -> bool:
        """사용자가 입력한 번호(1~4)가 정답과 일치하는지 반환합니다."""
        return user_answer == self.answer