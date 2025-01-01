import os
import pandas as pd  # pandas 라이브러리 사용

# Set up dynamic paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "stock_data")
PROCESSED_DATA_FILE = os.path.join(PROJECT_ROOT, "data", "formatted", "merged_stock_data.csv")

# Ensure the output directory exists
os.makedirs(os.path.dirname(PROCESSED_DATA_FILE), exist_ok=True)

# 함수 정의: 디렉토리 내 모든 파일 처리 및 병합
def merge_stock_data_by_date(input_dir, output_file):
    merged_data = pd.DataFrame()  # 빈 데이터 프레임 초기화
    
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):
            input_file_path = os.path.join(input_dir, file_name)
            
            # 파일 이름에서 주식 이름 추출 (예: AAPL.csv -> AAPL)
            stock_name = os.path.splitext(file_name)[0]
            
            try:
                # CSV 파일 읽기
                data = pd.read_csv(input_file_path)
                
                # "Date"와 "Close" 필터링
                filtered_data = data[["Date", "Close"]]
                
                # "Close" 컬럼 이름을 "{stock_name}_closing" 형식으로 변경
                filtered_data.rename(columns={"Close": f"{stock_name}_closing"}, inplace=True)
                
                # "Date"를 기준으로 병합
                if merged_data.empty:
                    merged_data = filtered_data
                else:
                    merged_data = pd.merge(
                        merged_data,
                        filtered_data,
                        on="Date",
                        how="outer"
                    )
                
                print(f"Processed: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # 병합된 데이터를 저장
    merged_data.sort_values(by="Date", inplace=True)  # 날짜 정렬
    merged_data.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")

# 함수 실행
merge_stock_data_by_date(RAW_DATA_DIR, PROCESSED_DATA_FILE)
