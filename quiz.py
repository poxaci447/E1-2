from typing import Any


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

    def to_dict(self) -> dict[str, Any]:
        """JSON 저장을 위해 Quiz 인스턴스를 딕셔너리로 변환합니다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        """딕셔너리 데이터를 검증한 뒤 Quiz 인스턴스로 복원합니다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목 형식이 올바르지 않습니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 텍스트가 올바르지 않습니다.")
        if (
            not isinstance(choices, list)
            or len(choices) != 4
            or not all(isinstance(c, str) and c.strip() for c in choices)
        ):
            raise ValueError("선택지는 4개의 문자열이어야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not (1 <= answer <= 4):
            raise ValueError("정답 번호는 1~4 사이의 정수여야 합니다.")

        return cls(question=question.strip(), choices=[c.strip() for c in choices], answer=answer)


def get_default_quizzes() -> list[Quiz]:
    """기본 영화 퀴즈 5문항을 Quiz 인스턴스 리스트로 반환합니다."""
    return [
        Quiz(
            question="영화 '기생충'의 감독은?",
            choices=["박찬욱", "봉준호", "나홍진", "이창동"],
            answer=2,
        ),
        Quiz(
            question="마블 시네마틱 유니버스에서 타노스가 모은 인피니티 스톤의 개수는?",
            choices=["4개", "5개", "6개", "7개"],
            answer=3,
        ),
        Quiz(
            question="영화 '인셉션(Inception)'에서 주인공 코브가 현실과 꿈을 구별하기 위해 사용하는 토템은?",
            choices=["주사위", "팽이", "체스 말", "회중시계"],
            answer=2,
        ),
        Quiz(
            question="영화 '올드보이'에서 주인공 오대수가 15년간 감금되어 있을 때 매일 먹었던 음식은?",
            choices=["자장면", "군만두", "김치찌개", "라면"],
            answer=2,
        ),
        Quiz(
            question="영화 '인터스텔라'에서 주인공 쿠퍼가 우주로 떠나며 딸 머피에게 남긴 물건은?",
            choices=["나침반", "손목시계", "만년필", "목걸이"],
            answer=2,
        ),
    ]