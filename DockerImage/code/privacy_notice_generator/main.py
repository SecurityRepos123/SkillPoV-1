import filter_data_collection
import filter_index_js_repo
import chatGPT_summary
import modify_index_js
import modify_json_code
import path as path
import shutil
import time
import os

if __name__ == "__main__":
    shutil.rmtree(path.data_collection_results_path, ignore_errors=True)
    print(f"data_collection_results_path deleted")

    os.makedirs(path.data_collection_results_path, exist_ok=True)
    os.makedirs(path.data_collection_results_path + "/chatGPT", exist_ok=True)
    os.makedirs(path.data_collection_results_path + "/final", exist_ok=True)

    print(f"filter data collection starts")
    filter_data_collection.get_final_report()
    final_rewrite_path = filter_index_js_repo.filter_js_file()
    print(f"The following repos contain data collection: {final_rewrite_path}")
    print(f"chatGpt output starts")
    chatGPT_summary.generate_chatgpt_output()
    print(f"chatGpt output ends")
    print(f"Generating new index_new.js files")
    modify_index_js.search_and_replace()
    print(f"Generating new index_new.js files")
    modify_json_code.modify_json_code()

