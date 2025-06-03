import streamlit as st
import math
from datetime import datetime, timedelta

st.title("レベルアップ時刻予測シミュレーション")

# 各境地・段位ごとの修練速度/周天（辞書で定義）
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

# サイドバーで各種入力
st.sidebar.header("現在の境地・段位")
current_stage = st.sidebar.selectbox("現在の境地", list(training_speeds.keys()))
current_rank = st.sidebar.selectbox("現在の段位", list(training_speeds[current_stage].keys()))

st.sidebar.header("次の境地・段位")
target_stage = st.sidebar.selectbox("次の境地", list(training_speeds.keys()), index=1)
target_rank = st.sidebar.selectbox("次の段位", list(training_speeds[target_stage].keys()), index=0)

st.sidebar.header("修練値入力")
current_value = st.sidebar.number_input("現在の修練の値", min_value=0, value=0, step=1)
target_value = st.sidebar.number_input("次の境地までに必要な修練の値", min_value=1, value=1000, step=1)

st.sidebar.header("霊峰バフ選択")
# 霊峰バフは手動修練にのみ効果がある
buff_options = {"なし": 0, "30%": 0.30, "20%": 0.20, "10%": 0.10, "3%": 0.03}
selected_buff_label = st.sidebar.radio("霊峰バフ", list(buff_options.keys()))
buff = buff_options[selected_buff_label]

# 定数
cycle_time = 8         # 1周天の所要時間（秒）
herb_interval = 15 * 60  # 仙草が手に入る間隔：15分 = 900秒
herb_cycles   = 40     # 仙草1つにつき加算される周天数

if st.button("シミュレーション開始"):
    base_speed = training_speeds[current_stage][current_rank]
    # 目標までに必要な修練値（補完する分）
    remaining = target_value - current_value
    if remaining <= 0:
        st.success("既に必要な修練値に達しています。")
    else:
        # 時間 t（秒）を1秒刻みで増加させながら、到達時刻を算出
        t = 0
        while True:
            # 手動修練による修練値（バフが適用される）
            manual_points = (t / cycle_time) * base_speed * (1 + buff)
            # 仙草による修練値：herb_intervalごとに 40 周天分
            herb_count = t // herb_interval
            herb_points = herb_count * herb_cycles * base_speed
            total_points = manual_points + herb_points
            if total_points >= remaining:
                break
            t += 1

        # シミュレーション終了時刻の計算（現在時刻から t 秒後）
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
