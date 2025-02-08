# DrugInsights

Welcome to the Drug Insights GitHub repository! This project is an open-source Retrieval-Augmented Generation (RAG) chatbot designed to provide healthcare professionals with accurate, context-aware drug information. Tailored to the unique challenges faced by African healthcare systems, Drug Insights aims to bridge the gap in medication knowledge accessibility, enhance patient safety, and streamline clinical workflows.

## Why Drug Insights?
Healthcare professionals in Africa often rely on time-intensive methods, such as printed formularies or general-purpose online resources, to access drug information. With limited pharmacist availability due to brain drain and resource constraints, a tool is critical to deliver timely and reliable medication insights. Drug Insights leverages the power of Large Language Models (LLMs) and advanced retrieval systems to address this gap, ensuring healthcare providers can access up-to-date and relevant drug data at their fingertips.

## Key Features
Real-Time Drug Lookup: Retrieve information on drug interactions, dosages, side effects, and contraindications effortlessly.
Optimized for African Formularies: Built using the EMDEX formulary and other regionally relevant resources.
Advanced RAG Architecture: Combines powerful Pinecone vector databases with GPT-4 for precise and reliable responses.
Minimal Hallucination: Uses prompt engineering and S-BERT evaluation to deliver contextually accurate outputs.
Open-Source and Scalable: Adaptable for integration with various datasets and applications.

## How It Works
* Data Extraction and Preprocessing: Extracts and processes text from drug formularies like EMDEX using PyMuPDF, ensuring structured and readable information.
* Vector Storage: Embeds drug information into a high-dimensional Pinecone database for efficient cosine similarity retrieval.
* Natural Language Understanding: GPT-4 refines retrieved data, generating detailed and human-like responses.
* Evaluation and Optimization: Uses S-BERT similarity scoring and human feedback to ensure accuracy and relevance.

## Future Enhancements
Expanded Data Integration: Incorporating more regional and global drug formularies.
Improved UI/UX: Enhancements to the interface for easier interaction and better visualization of drug data.
Chat Session Support: Enabling multi-turn conversations for complex queries.
Real-Time Feedback Mechanisms: Allowing users to rate responses for continuous improvement.

## Acknowledgement 
We are grateful to [Advantage Health Africa](https://advantagehealthafrica.com/) for the support and funding provided for this project

## Who we are
We are [Axum AI](https://axumai.org/) leveraging AI and Tech to empower Africa and Africans with custom, open-source solutions with a focus on social impact and development

## Dev Setup

- Install conda environment

```bash
conda install -n druginsights python=3.10
conda activate druginsights
pip install -e .
```

- Get the [access keys](https://www.notion.so/Setting-up-the-Azure-OpenAI-s-API-access-e9d1d231d2d0499694e955428005d545?pvs=4#319c86b7fd7842039137df3fe28f74880) and save them in a .env file.

- Rename the `example_config.json` to `config.json` and fill in the required fields as appropriate.

- Run the app with `streamlit run src/ui/main.py`

## Contributors

- [Ayomide O](https://github.com/Ayomidejoe)
- [Joshua Owoyemi](https://toluwajosh.github.io/)
- [Kelvin Akyea](https://github.com/khelvyn80)
- [Mohammed Afeez](https://github.com/NKASG)
- [Shamsudeen Abubakar](https://github.com/har-booh)
- [Favour Madubuko](https://github.com/favouralgo/)
- [Taofeeq Togunwa](https://github.com/Taofeeq-T)
- Samuel Oyatoye
- Zeenat Oyetolu
- Abimbola Adebakin
- [Advantage Health Africa](https://advantagehealthafrica.com/)
