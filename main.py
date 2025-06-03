import streamlit as st
import math
from datetime import datetime, timedelta

st.title("レベルアップ時刻予測シミュレーション")

# 各境地・段位ごとの修練速度/周天を定義
training_speeds = {
    "錬気": {1: 100, 2: 200, 3: 300},
    "築基": {1: 400, 2: 500, 3: 600},
    "結丹": {1: 700, 2: 800, 3: 900},
    "元嬰": {1: 1000, 2: 1100, 3: 1200, 4: 1300, 5: 1400, 6: 1500},
    "化神": {1: 1600, 2: 1700, 3: 1800, 4: 1900, 5: 2000, 6: 2100},
    "錬虚": {1: 2200, 2: 2300, 3: 2400, 4: 2500, 5: 2600, 6: 2700},
    "合体": {1: 2800, 2: 2900, 3: 3000, 4: 3100, 5: 3200, 6: 3300, 7: 3400, 8: 3500, 9: 3600},
    "大乗": {1: 3700, 2: 3800, 3: 3900, 4: 4000, 5: 4100, 6: 4200, 7: 4300, 8: 4400, 9: 4500}
}

# サイドバーに現在の境地・段位の入力
st.sidebar.header("現在の境地・段位")
current_stage = st.sidebar.selectbox("現在の境地", list(training_speeds.keys()))
current_rank = st.sidebar.selectbox("現在の段位", list(training_speeds[current_stage].keys()))

# サイドバーに修練値の入力（次の境地・段位自体は不要）
st.sidebar.header("修練値入力")
current_value = st.sidebar.number_input("現在の修練の値", min_value=0, value=0, step=1)
target_value = st.sidebar.number_input("次の境地までに必要な修練の値", min_value=1, value=10000, step=1)

# 霊峰バフの選択（仙草効果には影響しない）
st.sidebar.header("霊峰バフ選択")
buff_options = {"なし": 0, "30%": 0.30, "20%": 0.20, "10%": 0.10, "3%": 0.03}
selected_buff_label = st.sidebar.radio("霊峰バフ", list(buff_options.keys()))
buff = buff_options[selected_buff_label]

# 定数設定
cycle_time = 8           # 1周天に必要な秒数
herb_interval = 15 * 60  # 仙草取得間隔：15分（900秒）
herb_cycles = 40         # 仙草1個で補助される周天数

if st.button("シミュレーション開始"):
    # 現在の境地・段位から修練速度を取得
    base_speed = training_speeds[current_stage][current_rank]
    # 現在からの必要修練値（負荷アップ分）
    remaining = target_value - current_value

    if remaining <= 0:
        st.success("既に必要な修練値に到達しています。")
    else:
        # 経過秒 t を1秒刻みで試算して、手動と仙草合算で必要な修練値に到達する最小の時間を求める
        t = 0
        while True:
            # 【手動修練】　1周天あたり base_speed × (1+霊峰バフ)
            manual_points = (t / cycle_time) * base_speed * (1 + buff)
            # 【仙草】　15分ごとに1個、1個につき40周天分の修練値（霊峰バフは適用されない）
            herb_count = t // herb_interval
            herb_points = herb_count * herb_cycles * base_speed
            total_points = manual_points + herb_points

            if total_points >= remaining:
                break
            t += 1

        # 終了時刻を現在時刻＋ t 秒で計算
        finish_time = datetime.now() + timedelta(seconds=t)
        hours = t // 3600
        minutes = (t % 3600) // 60
        seconds = t % 60

        st.markdown("### シミュレーション結果")
        st.write(f"**予想到達時刻**: {finish_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**所要時間**: 約 {hours} 時間 {minutes} 分 {seconds} 秒")
        st.write("【内訳】")
        st.write(f"- 手動修練による修練値: {manual_points:.0f}")
        st.write(f"- 仙草による修練値: {herb_points:.0f}")
