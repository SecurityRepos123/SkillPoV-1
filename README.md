# Instructions

* Place your own openai api key in Line 6 of /DockerImage/code/privacy_notice_generator/chatGPT_summary.py
* Place the your own skills code in the /dataset/repos/your_name/your_skill_code. There is also an example folder under /dataset/repos.

If you prefer use Docker, Please exexute the following commands:
* Run ./build.sh
* Run ./run.sh (run again if /dataset/results directory has output but /dataset/repo doesn't have any update).
* You can check the reuslt from /dataset/repo. There will be a new index_new.js. And the json file has been modified. 
* Upload modified files to Alexs skill developer console to test.
* Please note everytime you upload new repos or do any changes, rerun ./build.sh

You can also exexute the code directly:
* Run pip install openai
* Run pip install spacy
* Run python -m spacy download en_core_web_sm
* Run DockerImage/code/data_collection_analysis/scan_skills.py
* Run DockerImage/code/privacy_notice_generator/main.py
