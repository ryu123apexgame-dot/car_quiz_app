import streamlit as st
import json
import random

# データ読み込み
with open("cars.json", "r", encoding="utf-8") as f:
    data = json.load(f)

st.title("🚗 車種クイズアプリ")

mode = st.radio("モード選択", ["一覧", "クイズ", "タイプ別クイズ"])

# ------------------------
# 一覧モード
# ------------------------
if mode == "一覧":
    makers = sorted(list(set([d["maker"] for d in data])))
    maker = st.selectbox("メーカー選択", makers)

    cars = [d for d in data if d["maker"] == maker]

    for car in cars:
        image_path = f"images/{car['maker_en']}_{car['model_en']}.jpg"
        st.image(image_path, width=300)
        st.write(f"{car['model']}（{car['type']}）")

# ========================
# 共通関数（choices生成）
# ========================
def generate_choices(dataset, question):
    choices = random.sample(dataset, min(3, len(dataset)-1))
    if question not in choices:
        choices.append(question)
    random.shuffle(choices)
    return choices

# ========================
# クイズモード
# ========================
if mode == "クイズ":

    TOTAL_QUESTIONS = min(10, len(data))

    # 初期化
    if "quiz_initialized" not in st.session_state:
        st.session_state.quiz_initialized = True
        st.session_state.count = 0
        st.session_state.score = 0
        st.session_state.answered = False

        st.session_state.question = random.choice(data)
        st.session_state.history = [st.session_state.question]

        st.session_state.choices = generate_choices(data, st.session_state.question)
        st.session_state.selected = None

    # 終了画面
    if st.session_state.count >= TOTAL_QUESTIONS:
        accuracy = st.session_state.score / TOTAL_QUESTIONS * 100
        st.subheader("結果発表")
        st.write(f"正解数：{st.session_state.score} / {TOTAL_QUESTIONS}")
        st.write(f"正解率：{accuracy:.1f}%")

        if st.button("もう一度"):
            st.session_state.clear()
            st.rerun()

    else:
        q = st.session_state.question

        st.write(f"問題 {st.session_state.count + 1} / {TOTAL_QUESTIONS}")

        image_path = f"images/{q['maker_en']}_{q['model_en']}.jpg"
        st.image(image_path, width=600)

        options = [c["model"] for c in st.session_state.choices]

        selected = st.radio(
            "この車は？",
            options,
            index=options.index(st.session_state.selected)
            if st.session_state.selected in options else 0,
            key="quiz_radio"
        )

        st.session_state.selected = selected

        # 回答
        if st.button("回答") and not st.session_state.answered:
            st.session_state.answered = True
            st.session_state.count += 1

            if selected == q["model"]:
                st.session_state.score += 1
                st.success("正解！")
            else:
                st.error(f"不正解：{q['model']}")

        # 次の問題
        if st.session_state.answered:
            if st.button("次の問題"):

                remaining = [d for d in data if d not in st.session_state.history]

                if remaining:
                    st.session_state.question = random.choice(remaining)
                    st.session_state.history.append(st.session_state.question)
                else:
                    st.session_state.question = random.choice(data)

                # choices固定生成
                st.session_state.choices = generate_choices(data, st.session_state.question)

                st.session_state.selected = None
                st.session_state.answered = False

                st.rerun()

# ========================
# タイプ別クイズ
# ========================
if mode == "タイプ別クイズ":

    types = sorted(list(set([d["type"] for d in data])))
    selected_type = st.selectbox("タイプ選択", types)

    filtered = [d for d in data if d["type"] == selected_type]

    if len(filtered) < 4:
        st.warning("このタイプはデータが少なすぎる")
    else:
        TOTAL_QUESTIONS = min(10, len(filtered))

        if "type_initialized" not in st.session_state:
            st.session_state.type_initialized = True
            st.session_state.count = 0
            st.session_state.score = 0
            st.session_state.answered = False

            st.session_state.question = random.choice(filtered)
            st.session_state.history = [st.session_state.question]

            st.session_state.choices = generate_choices(filtered, st.session_state.question)
            st.session_state.selected = None

        if st.session_state.count >= TOTAL_QUESTIONS:
            accuracy = st.session_state.score / TOTAL_QUESTIONS * 100
            st.subheader("結果発表")
            st.write(f"正解数：{st.session_state.score} / {TOTAL_QUESTIONS}")
            st.write(f"正解率：{accuracy:.1f}%")

            if st.button("もう一度"):
                st.session_state.clear()
                st.rerun()

        else:
            q = st.session_state.question

            st.write(f"問題 {st.session_state.count + 1} / {TOTAL_QUESTIONS}")

            image_path = f"images/{q['maker_en']}_{q['model_en']}.jpg"
            st.image(image_path, width=600)

            options = [c["model"] for c in st.session_state.choices]

            selected = st.radio(
                "この車は？",
                options,
                index=options.index(st.session_state.selected)
                if st.session_state.selected in options else 0,
                key="type_radio"
            )

            st.session_state.selected = selected

            if st.button("回答") and not st.session_state.answered:
                st.session_state.answered = True
                st.session_state.count += 1

                if selected == q["model"]:
                    st.session_state.score += 1
                    st.success("正解！")
                else:
                    st.error(f"不正解：{q['model']}")

            if st.session_state.answered:
                if st.button("次の問題"):

                    remaining = [d for d in filtered if d not in st.session_state.history]

                    if remaining:
                        st.session_state.question = random.choice(remaining)
                        st.session_state.history.append(st.session_state.question)
                    else:
                        st.session_state.question = random.choice(filtered)

                    st.session_state.choices = generate_choices(filtered, st.session_state.question)

                    st.session_state.selected = None
                    st.session_state.answered = False

                    st.rerun()