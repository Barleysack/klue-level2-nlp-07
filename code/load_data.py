import pickle as pickle
import os
import pandas as pd
import torch
import re

class RE_Dataset(torch.utils.data.Dataset):
  """ Dataset 구성을 위한 class."""
  def __init__(self, pair_dataset, labels):
    self.pair_dataset = pair_dataset
    self.labels = labels

  def __getitem__(self, idx):
    item = {key: val[idx].clone().detach() for key, val in self.pair_dataset.items()}
    item['labels'] = torch.tensor(self.labels[idx])
    return item

  def __len__(self):
    return len(self.labels)

def preprocessing_dataset(dataset):
  """ 처음 불러온 csv 파일을 원하는 형태의 DataFrame으로 변경 시켜줍니다."""
  subject_entity = []
  object_entity = []
  for i,j in zip(dataset['subject_entity'], dataset['object_entity']):
    i = i[1:-1].split(',')[0].split(':')[1]
    j = j[1:-1].split(',')[0].split(':')[1]

    subject_entity.append(i)
    object_entity.append(j)
  out_dataset = pd.DataFrame({'id':dataset['id'], 'sentence':dataset['sentence'],'subject_entity':subject_entity,'object_entity':object_entity,'label':dataset['label'],})
  return out_dataset

def load_data(dataset_dir):
  """ csv 파일을 경로에 맡게 불러 옵니다. """
  pd_dataset = pd.read_csv(dataset_dir)
  dataset = preprocessing_dataset(pd_dataset)
  
  return dataset

def clean_punc(text):
    punct_mapping = {'ʿ': '', 'ū': 'u', 'è': 'e', 'ȳ': 'y', 'ồ': 'o', 'ề': 'e', 'â': 'a', 'æ': 'ae', 'ő': 'o', 'ῶ': 'ω', '𑀕': 'Λ', 'ß': 'β', 'ヶ': 'ケ', '‘': "'", '₹': 'e', '´': "'", '°': '', '€': 'e', '™': 'tm', '√': ' sqrt ', '×': 'x', '²': '2', '—': '-', '–': '-', '’': "'", '_': '-', '`': "'", '“': '"', '”': '"', '£': 'e', '∞': 'infinity', '÷': '/', '•': '.', 'à': 'a', '−': '-', 'Ῥ': 'Ρ', 'ầ': 'a', '́': "'", 'ò': 'o', 'Ö': 'O', 'Š': 'S', 'ệ': 'e', 'Ś': 'S', 'ē': 'e', 'ä': 'a', 'ć': 'c', 'ë': 'e', 'å': 'a', 'Ǧ': 'G', 'ạ': 'a', 'ņ': 'n', 'İ': 'I', 'ğ': 'g', 'ê': 'e', 'Č': 'C', 'ã': 'a', 'ḥ': 'h', 'ả': 'a', 'ễ': 'e', '％': '%', 'ợ': 'o', 'Ú': 'U', 'ư': 'u', 'Ž': 'Z', 'ú': 'u', 'É': 'E', 'Ó': 'O', 'ü': 'u', 'é': 'e', 'ā': 'a', 'š': 's', '𑀥': 'D', 'í': 'i', 'û': 'u', 'ý': 'y', 'ī': 'i', 'ï': 'i', 'ộ': 'o', 'ì': 'i', 'ọ': 'o', 'ş': 's', 'ó': 'o', 'ñ': 'n', 'ậ': 'a', 'Â': 'A', 'ù': 'u', 'ô': 'o', 'ố': 'o', 'Á': 'A', 'ö': 'o', 'ơ': 'o', 'ç': 'c', 'ˈ': "'", 'µ': 'μ', '／': '/', '（': '(', 'ｍ': 'm', '˘': ' ', '𑀫': 'ma', '？': '?', 'ł': 'l', 'Đ': 'D', '：': ':', '･': ',', 'Ç': 'C', 'ı': 'i', '，': ',', '𥘺': '祉', '·': ',', '＇': "'", ' ': ' ', '）': ')', '１': '1', 'ø': 'o', '～': '~', '³': '3', '(˘ ³˘)': '', '˹': '"', '｢': '"', '｣': '"', '«': '<<', '˼': '"', '»': '>>', '®': 'R'}

    for p in punct_mapping:
        text=re.sub(p, punct_mapping[p],text)
    return text

def tokenized_dataset(dataset, tokenizer):
    
    copied_dataset = list(dataset['sentence'])
    cleaned_dataset = []
    for sentence in copied_dataset:
    #     sentence = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\[\]\<\>`\'…《》▲△]', ' ', sentence)
        sentence = clean_punc(sentence)
        sentence = re.sub('[^0-9a-zA-Z가-힣一-龥ぁ-ゔァ-ヴー々〆〤()\\u0250-\\u02AD\\u1200-\\u137F\\u0600-\\u06FF\\u0750-\\u077F\\uFB50-\\uFDFF\\uFE70‌​-\\uFEFF\\u0900-\\u097F\\u0400-\\u04FF\\u0370-\\u03FF ]',' ',sentence)
        sentence = re.sub('\s+',' ',sentence)
        cleaned_dataset.append(sentence)
    
    """ tokenizer에 따라 sentence를 tokenizing 합니다."""
    concat_entity = []
    for e01, e02 in zip(dataset['subject_entity'], dataset['object_entity']):
      temp = ''
      temp = e01 + '[SEP]' + e02
      concat_entity.append(temp)

    tokenized_sentences = tokenizer(
        concat_entity,
        cleaned_dataset, #여기를 수정해서 돌려주시면 됩니다. cleaned dataset으로.
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=256,
        add_special_tokens=True,
        )
    return tokenized_sentences