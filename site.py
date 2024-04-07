import streamlit as st

import pandas as pd

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

import queue

from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score, confusion_matrix

st.image('https://www.ayalon-ins.co.il/files/Zarmon/Banner_1920_644/Pic1/71375_general_banners_1920x644_1783.jpg')

st.markdown("""

<style>

body {

    font-family: 'Arial', sans-serif;

    background-color: #e6ecf0; 

}

.reportview-container .main .block-container {

    background: #e6ecf0; 

}

.stMarkdown {

    text-align: right;

}





.stTextInput label, .stSelectbox label, .stMultiSelect label, .stSlider label {

    text-align: right;

}





h1 {

    color: #1E0E62; 

    text-align: center; 

}



.stTextInput > div > div > input, 

.stSelectbox > div > div > select, 

.stMultiSelect > div > div > select {

    direction: rtl; 

    width: 100%;

    height: 3rem;

    line-height: 3rem;

    text-align: right; 

    padding-right: 1rem;

    border: 2px solid #1E0E62;

    border-radius: 5px;

}





.stTextInput > div > div > input:focus, 

.stSelectbox > div > div > select:focus, 

.stMultiSelect > div > div > select:focus {

    outline: none;

    border: 2px solid #1E0E62;

    box-shadow: none;

    text-align: right

    direction: rtl 

}





button {

    margin: 0;

    line-height: 2.5rem;

    border-radius: 5px;

    direction: rtl; 

    background-color: #4CAF50

}

    </style>

    """,

    unsafe_allow_html=True

)

def get_data(path, user_deal_braker, user_preferences, min_price, max_price, min_room, max_room):

  data= pd.read_csv(path)

  if user_deal_braker[1]:

    data = data[data['שכונה'].isin(user_preferences[0])]

  if user_deal_braker[2]:

    data = data[data['מספר חדרים'].astype(int).between(int(min_room), int(max_room))]

  if user_deal_braker[3]:

    data = data[data['מחיר (ש"ח)'].astype(int).between(int(min_price), int(max_price))]

  fillterd_data = data.copy(deep=True)

  return fillterd_data



def home_page():

  st.title('מיד נמצא את דירת חלומותייך')

  st.write('רק עוד כמה פרטים קטנים וממשיכים')

  min_room_num_input = ""

  max_room_num_input = ""

  min_price_input = ""

  max_price_input = ""

  checkbox_value = False

  city_options = ['תל אביב', 'חיפה', 'ירושלים']  

  selected_city = st.multiselect('בחר עיר:', city_options)

  area_options = []

  for city in selected_city:

    if city == 'תל אביב':

      area_options += ['בבלי','הדר יוסף','פלורנטין']

    if city == 'חיפה':

      area_options += ['בת גלים','דניה','נווה שאנן']

    if city == 'ירושלים':

      area_options += ['תלפיות','רמות','רחביה']

  selected_area = st.multiselect('בחר שכונה:', area_options)

  col1, col2 = st.columns(2)

  with col2:

    min_room_num_input = st.text_input("מספר חדרים מינימלי", min_room_num_input)

  with col1:

    max_room_num_input = st.text_input("מספר חדרים מקסימלי", max_room_num_input)

  if min_room_num_input!= "" and max_room_num_input!= "" and int(min_room_num_input)>int(max_room_num_input) :

    st.write('מספר החדרים המינימלי לא יכול להיות גדול ממספר החדרים המקסימלי')

  col1, col2 = st.columns(2)

  with col2:

    min_price_input = st.text_input("מחיר מינימלי", min_price_input)

  with col1:

    max_price_input = st.text_input("מחיר מקסימלי", max_price_input)

  if  min_price_input!="" and max_price_input!="" and int(min_price_input)>int(max_price_input):

    st.write('המחיר המינימלי לא יכול להיות גדול מהמחיר המקסימלי')

  st.write('איזה מאפיינים תרצה שיהיו בדירה?')

  col1, col2, col3, col4 = st.columns(4)

  with col4:

    balcony = st.checkbox("מרפסת", checkbox_value)

    protected_Space = st.checkbox("ממד", checkbox_value)

    storage = st.checkbox("מחסן", checkbox_value)

  with col3:

    elevators = st.checkbox("מעלית", checkbox_value)

    accessible = st.checkbox("נגיש לנכים", checkbox_value) 

    air_conditioner = st.checkbox("מזגן", checkbox_value)

  with col2:

    boiler = st.checkbox("בית פרטי", checkbox_value)

    pets = st.checkbox("האם מותר בעלי חיים", checkbox_value)

    parking = st.checkbox("חנייה", checkbox_value)

  with col1:

    sea_view = st.checkbox("נוף לים", checkbox_value)

    renovated = st.checkbox("משופצת", checkbox_value)

    bars = st.checkbox("סורגים", checkbox_value)

  if min_room_num_input == "" or max_room_num_input == "":

    selected_room = ""

  else:

    selected_room = 1

  if min_price_input == "" or max_price_input=="":

    selected_price = ""

  else:

    selected_price = 1

  user_preferences = [selected_area, selected_room, selected_price, balcony, protected_Space, storage, elevators, accessible, air_conditioner, boiler, pets, parking, sea_view, renovated, bars]

  if st.button("המשך"):

    st.write()

  return user_preferences, min_price_input, max_price_input, min_room_num_input, max_room_num_input



def page_2():

    st.title('מיד נמצא את דירת חלומותייך')

    st.write('רק עוד כמה פרטים קטנים וממשיכים')

    st.write('לכל אחד מהפרטים הבאים סמן האם הוא דיל ברייקר  מבחינתך, אם תסמן זאת המערכת לא תציג  לך דירות שלא עומדות בדרישה.')

    st.write('אם לא תסמן זאת, עליך לבחור מידת חשיבות לפריט מ-1 עד 10, כאשר 1 מסמן שהוא לא חשוב לך כלל ו 10 מסמן שהוא חשוב לך מאוד')

    st.write('אם תבחר באפשרות זו המערכת תשדל להתחשב בהעדפותייך אך גם עשויה להציע לך דירות שלא עומדות בתנאי')

    st.write()

    st.write('עיר:')

    city_deal_braker = False

    city_importance = 0

    city_deal_braker = st.checkbox("city - deal-braker:", city_deal_braker)

    if city_deal_braker==False:

      city_importance = int(st.slider('בחר מידת חשיבות עיר:', min_value=1, max_value=10, value=1))

    st.write()

    st.write('שכונה')

    area_deal_braker = False

    area_importance = 0

    area_deal_braker = st.checkbox("area - deal-braker:", area_deal_braker)

    if area_deal_braker==False:

      area_importance = int(st.slider('בחר מידת חשיבות שכונה:', min_value=1, max_value=10, value=1))

    else:

      city_deal_braker = True

    st.write()

    st.write('מספר חדרים')

    room_num_deal_braker = False

    room_num_importance = 0

    room_num_deal_braker = st.checkbox("number of rooms - deal-braker:", room_num_deal_braker)

    if room_num_deal_braker==False:

      room_num_importance = int(st.slider('בחר מידת חשיבות מספר חדרים:', min_value=1, max_value=10, value=1))

    st.write()

    st.write('מחיר')

    price_deal_braker = False

    price_importance = 0

    price_deal_braker = st.checkbox("price - deal-braker:", price_deal_braker)

    if price_deal_braker==False:

      price_importance = int(st.slider('בחר מידת חשיבות מחיר:', min_value=1, max_value=10, value=1))

    st.write()

    user_deal_braker = [city_deal_braker, area_deal_braker, room_num_deal_braker, price_deal_braker]

    user_importance = [city_importance, area_importance, room_num_importance, price_importance]

    if st.button(" המשך "):

      st.write()

    return user_deal_braker, user_importance



def page_3(preferences):

  st.title('מיד נמצא את דירת חלומותייך')

  st.write('רק עוד כמה פרטים קטנים וממשיכים')

  st.write('לכל אחד מהפריטים הבאים עליך לבחור מידת חשיבות לפריט מ- 1 עד 10 כאשר 1 מסמן שהוא כלל לא חשוב לך ו- 10 מסמן שהוא חשוב לך מאוד')

  features = ['מרפסת', 'ממ"ד', 'מחסן', 'מעלית', 'גישה לנכים', 'מזגן','בית פרטי', 'מותר לבעלי חיים', 'חניה', 'נוף לים', 'משופצת', 'סורגים']

  importance = []

  for i in range(0,12):

    if preferences[i]:

      importance += [st.slider(f'בחר מידת חשיבות {features[i]}:', min_value=1, max_value=10, value=1)]

    else:

      importance += [0]

  if st.button(" המשך"):

    st.write()

  return importance



def  page_4():

  st.title('מחפש את דירת חלומותייך')

  st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgKN-BTrNkrQ7sA8wDCaA_RUXN2COtlVfo3Pb43t2arg&s')



def apartments_embedding(apartment_details, user_importance):

  res = []

  for i in range(0,len(apartment_details)):

    for j in range(0,user_importance[i]):

      res += [apartment_details[i]]

  return res



def scale(x):

  return (x+1)/2



def calc_sim(apartment, user_preferences, user_importance):

  a1 = np.array(apartments_embedding(apartment, user_importance))

  a2 = np.array(apartments_embedding(user_preferences, user_importance))

  similarity = cosine_similarity([a1], [a2])

  return similarity[0][0]



def show_apartment(data, id, pq, tagged_data, x, y, sim_dict):

  if tagged_data<5:

    st.write('על סמך ההעדפות שהזנת ומידות החשיבות, הנה דירה שאולי תאהב')

    current_apartment = data[data['id'] == id]

    for index, row in current_apartment.iterrows():

        st.title(f" {row['עיר']}, {row['שכונה']}, {row['מספר חדרים']} חדרים")

        image = row['קישור לתמונה']

        st.image(image, use_column_width=True)

        col1, col2, col3 = st.columns(3)

        with col3:

          st.write('מחיר:')

          st.write(row['מחיר (ש"ח)'])

        with col2:

          st.write('קומה:')

          st.write(row['קומה'])

        with col1:

          st.write('גודל')

          st.write(row['גודל (מ"ר)'])

        features = [int(row['קומה']), int(row['גודל (מ"ר)'])]

        features += [int(row['מספר חדרים'])==2, int(row['מספר חדרים'])==3, int(row['מספר חדרים'])==4,int(row['מספר חדרים'])==5]

        prices = [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2800, 3000, 3200, 3500]

        for p in prices:

          features += [int(row['מחיר (ש"ח)'])==p]

        details = ['מרפסת', 'ממ"ד', 'מחסן', 'מעלית', 'גישה לנכים', 'מזגן', 'בית פרטי', 'מותר לבעלי חיים', 'חניה', 'נוף לים', 'משופצת', 'סורגים']

        for item in details:

          features += [int(row[item])]

        x += [features]

        if st.button('פרטים נוספים', key=f'more_{tagged_data}'):

          check_box_val = []

          for item in details:

            check_box_val += [row[item] == 1]

          col1, col2, col3, col4 = st.columns(4)

          cols = [col4, col3, col2, col1]

          for i in range(0, len(check_box_val), 3):

            with cols[int(i/3)]:

              st.checkbox(f"{details[i]}", key=f'fixed_checkbox_{i}', value=check_box_val[i])

              st.checkbox(f"{details[i+1]}", key=f'fixed_checkbox_{i+1}', value=check_box_val[i+1])

              st.checkbox(f"{details[i+2]}", key=f'fixed_checkbox_{i+2}', value=check_box_val[i+2])

          if st.button('הסתר', key=f'hide_{tagged_data}'):

            st.write()

    options = ['אהבתי', 'לא אהבתי']

    options_with_empty = [''] + options

    selected_option = st.selectbox('בחר אפשרות אחת:', options_with_empty, key = f"like_{tagged_data}")

    if selected_option=='אהבתי':

      y += [1]

    if selected_option=='לא אהבתי':

      y += [0]

    if selected_option=='אהבתי' or selected_option=='לא אהבתי':

      if tagged_data<4:

        priority, new_id = pq.get()

      else:

        new_id = id

      show_apartment(data[data['id'] != id], new_id, pq, tagged_data+1, x, y, sim_dict)

  else:

    X_train = np.array(x)

    y_train = np.array(y)

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)

    model = LogisticRegression()

    model.fit(X_train, y_train)

    reg_scores = {}

    for index, row in data.iterrows():

      features = [int(row['קומה']), int(row['גודל (מ"ר)'])]

      features += [int(row['מספר חדרים'])==2, int(row['מספר חדרים'])==3, int(row['מספר חדרים'])==4,int(row['מספר חדרים'])==5]

      prices = [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2800, 3000, 3200, 3500]

      for p in prices:

        features += [int(row['מחיר (ש"ח)'])==p]

      details = ['מרפסת', 'ממ"ד', 'מחסן', 'מעלית', 'גישה לנכים', 'מזגן','בית פרטי', 'מותר לבעלי חיים', 'חניה', 'נוף לים', 'משופצת', 'סורגים']

      for item in details:

        features += [int(row[item])]

      X_test = np.array([features])

      X_test_scaled = scaler.transform(X_test)

      y_pred = model.predict_proba(X_test_scaled)

      reg_scores[row['id']] = y_pred[0][1]

    scores = {}

    a = 5/(2*tagged_data)

    for key, value in reg_scores.items():

      scores[key] = (1-a)*value + a*scale(sim_dict[key])

    ids = []

    while not pq.empty():

      priority, id = pq.get()

      ids += [id]

    sum_sim = 0

    sum_reg = 0

    for id in ids:

      sum_sim += scale(sim_dict[id])

      sum_reg += reg_scores[id]

      pq.put((scores[id]*(-1), id))

    priority, id = pq.get()

    current_apartment = data[data['id'] == id]

    if scale(sim_dict[id])/sum_sim>reg_scores[id]/sum_reg:

      st.write('על סמך ההעדפות שהזנת ומידות החשיבות, הנה דירה שאולי תאהב')

    else:

      st.write('על סמך הדירות שאהבת, אולי תאהב גם את הדירה הבאה')

    for index, row in current_apartment.iterrows():

        st.title(f" {row['עיר']}, {row['שכונה']}, {row['מספר חדרים']} חדרים")

        image = row['קישור לתמונה']

        st.image(image, use_column_width=True)

        col1, col2, col3 = st.columns(3)

        with col3:

          st.write('מחיר:')

          st.write(row['מחיר (ש"ח)'])

        with col2:

          st.write('קומה:')

          st.write(row['קומה'])

        with col1:

          st.write('גודל')

          st.write(row['גודל (מ"ר)'])


        features = [int(row['קומה']), int(row['גודל (מ"ר)'])]

        features += [int(row['מספר חדרים'])==2, int(row['מספר חדרים'])==3, int(row['מספר חדרים'])==4,int(row['מספר חדרים'])==5]

        prices = [1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2800, 3000, 3200, 3500]

        for p in prices:

          features += [int(row['מחיר (ש"ח)'])==p]

        details = ['מרפסת', 'ממ"ד', 'מחסן', 'מעלית', 'גישה לנכים', 'מזגן','בית פרטי', 'מותר לבעלי חיים', 'חניה', 'נוף לים', 'משופצת', 'סורגים']

        for item in details:

          features += [int(row[item])]

        x += [features]

        if st.button('פרטים נוספים', key=f'more_{tagged_data}'):

          check_box_val = []

          for item in details:

            check_box_val += [row[item] == 1]

          col1, col2, col3, col4 = st.columns(4)

          cols = [col4, col3, col2, col1]

          for i in range(0, len(check_box_val), 3):

            with cols[int(i/3)]:

              st.checkbox(f"{details[i]}", key=f'fixed_checkbox_{i}', value=check_box_val[i])

              st.checkbox(f"{details[i+1]}", key=f'fixed_checkbox_{i+1}', value=check_box_val[i+1])

              st.checkbox(f"{details[i+2]}", key=f'fixed_checkbox_{i+2}', value=check_box_val[i+2])

          if st.button('הסתר', key=f'hide_{tagged_data}'):

            st.write()

    options = ['אהבתי', 'לא אהבתי']

    options_with_empty = [''] + options

    selected_option = st.selectbox('בחר אפשרות אחת:', options_with_empty, key = f"like_{tagged_data}")

    if selected_option=='אהבתי':

      y += [1]

    if selected_option=='לא אהבתי':

      y += [0]

    if selected_option=='אהבתי' or selected_option=='לא אהבתי':

      if tagged_data<4:

        priority, new_id = pq.get()

      else:

        new_id = id

      show_apartment(data[data['id'] != id], new_id, pq, tagged_data+1, x, y, sim_dict)

    





path = 'apartments.csv'

user_preferences, min_price, max_price, min_room, max_room = home_page()

user_deal_braker, user_importance = page_2()

user_importance += page_3(user_preferences[3:])

user_deal_braker[0] = True

user_deal_braker[1] = True

data = get_data(path, user_deal_braker, user_preferences, min_price, max_price, min_room, max_room)

page_4()

sim_dict = {}

details = ['מספר חדרים', 'מחיר (ש"ח)', 'מרפסת', 'ממ"ד', 'מחסן', 'מעלית', 'גישה לנכים', 'מזגן','בית פרטי', 'מותר לבעלי חיים', 'חניה', 'נוף לים', 'משופצת', 'סורגים']

for index, row in data.iterrows():

  row_details = []

  for item in details:

    if item == 'מחיר (ש"ח)':

      row_details += [int(row[item])>=int(min_price) and int(row[item])<=int(max_price)]

    elif item == 'מספר חדרים':

      row_details += [int(row[item])>=int(min_room) and int(row[item])<=int(max_room)]

    else:

      row_details += [row[item]]

  sim_dict[row['id']] = calc_sim(row_details, user_preferences[1:], user_importance[2:])

pq = queue.PriorityQueue()

for key, value in sim_dict.items():

  pq.put((value*(-1), key))

priority, id = pq.get()

tagged_data = 0

x = []

y = []

show_apartment(data, id, pq, tagged_data, x, y, sim_dict)