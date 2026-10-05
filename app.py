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
# ២. ប្រព័ន្ធទិន្នន័យបកស្រាយ និង គំនូរ SVG (Inline Graphics)
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
    
    # SVG Graphics HD
    svg_wulou = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><circle cx='50' cy='35' r='20' fill='#F5B041'/><circle cx='50' cy='70' r='28' fill='#F5B041'/><path d='M 45 15 C 45 5, 55 5, 55 15' stroke='#E67E22' stroke-width='4' fill='none'/></svg>"
    svg_water = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><path d='M50 10 C 20 40, 20 70, 50 90 C 80 70, 80 40, 50 10' fill='#3498DB'/><path d='M50 30 C 35 50, 35 70, 50 85 C 65 70, 65 50, 50 30' fill='#85C1E9'/></svg>"
    svg_mountain = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><polygon points='10,90 50,20 90,90' fill='#7F8C8D'/><polygon points='40,90 70,40 100,90' fill='#BDC3C7'/></svg>"
    svg_bamboo = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><rect x='35' y='10' width='12' height='80' rx='3' fill='#2ECC71'/><rect x='55' y='20' width='12' height='70' rx='3' fill='#27AE60'/><line x1='32' y1='35' x2='49' y2='35' stroke='#229954' stroke-width='3'/><line x1='32' y1='65' x2='49' y2='65' stroke='#229954' stroke-width='3'/><line x1='52' y1='50' x2='69' y2='50' stroke='#1E8449' stroke-width='3'/></svg>"
    svg_pottery = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><path d='M 30 30 C 0 60, 20 90, 50 90 C 80 90, 100 60, 70 30 Z' fill='#D35400'/><rect x='40' y='10' width='20' height='20' fill='#E67E22'/><ellipse cx='50' cy='10' rx='10' ry='5' fill='#BA4A00'/></svg>"
    svg_yinyang = "<svg width='28' height='28' viewBox='0 0 100 100' style='vertical-align: middle;'><circle cx='50' cy='50' r='45' fill='#FFF' stroke='#2C3E50' stroke-width='3'/><path d='M 50 5 A 45 45 0 0 0 50 95 A 22.5 22.5 0 0 0 50 50 A 22.5 22.5 0 0 1 50 5' fill='#2C3E50'/><circle cx='50' cy='27.5' r='6' fill='#FFF'/><circle cx='50' cy='72.5' r='6' fill='#2C3E50'/></svg>"

    # តក្កវិជ្ជាកម្រិតអាតូម (Atomic Logic) សម្រាប់ Period 9 ដែលបានកែតម្រូវ
    # ជំហានទី 1: សុវត្ថិភាពជាចម្បង (Safety First) - បន្សាបផ្កាយ ៥ និង ២
    if m == 5 or w == 5 or m == 2 or w == 2:
        return svg_wulou, "ឃ្លោកស្ពាន់/លោហៈ", "#c0392b"
        
    # ជំហានទី 2: គូផ្កាយពិសេស (Special Combos)
    elif combo in ["9-7", "7-9"]:
        return svg_pottery, "វត្ថុដីឥដ្ឋ/គ្រីស្តាល់", "#d35400"
    elif combo in ["1-6", "6-1"]:
        return svg_bamboo, "លោហៈ ឬ រុក្ខជាតិ", "#2980b9"
        
    # ជំហានទី 3: ដាស់ផ្កាយមហាសំណាងយុគ ៩ (Wang Qi) ឲ្យត្រូវក្បួន
    elif w == 9 and m == 9:
        return svg_water, "ទឹកផុស (ទាញលាភយុគ៩)", "#e74c3c"
    elif w == 9: # ផ្កាយទឹក ៩ (ទាញលុយ)
        return svg_water, "ចលនាទឹក (Water)", "#e74c3c"
    elif m == 9: # ផ្កាយភ្នំ ៩ (ការពារសុខភាព) - ហាមប្រើទឹក!
        return svg_mountain, "វត្ថុថ្ម/ភ្នំ (Mountain)", "#e74c3c"
        
    # ជំហានទី 4: ដាស់ផ្កាយអនាគតយុគ ៩ (Sheng Qi #1)
    elif w == 1:
        return svg_water, "ចលនាទឹក (Water)", "#27ae60"
    elif m == 1:
        return svg_mountain, "វត្ថុថ្ម/ភ្នំ (Mountain)", "#27ae60"
        
    # ជំហានទី 5: ផ្កាយថយយុគ ៨ (Retreating Qi)
    elif m == 8 and w == 8:
        return svg_mountain, "រក្សាភាពស្ងៀមស្ងាត់", "#7f8c8d" 
        
    # ជំហានទី 6: ទូទៅ
    else:
        return svg_yinyang, "រក្សាភាពស្ងប់ស្ងាត់", "#7f8c8d"

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
    
    grid_html = "<div style='display: grid; grid-template-columns: repeat(3, 1fr); max-width: 650px; margin: 0 auto; border: 3px solid #2c3e50; background-color: #bdc3c7; gap: 1px;'>"
    
    for pos in order:
        data = final_chart[pos]
        icon, text, color = get_cure_visual(data['m'], data['w'])
        
        grid_html += f"<div style='position: relative; height: 130px; background-color: #fcfcfc; padding: 5px;'><div style='position: absolute; top: 5px; left: 8px; color: #7f8c8d; font-weight: bold; font-size: 11px;'>{NAMES_DICT[pos]}</div><div style='position: absolute; top: 25px; left: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['m']}</div><div style='position: absolute; top: 25px; right: 15px; color: #000000; font-weight: bold; font-size: 22px;'>{data['w']}</div><div style='position: absolute; bottom: 35px; left: 50%; transform: translateX(-50%); color: #e74c3c; font-weight: bold; font-size: 26px;'>{data['b']}</div><div style='position: absolute; bottom: 5px; left: 0; right: 0; text-align: center; border-top: 1px dashed #ecf0f1; padding-top: 4px;'>{icon} <span style='font-size: 11px; font-weight: bold; color: {color}; margin-left: 5px;'>{text}</span></div></div>"
        
    grid_html += "</div>"
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
