# 🎓 EducationGuardianAgent (Coordinator Agent)
Acts as the master orchestrator in a multi-agent system designed to holistically support a student’s U.S. college journey. 
It initiates intake, stores key user data, and dispatches sub-agents based on student needs — collecting results and returning a unified guidance summary.

### Sub-Agents
1. **Goal setting agent**:
   - Gathers student background
   - academic history
   - course interest
   - preferences
     
3. **University matching agent**:
   - Suggests universities tailored to GPA
   - budget
   - course interest
   - region, etc. (Reach/Match/Safety)
     
5. **Test prep agent**:
   - Advises on SAT/ACT/TOEFL needs per target school
   - provides study resources
   - provides study plan
     
7. **Recommendationn agent**:
   - Explains the importance of recommendation letters
   - ideal recommenders
   - how many to collect based on contextual data
     
9. **Extracurricular agent**:
    - Analyzes hobbies/interests to suggest meaningful extracurriculars for strong apps
    - Makes suggestions for new hobbies that aligns to career path
      
11. **Essay mentor agent**:
    - Helps students brainstorm and draft personal statements for applications

### Testing: 
Sample Prompts for Each Agent
1. **Goal Setting Agent**
   I'm from Nigeria and currently in my final year of secondary school. I have a 4.5 GPA on a 5.0 scale.
   I'm passionate about technology, especially artificial intelligence and software development.
   I'm looking for a school that offers strong CS programs, ideally with scholarship opportunities.
   I’d prefer schools in safe urban areas with international student support.

2. **University Matching Agent**
   I’m looking for universities in the U.S. that are strong in engineering and tech, especially AI.
   I'd like a school that values diversity, has an inclusive culture, and provides substantial financial aid.
   My GPA is 4.5/5.0, and I’d prefer somewhere in the East Coast or Midwest. I'm open to public or private institutions.

3. **Test Prep Agent**
   I’m interested in going to Stanford or Duke, or any other great institution in the United States.
   I’m a native English speaker but will need to take the SAT. TOEFL isn’t required for my country of origin.
   I would like a personalized study plan. I’m planning to take the SAT at the end of the year.
   I can commit about 15 hours per week to practice and would like to include biweekly mock tests in my schedule.
   My target score is 1450+.

4. **Essay Mentor Agent**
   I’m focusing on the Common App prompt about overcoming a challenge and how it shaped me.
   A few schools also ask about community impact and academic interests. I’m considering writing about building a safety app for Nigeria,
   or teaching myself to code during COVID to support my sister’s restaurant. I want to emphasize resilience and initiative,
   and how I used technology to make a real-world impact.

5. **Recommendation Letter Agent**
   I'm applying to the University of California (UC) schools, Stanford University, and the Massachusetts Institute of Technology (MIT).
   I plan to ask my chemistry and math teachers for recommendation letters since I’ve done really well in their classes
   and they’ve seen my growth over time. I’d like tips on how to approach them and what makes a strong recommendation letter.

6. **Extracurricular Agent**
   I enjoy coding, playing chess, and volunteering in my community. I once led a tutoring program for younger students.
   I’m also passionate about using tech for social impact. I’d love suggestions on how to make my extracurriculars stand out,
   especially for computer science programs.

   
### Setup Environment
You only need to create one virtual environment for all examples in this course. Follow these steps to set it up:

Create virtual environment in the root directory
- python -m venv .venv

Activate (each new terminal)
   - macOS/Linux:
   source .venv/bin/activate
   - Windows CMD:
   .venv\Scripts\activate.bat
   - Windows PowerShell:
   .venv\Scripts\Activate.ps1

Install dependencies
- pip install -r requirements.txt

Run to trigger
- adb web
