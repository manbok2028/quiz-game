import json
import os

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


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

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }


def quiz_from_dict(data):
    if not isinstance(data, dict):
        raise ValueError("퀴즈 형식이 올바르지 않습니다.")

    question = data.get("question")
    choices = data.get("choices")
    answer = data.get("answer")

    if not isinstance(question, str) or question.strip() == "":
        raise ValueError("문제가 올바르지 않습니다.")
    if not isinstance(choices, list) or len(choices) != 4:
        raise ValueError("선택지는 4개여야 합니다.")
    for choice in choices:
        if not isinstance(choice, str) or choice.strip() == "":
            raise ValueError("선택지가 올바르지 않습니다.")
    if isinstance(answer, bool) or not isinstance(answer, int) or answer < 1 or answer > 4:
        raise ValueError("정답 번호는 1~4여야 합니다.")

    return Quiz(question, choices, answer)


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


def get_number(prompt, low, high):
    while True:
        text = input(prompt).strip()

        if text == "":
            print(f"⚠️ 아무것도 입력하지 않았습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        if number < low or number > high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue

        return number


def get_text(prompt):
    while True:
        text = input(prompt).strip()
        if text == "":
            print("⚠️ 아무것도 입력하지 않았습니다. 내용을 입력하세요.")
            continue
        return text


def is_plain_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0
        self.load_state()

    def reset_to_default(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError:
            print("⚠️ 데이터를 파일에 저장하지 못했습니다.")

    def load_state(self):
        if not os.path.exists(STATE_FILE):
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.\n")
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("데이터 형식이 올바르지 않습니다.")

            raw_quizzes = data.get("quizzes")
            if not isinstance(raw_quizzes, list):
                raise ValueError("quizzes 항목이 올바르지 않습니다.")
            quizzes = [quiz_from_dict(item) for item in raw_quizzes]

            best_score = data.get("best_score")
            best_correct = data.get("best_correct", 0)
            best_total = data.get("best_total", 0)

            if best_score is not None:
                if not is_plain_int(best_score) or best_score < 0 or best_score > 100:
                    raise ValueError("best_score 값이 올바르지 않습니다.")
            if not is_plain_int(best_correct) or not is_plain_int(best_total):
                raise ValueError("점수 기록이 올바르지 않습니다.")

        except (OSError, ValueError):
            print("⚠️ 데이터 파일이 손상되었거나 읽을 수 없어 기본 퀴즈로 초기화합니다.\n")
            self.reset_to_default()
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.best_correct = best_correct
        self.best_total = best_total

        if self.best_score is None:
            score_text = "없음"
        else:
            score_text = f"{self.best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})\n")

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def get_menu_choice(self):
        return get_number("선택: ", 1, 5)

    def play_quiz(self):
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.\n")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")

        for i, quiz in enumerate(self.quizzes, 1):
            quiz.show(i)
            answer = get_number("정답 입력: ", 1, 4)
            if quiz.is_correct(answer):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")

        score = correct * 100 // total
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")

        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.best_correct = correct
            self.best_total = total
            self.save_state()
            print("🎉 새로운 최고 점수입니다!")

        print("=" * 40)
        print()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")

        question = get_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = get_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = get_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def list_quizzes(self):
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다.\n")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)
        print()

    def show_best_score(self):
        if self.best_score is None:
            print("\n⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어 보세요.\n")
            return

        print(
            f"\n🏆 최고 점수: {self.best_score}점 "
            f"({self.best_total}문제 중 {self.best_correct}문제 정답)\n"
        )

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 5:
                self.save_state()
                print("👋 프로그램을 종료합니다.")
                break

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
                input("Enter 키를 누르면 메뉴로 돌아갑니다...")
            elif choice == 4:
                self.show_best_score()
                input("Enter 키를 누르면 메뉴로 돌아갑니다...")


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()