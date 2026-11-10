class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self, number):
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i in range(len(self.choices)):
            print(f"{i + 1}. {self.choices[i]}")
        print()

    def is_correct(self, user_answer):
        return user_answer == self.answer

def create_default_quizzes():
    return [
        Quiz(
            "다음 중 국세가 아닌 것은?",
            ["소득세", "법인세", "부가가치세", "재산세"],
            4,
        ),
        Quiz(
            "종합소득세 확정신고·납부 기한은 원칙적으로 언제일까요?",
            ["3월 31일", "5월 31일", "7월 25일", "12월 31일"],
            2,
        ),
        Quiz(
            "회사가 급여를 줄 때 세금을 미리 떼어 국가에 납부하는 제도는?",
            ["수정신고", "기한후신고", "원천징수", "경정청구"],
            3,
        ),
        Quiz(
            "부가가치세의 기본 세율은?",
            ["5%", "10%", "15%", "20%"],
            2,
        ),
        Quiz(
            "세금을 과다하게 신고·납부했을 때 돌려받기 위해 하는 청구는?",
            ["경정청구", "수정신고", "기한후신고", "이의신청"],
            1,
        ),
    ]


def show_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def get_menu_choice():
    while True:
        text = input("선택: ").strip()

        if text == "":
            print("⚠️ 아무것도 입력하지 않았습니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        if number < 1 or number > 5:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        return number


def main():
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 5:
            print("👋 프로그램을 종료합니다.")
            break

        print(f"(준비 중) {choice}번 메뉴를 선택했습니다.\n")




if __name__ == "__main__":
    main()