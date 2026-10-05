import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Smart Flying Star Pro", page_icon="🧭", layout="centered")

# ==========================================
# ១. ក្បួនតក្កវិជ្ជាគណនាហុងស៊ុយ (២៤ ភ្នំ)
# ==========================================
SECTORS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
SECTOR_NAMES = ['ជើង (N)', 'ជើងកើត (NE)', 'កើត (E)', 'ត្បូងកើត (SE)', 'ត្បូង (S)', 'ត្បូងលិច (SW)', 'លិច (W)', 'ជើងលិច (NW)']
GUAS = [1, 8, 3, 4, 9, 2, 7, 6]
PATH = ['C', 'NW', 'W', 'NE', 'S', 'N', 'SW', 'E', 'SE']
NAMES_DICT = {'SE': 'ត្បូងកើត (SE)', 'S': 'ត្បូង (S)', 'SW': 'ត្បូងលិច (SW)', 'E': 'កើត (E)', 'C': 'កណ្តាល (C)', 'W': 'លិច (W)', 'NE': 'ជើងកើត (NE)', 'N': 'ជើង (N)', 'NW': 'ជើងលិច (NW)'}

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

# ==========================================
# ២. ប្រព័ន្ធទិន្នន័យបកស្រាយយុគទី៩ (Period 9 Logic)
# ==========================================
period_9_single_star = {
    9: {"status": "Wang Qi (ចូលយុគ)", "desc": "ផ្កាយមហាសំណាងប្រចាំយុគទី៩ តំណាងឲ្យទ្រព្យសម្បត្តិ និងឱកាស។", "cure": "🔥 ដាស់ថាមពលដោយចលនាទឹក (សម្រាប់ Facing) ឬ ភ្នំ (សម្រាប់ Sitting)។"},
    1: {"status": "Sheng Qi (អនាគត)", "desc": "ផ្កាយអនាគតរុងរឿង ល្អសម្រាប់ការវិនិយោគ និងការសិក្សា។", "cure": "🌱 ប្រើរុក្ខជាតិ ឬទឹកផុសតូចៗ។"},
    2: {"status": "Tien Yi (អព្យាក្រឹត)", "desc": "ផ្កាយជំងឺចាប់ផ្តើមថយឥទ្ធិពល តែនៅត្រូវប្រុងប្រយ័ត្ន។", "cure": "🔔 ប្រើកណ្តឹងខ្យល់លោហៈ ៦បំពង់។"},
    3: {"status": "Dead Qi (ធ្លាក់យុគ)", "desc": "ផ្កាយជម្លោះ បណ្តឹង និងការយល់ច្រឡំ។", "cure": "🔴 ប្រើពណ៌ក្រហម ឬពន្លឺ។"},
    4: {"status": "Dead Qi (ធ្លាក់យុគ)", "desc": "ផ្កាយស្នេហាខុសក្បួន ឬបញ្ហាផ្លូវចិត្ត។", "cure": "🔥 ប្រើធាតុភ្លើង ដើម្បីដុតឈើ។"},
    5: {"status": "Killing Qi (កាចសាហាវ)", "desc": "ផ្កាយគ្រោះថ្នាក់ បង្កជំងឺ និងឧបសគ្គធំ។ ដាច់ខាតត្រូវបន្សាប។", "cure": "🪙 ប្រើកាក់ស្ពាន់ ៦ ឬកណ្តឹងខ្យល់លោហៈ (ហាមធាតុភ្លើង/ចលនា)។"},
    6: {"status": "Killing Qi (ធ្លាក់យុគ)", "desc": "ផ្កាយអំណាចដែលធ្លាក់យុគ បង្កជាបញ្ហាច្បាប់។", "cure": "💧 ប្រើទឹកស្ងៀម (Yin Water)។"},
    7: {"status": "Killing Qi (ធ្លាក់យុគ)", "desc": "ផ្កាយចោរកម្ម ការបាត់បង់លុយកាក់ និងគ្រោះថ្នាក់។", "cure": "🌊 ប្រើទឹកដើម្បីលាងសម្អាត។"},
    8: {"status": "Tui Qi (ថយយុគ)", "desc": "ផ្កាយអស់អំណាច មិនមែនជាផ្កាយនាំលុយធំទៀតទេ។ រក្សាលំនឹង តែមិនត្រូវពឹងផ្អែក។", "cure": "⛰️ ប្រើថ្ម ឬរបស់ធ្ងន់ៗដើម្បីរក្សាលំនឹង។"}
}

def get_cure_visual(m, w):
    combo = f"{m}-{w}"
    # រូបភាពកម្រិត HD ពី Icons8 ជំនួស Emoji
    img_wulou = "<img src='https://img.icons8.com/color/48/calabash.png' width='24' style='vertical-align: middle;'>"
    img_fountain = "<img src='https://img.icons8.com/color/48/fountain.png' width='24' style='vertical-align: middle;'>"
    img_mountain = "<img src='https://img.icons8.com/color/48/mountain.png' width='24' style='vertical-align: middle;'>"
    img_bamboo = "<img src='https://img.icons8.com/color/48/bamboo.png' width='24' style='vertical-align: middle;'>"
    img_pottery = "<img src='https://img.icons8.com/color/48/pottery.png' width='24' style='vertical-align: middle;'>"
    img_yin_yang = "<img src='https://img.icons8.com/color/48/yin-yang.png' width='24' style='vertical-align: middle;'>"
    img_water = "<img src='https://img.icons8.com/color/48/water.png' width='24' style='vertical-align: middle;'>"

    if m == 5 or w == 5 or m == 2 or w == 2:
        return img_wulou, "ឃ្លោកស្ពាន់/លោហៈ", "#c0392b"
    elif w == 9 or m == 9: 
        return img_fountain, "ដាស់ថាមពលយុគ៩", "#e74c3c"
    elif m == 8 and w == 8:
        return img_mountain, "រក្សាភាពស្ងៀមស្ងាត់", "#7f8c8d" 
    elif combo in ["1-6", "6-1"]:
        return img_bamboo, "លោហៈ ឬ រុក្ខជាតិ", "#2980b9"
    elif combo in ["9-7", "7-9"]:
        return img_pottery, "វត្ថុដីឥដ្ឋ/គ្រីស្តាល់", "#d35400"
    elif w in [1]:
        return img_water, "ចលនាទឹក (Water)", "#27ae60"
    else:
        return img_yin_yang, "រក្សាភាពស្ងប់ស្ងាត់", "#7f8c8d"

interpretations_p9 = {
    "9-9": "🌟 **មហាសំណាងទ្វេដងប្រចាំយុគ (Double 9):** ជាទីតាំងល្អឥតខ្ចោះបំផុតប្រចាំយុគទី៩។\n*   ✅ **វិធីជំរុញលាភ:** ដាក់អាងទឹកផុស ដើម្បីដាស់ផ្កាយលាភមុខផ្ទះ និងប្រើវត្ថុធាតុភ្លើង/ដី ដើម្បីគាំទ្រផ្កាយភ្នំ។",
    "8-8": "⚠️ **ផ្កាយថយយុគ (Double 8):** អំណាចលុយកាក់បានថយចុះ។ មិនគួរប្រើទឹកផុសធំៗដូចមុនទៀតទេ។\n*   🛡️ **វិធីកែប្រែ:** គួររក្សាលំនឹងដោយប្រើថ្ម ឬវត្ថុធ្ងន់ៗ ដើម្បីរក្សាភាពស្ងប់ស្ងាត់។",
    "5-2": "⚠️ **មហាឧបទ្រព និងជំងឺ (៥ លឿង + ២ ខ្មៅ):** ជាទីតាំងគ្រោះថ្នាក់បំផុត (ធាតុដីប៉ះដី)។\n*   🛡 **វិធីបន្សាប:** ត្រូវប្រើ 'ធាតុដែក' កម្រិតធ្ងន់ (កណ្តឹងខ្យល់ ឃ្លោកស្ពាន់)។ ហាមដាស់ថាមពល។",
    "2-5": "⚠️ **មហាឧបទ្រព និងជំងឺ (២ ខ្មៅ + ៥ លឿង):** ដូចគ្នានឹង 5-2 ដែរ។",
    "1-6": "🧠 **កំពូលបញ្ញា (១ ស + ៦ ស):** ថាមពលដ៏ប្រសើរបំផុតសម្រាប់ការសិក្សា និងការងារច្នៃប្រឌិត។",
    "6-1": "🧠 **កំពូលបញ្ញា (៦ ស + ១ ស):** ផ្តល់ផលល្អប្រសើរខ្លាំងដល់មុខតំណែង និងការសិក្សា។",
    "9-7": "🔥 **ភ្លើងរលាយដែក (៩ ស្វាយ + ៧ ក្រហម):** ងាយរងបញ្ហាពាក្យសម្តី ឬចោរកម្ម។\n*   🛡️ **វិធីបន្សាប:** ប្រើ 'ធាតុដី' (កុលាលភាជន៍ ថ្មពណ៌លឿង) ធ្វើជាស្ពាន។",
    "7-9": "🔥 **ភ្លើងរលាយដែក (៧ ក្រហម + ៩ ស្វាយ):** ដូចគ្នានឹង 9-7 ដែរ។"
}

def get_interpretation(m, w):
    combo = f"{m}-{w}"
    if combo in interpretations_p9: return interpretations_p9[combo]
    return "💡 **ថាមពលចម្រុះ:** ផ្កាយទឹក(ស្តាំ) តំណាងឲ្យលាភ ផ្កាយភ្នំ(ឆ្វេង) តំណាងឲ្យសុខភាព។ ត្រួតពិនិត្យផ្កាយនីមួយៗតាមច្បាប់យុគទី៩។"

# ==========================================
# ៣. ចំណុចប្រទាក់អ្នកប្រើប្រាស់ (UI)
# ==========================================
st.markdown("<h2 style='text-align: center; color: #d35400;'>🧭 Smart Flying Star Pro</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>គណនា ២៤ ភ្នំ និងវិភាគកម្រិតខ្ពស់តាមយុគទី៩ (Period 9)</p>", unsafe_allow_html=True)
st.divider()

col1, col2, col3 = st.columns(3)
with col1: period_input = st.number_input("🌟 យុគសាងសង់ផ្ទះ", min_value=1, max_value=9, value=8)
with col2: degree_input = st.number_input("🧭 អង្សាទិសមុខផ្ទះ", min_value=0.0, max_value=360.0, value=355.0, step=1.0)
with col3: main_door_sector = st.selectbox("🚪 ទីតាំងទ្វារធំជាក់ស្តែង", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"], index=0)

if st.button("🔮 គណនាទិសហុងស៊ុយ", use_container_width=True, type="primary"):
    final_chart, facing_name = calculate_flying_stars(period_input, degree_input)
    st.success(f"🏠 **ប្លង់ដើម: ផ្ទះយុគទី {period_input}** | បែរមុខទៅទិស **{facing_name} ({degree_input} ដឺក្រេ)**")
    
    st.markdown("### 🗺️ តារាងផ្កាយហោះ (Flying Star Chart)")
    
    order = ['SE', 'S', 'SW', 'E', 'C', 'W', 'NE', 'N', 'NW']
    
    # សរសេរកូដ HTML ជាបន្ទាត់តែមួយ (Single-line concatenation) ដើម្បីការពារកុំឲ្យ Streamlit Render ចេញជា Text ឆៅ
    grid_html = "<div style='display: grid; grid-template-columns: repeat(3, 1fr); max-width: 650px; margin: 0 auto; border: 3px solid #2c3e50; background-color: #ecf0f1; gap: 0;'>"
    
    for pos in order:
        data = final_chart[pos]
        icon, text, color = get_cure_visual(data['m'], data['w'])
        
        grid_html += f"<div style='border: 1px solid #95a5a6; position: relative; height: 130px; background-color: #ffffff; padding: 5px;'><div style='position: absolute; top: 5px; left: 8px; color: #7f8c8d; font-weight: bold; font-size: 11px;'>{NAMES_DICT[pos]}</div><div style='position: absolute; top: 25px; left: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['m']}</div><div style='position: absolute; top: 25px; right: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['w']}</div><div style='position: absolute; bottom: 35px; left: 50%; transform: translateX(-50%); color: #e74c3c; font-weight: bold; font-size: 26px;'>{data['b']}</div><div style='position: absolute; bottom: 5px; left: 0; right: 0; text-align: center; border-top: 1px dashed #ecf0f1; padding-top: 4px;'>{icon} <span style='font-size: 11px; font-weight: bold; color: {color}; margin-left: 5px;'>{text}</span></div></div>"
        
    grid_html += "</div>"
    
    # បញ្ជាឲ្យបង្ហាញតារាង
    st.markdown(grid_html, unsafe_allow_html=True)
    
    # ==========================================
    # ៤. ការវិភាគទ្វារធំឆ្លាតវៃ (Smart Main Door Analysis)
    # ==========================================
    st.markdown("---")
    st.markdown("### 🚪 ការវិភាគទ្វារធំ (The 3 Factors: Main Door)")
    
    door_facing_star = final_chart[main_door_sector]['w']
    door_interp = period_9_single_star[door_facing_star]
    
    st.write(f"ទ្វារធំរបស់បងស្ថិតនៅទិស **{NAMES_DICT[main_door_sector]}** ដែលមានផ្កាយមុខផ្ទះ (Facing Star) លេខ **{door_facing_star}**។ ផ្អែកតាមច្បាប់យុគទី៩៖")
    
    if door_facing_star == 9:
        st.success(f"**អបអរសាទរ!** ផ្កាយ **{door_facing_star}** គឺជាផ្កាយ {door_interp['status']}។ វាជាច្រកស្រូបទាញហិរញ្ញវត្ថុដ៏មានឥទ្ធិពលបំផុតប្រចាំយុគនេះ។")
    elif door_facing_star == 8:
        st.warning(f"**ចំណាំ:** ផ្កាយ **{door_facing_star}** គឺជាផ្កាយ {door_interp['status']}។ ទោះបីផ្ទះនេះសង់យុគ៨ តែបច្ចុប្បន្នផ្កាយនេះអស់អំណាចហើយ វាមិនអាចទាញយកលុយធំបានដូចមុនទេ។")
    elif door_facing_star in [1]:
        st.info(f"**ល្អប្រសើរ!** ផ្កាយ **{door_facing_star}** គឺជាផ្កាយ {door_interp['status']}។ ល្អសម្រាប់ការរកស៊ីរយៈពេលវែង។")
    else:
        st.error(f"**ប្រុងប្រយ័ត្ន!** ផ្កាយ **{door_facing_star}** គឺជាផ្កាយ {door_interp['status']}។ ត្រូវប្រយ័ត្នបញ្ហាហិរញ្ញវត្ថុ និងរៀបចំបន្សាប។")
        
    st.write(f"👉 **វិធីរៀបចំ:** {door_interp['cure']}")

    # ==========================================
    # ៥. ផ្នែកវិភាគលម្អិតតាមបន្ទប់ (Detailed Room Analysis)
    # ==========================================
    st.markdown("---")
    st.markdown("### 📊 លទ្ធផលវិភាគផ្កាយលម្អិតតាមទិស (Period 9 Cures)")
    
    for pos in order:
        data = final_chart[pos]
        meaning = get_interpretation(data['m'], data['w'])
        with st.expander(f"📍 {NAMES_DICT[pos]} [ ភ្នំ: {data['m']} | ទឹក: {data['w']} | គោល: {data['b']} ]", expanded=False):
            st.markdown(meaning)
