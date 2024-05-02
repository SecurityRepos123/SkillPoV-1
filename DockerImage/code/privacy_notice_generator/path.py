import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
data_set_path = os.path.join(root_path, 'dataset')

data_collection_results_path = os.path.join(data_set_path, 'data_collection_results')
results_path = os.path.join(data_set_path, 'results')
repo_path = os.path.join(data_set_path, 'repos')
filter_path = os.path.join(data_set_path, 'filtered_js_repo')
add_intent_path = os.path.join(data_set_path, 'add_intent.txt')

final_path = os.path.join(data_collection_results_path, 'final')
chatGPT_path = os.path.join(data_collection_results_path, 'chatGPT')