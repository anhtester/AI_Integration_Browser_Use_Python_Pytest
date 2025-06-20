import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
from browser_use.browser.session import BrowserSession
from browser_use.browser.profile import BrowserProfile
from pydantic import SecretStr
import os
from dotenv import load_dotenv
from playwright.sync_api import ViewportSize

# Load the environment variables
load_dotenv()

# Initialize the model
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', api_key=SecretStr(os.getenv('GOOGLE_API_KEY')))

# Ensure project_root is a string
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
recording_path = os.path.join(project_root, 'exports', 'recordings')
trace_path = os.path.join(project_root, 'exports', 'traces')

# Create the directory if it does not exist
if not os.path.exists(recording_path):
   os.makedirs(recording_path)
if not os.path.exists(trace_path):
   os.makedirs(trace_path)

browser_profile = BrowserProfile(
   user_data_dir=None,
   headless=False,
   no_viewport=True,
   disable_security=True,
   wait_for_network_idle_page_load_time=3.0,
   highlight_elements=True,
   viewport_expansion=-1,
   record_video_dir=os.path.join(project_root, 'exports', 'recordings'),
   record_har_path=os.path.join(project_root, 'exports', 'recordings'),
   record_video_size=ViewportSize(width=1920, height=1080),
   traces_dir=os.path.join(project_root, 'exports', 'traces')
)

browser_session = BrowserSession(
   browser_profile=browser_profile,
)

# Create agent with the model and browser context
agent = Agent(
   task='''
            Go to 'https://crm.anhtester.com/admin/authentication'
            Login with email and password: 'admin@example.com' and '123456'
            Click menu Customers to open the Customer page
            Search the customer 'Anh Tester' on search field in customer page
            Get the Company column of the table
            Verify the Company column results contains 'Anh Tester' value on table
        ''',
   llm=llm,
   use_vision=True,  # Enable vision capabilities
   # save_conversation_path="exports/logs/",  # Save chat logs
   browser_session=browser_session,
)


async def main():
   # Run the agent to perform the task
   await agent.run()
   
   # Stop the browser session after the task is done
   # await browser_session.stop()
   await browser_session.kill()


asyncio.run(main())
