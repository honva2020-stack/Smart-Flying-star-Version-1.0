import streamlit as st

st.set_page_config(page_title="Smart Flying Star", page_icon="🧭", layout="centered")

# --- ១. ក្បួនតក្កវិជ្ជាគណនាហុងស៊ុយ (Feng Shui Calculation Engine) ---
SECTORS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
SECTOR_NAMES = ['ជើង (N)', 'ជើងកើត (NE)', 'កើត (E)', 'ត្បូងកើត (SE)', 'ត្បូង (S)', 'ត្បូងលិច (SW)', 'លិច (W)', 'ជើងលិច (NW)']
GUAS = [1, 8, 3, 4, 9, 2, 7, 6] # លេខកូដ គ័រ ប្រចាំទិស
PATH = ['C', 'NW', 'W', 'NE', 'S', 'N', 'SW', 'E', 'SE'] # គន្លងហោះ Luo Shu

# កំណត់ យិន(-) ឬ យ៉ាង(+) សម្រាប់ភ្នំទាំង៣ នៃគ័រនីមួយៗ (24 Mountains Polarity)
POLARITY = {
    1: [1, -1, -1],  2: [-1, 1, 1],
    3: [1, -1, -1],  4: [-1, 1, 1],
    6: [-1, 1, 1],   7: [1, -1, -1],
    8: [-1, 1, 1],   9: [1, -1, -1]
}

def fly_stars(star, direction):
    """អនុគមន៍សម្រាប់ហោះផ្កាយតាមគន្លង Luo Shu"""
    chart = {}
    curr = star
    for pos in PATH:
        chart[pos] = curr
        curr += direction
        if curr > 9: curr = 1
        if curr < 1: curr = 9
    return chart

def calculate_flying_stars(period, degree):
    # កំណត់ទិស Facing និង Sitting ផ្អែកលើអង្សា
    norm_deg = (degree + 22.5) % 360
    facing_idx = int(norm_deg // 45)
    sub_m_idx = int((norm_deg % 45) // 15) # ភ្នំទី 1, 2, ឬ 3
    sitting_idx = (facing_idx + 4) % 8
    
    # គណនាផ្កាយគោល (Base Chart)
    base_chart = fly_stars(period, 1)
    
    # គណនាផ្កាយភ្នំ (Mountain Chart - Sitting)
    m_star = base_chart[SECTORS[sitting_idx]]
    m_gua = GUAS[sitting_idx] if m_star == 5 else m_star # ច្បាប់ពិសេសសម្រាប់ផ្កាយ 5
    m_dir = POLARITY[m_gua][sub_m_idx]
    m_chart = fly_stars(m_star, m_dir)
    
    # គណនាផ្កាយទឹក (Water Chart - Facing)
    w_star = base_chart[SECTORS[facing_idx]]
    w_gua = GUAS[facing_idx] if w_star == 5 else w_star
    w_dir = POLARITY[w_gua][sub_m_idx]
    w_chart = fly_stars(w_star, w_dir)
    
    # ចងក្រងលទ្ធផលប្រចាំទិស
    final_chart = {}
    for pos in PATH:
        final_chart[pos] = {
            'm': m_chart[pos],
            'w': w_chart[pos],
            'b': base_chart[pos]
        }
    return final_chart, SECTOR_NAMES[facing_idx]

# --- ២. ការបកស្រាយអត្ថន័យ ---
interpretations = {
    "8-8": "🌟 **Double 8 (រាជាលាភ):** ទីតាំងល្អឥតខ្ចោះសម្រាប់ការទាញយកទ្រព្យ និងសុខភាព។ ត្រូវការទឹក (ឡាបូ/ទ្វារ) និងជញ្ជាំងដើម្បីដាស់ថាមពល។",
    "1-6": "🧠 **បញ្ញា និង ជោគជ័យ (ទឹក-ដែក):** កំពូលថាមពលសម្រាប់ការសិក្សា កាត់ត និងការងារច្នៃប្រឌិត។ ស័ក្តិសមបំផុតសម្រាប់តុធ្វើការ។",
    "6-1": "🧠 **បញ្ញា និង ជោគជ័យ (ដែក-ទឹក):** ស័ក្តិសមសម្រាប់តុធ្វើការ ជួយដល់ការគិត និងភាពវៃឆ្លាត។",
    "9-7": "🔥 **ភ្លើង និង ដែក (ប្រទាញប្រទង់):** ផ្កាយ ៩ ជាលាភថ្មី តែប៉ះ ៧ បង្កជាបញ្ហាពាក្យសម្តី ឬភ្លើង។ គួរប្រើធាតុដី (វត្ថុដីឥដ្ឋ) ដើម្បីបន្សាប។",
    "7-9": "🔥 **ភ្លើង និង ដែក (ប្រទាញប្រទង់):** ប្រយ័ត្នបញ្ហាជម្លោះ និងសុខភាព។",
    "5-2": "⚠️ **ផ្កាយជំងឺ និង ឧបទ្រព (ដី-ដី):** ទាមទារការបន្សាបជាដាច់ខាត។ ត្រូវប្រើធាតុដែក (ឃ្លោកស្ពាន់ ពណ៌ស ប្រផេះ) ហាមដាស់ថាមពលនៅទីនេះ។",
    "2-5": "⚠️ **ផ្កាយជំងឺ និង ឧបទ្រព (ដី-ដី):** អត្ថន័យដូចគ្នានឹង 5-2 ត្រូវការធាតុដែកដើម្បីបន្សាប។",
    "3-4": "🌸 **ផ្កាយមនោសញ្ចេតនា (ឈើ-ឈើ):** ជួយរឿងស្នេហា តែបើមានទម្រង់ខាងក្រៅអាក្រក់ (ទឹកកខ្វក់) វានឹងនាំរឿងអាស្រូវ។",
    "4-3": "🌸 **ផ្កាយមនោសញ្ចេតនា (ឈើ-ឈើ):** អត្ថន័យដូចគ្នានឹង 3-4។"
}

def render_box(pos, chart_data, name=""):
    """គូរប្រអប់តារាង 3x3"""
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
st.markdown("<h2 style='text-align: center; color: #d35400;'>🧭 Smart Flying Star</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>គណនាស្វ័យប្រវត្តិ ១០០% តាមក្បួន ២៤ ភ្នំ និងអង្សាជាក់ស្តែង</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)
with col1: period_input = st.number_input("🌟 បញ្ចូលលេខយុគ", min_value=1, max_value=9, value=8)
with col2: degree_input = st.number_input("🧭 អង្សាទិសមុខផ្ទះ", min_value=0.0, max_value=360.0, value=180.0, step=1.0)

if st.button("🔮 គណនាទិសហុងស៊ុយ", use_container_width=True, type="primary"):
    final_chart, facing_name = calculate_flying_stars(period_input, degree_input)
    st.success(f"🏠 **ផ្ទះយុគទី {period_input}** | បែរមុខទៅទិស **{facing_name} ({degree_input} ដឺក្រេ)**")
    
    # បង្ហាញតារាង 3x3 ឲ្យដូចសៀវភៅ
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
    st.markdown("### 📊 លទ្ធផលវិភាគផ្កាយតាមទីតាំង")
    
    mapping = [
        ('SE', 'ត្បូងកើត (SE)'), ('S', 'ត្បូង (S)'), ('SW', 'ត្បូងលិច (SW)'),
        ('E', 'កើត (E)'), ('W', 'លិច (W)'),
        ('NE', 'ជើងកើត (NE)'), ('N', 'ជើង (N)'), ('NW', 'ជើងលិច (NW)')
    ]
    
    for pos, name in mapping:
        data = final_chart[pos]
        combo = f"{data['m']}-{data['w']}"
        meaning = interpretations.get(combo) or "🔮 ថាមពលចម្រុះ ទាមទារការរៀបចំទម្រង់ ភ្នំ/ទឹក ជាក់ស្តែង។"
        with st.expander(f"📍 {name} [ ភ្នំ: {data['m']} | ទឹក: {data['w']} | គោល: {data['b']} ]"):
            st.markdown(meaning)
