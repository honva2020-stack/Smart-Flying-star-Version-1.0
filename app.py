import streamlit as st

st.set_page_config(page_title="Smart Flying Star", page_icon="🧭", layout="centered")

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

# --- ២. ប្រព័ន្ធទាញយករូបភាពវត្ថុហុងស៊ុយ (Cures & Enhancers) ---
def get_cure_visual(m, w):
    """វិភាគផ្កាយទាំង២ ដើម្បីផ្តល់រូបតំណាង និងអត្ថបទខ្លីសម្រាប់ដាក់ក្នុងតារាង"""
    combo = f"{m}-{w}"
    
    # បើមានផ្កាយអាក្រក់ 5 ឬ 2 ត្រូវបន្សាបដោយលោហៈមុនគេ
    if m == 5 or w == 5 or m == 2 or w == 2:
        return "🧉", "ឃ្លោកស្ពាន់/លោហៈ", "#c0392b" # ពណ៌ក្រហមចាស់ (ព្រមាន)
    # លាភធំ 8-8
    elif m == 8 and w == 8:
        return "⛲", "ទឹកផុស & គ្រីស្តាល់", "#27ae60" # ពណ៌បៃតង (លាភ)
    # ការសិក្សា/ការងារ
    elif combo in ["1-6", "6-1"]:
        return "🪴", "លោហៈ ឬ រុក្ខជាតិ", "#2980b9" # ពណ៌ខៀវ
    # ជម្លោះ ភ្លើងនិងដែក
    elif combo in ["9-7", "7-9"]:
        return "🪨", "វត្ថុដីឥដ្ឋ/គ្រីស្តាល់", "#d35400" # ពណ៌ទឹកក្រូច
    # បើមានផ្កាយទឹកល្អ (8, 9, 1) ជំរុញដោយទឹក
    elif w in [8, 9, 1]:
        return "⛲", "ចលនាទឹក (Water)", "#27ae60"
    # បើមានផ្កាយភ្នំល្អ (8, 9, 1) ជំរុញដោយភ្នំ
    elif m in [8, 9, 1]:
        return "🪨", "វត្ថុថ្ម/ភ្នំ (Mountain)", "#27ae60"
    else:
        return "☯️", "រក្សាភាពស្ងប់ស្ងាត់", "#7f8c8d" # ពណ៌ប្រផេះ

# វចនានុក្រមបកស្រាយលម្អិត (សម្រាប់ផ្នែកខាងក្រោម)
interpretations = {
    "8-8": "🌟 **មហាសំណាងទ្វេដង (Double 8):** ជាទីតាំងល្អឥតខ្ចោះបំផុត នាំមកនូវទ្រព្យសម្បត្តិហូរហៀរ និងសុខភាពមាំមួន។\n*   ✅ **វិធីជំរុញលាភ:** ដាក់អាងទឹកផុស (ចលនាទឹក) ដើម្បីដាស់ផ្កាយលាភលុយកាក់ និងដាក់ថ្មគ្រីស្តាល់ ឬវត្ថុធ្វើពីដីឥដ្ឋ ដើម្បីពង្រឹងផ្កាយភ្នំការពារសុខភាព។",
    "5-2": "⚠️ **មហាឧបទ្រព និងជំងឺ (៥ លឿង + ២ ខ្មៅ):** ជាទីតាំងគ្រោះថ្នាក់បំផុត (ធាតុដីប៉ះដី) នាំមកនូវគ្រោះថ្នាក់ ជំងឺតម្កាត់។\n*   🛡️ **វិធីបន្សាប:** ត្រូវប្រើ 'ធាតុដែក' កម្រិតធ្ងន់ដើម្បីស្រូបទាញកម្លាំងដីចេញ។ ព្យួរកណ្តឹងខ្យល់ធ្វើពីលោហៈ ៦ បំពង់ ឬដាក់ឃ្លោកស្ពាន់។ ហាមដាស់ថាមពលនៅទីនេះ។",
    "2-5": "⚠️ **មហាឧបទ្រព និងជំងឺ (២ ខ្មៅ + ៥ លឿង):** ដូចគ្នានឹង 5-2 ដែរ ទីនេះសម្បូរថាមពលអវិជ្ជមានខាងសុខភាព និងគ្រោះថ្នាក់។\n*   🛡️ **វិធីបន្សាប:** តម្រូវឲ្យប្រើធាតុដែក (កណ្តឹងខ្យល់ស្ពាន់ ឃ្លោកស្ពាន់) ជាចាំបាច់។",
    "1-6": "🧠 **កំពូលបញ្ញា និងភាពជោគជ័យ (១ ស + ៦ ស):** ធាតុដែក(៦) បង្កើតទឹក(១) ជាថាមពលដ៏ប្រសើរបំផុតសម្រាប់ការសិក្សា ការងារច្នៃប្រឌិត និងការកាត់តវីដេអូ។\n*   ✅ **វិធីជំរុញលាភ:** ស័ក្តិសមបំផុតសម្រាប់រៀបចំជា 'តុធ្វើការ'។",
    "6-1": "🧠 **កំពូលបញ្ញា និងភាពជោគជ័យ (៦ ស + ១ ស):** ដូចគ្នានឹង 1-6 ផ្តល់ផលល្អប្រសើរខ្លាំងដល់មុខតំណែង និងការសិក្សា។",
    "9-7": "🔥 **ភ្លើងរលាយដែក (៩ ស្វាយ + ៧ ក្រហម):** ងាយរងបញ្ហាពាក្យសម្តី ជម្លោះ ឬរងគ្រោះដោយសារភ្លើង និងចោរកម្ម។\n*   🛡️ **វិធីបន្សាប:** ត្រូវប្រើ 'ធាតុដី' ដើម្បីធ្វើជាស្ពាន។ ដាក់វត្ថុធ្វើពីដីឥដ្ឋ កុលាលភាជន៍ ថ្មគ្រីស្តាល់ពណ៌លឿង។",
    "7-9": "🔥 **ភ្លើងរលាយដែក (៧ ក្រហម + ៩ ស្វាយ):** ដូចគ្នានឹង 9-7 ងាយមានជម្លោះប្រកែកប្រជែង។ គួរប្រើធាតុដីដើម្បីបន្សាប។"
}

def get_interpretation(m, w):
    combo = f"{m}-{w}"
    if combo in interpretations: return interpretations[combo]
    return "💡 **ថាមពលចម្រុះ:** ជាទូទៅ ផ្កាយទឹក(ស្តាំ) តំណាងឲ្យលាភសក្ការៈ ឯផ្កាយភ្នំ(ឆ្វេង) តំណាងឲ្យសុខភាព។ រៀបចំទីតាំងឲ្យមានរបៀបរៀបរយ និងពន្លឺគ្រប់គ្រាន់។"

# --- ៣. ចំណុចប្រទាក់អ្នកប្រើប្រាស់ (UI) ---
st.markdown("<h2 style='text-align: center; color: #d35400;'>🧭 Smart Flying Star Pro</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>គណនា និងបកស្រាយក្បួន ២៤ ភ្នំ លម្អិត ១០០%</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
with col1: period_input = st.number_input("🌟 បញ្ចូលលេខយុគ", min_value=1, max_value=9, value=8)
with col2: degree_input = st.number_input("🧭 អង្សាទិសមុខផ្ទះ", min_value=0.0, max_value=360.0, value=355.0, step=1.0)

if st.button("🔮 គណនាទិសហុងស៊ុយ", use_container_width=True, type="primary"):
    final_chart, facing_name = calculate_flying_stars(period_input, degree_input)
    st.success(f"🏠 **ផ្ទះយុគទី {period_input}** | បែរមុខទៅទិស **{facing_name} ({degree_input} ដឺក្រេ)**")
    
    # គូរតារាង Grid ជាប់គ្នា (Seamless Grid) ដូចស្តង់ដារហុងស៊ុយពិត
    grid_html = """
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); max-width: 100%; border: 3px solid #2c3e50; background-color: #ecf0f1; border-radius: 8px; overflow: hidden; margin-bottom: 30px;">
    """
    
    # លំដាប់នៃការបង្ហាញប្រអប់ (ត្បូងនៅខាងលើ ជើងនៅខាងក្រោម)
    order = ['SE', 'S', 'SW', 'E', 'C', 'W', 'NE', 'N', 'NW']
    names = {'SE': 'ត្បូងកើត (SE)', 'S': 'ត្បូង (S)', 'SW': 'ត្បូងលិច (SW)', 'E': 'កើត (E)', 'C': 'កណ្តាល (C)', 'W': 'លិច (W)', 'NE': 'ជើងកើត (NE)', 'N': 'ជើង (N)', 'NW': 'ជើងលិច (NW)'}
    
    for pos in order:
        data = final_chart[pos]
        icon, text, color = get_cure_visual(data['m'], data['w'])
        
        # កូដ HTML សម្រាប់ប្រអប់នីមួយៗ (មានស៊ុមខណ្ឌចែកគ្នា)
        grid_html += f"""
        <div style="border: 1px solid #bdc3c7; padding: 8px; text-align: center; background-color: #ffffff; display: flex; flex-direction: column; justify-content: space-between; height: 160px;">
            <div style="font-size: 11px; color: #7f8c8d; font-weight: bold;">{names[pos]}</div>
            
            <div style="display: flex; justify-content: space-between; padding: 0 10px; margin-top: 5px;">
                <span style="font-size: 22px; font-weight: bold; color: #000000;">{data['m']}</span>
                <span style="font-size: 22px; font-weight: bold; color: #000000;">{data['w']}</span>
            </div>
            
            <div style="font-size: 26px; font-weight: bold; color: #e74c3c;">{data['b']}</div>
            
            <div style="margin-top: auto; padding-top: 5px; border-top: 1px dashed #ecf0f1;">
                <div style="font-size: 20px;">{icon}</div>
                <div style="font-size: 10px; font-weight: bold; color: {color};">{text}</div>
            </div>
        </div>
        """
        
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)
    
    st.markdown("### 📊 លទ្ធផលវិភាគផ្កាយ និងវិធីបន្សាប")
    
    for pos in order:
        data = final_chart[pos]
        meaning = get_interpretation(data['m'], data['w'])
        # ប្តូរ expanded=True ដើម្បីឲ្យវាលោតបើកអត្ថបទពន្យល់ស្រាប់តែម្តង
        with st.expander(f"📍 {names[pos]} [ ភ្នំ: {data['m']} | ទឹក: {data['w']} | គោល: {data['b']} ]", expanded=True):
            st.markdown(meaning)
