import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

st.title("いつ段位アップ？")

# （略）required_training, training_speeds 定義
# セッション初期化 も同じ…

# 定数
cycle_time    = 8
herb_interval = 15 * 60
herb_cycles   = 40
buff_options  = {"30%": 0.30, "20%": 0.20, "10%": 0.10, "3%": 0.03}

# シミュレーション関数（略、前回と同じ）

if st.button("シミュレーション開始"):
    current   = st.session_state.current_value_w10k * 10000
    target    = st.session_state.target_value_w10k * 10000
    remaining = target - current
    items     = st.session_state.item_count
    base_speed = training_speeds[st.session_state.current_stage][st.session_state.current_rank]
    now_jst    = datetime.now(ZoneInfo("Asia/Tokyo"))

    rows = []
    for label, buff in buff_options.items():
        # 1) 未使用シナリオ
        t0, m0, h0 = simulate_time(remaining, base_speed, buff, init_herbs=0)
        finish0    = now_jst + timedelta(seconds=t0)
        rows.append({
            "シナリオ":       "未使用",
            "バフ":         label,
            "到達時刻":     finish0.strftime("%Y-%m-%d %H:%M"),
            "所要時間":     f"{t0//3600}h {(t0%3600)//60}m",
            "手動修練(万)": f"{int(m0)//10000}",
            "仙草修練(万)": f"{int(h0)//10000}"
        })

        # 2) アイテム使用シナリオ
        if items > 0:
            # 1個で得られるポイント
            per_item_pts = 3 * herb_cycles * base_speed
            needed_items = math.ceil(remaining / per_item_pts)
            used_items   = min(items, needed_items)

            t1, m1, h1 = simulate_time(remaining, base_speed, buff, init_herbs=used_items*3)
            finish1    = now_jst + timedelta(seconds=t1)
            rows.append({
                "シナリオ":       f"{used_items}個使用",
                "バフ":         label,
                "到達時刻":     finish1.strftime("%Y-%m-%d %H:%M"),
                "所要時間":     f"{t1//3600}h {(t1%3600)//60}m",
                "手動修練(万)": f"{int(m1)//10000}",
                "仙草修練(万)": f"{int(h1)//10000}"
            })

    df = pd.DataFrame(rows)
    # 表示したい列の順序を固定
    df = df[[
        "シナリオ",
        "バフ",
        "到達時刻",
        "所要時間",
        "手動修練(万)",
        "仙草修練(万)"
    ]]

    st.markdown("### シミュレーション結果")
    st.table(df)
