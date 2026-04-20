import streamlit as st
import json
import random

# ------------------------
# ページ設定（重要）
# ------------------------
st.set_page_config(
    page_title="車種クイズ",
    page_icon="🚗",
    layout="centered"
)

# CSS（ボタン強化）
st.markdown("""
<style>
button {
    width: 100%;
    height: 50px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# データ読み込み
# ------------------------
with open("cars.json", "r", encoding="utf-8") as f:
    data = json.load(f)
# ------------------------
# 言語切替
# ------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "ja"

lang = st.toggle(
    "🌐 Language / 言語",
    value=(st.session_state.get("lang", "ja") == "en")
)

st.session_state.lang = "en" if lang else "ja"
lang = st.session_state.lang

lang = st.session_state.lang
st.markdown("---")

TEXT = {
    "title": {"ja": "🚗 車種クイズアプリforゆうみさん", "en": "🚗 Car Quiz App for yumi"},
    "mode": {"ja": "モード選択", "en": "Select Mode"},
    "list": {"ja": "一覧", "en": "List"},
    "quiz": {"ja": "クイズ", "en": "Quiz"},
    "type_quiz": {"ja": "タイプ別クイズ", "en": "Type Quiz"},
    "maker": {"ja": "メーカー選択", "en": "Select Maker"},
    "question": {"ja": "この車は？", "en": "What car is this?"},
    "select": {"ja": "車種を選択してください", "en": "Select the car model"},
    "choices": {"ja": "選択肢", "en": "Choices"},
    "answer": {"ja": "回答", "en": "Answer"},
    "next": {"ja": "次の問題", "en": "Next"},
    "correct": {"ja": "正解！", "en": "Correct!"},
    "wrong": {"ja": "不正解", "en": "Wrong"},
    "result": {"ja": "結果発表", "en": "Result"},
    "retry": {"ja": "もう一度", "en": "Retry"},
}
# タイトル
st.markdown(
    f"<h1 style='text-align: center; font-size: 16px; margin-bottom: 5px;'>{TEXT['title'][lang]}</h1>",
    unsafe_allow_html=True
)

with st.expander("🆕 アップデート情報（4/20）", expanded=True):
    st.write("・UIをアプリ風に改善したよ👍")
    st.write("・ナンバープレートの文字削除したよ😙")
    st.write("・英語切り替え機能を上部につけたよ🤗")

st.markdown("---")
lang = st.session_state.lang

mode = st.radio(
    TEXT["mode"][lang],
    [TEXT["list"][lang], TEXT["quiz"][lang], TEXT["type_quiz"][lang]]
)

# ------------------------
# 一覧モード（カード風）
# ------------------------
if mode == TEXT["list"][lang]:
    makers = sorted(list(set([d["maker"] for d in data])))
    maker = st.selectbox(TEXT["maker"][lang], makers)

    cars = [d for d in data if d["maker"] == maker]

    for car in cars:
        st.markdown("---")
        image_path = f"images/{car['maker_en']}_{car['model_en']}.jpg"
        st.image(image_path, use_container_width=True)
        st.markdown(f"### 🚗 {car['model']}")
        st.caption(f"タイプ：{car['type']}")
        st.markdown("<br>", unsafe_allow_html=True)


# ------------------------
# 共通関数
# ------------------------
def generate_choices(dataset, question):
    choices = random.sample(dataset, min(3, len(dataset)-1))
    if question not in choices:
        choices.append(question)
    random.shuffle(choices)
    return choices

# ========================
# クイズモード
# ========================
if mode == TEXT["quiz"][lang]:

    TOTAL_QUESTIONS = min(10, len(data))

    if "quiz_initialized" not in st.session_state:
        st.session_state.quiz_initialized = True
        st.session_state.count = 0
        st.session_state.score = 0
        st.session_state.answered = False

        st.session_state.question = random.choice(data)
        st.session_state.history = [st.session_state.question]
        st.session_state.choices = generate_choices(data, st.session_state.question)
        st.session_state.selected = None

    if st.session_state.count >= TOTAL_QUESTIONS:
        accuracy = st.session_state.score / TOTAL_QUESTIONS * 100

        st.subheader(f"🎉 {TEXT['result'][lang]}")
        st.metric("正解数", f"{st.session_state.score} / {TOTAL_QUESTIONS}")
        st.metric("正解率", f"{accuracy:.1f}%")
        if st.session_state.score == TOTAL_QUESTIONS:
           st.balloons()
           st.success("🏆 パーフェクト！すごい！転職先でもがんばって、応援してるよ、ゆうみさん🥳")
        elif st.session_state.score >= TOTAL_QUESTIONS * 0.8:
           st.info("🔥 惜しい！かなり良い！")
        elif st.session_state.score >= TOTAL_QUESTIONS * 0.5:
           st.warning("👍 まずまず！")
        else:
           st.error("📚 もう一回挑戦！")


        if st.button(TEXT["retry"][lang]):
            st.session_state.clear()
            st.rerun()

    else:
        q = st.session_state.question

        st.markdown(f"## 📝 問題 {st.session_state.count + 1} / {TOTAL_QUESTIONS}")
        st.markdown(f"### 📸 {TEXT['question'][lang]}")

        image_path = f"images/{q['maker_en']}_{q['model_en']}.jpg"
        st.image(image_path, use_container_width=True)
        st.caption(TEXT["select"][lang])

        st.markdown(f"### 🔽 {TEXT['choices'][lang]}")

        options = [c["model"] for c in st.session_state.choices]

        selected = st.radio(
            "",
            options,
            index=options.index(st.session_state.selected)
            if st.session_state.selected in options else 0,
            key="quiz_radio"
        )

        st.session_state.selected = selected

        col1, col2 = st.columns(2)

        with col1:
            if st.button(TEXT["answer"][lang]) and not st.session_state.answered:
                st.session_state.answered = True
                st.session_state.count += 1

                if selected == q["model"]:
                    st.session_state.score += 1
                    st.success(f"✅ {TEXT['correct'][lang]}")
                else:
                    st.error(f"❌ {TEXT['wrong'][lang]}：{q['model']}")

        with col2:
            if st.session_state.answered:
                if st.button(TEXT["next"][lang]):

                    remaining = [d for d in data if d not in st.session_state.history]

                    if remaining:
                        st.session_state.question = random.choice(remaining)
                        st.session_state.history.append(st.session_state.question)
                    else:
                        st.session_state.question = random.choice(data)

                    st.session_state.choices = generate_choices(data, st.session_state.question)
                    st.session_state.selected = None
                    st.session_state.answered = False

                    st.rerun()

# ========================
# タイプ別クイズ
# ========================
if mode == TEXT["type_quiz"][lang]:

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

            st.subheader("🎉 結果発表")
            st.metric("正解数", f"{st.session_state.score} / {TOTAL_QUESTIONS}")
            st.metric("正解率", f"{accuracy:.1f}%")

            if st.button("もう一度"):
                st.session_state.clear()
                st.rerun()

        else:
            q = st.session_state.question

            st.markdown(f"### 問題 {st.session_state.count + 1} / {TOTAL_QUESTIONS}")
            st.markdown("### 📸 この車は？")

            image_path = f"images/{q['maker_en']}_{q['model_en']}.jpg"
            st.image(image_path, use_container_width=True)
            st.caption("車種を選択してください")

            st.markdown("### 🔽 選択肢")

            options = [c["model"] for c in st.session_state.choices]

            selected = st.radio(
                "",
                options,
                index=options.index(st.session_state.selected)
                if st.session_state.selected in options else 0,
                key="type_radio"
            )

            st.session_state.selected = selected

            col1, col2 = st.columns(2)

            with col1:
                if st.button("回答") and not st.session_state.answered:
                    st.session_state.answered = True
                    st.session_state.count += 1

                    if selected == q["model"]:
                        st.session_state.score += 1
                        st.success("✅ 正解！")
                    else:
                        st.error(f"❌ 不正解：{q['model']}")

            with col2:
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

# すべての処理の外（共通領域）

st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 20px;
    left: 20px;
    font-size: 12px;
    color: gray;
}
</style>

<div class="footer">
    Created by ryu😊 | Ver1.1
</div>
""", unsafe_allow_html=True)