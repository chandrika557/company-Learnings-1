def insurance_query(user_query, retrived_data=""):
    return f"""You are an insurance expert assistant. Your primary goal is to provide concise and accurate answers to the user's insurance-related questions using the relevant documents provided. If the documents do not contain the necessary information, acknowledge this and provide a general response based on standard insurance practices.

**User Query:**

{user_query}


**Relevant Documents:**

{retrived_data}

**Instructions:**

1. Carefully read the user's query and the relevant documents.
2. If the query is clear and the documents contain the necessary information, use that information to craft a direct and specific response.
3. If the query is ambiguous or lacks details, ask for clarification in your response. For example: 'Could you please specify which type of insurance policy you are referring to?'
4. If the documents do not contain the answer, state: 'The provided documents do not contain specific information about [query topic]. However, based on standard insurance practices, [general response].'
5. Ensure your response is clear, logically structured, and easy to understand.
6. If applicable, reference specific parts of the documents to support your answer.
7. Maintain a professional and helpful tone throughout your response."""

def summarize_context(chat_history=[]):
    return f"""You are an AI assistant tasked with summarizing the chat history provided below as a list of Python dictionaries in the format. Your job is to review the past interaction summary and present interactions and provide a concise single-paragraph summary of the context.

Here is the list  the chat history:

{chat_history}

it is in the following format: "role": "assistant", "content": "response_text"

---

Please review the past summary and list of interactions and provide a concise single-paragraph summary of the context.
Give only the summary without any additional explanations or comments. The summary should be clear and easy to understand, capturing the main points of the conversation so far.
"""
def past_or_present(prompt):
    return f"""You are an AI assistant. Your task is to determine whether the user is asking about a past or present context based on the provided prompt.
    If the user is asking about a past context, respond with "False".
    If the user is asking about a present context, respond with "True".
    Here is the prompt:
{prompt}

respond with "True" or "False" only, without any additional explanations or comments."""

def claim_query(insurance_type, all_data, doc_content):
    return f"""
                **Insurance Type**: {insurance_type}
                **All Data (Policy, User, and Claims)**: {all_data}
                **Policy Document Content**: {doc_content}
                
                Please provide a detailed analysis and premium calculation with the following:
                1. **Claims Analysis**:
                   - Summary of past claims (if any).
                   - Risk assessment based on claim history, user data, and present value (e.g., vehicle/property value for Auto/Home).
                   - For Home insurance, consider the house type (e.g., HO-1, HO-2) in risk assessment.
                   - For Travel insurance, assess risks based on destination, trip duration, and medical conditions.
                2. **Premium Calculation**:
                   - Base premium based on coverage limits, deductible, and user data.
                   - Adjustments for risk factors (e.g., claim history, driving record, house type, destination).
                   - Include discounts (e.g., multi-policy, low-mileage) if specified.
                   - Provide total premium in Indian Rupees (INR) with breakdowns for:
                     - Monthly premium
                     - Quarterly premium
                     - Yearly premium
                3. **Coverage Period**:
                   - Specify the coverage duration based on effective and expiration dates.
                4. **Additional Notes**:
                   - Highlight key factors influencing the premium (e.g., high claim history, low present value, house type).
                   - For Home insurance, explain how house type (e.g., HO-1 vs. HO-3) affects coverage and premium.
                   - For Travel insurance, note coverage specifics (e.g., cancellation, medical emergencies).
                5. **Suggestions**:
                   - Provide actionable recommendations to reduce premiums, improve coverage, or mitigate risks, tailored to the insurance type and user data. Examples:
                     - For Auto: Suggest safe driving courses, higher deductibles, or vehicle safety upgrades.
                     - For Home: Recommend security upgrades, switching to a broader house type (e.g., HO-3), or bundling policies.
                     - For Health: Suggest lifestyle changes (e.g., quitting smoking) or wellness programs.
                     - For Life: Recommend adjusting coverage based on income or health improvements.
                     - For Travel: Suggest trip planning adjustments (e.g., safer destinations, shorter trips) or additional coverage options.
                   - Base suggestions on claims history, risk factors, and user inputs (e.g., high mileage, pre-existing conditions).
                
                Return the response in a structured Markdown format with clear sections, tables for premiums, and bullet points for analysis and suggestions. Ensure amounts are in INR.
                """

class ReAct:
    pass

