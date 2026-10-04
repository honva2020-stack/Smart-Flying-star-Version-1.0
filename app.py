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

# --- ២. វចនានុក្រមបកស្រាយហុងស៊ុយជាន់ខ្ពស់ (១០០% តាមក្បួនពិត) ---
interpretations = {
    "8-8": "🌟 **មហាសំណាងទ្វេដង (Double 8):** ជាទីតាំងល្អឥតខ្ចោះបំផុត នាំមកនូវទ្រព្យសម្បត្តិហូរហៀរ និងសុខភាពមាំមួន។\n*   ✅ **វិធីជំរុញលាភ:** ដាក់អាងទឹកផុស (ចលនាទឹក) ដើម្បីដាស់ផ្កាយលាភលុយកាក់ និងដាក់ថ្មគ្រីស្តាល់ ឬវត្ថុធ្វើពីដីឥដ្ឋ ដើម្បីពង្រឹងផ្កាយភ្នំការពារសុខភាព។ រៀបចំកន្លែងនេះឲ្យមានពន្លឺភ្លឺល្អ និងមានចលនា។",
    
    "5-2": "⚠️ **មហាឧបទ្រព និងជំងឺ (៥ លឿង + ២ ខ្មៅ):** ជាទីតាំងគ្រោះថ្នាក់បំផុត (ធាតុដីប៉ះដី) នាំមកនូវគ្រោះថ្នាក់ ជំងឺតម្កាត់ និងការបាត់បង់ប្រាក់កាសធ្ងន់ធ្ងរ។\n*   ❌ **បម្រាម:** ហាមវាយជញ្ជាំង ជួសជុល ជីកដី ឬមានចលនារំខានដាច់ខាត។ ហាមប្រើពណ៌ក្រហម (ភ្លើង) និងវត្ថុធាតុដី។\n*   🛡️ **វិធីបន្សាប:** ត្រូវប្រើ 'ធាតុដែក' កម្រិតធ្ងន់ដើម្បីស្រូបទាញកម្លាំងដីចេញ។ ព្យួរកណ្តឹងខ្យល់ធ្វើពីលោហៈ ៦ បំពង់ (6-rod metal wind chime), ដាក់ឃ្លោកស្ពាន់, កាក់ស្ពាន់ ៦ ស៊ីន, ឬដាក់ដុំដែកទម្ងន់ធ្ងន់ពណ៌ស/ប្រផេះ។",
    "2-5": "⚠️ **មហាឧបទ្រព និងជំងឺ (២ ខ្មៅ + ៥ លឿង):** ដូចគ្នានឹង 5-2 ដែរ ទីនេះសម្បូរថាមពលអវិជ្ជមានខាងសុខភាព និងគ្រោះថ្នាក់។\n*   🛡️ **វិធីបន្សាប:** អនុវត្តដូច 5-2 ដោយតម្រូវឲ្យប្រើធាតុដែក (កណ្តឹងខ្យល់ស្ពាន់ ឃ្លោកស្ពាន់) ជាចាំបាច់ដើម្បីបន្សាបធាតុដីដ៏កាចសាហាវនេះ។",
    
    "1-6": "🧠 **កំពូលបញ្ញា និងភាពជោគជ័យ (១ ស + ៦ ស):** ធាតុដែក(៦) បង្កើតទឹក(១) ជាថាមពលដ៏ប្រសើរបំផុតសម្រាប់ការសិក្សា ការងារច្នៃប្រឌិត និងការកាត់តវីដេអូ។\n*   ✅ **វិធីជំរុញលាភ:** ស័ក្តិសមបំផុតសម្រាប់រៀបចំជា 'តុធ្វើការ'។ អាចដាក់វត្ថុធ្វើពីលោហៈ (ពណ៌មាស ពណ៌ប្រាក់) ឬដាក់ទឹកស្ងៀម (យិន) ដើម្បីជំរុញភាពវៃឆ្លាត និងការគិតបានលឿន។",
    "6-1": "🧠 **កំពូលបញ្ញា និងភាពជោគជ័យ (៦ ស + ១ ស):** ដូចគ្នានឹង 1-6 ផ្តល់ផលល្អប្រសើរខ្លាំងដល់មុខតំណែង ការងារ និងការសិក្សា។\n*   ✅ **វិធីជំរុញលាភ:** រៀបចំតុធ្វើការនៅទីនេះ ប្រើប្រាស់សម្ភារៈការិយាល័យធ្វើពីលោហៈ ឬរបស់មានរាងមូលពណ៌ស/ប្រផេះ ដើម្បីពង្រឹងថាមពលគិត។",
    
    "9-7": "🔥 **ភ្លើងរលាយដែក (៩ ស្វាយ + ៧ ក្រហម):** ផ្កាយ ៩ ជាលាភអនាគត តែជួបផ្កាយ ៧ គឺធាតុភ្លើងដុតដែក។ ងាយរងបញ្ហាពាក្យសម្តី ជម្លោះ ឬរងគ្រោះដោយសារភ្លើង និងចោរកម្ម។\n*   🛡️ **វិធីបន្សាប:** ត្រូវប្រើ 'ធាតុដី' ដើម្បីធ្វើជាស្ពាន (ភ្លើងបង្កើតដី ដីបង្កើតដែក)។ ដាក់វត្ថុធ្វើពីដីឥដ្ឋ កុលាលភាជន៍ ថ្មគ្រីស្តាល់ពណ៌លឿង ឬកម្រាលព្រំរាងការ៉េ។ ហាមប្រើពណ៌ក្រហមនៅទីនេះ។",
    "7-9": "🔥 **ភ្លើងរលាយដែក (៧ ក្រហម + ៩ ស្វាយ):** ដូចគ្នានឹង 9-7 ងាយមានជម្លោះប្រកែកប្រជែង និងបញ្ហាសុខភាពទាក់ទងនឹងប្រព័ន្ធដកដង្ហើម។\n*   🛡️ **វិធីបន្សាប:** ប្រើធាតុដី (ក្អមដី ថ្មពណ៌លឿង/ត្នោត) ដើម្បីផ្សះផ្សាការប៉ះទង្គិចរវាងភ្លើងនិងដែក។",
    
    "3-4": "🌸 **មនោសញ្ចេតនា និងភាពរកាំរកូស (៣ បៃតង + ៤ បៃតង):** ធាតុឈើជួបឈើ។ អាចនាំមកនូវមនោសញ្ចេតនាល្អ តែបើមានកម្លាំងរំខាន វានឹងប្រែជាជម្លោះ និងរឿងអាស្រូវស្នេហា។\n*   🛡️ **វិធីបន្សាប:** ប្រើ 'ធាតុភ្លើងកម្រិតស្រាល' (ឧទាហរណ៍៖ ចង្កៀងពណ៌ក្រហម ព្រំពណ៌ក្រហម ឬខ្នើយក្រហម) ដើម្បីដុតបញ្ចេញថាមពលឈើដែលលើសលុប និងបន្សាបភាពកាចរបស់ផ្កាយ៣។",
    "4-3": "🌸 **មនោសញ្ចេតនា និងភាពរកាំរកូស (៤ បៃតង + ៣ បៃតង):** ដូចគ្នានឹង 3-4 ត្រូវការការគ្រប់គ្រងអារម្មណ៍ និងការអត់ធ្មត់។\n*   🛡️ **វិធីបន្សាប:** ប្រើពន្លឺភ្លើងពណ៌កក់ក្តៅ (Warm light) ឬវត្ថុពណ៌ក្រហមតិចតួច ដើម្បីបន្ថយកម្លាំងឈើ។",

    "1-4": "📚 **ជោគជ័យការសិក្សា និងស្នេហា (១ ស + ៤ បៃតង):** កំពូលទីតាំងសិល្បៈ អក្សរសាស្ត្រ និងការស្រាវជ្រាវ (ទឹកស្រោចស្រពឈើ)។\n*   ✅ **វិធីជំរុញលាភ:** ដាក់ដើមឬស្សីសំណាង ៤ ដើម ក្នុងថូទឹក ជួយឲ្យខួរក្បាលភ្លឺស្វាង និងមានសំណាងខាងទំនាក់ទំនងស្នេហា។",
    "4-1": "📚 **ជោគជ័យការសិក្សា និងស្នេហា (៤ បៃតង + ១ ស):** ដូចគ្នានឹង 1-4 ល្អសម្រាប់ការសិក្សា។\n*   ✅ **វិធីជំរុញលាភ:** រៀបចំតុរៀន ឬដាក់ជក់សរសេរអក្សរចិន ៤ ដើម ព្យួរនៅទីនេះ។",

    "8-6": "💰 **លាភអចលនទ្រព្យ និងអំណាច (៨ ស + ៦ ស):** ដីបង្កើតដែក ល្អខ្លាំងសម្រាប់ការវិនិយោគ និងមុខតំណែង។\n*   ✅ **វិធីជំរុញលាភ:** ប្រើវត្ថុធាតុដី (គ្រីស្តាល់) ឬលោហៈ ដើម្បីរក្សាថាមពលនេះឲ្យសកម្ម។",
    "6-8": "💰 **លាភអចលនទ្រព្យ និងអំណាច (៦ ស + ៨ ស):** ដូចគ្នានឹង 8-6។\n*   ✅ **វិធីជំរុញលាភ:** ដាក់តុធ្វើការទីនេះ ឬទូដែកផ្ទុកឯកសារសំខាន់ៗ។"
}

def get_interpretation(m, w):
    """អនុគមន៍ស្វែងរកការបកស្រាយ បើគ្មានក្នុងបញ្ជី ទាញយកអត្ថន័យស្តង់ដារ"""
    combo = f"{m}-{w}"
    if combo in interpretations:
        return interpretations[combo]
    # ករណីទូទៅដែលមិនមានក្នុងបញ្ជីខាងលើ
    return "💡 **ថាមពលចម្រុះ:** ទីតាំងនេះទាមទារការសង្កេតលើទម្រង់ (Form) ផ្ទះជាក់ស្តែង។ ជាទូទៅ ផ្កាយទឹក(លេខខាងស្តាំ) តំណាងឲ្យលាភសក្ការៈ ឯផ្កាយភ្នំ(លេខខាងឆ្វេង) តំណាងឲ្យសុខភាព។ គួររក្សាទីតាំងឲ្យមានរបៀបរៀបរយ។"

def render_box(pos, chart_data, name=""):
    data = chart_data[pos]
    title = name if pos != 'C' else 'កណ្តាល (C)'
    html = f"""
    <div style="border: 2px solid #2c3e50; padding: 10px; text-align: center; height: 110px; background-color: #f8f9fa; border-radius: 5px;">
        <div style="font-size: 12px; color: #7f8c8d; font-weight: bold; margin-bottom: 5px;">{title}</div>
        <div style="display: flex; justify-content: space-between; font-size: 20px; font-weight: bold; color: #c0392b; padding: 0 10px;">
            <span>{data['m']}</span><span>{data['w']}</span>
        </div>
        <div style="font-size: 28px; font-weight: bold; margin-top: 5px; color: #2980b9;">{data['b']}</div>
    </div>
    """
    return html

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
    
    # គូរតារាង
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(render_box('SE', final_chart, 'ត្បូងកើត (SE)'), unsafe_allow_html=True)
    with c2: st.markdown(render_box('S', final_chart, 'ត្បូង (S)'), unsafe_allow_html=True)
    with c3: st.markdown(render_box('SW', final_chart, 'ត្បូងលិច (SW)'), unsafe_allow_html=True)
    
    c4, c5, c6 = st.columns(3)
    with c4: st.markdown(render_box('E', final_chart, 'កើត (E)'), unsafe_allow_html=True)
    with c5: st.markdown(render_box('C', final_chart), unsafe_allow_html=True)
    with c6: st.markdown(render_box('W', final_chart, 'លិច (W)'), unsafe_allow_html=True)
    
    c7, c8, c9 = st.columns(3)
    with c7: st.markdown(render_box('NE', final_chart, 'ជើងកើត (NE)'), unsafe_allow_html=True)
    with c8: st.markdown(render_box('N', final_chart, 'ជើង (N)'), unsafe_allow_html=True)
    with c9: st.markdown(render_box('NW', final_chart, 'ជើងលិច (NW)'), unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📊 លទ្ធផលវិភាគផ្កាយ និងវិធីបន្សាប")
    
    mapping = [
        ('SE', 'ត្បូងកើត (SE)'), ('S', 'ត្បូង (S)'), ('SW', 'ត្បូងលិច (SW)'),
        ('E', 'កើត (E)'), ('C', 'កណ្តាល (C)'), ('W', 'លិច (W)'),
        ('NE', 'ជើងកើត (NE)'), ('N', 'ជើង (N)'), ('NW', 'ជើងលិច (NW)')
    ]
    
    # បង្ហាញការវិភាគលម្អិតសម្រាប់គ្រប់ប្រអប់
    for pos, name in mapping:
        data = final_chart[pos]
        meaning = get_interpretation(data['m'], data['w'])
        with st.expander(f"📍 {name} [ ភ្នំ: {data['m']} | ទឹក: {data['w']} | គោល: {data['b']} ]", expanded=False):
            st.markdown(meaning)
