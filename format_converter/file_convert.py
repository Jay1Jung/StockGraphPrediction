import pandas as pd

# 파일 경로 설정
input_file_path = '/Users/jayjung/Desktop/dataset/USA_Leading_Index_filtered.csv'

# 데이터 읽기 (UTF-8 BOM 처리)
data = pd.read_csv(input_file_path, encoding='utf-8-sig')

# 열 이름 확인
print("Columns in the file:", data.columns)

# USA 데이터 필터링 (REF_AREA 또는 다른 확인된 열 이름 사용)
usa_data = data[data['REF_AREA'] == 'USA']

# 필요한 열만 선택
usa_leading_data_filtered = usa_data[['TIME_PERIOD', 'OBS_VALUE']]

# 결과를 저장할 파일 경로
filtered_file_path = '/Users/jayjung/Desktop/dataset/USA_Leading_Index_Converted.csv'

# 선택한 열만 포함된 데이터를 새 CSV로 저장
usa_leading_data_filtered.to_csv(filtered_file_path, index=False)

# 파일 저장 확인
print(f"Filtered file saved: {filtered_file_path}")