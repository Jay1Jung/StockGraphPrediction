import os
import pandas as pd  # pandas 라이브러리 사용

# Set up dynamic paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data","processed")  # input_path
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data","formatted")  # output_path

# Ensure the output directory exists
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# 
def process_pmi_files_with_date_filter(input_dir, output_dir):
    all_data = []  # 
    
    for file_name in os.listdir(input_dir):
        # if the file contains the name"pmi" process
        if "pmi" in file_name.lower() and file_name.endswith(".csv"):
            input_file_path = os.path.join(input_dir, file_name)
            
            try:
               
                data = pd.read_csv(input_file_path)
                
                # extract the file name
                pmi_type = os.path.splitext(file_name)[0]
                
                # filter only date and actual section
                filtered_data = data[["Date", "Actual"]]
                
                # select data only after 2020
                filtered_data["Date"] = pd.to_datetime(filtered_data["Date"])  
                filtered_data = filtered_data[filtered_data["Date"].dt.year >= 2020]
                
                # unifying the format
                filtered_data["Date"] = filtered_data["Date"].dt.strftime("%Y-%m-%d")
                
                
                filtered_data.rename(columns={"Actual": f"{pmi_type}_Actual"}, inplace=True)
                
               
                all_data.append(filtered_data)
                print(f"Processed: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    
    if all_data:
        merged_data = pd.concat(all_data, axis=1)
        merged_data = merged_data.loc[:, ~merged_data.columns.duplicated()] 
        
       
        merged_data.sort_values(by="Date", inplace=True) 
        output_file_path = os.path.join(output_dir, "merged_pmi_data.csv")
        merged_data.to_csv(output_file_path, index=False)
        print(f"Merged data saved to {output_file_path}")
    else:
        print("No valid data to merge.")


process_pmi_files_with_date_filter(RAW_DATA_DIR, PROCESSED_DATA_DIR)
