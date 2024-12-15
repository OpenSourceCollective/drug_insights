from op_generate import generate_drug_insights_responses
from op_compare import compare_responses


generate_drug_insights_responses("queries_and_human.tsv", "queries_human_and_drug_insights.tsv")

good_count, good_ratio = compare_responses(
    input_file="queries_human_and_drug_insights.tsv",
    output_file="human_drug_insights_compare.tsv"
)

print(f"Good Matches: {good_count}, Proportion: {good_ratio:.2f}")
