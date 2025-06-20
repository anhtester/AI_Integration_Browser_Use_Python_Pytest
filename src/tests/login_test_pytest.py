import pytest
from browser_use import Agent


@pytest.fixture(scope="function")
def agent1(session, llm_model):
    return Agent(
        task='''
            Go to 'https://crm.anhtester.com/admin/authentication'
            Login with email and password: 'admin@example.com' and '123456'
            Click menu Customers to open the Customer page
            Search the customer 'Anh Tester' on search field in customer page
            Get the Company column of the table
            Verify the Company column results contains 'Anh Tester' value on table
        ''',
        llm=llm_model,
        use_vision=True,
        browser_session=session,
    )


@pytest.fixture(scope="function")
def agent2(session, llm_model):
    return Agent(
        task='''
            Go to 'https://cms.anhtester.com/login'
            Login with email and password: 'admin@example.com' and '123456'
            Get the Total Customers number on the dashboard
            Verify the Total Customers number results equals '657' value on dashboard
        ''',
        llm=llm_model,
        use_vision=True,
        browser_session=session,
    )


def test_login_crm(agent1):
    import asyncio
    print("Running test_login_crm")
    asyncio.run(agent1.run())


def test_login_cms(agent2):
    import asyncio
    print("Running test_login_cms")
    asyncio.run(agent2.run())
