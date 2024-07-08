# Adding new prompts

Experiment with different prompts to see how they affect the output.

Do not edit the content of the defaults.py file. 
Instead, create a new file (for example my_prompts.py) and define your custom prompts there.

To use your prompt, import it in the `src/ui/main.py` and add it as an argument to the executor. An example is shown below:

```python
...
from agents.prompts.my_prompts import special_system_prompt, special_user_prompt

# define agent executor
agent_executor = ChatAndRetrievalExecutor(
  system_prompt=special_system_prompt, user_prompt=special_user_prompt
)
...
```

You can replace either the system_prompt or user_prompt with your custom prompt. If you only want to replace one of them, you can leave the other.
```
