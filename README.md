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

# Demo Vide
* When the user opens this skill for the first time:
* <video width="320" height="240" controls>
  <source src="[movie.mp4](https://github.com/SkillPoV/SkillPoV/assets/168246960/cd7eb598-273f-402c-8d2a-bee04e151aed">
</video>
https://github.com/SkillPoV/SkillPoV/assets/168246960/cd7eb598-273f-402c-8d2a-bee04e151aed
* When the user opens this skill not for the first time:
https://github.com/SkillPoV/SkillPoV/assets/168246960/0036392e-d370-4612-a784-9312e62eea9b
