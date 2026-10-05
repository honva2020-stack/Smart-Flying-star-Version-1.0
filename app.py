import streamlit as st
from datetime import datetime

# ==========================================
# 1. ទិន្នន័យបកស្រាយហុងស៊ុយយុគទី៩ (Period 9: 2024 - 2043)
# ==========================================
# គ្រប់ការបកស្រាយទាំងអស់ត្រូវតែផ្អែកលើច្បាប់យុគទី៩ ទោះបីជាផ្ទះសង់ក្នុងយុគណាក៏ដោយ
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

# ==========================================
# 2. មុខងារគណនាប្លង់ដើម (Mockup Core Calculation)
# ==========================================
# កន្លែងនេះបងនឹងត្រូវភ្ជាប់រូបមន្ត 24 Mountains ពិតប្រាកដរបស់បង
def generate_chart(period, facing_dir):
    # ទិន្នន័យឧទាហរណ៍ (Mock Data) សម្រាប់ផ្ទះយុគ៨ បែរមុខទៅជើង
    # ទម្រង់: (Base, Sitting, Facing)
    return {
        "SE": (7, 3, 4), "S": (3, 8, 8), "SW": (5, 1, 6),
        "E": (6, 4, 3),  "Center": (8, 4, 8), "W": (1, 6, 1),
        "NE": (2, 5, 2), "N": (4, 9, 7), "NW": (9, 7, 9)
    }

# ==========================================
# 3. ការរៀបចំ UI និង Logic របស់កម្មវិធី
# ==========================================
st.set_page_config(page_title="Smart Flying Star Pro", layout="wide")

st.title("ត្រីវិស័យហុងស៊ុយផ្កាយហោះកម្រិតខ្ពស់ 🧭")
st.markdown("### ការវិភាគយុគទី៩ (Period 9: 2024-2043) ផ្អែកលើទម្រង់ខាងក្រៅ")

# Input Section
col1, col2, col3 = st.columns(3)
with col1:
    house_period = st.selectbox("យុគសាងសង់ផ្ទះ (Natal Period):", [7, 8, 9], index=1)
with col2:
    facing_direction = st.selectbox("ទិសបែរមុខ (Facing Direction):", ["N1", "N2/3", "S1", "S2/3", "E1", "E2/3"])
with col3:
    main_door_sector = st.selectbox("ទីតាំងទ្វារធំ (Main Door Sector):", ["N", "NE", "E", "SE", "S", "SW", "W", "NW"])

chart_data = generate_chart(house_period, facing_direction)

# Render Chart
st.markdown("---")
st.subheader("តារាងផ្កាយហោះ (Flying Star Chart)")

# CSS Grid សម្រាប់ការបង្ហាញដ៏ប្រណិត
grid_html = f"""
<style>
    .grid-container {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        background-color: #2c3e50;
        padding: 10px;
        border-radius: 10px;
        max-width: 600px;
        margin: 0 auto;
    }}
    .grid-item {{
        background-color: #ecf0f1;
        padding: 20px;
        text-align: center;
        border-radius: 5px;
        position: relative;
        height: 120px;
    }}
    .sector {{ font-weight: bold; color: #7f8c8d; position: absolute; top: 5px; left: 5px; }}
    .base {{ font-size: 24px; color: #34495e; position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); }}
    .sitting {{ font-size: 20px; font-weight: bold; color: #2980b9; position: absolute; top: 10px; left: 20px; }}
    .facing {{ font-size: 20px; font-weight: bold; color: #c0392b; position: absolute; top: 10px; right: 20px; }}
</style>
<div class="grid-container">
    <!-- Row 1 -->
    <div class="grid-item"><span class="sector">SE</span><span class="sitting">{chart_data['SE'][1]}</span><span class="facing">{chart_data['SE'][2]}</span><span class="base">{chart_data['SE'][0]}</span></div>
    <div class="grid-item"><span class="sector">S</span><span class="sitting">{chart_data['S'][1]}</span><span class="facing">{chart_data['S'][2]}</span><span class="base">{chart_data['S'][0]}</span></div>
    <div class="grid-item"><span class="sector">SW</span><span class="sitting">{chart_data['SW'][1]}</span><span class="facing">{chart_data['SW'][2]}</span><span class="base">{chart_data['SW'][0]}</span></div>
    <!-- Row 2 -->
    <div class="grid-item"><span class="sector">E</span><span class="sitting">{chart_data['E'][1]}</span><span class="facing">{chart_data['E'][2]}</span><span class="base">{chart_data['E'][0]}</span></div>
    <div class="grid-item"><span class="sector">Center</span><span class="sitting">{chart_data['Center'][1]}</span><span class="facing">{chart_data['Center'][2]}</span><span class="base">{chart_data['Center'][0]}</span></div>
    <div class="grid-item"><span class="sector">W</span><span class="sitting">{chart_data['W'][1]}</span><span class="facing">{chart_data['W'][2]}</span><span class="base">{chart_data['W'][0]}</span></div>
    <!-- Row 3 -->
    <div class="grid-item"><span class="sector">NE</span><span class="sitting">{chart_data['NE'][1]}</span><span class="facing">{chart_data['NE'][2]}</span><span class="base">{chart_data['NE'][0]}</span></div>
    <div class="grid-item"><span class="sector">N</span><span class="sitting">{chart_data['N'][1]}</span><span class="facing">{chart_data['N'][2]}</span><span class="base">{chart_data['N'][0]}</span></div>
    <div class="grid-item"><span class="sector">NW</span><span class="sitting">{chart_data['NW'][1]}</span><span class="facing">{chart_data['NW'][2]}</span><span class="base">{chart_data['NW'][0]}</span></div>
</div>
"""
st.markdown(grid_html, unsafe_allow_html=True)

# ==========================================
# 4. ការវិភាគទ្វារធំ (The Main Door Interpretation)
# ==========================================
st.markdown("---")
st.subheader("🚪 ការវិភាគទ្វារធំ (The 3 Factors Analysis)")

# ទាញយកលេខផ្កាយមុខផ្ទះ (Facing Star) នៅទីតាំងទ្វារធំ
door_facing_star = chart_data[main_door_sector][2]
interpretation = period_9_interpretation[door_facing_star]

# បង្ហាញលទ្ធផលវិភាគដោយផ្អែកលើក្បួនយុគ ៩
if door_facing_star == 9:
    st.success(f"**អបអរសាទរ!** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")
elif door_facing_star in [1]:
    st.info(f"**ល្អប្រសើរ!** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")
elif door_facing_star == 8:
    st.warning(f"**ចំណាំ:** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")
    st.write("ទោះបីជាផ្ទះនេះសង់ក្នុងយុគទី៨ ក៏ដោយ តែបច្ចុប្បន្នផ្កាយ៨ បានអស់អំណាចហើយ។ វាមិនអាចទាញយកថាមពលលុយកាក់ធំៗបានដូចមុនទេ។")
else:
    st.error(f"**ប្រុងប្រយ័ត្ន!** ទ្វារធំរបស់អ្នកស្ថិតនៅទីតាំងផ្កាយមុខផ្ទះលេខ **{door_facing_star}** ({interpretation['status']})")

st.markdown(f"**អត្ថន័យយុគទី៩:** {interpretation['desc']}")
st.markdown(f"**វិធីកែប្រែ/ដាស់ថាមពល (Cure/Enhancer):** {interpretation['cure']}")

# លក្ខខណ្ឌក្បួន Form (ទម្រង់រូបរាងខាងក្រៅ)
st.markdown("#### ការវិភាគទម្រង់ខាងក្រៅ (External Forms Factor)")
st.write(f"ដោយសារទីតាំងនេះជាទ្វារធំ (ចលនា/Yang) ថាមពលនៃផ្កាយលេខ **{door_facing_star}** ត្រូវបាន **ដាស់ (Activated)** ជាស្រេច។ ប្រសិនបើមានផ្លូវបំបែក ឬទឹកផុសនៅមុខទ្វារនេះទៀត ឥទ្ធិពលរបស់វានឹងកាន់តែខ្លាំង។")
