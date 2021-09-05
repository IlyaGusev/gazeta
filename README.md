# Gazeta dataset
Paper: [Dataset for Automatic Summarization of Russian News](https://arxiv.org/abs/2006.11063)

## Download
### Dropbox:
* v1, Full dataset: [gazeta_jsonl.tar.gz](https://www.dropbox.com/s/cmpfvzxdknkeal4/gazeta_jsonl.tar.gz)
* v1, Train: [gazeta_train.jsonl](https://www.dropbox.com/s/43l702z5a5i2w8j/gazeta_train.jsonl)
* v1, Validation: [gazeta_val.jsonl](https://www.dropbox.com/s/k2egt3sug0hb185/gazeta_val.jsonl)
* v1, Test: [gazeta_test.jsonl](https://www.dropbox.com/s/3gki5n5djs9w0v6/gazeta_test.jsonl)
* v1, Raw version without any cleaning (not recommended): [gazeta_raw.txt](https://www.dropbox.com/s/4fxj5wmt7tjr5f2/gazeta_raw.txt)
* v1, Train with oracle summaries: [gazeta_train_oracle.jsonl](https://www.dropbox.com/s/5dva37fm1v4zp3j/gazeta_train_oracle.jsonl)
* v1, Validation with oracle summaries: [gazeta_val_oracle.jsonl](https://www.dropbox.com/s/hc9tab4ewe352jt/gazeta_val_oracle.jsonl)
* v1, Test with oracle summaries: [gazeta_test_oracle.jsonl](https://www.dropbox.com/s/cjbciavdxg54mlq/gazeta_test_oracle.jsonl)
* v1, Preprocessed data for mBART: [gazeta_data_mbart_600_160_v2.tar.gz](https://www.dropbox.com/s/70d75da8h8f16ox/gazeta_data_mbart_600_160_v2.tar.gz)

**UPDATE**:
* v2, Full dataset: [gazeta_jsonl_v2.tar.gz](https://www.dropbox.com/s/lb50mk5jujjjqbi/gazeta_jsonl_v2.tar.gz)
* v2/v1 diff: [gazeta_new.jsonl](https://www.dropbox.com/s/c5y8q7pb3kv6cdu/gazeta_new.jsonl)
* v2/v1 raw diff without any clenaning: [gazeta_raw_new.jsonl](https://www.dropbox.com/s/gyv841mph04qweu/gazeta_raw_new.jsonl)

### Other sources:
* GitHub: https://github.com/IlyaGusev/gazeta/releases/tag/1.0
* Kaggle: https://www.kaggle.com/phoenix120/gazeta-summaries
* Huggingface: https://huggingface.co/datasets/IlyaGusev/gazeta

### Trained MBART model:
https://huggingface.co/IlyaGusev/mbart_ru_sum_gazeta

## Additional notes
* Legal basis for distribution of the dataset: https://www.gazeta.ru/credits.shtml, paragraph 2.1.2. All rights belong to "www.gazeta.ru". This dataset can be removed at the request of the copyright holder. Usage of this dataset is possible only for personal purposes on a non-commercial basis. 
* Cleaning: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Ed_chVrslp_7vJNS3PmRC0_ZJrRQYv0C)
* Data analysis: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Rp4-COj8RNbvH4jvRQkc5fik5XuhGU5y)
* Summarization methods: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1B26oDFEKSNCcI0BPkGXgxi13pbadriyN)
* If you are interested in another Russian summarization dataset, check out a Russian part of [XL-Sum](https://github.com/csebuetnlp/xl-sum)

## Contacts
* Gitter chat: [summarus/community](https://gitter.im/summarus/community)
* Telegram: [@YallenGusev](https://t.me/YallenGusev)

## Citation

```bibtex
@InProceedings{10.1007/978-3-030-59082-6_9,
    author="Gusev, Ilya",
    editor="Filchenkov, Andrey and Kauttonen, Janne and Pivovarova, Lidia",
    title="Dataset for Automatic Summarization of Russian News",
    booktitle="Artificial Intelligence and Natural Language",
    year="2020",
    publisher="Springer International Publishing",
    address="Cham",
    pages="122--134",
    isbn="978-3-030-59082-6"
}
```

