import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Smart Flying Star Pro", page_icon="🧭", layout="wide")

# --- ១. ក្បួនតក្កវិជ្ជាគណនាហុងស៊ុយ ---
SECTORS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
SECTOR_NAMES = ['ជើង (N)', 'ជើងកើត (NE)', 'កើត (E)', 'ត្បូងកើត (SE)', 'ត្បូង (S)', 'ត្បូងលិច (SW)', 'លិច (W)', 'ជើងលិច (NW)']
GUAS = [1, 8, 3, 4, 9, 2, 7, 6]
PATH = ['C', 'NW', 'W', 'NE', 'S', 'N', 'SW', 'E', 'SE']

POLARITY = {
    1: [1, -1, -1],  2: [-1, 1, 1],
    3: [1, -1, -1],  4: [-1, 1, 1],
    6: [-1, 1, 1],   7: [1, -1, -1],
    8: [-1, 1, 1],   9: [1, -1, -1]
}

def fly_stars(star, direction):
    chart = {}
    curr = star
    for pos in PATH:
        chart[pos] = curr
        curr += direction
        if curr > 9: curr = 1
        if curr < 1: curr = 9
    return chart

def calculate_flying_stars(period, degree):
    norm_deg = (degree + 22.5) % 360
    facing_idx = int(norm_deg // 45)
    sub_m_idx = int((norm_deg % 45) // 15)
    sitting_idx = (facing_idx + 4) % 8
    
    base_chart = fly_stars(period, 1)
    
    m_star = base_chart[SECTORS[sitting_idx]]
    m_gua = GUAS[sitting_idx] if m_star == 5 else m_star
    m_dir = POLARITY[m_gua][sub_m_idx]
    m_chart = fly_stars(m_star, m_dir)
    
    w_star = base_chart[SECTORS[facing_idx]]
    w_gua = GUAS[facing_idx] if w_star == 5 else w_star
    w_dir = POLARITY[w_gua][sub_m_idx]
    w_chart = fly_stars(w_star, w_dir)
    
    final_chart = {}
    for pos in PATH:
        final_chart[pos] = {'m': m_chart[pos], 'w': w_chart[pos], 'b': base_chart[pos]}
    return final_chart, SECTOR_NAMES[facing_idx]


# --- ២. ទិន្នន័យបកស្រាយហុងស៊ុយយុគទី៩ (Period 9: 2024 - 2043) ---
period_9_interpretation = {
    9: {"status": "Wang Qi (ចូលយុគ)", "type": "វិជ្ជមានបំផុត", "desc": "ផ្កាយមហាសំណាងប្រចាំយុគទី៩។ តំណាងឲ្យទ្រព្យសម្បត្តិ ភាពល្បីល្បាញ និងឱកាសធំៗ។", "cure": "🔥 ដាស់ថាមពលដោយចលនា ទឹក ឬពន្លឺ។"},
    1: {"status": "Sheng Qi (កំពុងលូតលាស់)", "type": "វិជ្ជមាន", "desc": "ផ្កាយអនាគតរុងរឿង។ ល្អសម្រាប់ការវិនិយោគ ការសិក្សា និងគម្រោងរយៈពេលវែង។", "cure": "🌱 ប្រើរុក្ខជាតិ ឬទឹកផុសតូចៗ។"},
    2: {"status": "Tien Yi (អនាគតឆ្ងាយ)", "type": "អព្យាក្រឹត/អវិជ្ជមាន", "desc": "ផ្កាយជំងឺចាប់ផ្តើមថយឥទ្ធិពល តែនៅទាមទារការប្រុងប្រយ័ត្នចំពោះសុខភាព។", "cure": "🔔 ប្រើកណ្តឹងខ្យល់លោហៈ ៦បំពង់។"},
    3: {"status": "Dead Qi (ធ្លាក់យុគ)", "type": "អវិជ្ជមាន", "desc": "ផ្កាយជម្លោះ បណ្តឹង និងការយល់ច្រឡំ។", "cure": "🔴 ប្រើពណ៌ក្រហម ពន្លឺ ឬកម្រាលព្រំក្រហម។"},
    4: {"status": "Dead Qi (ធ្លាក់យុគ)", "type": "អវិជ្ជមាន", "desc": "ផ្កាយស្នេហាខុសក្បួន ឬបញ្ហាផ្លូវចិត្ត។", "cure": "🔥 ប្រើធាតុភ្លើង ដើម្បីដុតឈើ។"},
    5: {"status": "Killing Qi (កាចសាហាវ)", "type": "អវិជ្ជមានបំផុត", "desc": "ផ្កាយគ្រោះថ្នាក់ បង្កជំងឺ និងឧបសគ្គធំ។ ដាច់ខាតត្រូវបន្សាប កុំឲ្យមានចលនា។", "cure": "🪙 ប្រើកាក់ស្ពាន់ ៦ ឬកណ្តឹងខ្យល់លោហៈ (ហាមធាតុភ្លើង)។"},
    6: {"status": "Killing Qi (ធ្លាក់យុគ)", "type": "អវិជ្ជមាន", "desc": "ផ្កាយអំណាចដែលធ្លាក់យុគ បង្កជាបញ្ហាច្បាប់ ឬការបាត់បង់តំណែង។", "cure": "💧 ប្រើទឹកស្ងៀម (Yin Water) ដើម្បីបញ្ចុះកម្តៅលោហៈ។"},
    7: {"status": "Killing Qi (ធ្លាក់យុគ)", "type": "អវិជ្ជមាន", "desc": "ផ្កាយចោរកម្ម ការបាត់បង់លុយកាក់ និងគ្រោះថ្នាក់ដោយអាវុធ។", "cure": "🌊 ប្រើទឹកដើម្បីលាងសម្អាតថាមពលអាក្រក់។"},
    8: {"status": "Tui Qi (ថយយុគ)", "type": "ខ្សោយ", "desc": "ផ្កាយអស់អំណាច។ មិនមែនជាផ្កាយនាំលុយធំទៀតទេ។ រក្សាលំនឹង តែមិនត្រូវពឹងផ្អែក។", "cure": "⛰️ ប្រើថ្ម ឬរបស់ធ្ងន់ៗដើម្បីរក្សាលំនឹង (Yin Form)។"}
}


# --- ៣. ប្រព័ន្ធទាញយករូបភាពវត្ថុហុងស៊ុយ (Update សម្រាប់យុគ ៩) ---
def get_cure_visual(m, w):
    combo = f"{m}-{w}"
    if m == 5 or w == 5 or m == 2 or w == 2:
        return "🧉", "ឃ្លោកស្ពាន់/លោហៈ", "#c0392b"
    elif w == 9: # ដាស់ផ្កាយលុយយុគ ៩
        return "⛲", "ចលនាទឹក & ពន្លឺ", "#27ae60"
    elif m == 9: # ដាស់ផ្កាយសុខភាពយុគ ៩
        return "🪨", "វត្ថុថ្ម/ភ្នំខ្ពស់", "#27ae60"
    elif w == 1:
        return "⛲", "ចលនាទឹក (Water)", "#27ae60"
    elif m == 1:
        return "🪨", "វត្ថុថ្ម/ភ្នំ (Mountain)", "#27ae60"
    elif combo in ["1-6", "6-1"]:
        return "🪴", "លោហៈ ឬ រុក្ខជាតិ", "#2980b9"
    elif combo in ["9-7", "7-9"]:
        return "🪨", "វត្ថុដីឥដ្ឋ/គ្រីស្តាល់", "#d35400"
    else:
        return "☯️", "រក្សាភាពស្ងប់ស្ងាត់", "#7f8c8d"


def get_interpretation(m, w):
    combo = f"{m}-{w}"
    interpretations = {
        "8-8": "⚠️ **ផ្កាយថយយុគ (Double 8):** អំណាចលុយកាក់បានថយចុះ។ គួររក្សាលំនឹង។",
        "5-2": "⚠️ **មហាឧបទ្រព និងជំងឺ (៥ លឿង + ២ ខ្មៅ):** ជាទីតាំងគ្រោះថ្នាក់បំផុត (ធាតុដីប៉ះដី) នាំមកនូវគ្រោះថ្នាក់ ជំងឺតម្កាត់។\n*   🛡️ **វិធីបន្សាប:** ត្រូវប្រើ 'ធាតុដែក' កម្រិតធ្ងន់។",
        "2-5": "⚠️ **មហាឧបទ្រព និងជំងឺ (២ ខ្មៅ + ៥ លឿង):** ដូចគ្នានឹង 5-2 ដែរ។",
        "1-6": "🧠 **កំពូលបញ្ញា (១ ស + ៦ ស):** ល្អសម្រាប់ការសិក្សា។",
        "6-1": "🧠 **កំពូលបញ្ញា (៦ ស + ១ ស):** ល្អសម្រាប់ការសិក្សា និងការងារ។",
        "9-7": "🔥 **ភ្លើងរលាយដែក (៩ ស្វាយ + ៧ ក្រហម):** ងាយរងបញ្ហាពាក្យសម្តី។ ប្រើធាតុដីបន្សាប។",
        "7-9": "🔥 **ភ្លើងរលាយដែក (៧ ក្រហម + ៩ ស្វាយ):** ដូចគ្នានឹង 9-7 ដែរ។"
    }
    if combo in interpretations: return interpretations[combo]
    return "💡 **ថាមពលចម្រុះ:** ត្រូវពិនិត្យមើលផ្កាយនីមួយៗតាមយុគទី៩។"


# --- ៤. ចំណុចប្រទាក់អ្នកប្រើប្រាស់ (UI) ---
st.title("ត្រីវិស័យហុងស៊ុយផ្កាយហោះកម្រិតខ្ពស់ 🧭")
st.markdown("### ការវិភាគយុគទី៩ (Period 9: 2024-2043) ផ្អែកលើទម្រង់ខាងក្រៅ")

# Input Section
col1, col2, col3 = st.columns(3)
with col1: 
    period_input = st.number_input("🌟 យុគសាងសង់ផ្ទះ (Natal Period)", min_value=1, max_value=9, value=8)
with col2: 
    degree_input = st.number_input("🧭 អង្សាទិសមុខផ្ទះ", min_value=0.0, max_value=360.0, value=355.0, step=1.0)
with col3:
    main_door_sector = st.selectbox("🚪 ទីតាំងទ្វារធំ (Main Door Sector)", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], index=0)


if st.button("🔮 គណនាទិសហុងស៊ុយ", use_container_width=True, type="primary"):
    final_chart, facing_name = calculate_flying_stars(period_input, degree_input)
    st.success(f"🏠 **ផ្ទះយុគទី {period_input}** | បែរមុខទៅទិស **{facing_name} ({degree_input} ដឺក្រេ)**")
    
    # គូរតារាង Grid (ប្រើ Native Streamlit Columns ជួសជុលបញ្ហាធ្លាក់ជួរ)
    st.markdown("---")
    st.subheader("តារាងផ្កាយហោះ (Flying Star Chart)")
    
    rows = [
        ['SE', 'S', 'SW'],
        ['E', 'C', 'W'],
        ['NE', 'N', 'NW']
    ]
    
    names = {'SE': 'ត្បូងកើត (SE)', 'S': 'ត្បូង (S)', 'SW': 'ត្បូងលិច (SW)', 'E': 'កើត (E)', 'C': 'កណ្តាល (C)', 'W': 'លិច (W)', 'NE': 'ជើងកើត (NE)', 'N': 'ជើង (N)', 'NW': 'ជើងលិច (NW)'}
    
    for row in rows:
        cols = st.columns(3)
        for i, sector in enumerate(row):
            with cols[i]:
                data = final_chart[sector]
                icon, text, color = get_cure_visual(data['m'], data['w'])
                
                st.markdown(f"""
                <div style='border: 2px solid #bdc3c7; border-radius: 10px; padding: 10px; height: 160px; position: relative; background-color: #f8f9fa; margin-bottom: 15px;'>
                    <span style='position: absolute; top: 5px; left: 10px; color: #7f8c8d; font-weight: bold; font-size: 12px;'>{names[sector]}</span>
                    <span style='position: absolute; top: 25px; left: 20px; color: #000000; font-weight: bold; font-size: 22px;'>{data['m']}</span>
                    <span style='position: absolute; top: 25px; right: 20px; color: #000000; font-weight: bold; font-size: 22px;'>{data['w']}</span>
                    <span style='position: absolute; bottom: 45px; left: 50%; transform: translateX(-50%); color: #e74c3c; font-weight: bold; font-size: 26px;'>{data['b']}</span>
                    <div style='position: absolute; bottom: 5px; left: 0; right: 0; text-align: center; border-top: 1px dashed #ecf0f1; padding-top: 5px;'>
                        <span style='font-size: 18px;'>{icon}</span><br>
                        <span style='font-size: 10px; font-weight: bold; color: {color};'>{text}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


    # ==========================================
    # ការវិភាគទ្វារធំ (The Main Door Interpretation)
    # ==========================================
    st.markdown("---")
    st.subheader("🚪 ការវិភាគទ្វារធំ (The 3 Factors Analysis)")

    door_facing_star = final_chart[main_door_sector]['w']
    door_sitting_star = final_chart[main_door_sector]['m']
    interpretation = period_9_interpretation[door_facing_star]

    st.write(f"ទីតាំងទ្វារធំរបស់អ្នកស្ថិតនៅទិស **{names[main_door_sector]}** ដែលមានផ្កាយមុខផ្ទះលេខ **{door_facing_star}** និងផ្កាយក្រោយផ្ទះលេខ **{door_sitting_star}**។")

    if door_facing_star == 9:
        st.success(f"**អបអរសាទរ!** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")
    elif door_facing_star in [1]:
        st.info(f"**ល្អប្រសើរ!** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")
    elif door_facing_star == 8:
        st.warning(f"**ចំណាំ:** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")
        st.write("ទោះបីជាផ្ទះនេះសង់ក្នុងយុគទី៨ ក៏ដោយ តែបច្ចុប្បន្នផ្កាយ៨ បានអស់អំណាចហើយ។ វាមិនអាចទាញយកថាមពលលុយកាក់ធំៗបានដូចមុនទេ។")
    else:
        st.error(f"**ប្រុងប្រយ័ត្ន!** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")

    st.markdown(f"**អត្ថន័យយុគទី៩ (ផ្កាយមុខផ្ទះ {door_facing_star}):** {interpretation['desc']}")
    st.markdown(f"**វិធីកែប្រែ/ដាស់ថាមពល (Cure/Enhancer):** {interpretation['cure']}")

    st.markdown("#### ការវិភាគទម្រង់ខាងក្រៅ (External Forms Factor)")
    st.write(f"ដោយសារទីតាំងនេះជាទ្វារធំ (ចលនា/Yang) ថាមពលនៃផ្កាយលេខ **{door_facing_star}** ត្រូវបាន **ដាស់ (Activated)** ជាស្រេច។ ប្រសិនបើមានផ្លូវបំបែក ឬទឹកផុសនៅមុខទ្វារនេះទៀត ឥទ្ធិពលរបស់វានឹងកាន់តែខ្លាំង។")


    # ==========================================
    # លទ្ធផលវិភាគតាមបន្ទប់ (General Interpretation)
    # ==========================================
    st.markdown("---")
    st.markdown("### 📊 លទ្ធផលវិភាគផ្កាយ និងវិធីបន្សាបលម្អិត")
    
    order = ['SE', 'S', 'SW', 'E', 'C', 'W', 'NE', 'N', 'NW']
    for pos in order:
        data = final_chart[pos]
        meaning = get_interpretation(data['m'], data['w'])
        with st.expander(f"📍 {names[pos]} [ ភ្នំ: {data['m']} | ទឹក: {data['w']} | គោល: {data['b']} ]", expanded=False):
            st.markdown(meaning)
