import yaml 
from typing import Sequence, Mapping, Any, Union, Callable
PLAN_F = 'prompts_plan.yaml'
CODE_F = 'prompts_code.yaml'
import openai
KEY = open('/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/openai_key.txt').read().strip()

def get_plan_prompt(data: dict, k_fewshot:int=1)->str:
    '''
    prep prompt for plan generation
    '''
    prompt_d = yaml.full_load(open(PLAN_F))
    
    q = data['question']
    system = prompt_d['system_msg']
    user_tmp = prompt_d['user_template']
    fewshots = prompt_d['fewshots'][:k_fewshot] # list of fewshot strings include </end> tag included.
    fewshots_concat = "\n\n".join(fewshots)
    assistant_start = prompt_d['assistant_start']


    user = user_tmp.replace('{NEWLINE2_FEWSHOTS}', fewshots_concat).replace('{QUESTION}', q)
    assistant = assistant_start
    msgs = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user},
        {'role': 'assistant', 'content': assistant}
    ]
    return msgs
    
    
def get_plan2code_prompt(data:dict, plan:str=''):
    # little bit revision from PAL prompt.
    # `solution()` is returned (can execute with solution() call w/o argument
    q = data['question']
    prompt_d = yaml.full_load(open(CODE_F))
    system = prompt_d['system_msg']
    user_tmp = prompt_d['user_template']
    assistant = prompt_d['assistant_start']
    
    user = user_tmp.replace('{QUESTION}', q)
    assistant = assistant.replace('{PROCESSEDPLAN}', add_indents2plan(plan)) 
    
    msgs = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': user},
        {'role': 'assistant', 'content': assistant}
    ]


    return  msgs

def add_indents2plan(plan:str)->str:
    indent = " "*4
    plan_ = plan.split("\n")
    plan__ = [indent+p for p in plan_ if p!='</end>'] # remove </end> if exists
    processed = "\n".join(plan__)
    processed = f"\n{processed}\n" + indent
    return processed

def postprocess_code_answer(rawanswer:str, docdef:str=''):
    try:
        if "```python" in rawanswer:
            code = rawanswer.split("```python")[1].split("```")[0]
        else: # consider it continuates from prompt (starting with docstring)
            code = rawanswer.split("```")[0] #
            if code.startswith('def solution():'):
                code = "\n".join(code.split('\n')[1:]) # avoid def solution twice
            code = docdef+'\n'+code # when continuates from the prompt (containint def)
                 
    except: 
        print(f"{rawanswer=}")
        code = ''
    return remove_prints(code)

def remove_prints(code:str)->str:
    lines = code.split("\n")
    lines_ = [l for l in lines if not l.strip().startswith('print')]
    code_ = "\n".join(lines_)
    return code_


def make_code_examples()->Sequence[str]:
    def parse_fewshot2q_plan(txt):
        lines = txt.strip().split("\n")
        q = lines[0] 
        assert q.startswith('Question:')
        
        planlines = []
        start = lines.index('Suggestion:')+1
        for i in range(start, len(lines)):
            if lines[i].startswith('</end>'):
                break
            planlines.append(lines[i])
        plan = "\n".join(planlines)
        return q, plan

    

    prompt_d = yaml.full_load(open(PLAN_F))
    fewshots = prompt_d['fewshots']

    code_fewshots = []
    
    for shot in fewshots:
        q, plan = parse_fewshot2q_plan(shot)
        indent=" "*4
        docstring_def = f'def solution():\n{indent}"""{add_indents2plan(plan)}"""'
        qd = {'question': q}
        cprompt0 = get_plan2code_prompt(qd, plan=plan)
        if 'solution' in globals():
            del globals()['solution']
        while 'solution' not in globals():
            resp = openai.ChatCompletion.create(api_key=KEY,
                                model='gpt-3.5-turbo',
                                max_tokens=1024,
                                stop='</end>',
                                messages=cprompt0,
                                temperature=0,
                                top_p=1.0,
                                n=1)
            code = resp['choices'][0]['message']['content']
            # try: 
            codeonly = postprocess_code_answer(code, docdef=docstring_def)
            exec(codeonly, globals())
            # verify answer of the question
            # except:
            #     print(f'retrying (not a code)\n{code=}\n{codeonly=}')
        
        # print(code)
        # pack fewshots into list
        code_rev =[(docstring_def if l.startswith('def solution():') and (docstring_def not in l) else l) for l in codeonly.split('\n')]
        code_rev = "\n".join(code_rev)

        code_shot = f"{q}\n# solution in Python:\n\n\n{code_rev}"
        code_fewshots.append(code_shot)
        print('completed_fewshots')
        for fs in code_fewshots:
            print(fs)
    return code_fewshots
 


if __name__ == '__main__':

    """data = {"question": "Question: What do you do for a living?"}
    pp1 = get_plan_prompt(data, k_fewshot=1)
    pp3 = get_plan_prompt(data, k_fewshot=3)
    plan = '''1. Check how much money Olivia had at first, and store it into some variable.
2. She's consuming it to buy bagels. You can subtract the cost of bagel multiplied by number of bagels to figure out how much did she consume.
3. Subtract the cost from initial deposit.
4. Return the calculated number.
</end>'''
    cp0 = get_plan2code_prompt(data, plan=plan)
    
    def kvprint(record):
        for r in record:
            print(r['role'])
            print(r['content'])

    print("pp3")
    kvprint(pp3)
    print("===============================")
    print("pp1")
    kvprint(pp1)
    print("===============================")
    print("cp0")
    kvprint(cp0)
    print("===============================")"""

    # print(KEY);print(KEY)
    code_fewshots = make_code_examples()
    prompt_d = yaml.full_load(open(CODE_F))
    prompt_d.update({'fewshots': code_fewshots})
    with open('prompts_code_fewshot.yaml', 'w') as ymlf:
        yaml.dump(prompt_d, ymlf, default_flow_style=False)


    

    