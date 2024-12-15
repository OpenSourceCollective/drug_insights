import pandas as pd
from src.agents.executors import ChatAndRetrievalExecutor
from src.agents.helpers import get_by_session_id
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.history import RunnableWithMessageHistory

def generate_drug_insights_responses(input_file: str, output_file: str, session_id: str = "abc123"):
    """
    Process queries from a TSV file, generate responses using ChatAndRetrievalExecutor, and save the results.

    Parameters:
        input_file (str): Path to the input TSV file containing queries and human feedback.
        output_file (str): Path to save the output TSV with generated answers and context.
        session_id (str): Session ID for the agent executor. Default is "abc123".
    """
    # Initialize agent executor
    agent_executor = ChatAndRetrievalExecutor()

    # Read input file
    df_in = pd.read_csv(input_file, names=["query", "human"], header=None, sep="\t")
    data_out = df_in.assign(di_answer=None, di_context=None)

    # Iterate through input rows
    for row in df_in.itertuples(index=True, name="Row"):
        query = row.query
        agent_executor.msgs.add_user_message(query)

        cfg = RunnableConfig()
        cfg["configurable"] = {"session_id": session_id}

        runner = RunnableWithMessageHistory(
            agent_executor.executor,
            get_by_session_id,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        # Execute and collect the response
        response = runner.invoke({"input": query}, config=cfg)
        data_out.loc[row.Index, "di_answer"] = response.get("answer", "")
        data_out.loc[row.Index, "di_context"] = str(response.get("context", ""))
        print(f"Processed {row.Index + 1} / {len(df_in)}",  end="\r")

    # Save output file
    data_out.to_csv(output_file, sep="\t", index=False)
    print(f"Done. Output saved to {output_file}")


# from op_generate_copy import generate_drug_insights

# generate_drug_insights("queries_and_human.tsv", "queries_human_and_drug_insights.tsv")