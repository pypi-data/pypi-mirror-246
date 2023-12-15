from dataclasses import dataclass

@dataclass
class Prompts:

    generate_steps_for_plot_save = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including any values necessary to answer the question, 
such as names of dataframe columns. Make sure to state saving the plot to '{plotname}' in the last step. Do not include showing the plot to the user interractively; only save it to the '{plotname}'.

This algorithm will be later used to write a Python code and applied to the existing pandas DataFrame `df`. 
The DataFrame `df` is already defined and populated with necessary data. So there is no need to define it again or load it. Here's the beggining of the 'df': 
{df_head}

Present your algorithm in up to six simple, clear English steps. 
Remember to explain steps rather than to write code.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example of output for your inspiration:
1. Sort the DataFrame `df` in descending order based on the 'happiness_index' column.
2. Extract the 5 rows from the sorted DataFrame.
3. Multiply each found value in the extracted dataframe by 3.
4. Create a bar plot with 'Voltage' on the x axis and multiplied 'Speed' on the y axis.
5. Save the bar plot to 'plots/example_plot00.png'.
"""

    generate_steps_for_plot_show = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including any values necessary to answer the question, 
such as names of dataframe columns. Make sure to state showing the plot in the last step.

This algorithm will be later used to write a Python code and applied to the existing pandas DataFrame `df`. 
The DataFrame `df` is already defined and populated with necessary data. So there is no need to define it again or load it. Here's the beggining of the 'df': 
{df_head}

Present your algorithm in up to six simple, clear English steps. 
Remember to explain steps rather than to write code.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example of output for your inspiration:
1. Sort the DataFrame `df` in descending order based on the 'happiness_index' column.
2. Extract the 5 rows from the sorted DataFrame.
3. Multiply each found value in the extracted dataframe by 3.
4. Create a bar plot with 'Voltage' on the x axis and multiplied 'Speed' on the y axis.
5. Show the plot.
"""

    generate_steps_no_plot = """You are an AI data analyst and your job is to assist the user with simple data analysis.
The user asked the following question: '{input}'.

Formulate your response as an algorithm, breaking the solution into steps, including any values necessary to answer the question, 
such as names of dataframe columns.

This algorithm will be later used to write a Python code and applied to the existing pandas DataFrame 'df'. 
The DataFrame 'df' is already defined and populated with necessary data. So there is no need to define it again or load it. Here's the beggining of the 'df': 
{df_head}

Present your algorithm with at most six simple, clear English steps. 
Remember to explain steps rather than to write code.
Don't include any visualization steps like plots or charts.
You must output only these steps, the code generation assistant is going to follow them.

Here's an example of output for your inspiration:
1. Find and store the minimal value in the 'Speed' column.
2. Find and store the maximal value in the 'Voltage' column.
3. Subtract the minimal speed from the maximal voltage.
4. Raise the result to the third power.
5. Print the result.
"""

    generate_code = """The user provided a query that you need to help achieving: {input}. 
You also have a list of subtasks to be accomplished using Python.

You have been presented with a pandas dataframe named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
The result of `print(df.head({head_number}))` is:
{df_head}

Return only the python code that accomplishes the following tasks:
{plan}

Approach each task from the list in isolation, advancing to the next only upon its successful resolution. 
Strictly follow to the prescribed instructions to avoid oversights and ensure an accurate solution.
You must include the neccessery import statements at the top of the code.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.

Example of the output format:
```python

```"""

    generate_code_for_plot_save = """The user provided a query that you need to help achieving: {input}. 
You also have a list of subtasks to be accomplished using Python.

You have been presented with a pandas dataframe named `df`.
The DataFrame `df` has already been defined and populated with the required data, so don't load it and don't create a new one.
The result of `print(df.head({head_number}))` is:
{df_head}

Return only the python code that accomplishes the following tasks:
{plan}

Approach each task from the list in isolation, advancing to the next only upon its successful resolution. 
Strictly follow to the prescribed instructions to avoid oversights and ensure an accurate solution.
You must include the neccessery import statements at the top of the code.
You must not include `plt.show()`. Just save the plot the way it is stated in the tasks.
You must include print statements to output the final result of your code.
You must use the backticks to enclose the code.

Example of the output format:
```python

```"""

    fix_code = """You are a helpful assistant that corrects the python code that resulted in an error and returns the corrected code.

The code was designed to achieve this user request: {input}.
The DataFrame `df`, that we are working with has already been defined and populated with the required data, so don't load it and don't create a new one.
The result of `print(df.head({head_number}))` is:
{df_head}

The execution of the following code that was provided in the previous step resulted in an error:
```python
{code}
```

The error message is: '{error}'

Return a corrected python code that fixes the error.
Always include the import statements at the top of the code, and comments and print statements where necessary.
Use the same format with backticks. Example of the output format:
```python

```"""
