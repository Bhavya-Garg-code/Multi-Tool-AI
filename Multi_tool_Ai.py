from openai import OpenAI
import time
import streamlit as  st

try:
    api = st.secrets('API')
except Exception as e:
    st.error("No API Key Found")

client = OpenAI(api_key = api,base_url = 
"https://api.groq.com/openai/v1")
model = 'openai/gpt-oss-20b'

st.set_page_config(
    page_title='Multi tool AI',
    page_icon = '🤖',
    layout = 'wide'

)

if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []
if 'math_history' not in st.session_state:
    st.session_state.math_history = []

def generate(prompt):
    sys_pro = '''
You are a helpful and friendly teacher.
You have to explain every topic clearly.
Add headings and bullet points besides examples to your explanation
'''
    try:
          response = client.chat.completions.create(
            model = model,
            messages = [
               {'role':'system', 'content':sys_pro},
               {'role':'user','content':prompt}],
            temperature=0.3,
            max_tokens = 2056
        )
          return response.choices[0].message.content
    except Exception as e:
           return f'Error Occured : {e}'

math_pro = """
You are a math mastermind.
You have to behave like a maths teacher.
Explain every solution properly with logical reasoning and clarity
IMPORTANT FORMATTING RULES:

1. Use plain text for mathematical equations.

2. Do NOT use LaTeX syntax.

3. Do NOT use dollar signs for equations.

4. Do NOT use \\( \\), \\[ \\], \\frac, \\boxed, or other LaTeX commands.

5. Write x² instead of x^2 where appropriate.

6. Write fractions as 1/2, square roots as sqrt(25) = 5,

and multiplication using ×.

7. Use clear headings and numbered steps.

8. Put each equation on a separate line.

9. End with a clearly labelled FINAL ANSWER.

10. Verify the answer when possible.

Use this format:

PROBLEM:

Write the given problem.

STEP 1: ...

Explanation...

STEP 2: ...

Explanation...

FINAL ANSWER:

Write the final answer clearly.

VERIFICATION:

Check the answer if possible.
"""

def math_solver(problem,level):
     sys_pro = f"""
{math_pro}
'difficulty:{level}
problem:{problem}
"""
     try:
           response = client.chat.completions.create(
             model = model,
             messages = [
                {'role':'system', 'content':sys_pro},
                {'role':'user','content':sys_pro}],
             temperature=0.3,
             max_tokens = 2056
         )
           return response.choices[0].message.content
     except Exception as e:
            return f'Error Occured : {e}'
   
st.sidebar.title("Choose your preferred AI")

options = st.sidebar.radio('Chose an application',['Math Mastermind','General AI'])

st.title("Multi tasking AI")

if options == 'General AI':
     st.header('AI teaching assistant')
     st.write("Use the Ai to get general answers to questions")
     ques = st.text_input("Ask your question", placeholder="What is AI?")

     if st.button("Ask"):
          
          if ques.strip():
               with st.spinner("Generating"):
                    ans = generate(ques)
               st.session_state.ai_history.insert(0,{'Question':ques, 'Answer':ans})

          else:
               st.error("No question entered")
     if st.session_state.ai_history:
          down_txt  = ''
          st.markdown("Conversation history")

          for i, chat in enumerate(st.session_state.ai_history,1):
               down_txt += f'Question{i}\n'
               down_txt += f"{chat['Question']} \n\n"
               down_txt += f"Answer{i}\n"
               down_txt += f"{chat['Answer']} \n\n"

               with st.container(border = True):
                    st.write(f"Question{i} :  {chat['Question']}")
                    st.markdown(f"Answer{i} :  {chat['Answer']}")
          st.download_button(label = 'Download', data = down_txt, file_name = 'Conversation.txt', mime = 'text/plain', use_container_width=True)
          if(st.button('Clear history')):
                st.session_state.ai_history = []
                st.rerun()
elif(options == 'Math Mastermind'):
     
     st.header("Math Mastermind")
     st.write("Enter your problem to get solutions")
     problem = st.text_area("Enter your problem", placeholder = 'x+y = 35')
     levels = st.selectbox('Difficulty level',['Basic','Moderate','Advanced'])

     if(st.button('Solve')):
          if not problem.strip():
               st.error("No problem found")

          else:
               with st.spinner("Solving..."):
                 answer = math_solver(problem,levels)
               st.session_state.math_history.insert(0,{'problem':problem,'Answer':answer})
               st.markdown(answer)

     if (st.session_state.math_history):
          for i,a in enumerate(st.session_state.math_history,1):
               with st.container(border=True):
                    st.write(f"Problem{i}")
                    st.markdown(a['problem'])
                    st.write(f"Answer{i}")
                    st.markdown(a['Answer'])

          if st.button('Clear history'):
               st.session_state.math_history = []
               st.rerun()

st.sidebar.divider()
st.sidebar.caption("AI mastermind hub  [Math solver, General AI]")
