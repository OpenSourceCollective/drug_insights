import pandas as pd
from sentence_transformers import SentenceTransformer, util

def compare_responses(input_file: str, output_file: str, model_name: str = 'all-MiniLM-L6-v2', min_good_score: float = 0.3):
    """
    Compare human responses with generated responses using a pre-trained Sentence-BERT model.

    Parameters:
        input_file (str): Path to the input TSV file containing queries, human responses, and generated answers.
        output_file (str): Path to save the output TSV with similarity scores.
        model_name (str): Name of the pre-trained Sentence-BERT model. Default is 'all-MiniLM-L6-v2'.
        min_good_score (float): Minimum cosine similarity score to classify as a "good" match. Default is 0.3.

    Returns:
        int: Count of good matches based on the similarity score.
        float: Proportion of good matches relative to the total rows.
    """
    # Load the pre-trained Sentence-BERT model
    model = SentenceTransformer(model_name)
    
    # Read input file
    df_in = pd.read_csv(input_file, names=["query", "human", "di_answer", "di_context"], sep='\t', skiprows=1)
    df_out = df_in.copy()
    df_out['sim_score'] = None

    good_count = 0

    # Compare responses and calculate similarity
    for row in df_in.itertuples(index=True, name="Row"):
        sentence1 = row.human
        sentence2 = row.di_answer

        # Encode sentences and compute cosine similarity
        embedding1 = model.encode(sentence1, convert_to_tensor=True)
        embedding2 = model.encode(sentence2, convert_to_tensor=True)
        cosine_sim = util.cos_sim(embedding1, embedding2).item()

        # Update the similarity score and good match count
        df_out.loc[row.Index, 'sim_score'] = cosine_sim
        if cosine_sim >= min_good_score:
            good_count += 1

        print(f"Processed {row.Index + 1} / {len(df_in)}",  end="\r")

    # Save output to a TSV file
    df_out.to_csv(output_file, sep='\t', index=False)
    print(f"Output saved to {output_file}")

    # Return summary statistics
    total_rows = len(df_in)
    good_ratio = good_count / total_rows
    return good_count, good_ratio
