import os

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import random

from .llms import LLM
from .code_manipulation import Code
from .logger import *


class AgentTBN:
    def __init__(self, table_file_path: str, max_debug_times: int = 2, gpt_model="gpt-3.5-turbo-1106", head_number=2):
        self.filename = Path(table_file_path).name
        self.head_number = head_number
        if table_file_path.endswith('.csv'):
            self.df = pd.read_csv(table_file_path)
        elif table_file_path.endswith('.xlsx'):
            self.df = pd.read_excel(table_file_path)
        else:
            raise Exception("Only csvs and xlsx are currently supported.")
        self.gpt_model = gpt_model
        self.max_debug_times = max_debug_times
        pd.set_option('display.max_columns', None) # So that df.head(1) did not truncate the printed table
        pd.set_option('display.expand_frame_repr', False) # So that did not insert new lines while printing the df
        # print('damn!')

    def answer_query(self, query: str, show_plot=False, save_plot_path=None):
        """
        Additionally returns a dictionary with info:
            - Which prompts were used and where,
            - Generated code,
            - Number of error corrections etc.
        """
        details = {}

        possible_plotname = None
        if not show_plot: # No need to plt.show()
            if save_plot_path is None: # Save plot to a random filepath
                possible_plotname = "plots/" + os.path.splitext(os.path.basename(self.filename))[0] + str(random.randint(10, 99)) + ".png"
            else: # Save plot to a provided filepath
                possible_plotname = save_plot_path

        llm_calls = LLM(use_assistants_api=False, model=self.gpt_model, head_number=self.head_number)

        plan, planner_prompt = llm_calls.plan_steps_with_gpt(query, self.df, save_plot_name=possible_plotname)
        tagged_query_type = planner_prompt[1]

        generated_code, coder_prompt = llm_calls.generate_code_with_gpt(query, self.df, plan, show_plot=show_plot, tagged_query_type=tagged_query_type)
        code_to_execute = Code.extract_code(generated_code, provider='local', show_plot=show_plot)  # 'local' removes the definition of a new df if there is one
        details["first_generated_code"] = code_to_execute

        res, exception = Code.execute_generated_code(code_to_execute, self.df, tagged_query_type=tagged_query_type)

        debug_prompt = ""

        count = 0
        errors = []
        while res == "ERROR" and count < self.max_debug_times:
            errors.append(exception)
            regenerated_code, debug_prompt = llm_calls.fix_generated_code(self.df, code_to_execute, exception, query)
            code_to_execute = Code.extract_code(regenerated_code, provider='local')
            res, exception = Code.execute_generated_code(code_to_execute, self.df, tagged_query_type)
            count += 1
        errors = errors + exception if res == "ERROR" else []

        if res == "" and tagged_query_type == "general":
            print(f"{RED}Empty output from exec() with the text-intended answer!{RESET}")


        # to remove outputs of the previous plot, works with show_plot=True, because plt.show() waits for user to close the window
        plt.clf()
        plt.cla()
        plt.close()

        details["plan"] = plan
        details["coder_prompt"] = coder_prompt
        details["prompt_user_for_planner"] = planner_prompt[0]
        details["tagged_query_type"] = tagged_query_type
        details["count_of_fixing_errors"] = str(count)
        details["final_generated_code"] = code_to_execute
        details["last_debug_prompt"] = debug_prompt
        details["successful_code_execution"] = "True" if res != "ERROR" else "False"
        details["result_repl_stdout"] = res
        details["plot_filename"] = possible_plotname if tagged_query_type == "plot" else ""
        details["code_errors"] = '\n'.join([f"{index}. \"{item}\"" for index, item in enumerate(errors)])

        ret_value = res
        if res == "":
            if tagged_query_type == "general":
                ret_value = "Empty output from the exec() function for the text-intended answer."
            elif tagged_query_type == "plot":
                ret_value = possible_plotname

        return ret_value, details
