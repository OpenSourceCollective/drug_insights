# DrugInsights

DrugInsights is a LLM-based application that provides insights into drugs and their interactions with other drugs.

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
