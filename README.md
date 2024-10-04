# SkillPoV: Towards Accessible and Effective Privacy Notice for Amazon Alexa Voice Applications
<img width="1401" alt="Screenshot 2024-05-02 at 4 22 36 PM" src="https://github.com/SkillPoV/SkillPoV/assets/168246960/a989057e-d518-4a30-8d82-33bc0115ded6">

# Instructions

* Place your own openai api key in Line 6 of /DockerImage/code/privacy_notice_generator/chatGPT_summary.py
* Place the your own skills code in the /dataset/repos/your_name/your_skill_code. There is also an example folder under /dataset/repos.
* For more skills, please refer dataset/all_skills_dataset.csv.

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

# Result
<img width="auto" alt="" src="https://github.com/SkillPoV/SkillPoV/assets/168246960/d58058a2-a31c-4849-8f74-8209f7f66ed8">

# Test on Alexa Developer Console

# Demo Vide
* When the user opens this skill for the first time:


https://github.com/SkillPoV/SkillPoV/assets/168246960/bb10a404-2bb9-430d-888b-1e390514465c


* When the user opens this skill for the first time:



https://github.com/SkillPoV/SkillPoV/assets/168246960/09ebc07a-e143-499e-a3fb-73982505f404

