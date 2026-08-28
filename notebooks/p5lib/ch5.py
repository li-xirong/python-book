import csv
import os

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from transformers import BertForSequenceClassification, BertTokenizerFast, get_linear_schedule_with_warmup


# 读取并固定划分IMDB英文影评数据
def load_imdb_data():
    data_file = "../pybook-data/ch5/imdb_labelled.txt"
    df = pd.read_csv(data_file, names=["sentence", "label"], sep="\t", quoting=csv.QUOTE_NONE)
    sents = df["sentence"].tolist()
    y = df["label"].tolist()

    out_dir = "output"
    train_file = os.path.join(out_dir, "imdb_labelled_train.csv")
    test_file = os.path.join(out_dir, "imdb_labelled_test.csv")
    if os.path.exists(train_file) and os.path.exists(test_file):
        df_train, df_test = pd.read_csv(train_file), pd.read_csv(test_file)
        sents_train, sents_test = df_train["sentence"].tolist(), df_test["sentence"].tolist()
        y_train, y_test = df_train["label"].tolist(), df_test["label"].tolist()
    else:
        os.makedirs(out_dir, exist_ok=True)
        sents_train, sents_test, y_train, y_test = train_test_split(sents, y, test_size=0.2, random_state=1)
        pd.DataFrame({"sentence": sents_train, "label": y_train}).to_csv(train_file, index=False)
        pd.DataFrame({"sentence": sents_test, "label": y_test}).to_csv(test_file, index=False)
    return sents_train, sents_test, y_train, y_test


# 读取并固定划分中文酒店评论数据
def load_hotel_data():
    data_file = "../pybook-data/ch5/ChnSentiCorp_htl_all.csv"
    df = pd.read_csv(data_file).dropna(subset=["review"])
    sents = df["review"].tolist()
    y = df["label"].tolist()

    out_dir = "output"
    train_file = os.path.join(out_dir, "ChnSentiCorp_train.csv")
    test_file = os.path.join(out_dir, "ChnSentiCorp_test.csv")
    if os.path.exists(train_file) and os.path.exists(test_file):
        df_train, df_test = pd.read_csv(train_file), pd.read_csv(test_file)
        sents_train, sents_test = df_train["review"].tolist(), df_test["review"].tolist()
        y_train, y_test = df_train["label"].tolist(), df_test["label"].tolist()
    else:
        os.makedirs(out_dir, exist_ok=True)
        sents_train, sents_test, y_train, y_test = train_test_split(sents, y, test_size=0.2, random_state=1)
        pd.DataFrame({"review": sents_train, "label": y_train}).to_csv(train_file, index=False)
        pd.DataFrame({"review": sents_test, "label": y_test}).to_csv(test_file, index=False)
    return sents_train, sents_test, y_train, y_test


# 从本地加载Sentence-Transformers模型
def load_sentence_model(local_model_path):
    import sentence_transformers as sentrans

    return sentrans.SentenceTransformer(local_model_path)


# 读取学生信息并生成肖像文件路径
def load_student_portrait_data():
    columns = "姓名 性别 出生日期 学号 所属学院 入学年份 籍贯 GPA 总学分".split()
    students = pd.read_csv("../pybook-data/ch3/rawdata.txt", header=None, names=columns)
    s_ids = students["学号"].values
    img_path_list = [f"../pybook-data/ch3/portraits/{x}.png" for x in s_ids]
    return students, img_path_list


# 在训练集上构造BoW特征
def build_bow_features(sents_train, sents_test):
    fe = CountVectorizer()
    fe.fit(sents_train)
    vob = fe.get_feature_names_out()
    return fe, vob, fe.transform(sents_train), fe.transform(sents_test)


class FeatSet(Dataset):
    # 保存BoW特征和标签
    def __init__(self, feats, labels):
        self.feats = feats
        self.labels = labels

    # 返回数据集样本数
    def __len__(self):
        return len(self.labels)

    # 返回指定位置的稠密特征和标签
    def __getitem__(self, idx):
        dense = self.feats[idx].toarray().squeeze()
        return torch.tensor(dense, dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.long)


class SimpleNet(nn.Module):
    # 创建仅有一个线性层的网络
    def __init__(self, vocab_size, num_class=2):
        super().__init__()
        self.net = nn.Linear(vocab_size, num_class)

    # 执行网络前向计算
    def forward(self, x):
        return self.net(x)


# 从本地加载BERT模型和分词器
def load_bert_model():
    local_model_path = "./bert-base-uncased"
    model = BertForSequenceClassification.from_pretrained(local_model_path, num_labels=2)
    tokenizer = BertTokenizerFast.from_pretrained(local_model_path)
    return model, tokenizer


# 从本地加载BERT分词器
def load_bert_tokenizer():
    return BertTokenizerFast.from_pretrained("./bert-base-uncased")


class BertDataset(Dataset):
    # 保存文本、标签和BERT分词器
    def __init__(self, sents, labels, tokenizer, max_len=64):
        self.texts = sents
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    # 返回数据集样本数
    def __len__(self):
        return len(self.labels)

    # 返回指定位置的BERT编码结果和标签
    def __getitem__(self, idx):
        encoded = self.tokenizer(
            self.texts[idx],
            add_special_tokens=True,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt",
        )
        item = {key: val.squeeze(0) for key, val in encoded.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item


# 创建用于微调BERT的训练DataLoader
def create_bert_train_loader(sents_train, y_train, tokenizer):
    train_ds = BertDataset(sents_train, y_train, tokenizer)
    return DataLoader(train_ds, batch_size=32, shuffle=True)


# 训练SimpleNet并计算额外影评的情感得分
def get_simplenet_scores(input_texts):
    sents_train, sents_test, y_train, y_test = load_imdb_data()
    fe, vob, x_train, x_test = build_bow_features(sents_train, sents_test)
    train_ds = FeatSet(x_train, y_train)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleNet(len(vob)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=1e-4)
    total_steps = len(train_loader) * 300
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
    for _ in range(300):
        model.train()
        for xb, yb in train_loader:
            loss = criterion(model(xb.to(device)), yb.to(device))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
    input_ds = FeatSet(fe.transform(input_texts), [0] * len(input_texts))
    input_loader = DataLoader(input_ds, batch_size=16, shuffle=False)
    model.eval()
    all_scores = []
    with torch.no_grad():
        for xb, _ in input_loader:
            all_scores.append(torch.softmax(model(xb.to(device)), dim=1).cpu().numpy())
    return np.vstack(all_scores)


# 微调BERT并计算额外影评的情感得分
def get_bert_scores(input_texts):
    sents_train, sents_test, y_train, y_test = load_imdb_data()
    model, tokenizer = load_bert_model()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_ds = BertDataset(sents_train, y_train, tokenizer)
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
    total_steps = len(train_loader) * 10
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
    for epoch in range(10):
        model.train()
        for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}"):
            batch = {k: v.to(device) for k, v in batch.items()}
            loss = model(**batch).loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()
    input_ds = BertDataset(input_texts, [0] * len(input_texts), tokenizer)
    input_loader = DataLoader(input_ds, batch_size=16, shuffle=False)
    model.eval()
    all_scores = []
    with torch.no_grad():
        for batch in input_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"])
            all_scores.append(torch.softmax(outputs.logits, dim=1).cpu().numpy())
    return np.vstack(all_scores)
