import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import rc
import streamlit as st
from sympy import Integral, Symbol, pi, exp, sqrt

font_path = 'NanumGothic.ttf'
plt.rcParams['font.family'] = 'NanumGothic'


def calculate_carbon_footprint(platform, minutes):
    # 소셜 미디어별 탄소 배출량 (g CO2 / 분)
    carbon_emissions = {
        "Youtube": 0.46,
        "Twitter": 0.6,
        "Facebook": 0.79,
        "Instagram": 1.05,
        "Pinterest": 1.3,
        "Tiktok": 2.63
    }

    if platform in carbon_emissions:
        return carbon_emissions[platform] * minutes / 1000
    else:
        return None

def main(day):
    total_carbon_footprint = 0

    if 'platforms_' + str(day) not in st.session_state:
        st.session_state['platforms_' + str(day)] = []
    if 'times_' + str(day) not in st.session_state:
        st.session_state['times_' + str(day)] = []

    platform = st.selectbox("사용한 소셜 미디어 플랫폼을 입력하세요.", ['Youtube', 'Twitter', 'Facebook', 'Instagram', 'Pinterest', 'Tiktok'], key = 'social_platform_' + str(day))
    minutes = st.number_input(platform + "를 사용한 시간을 분 단위로 입력하세요.", min_value = 0, step = 1, key = 'social_time_' + str(day))
    if st.button('추가', key = 'social_button_' + str(day)):
        st.session_state['platforms_' + str(day)].append(platform)
        st.session_state['times_' + str(day)].append(minutes)
        st.success(platform + '이(가) 추가되었습니다.')
    
    st.write('현재 입력 목록')

    for platform, minutes in zip(st.session_state['platforms_' + str(day)], st.session_state['times_' + str(day)]):
        st.write(platform, ":", minutes, "분")


    for platform, minutes in zip(st.session_state['platforms_' + str(day)], st.session_state['times_' + str(day)]):
        carbon_footprint = calculate_carbon_footprint(platform, minutes)
        if carbon_footprint is not None:
            st.write(f"{minutes}분 동안 {platform}를 사용했을 때의 탄소 배출량은 {carbon_footprint:.2f}kg CO2 입니다.")
            total_carbon_footprint += carbon_footprint
        else:
            st.write(f"유효하지 않은 소셜 미디어 플랫폼: {platform}")
    
    st.write('--------------------')
    st.write(f"소셜 미디어 탄소 배출량: {total_carbon_footprint:.2f} kg CO2")

    return total_carbon_footprint

def reward(emission, daily_goal):
    
    if emission <= daily_goal*0.2:
        return 10
    elif emission <= daily_goal*0.5:
        return 5
    elif emission <= daily_goal*0.7:
        return 3
    elif emission <= daily_goal*0.9:
        return 1
    else:
        return 0


st.title("🌱탄소발자국 계산기👣")

day = st.number_input("탄소배출량 계산 기간(숫자만 입력)", min_value = 1, step = 1)
mode = day
goal = st.number_input("탄소배출량 목표", min_value = 10.0, step = 10.0)

total_emission = 0
total_points = 0

total_transport_emission = 0
total_electricity_emission = 0
total_gas_emission = 0
total_water_emission = 0
total_trash_emission = 0
total_social_media_emission = 0

daily_goal = goal/mode

goal_20_achieve = False
goal_50_achieve = False
goal_70_achieve = False
goal_90_achieve = False
goal_100_achieve = False

st.subheader("🎯 Daily 목표: ")
st.write(round(daily_goal, 2))
st.write("---")

days = []
emissions = []
pred_history = []

if mode < 20:
    start_day = mode // 2

else:
    start_day = 10

for i in range (1, mode+1, 1):
    with st.expander('📆 <DAY ' + str(i) + ' 입력>'):
        daily_emission = 0

        carbon_calculate = st.multiselect('탄소발자국 계산기', ['교통수단', '전기', '가스', '수도', '폐기물', '소셜 미디어'], key = 'carbon_' + str(i))
        
        if '교통수단' in carbon_calculate:
            trans = st.multiselect('승용차, 버스, 지하철 중 선택', ['승용차', '버스', '지하철'], key = 'trans_' + str(i))
            if '승용차' in trans:
                fuel = st.multiselect('휘발유/경유/LPG 중 선택', ['휘발유', '경유', 'LPG'], key = 'fuel_' + str(i))
                if '휘발유' in fuel:
                    gasoline = st.number_input('이동거리(휘발유):', min_value = 0.0, step = 1.0, key = 'gasoline_' + str(i))
                    gasoline = gasoline / 16.04 * 2.097
                    total_transport_emission += gasoline
                    daily_emission += gasoline
                if '경유' in fuel:
                    diesel = st.number_input('이동거리(경유):', min_value = 0.0, step = 1.0, key = 'diesel_' + str(i))
                    diesel = diesel / 15.35 * 2.582
                    total_transport_emission += diesel
                    daily_emission += diesel
                if 'LPG' in fuel:
                    lpg = st.number_input('이동거리(LPG):', min_value = 0.0, step = 1.0, key = 'lpg_' + str(i))
                    lpg = lpg / 11.06 * 1.868
                    total_transport_emission += lpg
                    daily_emission += lpg
            
            if '버스' in trans:
                    bus = st.number_input('버스 이동거리(km)):', min_value = 0.0, step = 1.0, key = 'bus_' + str(i))
                    bus = bus * 0.0277
                    total_transport_emission += bus
                    daily_emission += bus
            
            if '지하철' in trans:
                    subway = st.number_input('지하철 이동거리(km):', min_value = 0.0, step = 1.0, key = 'subway_' + str(i))
                    subway = subway * 0.0015
                    total_transport_emission += subway
                    daily_emission += subway

        if '전기' in carbon_calculate:
            elec = st.number_input('전기 사용량(kwh):', min_value = 0.0, step = 1.0, key = 'elec_' + str(i))
            elec *= 0.4781
            total_electricity_emission += elec
            daily_emission += elec

        if '가스' in carbon_calculate:
            gas = st.number_input('가스 사용량(m³):', min_value = 0.0, step = 1.0, key = 'gas_' + str(i))
            gas *= 2.176
            total_gas_emission += gas
            daily_emission += gas

        if '수도' in carbon_calculate:
            water = st.number_input('수도 사용량(m³):', min_value = 0.0, step = 1.0, key = 'water_' + str(i))
            water *= 0.237
            total_water_emission += water
            daily_emission += water

        if '폐기물' in carbon_calculate:
            trash = st.number_input('폐기물(kg):', min_value = 0.0, step = 1.0, key = 'trash_' + str(i))
            trash *= 0.5573
            total_trash_emission += trash
            daily_emission += trash

        if '소셜 미디어' in carbon_calculate:
            social = main(i)
            total_social_media_emission += social
            daily_emission += social


        days.append(i)
        emissions.append(daily_emission)

        category_emissions = {
            "교통수단": total_transport_emission,
            "전기": total_electricity_emission,
            "가스": total_gas_emission,
            "수도": total_water_emission,
            "폐기물": total_trash_emission,
            "소셜 미디어": total_social_media_emission
        }

        most_used_category = max(category_emissions, key=category_emissions.get)
        most_emission = category_emissions[most_used_category]

        total_emission = total_transport_emission + total_electricity_emission + total_gas_emission + total_water_emission + total_trash_emission + total_social_media_emission

        points = reward(daily_emission, daily_goal)
        total_points += points

        achieve = total_emission / goal * 100
    # ---추가---
        st.progress(min(achieve / 100, 1.0))

        st.write("오늘의 탄소배출량: ", round(daily_emission, 2), "kg CO2")
        st.write('현재 목표량의 ', round(achieve, 2), '%')

        if points > 0:
            st.write('오늘의 포인트는 ', points, '점!')
        else:
            st.write('아쉽네요, 내일은 탄소 배출량을 줄여봅시다!')
        st.write('현재까지의 누적 포인트: ', total_points, '점')

        goal_20 = goal*0.2
        goal_50 = goal*0.5
        goal_70 = goal*0.7
        goal_90 = goal*0.9

        if total_emission >= goal and not goal_100_achieve:
            st.error('💣이런...목표량 초과!!!!')
            goal_100_achieve = True
        elif total_emission >= goal_90 and not goal_90_achieve and not goal_100_achieve:
            st.warning('🚨#주의# 목표량의 90% 달성!!')
            goal_90_achieve = True
        elif total_emission >= goal_70 and not goal_70_achieve and not goal_90_achieve and not goal_100_achieve:
            st.warning('⚠️ 목표량의 70% 초과!!')
            goal_70_achieve = True
        elif total_emission >= goal_50 and not goal_50_achieve and not goal_70_achieve and not goal_90_achieve and not goal_100_achieve:
            st.info('>>목표량의 절반 달성!')
            goal_50_achieve = True
        elif total_emission >= goal_20 and not goal_20_achieve and not goal_50_achieve and not goal_70_achieve and not goal_90_achieve and not goal_100_achieve:
            st.info('>>목표량의 20% 넘었어요!')
            goal_20_achieve = True
        

        if i >= start_day:
            X = np.array(days).reshape(-1, 1)
            y = np.array(emissions)

            model = LinearRegression()
            model.fit(X, y)

            if i < mode:
                next_day = i + 1
                pred = model.predict([[next_day]])

                final_pred = pred[0]

                if final_pred < 0:
                    final_pred = 0.0
                st.write("📊내일 (DAY ", next_day, ") 예상 탄소배출량: ", round(final_pred, 2), "kg CO2")
                pred_history.append((next_day, final_pred))

        else:
            if i < mode:
                st.write("📊내일 예상 탄소배출량: 데이터 축적 중입니다 (DAY ", start_day, "부터 제공)")

st.write('---')

if total_emission > goal:
    st.subheader('<결과>')
    st.write('목표: ',goal)
    st.write("총 탄소 배출량은 ",round(total_emission, 2),"kg CO2 입니다.")
    st.error('--> ❌ 목표 달성 실패')
    st.write("가장 많이 사용한 분야는 ",most_used_category,"입니다.")
    with st.expander('💡 가장 많이 사용한 분야의 절약 TIP'):
        if most_emission == total_transport_emission:
            st.write('가까운 거리는 도보나 자전거로!')
            st.write('불필요한 짐은 트렁크에서 빼기!')
            st.write('타이어 공기압 체크하기!')
            st.write('실시간 내비게이션 -> 더 빠른 길로 go!')

        if most_emission == total_electricity_emission:
            st.write('전기 사용량 줄이기!')
            st.write('가전제품 플러그 뽑기!')
            st.write('실내 온도 여름에는 26℃ 이상, 겨울에는 20℃ 이하로 유지하기!')
            st.write('에어컨 대신 선풍기 사용하기!')
            st.write('세탁물은 모아서~')

        if most_emission == total_gas_emission:
            st.write('가스 사용량 줄이기!')
            st.write('보일러 사용 줄이고 얇은 옷 여러겹 입기!')
            st.write('자동 가스 잠금 밸브 설치하기!')
            st.write('겨울 난방 온도는 20℃로 유지하고 단열 아이템 사용하기~')

        if most_emission == total_water_emission:
            st.write('수도 사용량 줄이기!')
            st.write('절수기 설치하기!')
            st.write('양치할 때 양치컵 사용하기!')
            st.write('설거지할 때 물 받아서 사용하기!')
            st.write('샤워는 짧게~')

        if most_emission == total_trash_emission:
            st.write('일회용품 사용 줄이기!')
            st.write('분리수거 제대로 하기!')
            st.write('친환경 제품 구매하기!')
            st.write('음식은 먹을만큼만 만들기~')

        if most_emission == total_social_media_emission:
            st.write('소셜 미디어 사용 줄이기!')
            st.write('핸드폰 대신 가족들과 대화하기!')
            st.write('소셜 미디어 사용시간 정하기!')

else:
    st.subheader('<결과>')
    st.write('목표:',goal)
    st.write("총 탄소 배출량은", round(total_emission, 2),"kg CO2 입니다.")
    st.write('--> 🎉 목표 달성 성공!')

st.write('총 누적 포인트는 ',total_points,'점입니다!')

if total_points == day*10:
    st.success('탄소 감축 마스터! 훌륭해요!')

elif total_points >= day*5:
    st.success('정말 잘하고 있어요!')

elif total_points >= day*3:
    st.info('조금 더 열심히 해봅시다!')

elif total_points >= day*1:
    st.warning('더 노력해봐요!')

elif total_points == 0:
    st.error('심각하네요, 바로 내일부터 탄소배출량을 줄여봅시다.')

valid_labels = []
valid_values = []
valid_colors = []

if total_transport_emission > 0:
  valid_labels.append('교통수단')
  valid_values.append(total_transport_emission)
  valid_colors.append('green')

if total_electricity_emission > 0:
  valid_labels.append('전기')
  valid_values.append(total_electricity_emission)
  valid_colors.append('yellow')

if total_gas_emission > 0:
  valid_labels.append('가스')
  valid_values.append(total_gas_emission)
  valid_colors.append('darkturquoise')

if total_water_emission > 0:
  valid_labels.append('수도')
  valid_values.append(total_water_emission)
  valid_colors.append('royalblue')

if total_trash_emission > 0:
  valid_labels.append('폐기물')
  valid_values.append(total_trash_emission)
  valid_colors.append('darkorchid')

if total_social_media_emission > 0:
  valid_labels.append('소셜 미디어')
  valid_values.append(total_social_media_emission)
  valid_colors.append('orangered')

if len(valid_values) > 0:
  st.subheader('<카테고리별 탄소 배출량>')
  plt.figure(figsize = (7, 7))
  plt.pie(valid_values, labels = valid_labels, autopct = '%1.1f%%', colors = valid_colors, startangle = 140)
  plt.title('카테고리별 누적 탄소 배출량 비율', fontsize = 14, fontweight = 'bold')
  st.pyplot(plt)
  plt.close()

else:
  st.write('입력된 탄소 배출 데이터가 없어 그래프를 생성하지 못했습니다.')


st.subheader('<일별 탄소 배출량 추이 및 내일 예측>')
plt.figure(figsize = (10, 5))
plt.plot(days, emissions, marker = 'o', color = 'dodgerblue', linewidth = 2, label = '실제 일별 배출량')
plt.axhline(y = daily_goal, color = 'red', linestyle = '--', linewidth = 2, label = '일별 목표량')

if 'final_pred' in locals() and mode > 1:
  next_day = mode + 1
  plt.scatter([next_day], [final_pred], color = 'green', marker = '*', s = 200, zorder = 5, label = '내일 예측치')
  plt.plot([mode, next_day], [emissions[-1], final_pred], color = 'green', linestyle = ':')

if 'pred_history' in locals() and len(pred_history) > 0:
    for pred_data in pred_history:
        p_day = pred_data[0]
        p_value = pred_data[1]
        plt.scatter(p_day, p_value, color='orange', marker='*', s=100, zorder=4)
    plt.scatter([], [], color='orange', marker='*', s=100, label='전날 예측했던 양')

plt.xticks(range(1, mode + 1, 1))
plt.title('일별 탄소 배출량 추이 및 내일 예측', fontsize=14, fontweight='bold')
plt.xlabel('날짜 (Day)', fontsize=12)
plt.ylabel('탄소 배출량 (kg CO2)', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, linestyle=':', alpha=0.6)
st.pyplot(plt)
plt.close() 


st.subheader('나의 위치는?')

carbon_data = [1.50, 1.78, 1.96, 2.12, 2.23, 2.35, 2.41, 2.57, 2.66, 2.69, 
2.77, 2.85, 2.96, 3.01, 3.17, 3.36, 3.58, 3.78, 3.85, 3.92, 
3.00, 3.05, 3.12, 3.15, 3.21, 3.25, 3.33, 3.41, 3.48, 3.51, 
3.56, 3.62, 3.71, 3.77, 3.80, 3.83, 3.99, 4.02, 4.08, 4.11, 
4.17, 4.20, 4.24, 4.29, 4.33, 4.37, 4.44, 4.49, 4.55, 4.56, 
4.62, 4.67, 4.72, 4.77, 4.79, 4.81, 4.85, 4.92, 4.99, 5.01, 
4.87, 4.95, 5.02, 5.07, 5.11, 5.17, 5.18, 5.20, 5.22, 5.26, 
5.31, 5.34, 5.38, 5.41, 5.44, 5.46, 5.48, 5.50, 5.53, 5.59, 
5.62, 5.65, 5.68, 5.70, 5.73, 5.78, 5.82, 5.86, 5.88, 5.92, 
5.96, 5.97, 5.99, 6.04, 6.08, 6.13, 6.14, 6.18, 6.22, 6.25, 
6.29, 6.33, 6.35, 6.38, 6.40, 6.43, 6.48, 6.52, 6.54, 6.55, 
6.57, 6.59, 6.61, 6.65, 6.69, 6.71, 6.77, 6.82, 6.89, 6.95, 
5.04, 5.24, 5.33, 5.42, 5.51, 5.61, 5.69, 5.77, 5.83, 5.91, 
6.07, 6.11, 6.27, 6.34, 6.41, 6.49, 6.56, 6.66, 6.79, 6.85, 
6.99, 7.02, 7.15, 7.26, 7.34, 7.44, 7.58, 7.69, 7.77, 7.90, 
7.99, 8.05, 8.19, 8.28, 8.33, 8.41, 8.46, 8.52, 8.59, 8.62, 
8.70, 8.79, 8.88, 8.92, 8.98, 9.08, 9.16, 9.22, 9.31, 9.38, 
9.43, 9.51, 9.58, 9.63, 9.70, 9.77, 9.83, 9.89, 9.95, 10.00, 
10.08, 10.16, 10.28, 10.33, 10.57, 
10.31, 10.87, 11.10, 11.28, 11.72, 12.34, 12.89, 13.55, 13.85, 15.84, 
16.99, 17.91, 18.83, 19.79, 21.14]

average_emission = total_emission / day

m = np.mean(carbon_data)
sigma = np.std(carbon_data)
z_value = (average_emission - m) / sigma

z = Symbol('z')

fz = (1/(sqrt(2*pi)))*exp(-(z**2)/2)

if z_value >= 0:
    integral_value = Integral(fz, (z, 0, z_value)).doit().evalf(4)
    prob = 0.5 + float(integral_value)
else:
    integral_value = Integral(fz, (z, 0, -z_value)).doit().evalf(4)
    prob = 0.5 - float(integral_value)

if average_emission == 0:
    top_percent = 0
else:
    top_percent = prob * 100



x = np.linspace(0.50, 20.79, 300)
y = (1/(np.sqrt(2*np.pi)*sigma))*np.exp(-((x-m)**2)/(2*sigma**2))

plt.figure(figsize = (10, 5))
plt.plot(x, y, color = 'lightseagreen')
plt.axvline(average_emission, color = 'red', linestyle = '--', label = '내 탄소배출량')
plt.axvline(m, color = 'gray', linestyle = ':', label = '평균')
plt.fill_between(
    x[x <= average_emission],
    y[x <= average_emission],
    color='lightseagreen',
    alpha=0.3
)
plt.title('일 평균 탄소 배출량 분포')
plt.xlabel('일 평균 탄소 배출량 (kg CO2)')
plt.legend()
st.pyplot(plt)
plt.close()

st.write('평균:', round(m, 2))
st.write('표준편차:', round(sigma, 2))
st.write('나의 일 평균 탄소 배출량: ', round(average_emission, 2))
st.write('당신은 전체 사용자 중 탄소 배출량이 낮은 상위', round(top_percent, 2), '%입니다!')
