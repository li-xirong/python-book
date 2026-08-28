# 自定义库 p5lib

+ [ch5.py](ch5.py): 第5章案例的公共前置代码。
  - `load_imdb_data()`：读取并固定划分英文影评数据。
  - `load_hotel_data()`：读取并固定划分中文酒店评论数据。
  - `load_sentence_model()`：加载本地 MiniLM、M3E 等 Sentence-Transformers 模型。
  - `load_student_portrait_data()`：读取学生信息并生成肖像路径。
  - `build_bow_features()`：构造英文影评的 BoW 特征。
  - `FeatSet`、`SimpleNet`：BoW + SimpleNet 案例使用的数据集类和网络类。
  - `load_bert_model()`、`load_bert_tokenizer()`、`BertDataset`、`create_bert_train_loader()`：BERT 英文影评案例的模型、分词器、数据集和训练批次准备。
  - `get_simplenet_scores()`、`get_bert_scores()`：为示例代码 5.59 生成两种模型的额外样本情感得分。
