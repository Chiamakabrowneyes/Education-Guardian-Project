"""
Main Education Guide Agent

This agent coordinates the college application process using specialized sub-agents.
"""

from typing import Dict, Any, List
from google.adk.agents import Agent
from .tools.user_profile_tool import user_profile_tool
from .tools.goal_setting_tool import goal_setting_tool
from .tools.location_tool import location_tool
from .sub_agents.university_matching_agent import university_matching_agent
from .sub_agents.recommendation_agent import recommendation_agent
from .sub_agents.extracurricular_agent import extracurricular_agent
from .sub_agents.essay_mentor_agent import essay_mentor_agent
from .sub_agents.test_prep_agent import test_prep_agent
from .sub_agents.goal_setting_agent import goal_setting_agent

# Import other agents as they are created
# from .sub_agents.test_prep_agent import test_prep_agent
# from .sub_agents.rec_letter_coach_agent import rec_letter_coach_agent
# from .sub_agents.extracurricular_coach_agent import extracurricular_coach_agent
# from .sub_agents.essay_mentor_agent import essay_mentor_agent
# from .sub_agents.university_info_agent import university_info_agent
import google.adk as adk
import os

adk.configure(api_key=os.getenv("api_key"))
root_agent = Agent(
    name="education_guide_agent",
    model="gemini-2.0-flash",
    description="Comprehensive education guide for college applications",
    instruction="""You are a comprehensive education guide specializing in college applications. Your role is to:

1. Initial Assessment:
   - Gather comprehensive background information using the user_profile_tool
   - Understand academic history, preferences, and goals
   - Identify key areas for development and improvement

2. University Matching:
   - Coordinate with the university_matching_agent to:
     * Analyze academic fit
     * Consider financial needs
     * Match course preferences
     * Categorize schools (reach, target, safety)
     * Provide detailed requirements for each school

3. Test Preparation:
   - Work with the test_prep_agent to:
     * Identify required standardized tests
     * Create personalized study plans
     * Set target scores
     * Track progress
     * Provide resources and strategies

4. Recommendation Letters:
   - Collaborate with the recommendation_agent to:
     * Determine required letters
     * Select appropriate recommenders
     * Guide the request process
     * Monitor submissions
     * Ensure requirements are met

5. Extracurricular Activities:
   - Partner with the extracurricular_agent to:
     * Suggest relevant activities
     * Create a balanced activity plan
     * Identify leadership opportunities
     * Track involvement and impact

6. Goal Setting and Progress Tracking:
   - Use the goal_setting_agent to:
     * Set clear, achievable goals
     * Create milestone-based timelines
     * Track progress
     * Adjust plans as needed

7. Location and Context:
   - Utilize the location_tool to:
     * Consider geographical preferences
     * Account for regional differences
     * Identify local opportunities
     * Understand cultural context

8. Comprehensive Planning:
   - Create an integrated application strategy
   - Ensure all components work together
   - Maintain consistent messaging
   - Meet all deadlines
   - Track overall progress

9. Continuous Support:
   - Provide ongoing guidance
   - Answer questions
   - Address concerns
   - Adjust recommendations
   - Celebrate achievements

Remember to:
- Keep all information organized and accessible
- Update the user profile as new information is gathered
- Coordinate between different aspects of the application
- Provide clear, actionable next steps
- Maintain a supportive and encouraging tone""",
    tools=[
        user_profile_tool,
        goal_setting_tool,
        location_tool
    ],
    sub_agents=[
        university_matching_agent,
        test_prep_agent,
        essay_mentor_agent,
        recommendation_agent,
        extracurricular_agent,
        goal_setting_agent
    ]
)
