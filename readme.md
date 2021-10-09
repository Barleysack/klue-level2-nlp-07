
# 1. Introduction  
<br/>
<p align="center">
   <img src="./_img/AI_Tech_head.png" style="width:350px; height:70px;" />
</p>
<p align="center">
   <img src="./_img/value_boostcamp.png" style="width:800px; height:240px;" />
</p>

Introduction
  
<br/>

## ☕ 조지KLUE니 

### 🔅 Members  

김보성|김지후|김혜수|박이삭|이다곤|전미원|정두해
:-:|:-:|:-:|:-:|:-:|:-:|:-:
![image1][image1]|![image2][image2]|![image3][image3]|![image4][image4]|![image5][image5]|![image6][image6]|![image7][image7]
[Github](https://github.com/Barleysack)|[Github](https://github.com/JIHOO97)|[Github](https://github.com/vgptnv)|[Github](https://github.com/Tentoto)|[Github](https://github.com/DagonLee)|[Github](https://github.com/ekdub92)|[Github](https://github.com/Doohae)

### 🔅 Contribution  
`김보성` &nbsp; Modeling • Preprocessing(Data pruning • special character removals) • Ensemble(Weighted Vote) • Github management  
`김지후` &nbsp; EDA • Data Augmentation(`EDA` • `BackTranslation`) • Binary classifier experiment  
`김혜수` &nbsp; Preprocessing (NER Marker) • Data Augmentation(Entity Swap augmentation)  
`박이삭` &nbsp; Preprocessing(clean punctuation • special character removal) • Binary classifier experiment  
`이다곤` &nbsp; Custom Token Addition • Model Embedding Size Modification • Vocab Modification • Tokenizer Experiment  
`전미원` &nbsp; Data Visualization • Modeling • Binary classifier experiment • Ensemble  
`정두해` &nbsp; EDA • Data Augmentation(`EDA` • `AEDA` • `RandomDeletion` • `BackTranslation`) • Code Abstraction  

[image1]: ./_img/김보성.jpg
[image2]: ./_img/김지후.png
[image3]: ./_img/김혜수.jpg
[image4]: ./_img/박이삭.png
[image5]: ./_img/이다곤.png
[image6]: ./_img/전미원.jpg
[image7]: ./_img/정두해.jpg

<br/>

# 2. Project Outline  

![competition_title](./_img/competition_title.png)

<p align="center">
   <img src="./_img/mask_sample.png" width="300" height="300">
   <img src="./_img/class.png" width="300" height="300">
</p>

- Task : Image Classification
- Date : 2021.08.22 - 2021.09.02 (2 weeks)
- Description : 사람의 정면 사진을 입력받아서 `마스크 착용여부`, `성별`, `나이`를 추측하여 `18개의 class`로 분류함  
- Image Resolution : (384 x 512)
- Train : 18,900 + (External Dataset : https://www.kaggle.com/tapakah68/medical-masks-p4)
- Test1 : 6,300
- Test2 : 6,300

### 🏆 Final Score  
<p align="center">
   <img src="./_img/final_score.png" width="700" height="90">
</p>

<br/>

# 3. Solution
![process][process]

### KEY POINT
- 마스크 착용여부, 성별에 대해서는 정확도가 높았으나 나이 분류(특히 60대 이상)에서 상대적으로 정확도가 낮아 이를 해결하는 것이 가장 중요했습니다. 
- 나이와 성별이 다르지만 의상이 비슷한 경우, 또는 마스크와 비슷한 물체나 형태가 이미지에 등장하는 경우 상대적으로 정확도가 낮았습니다 .
- Cutmix, Cutout은 일반적으로 이미지 분류 문제 해결에 있어서 효과적이지만 잘못된 예제를 생성하는 현상을 보였습니다. 

&nbsp; &nbsp; → 주요 논점을 해결하는 방법론을 제시하고 실험결과를 공유하며 토론을 반복했습니다   

[process]: ./_img/process.png
<br/>

### Checklist
More Detail : https://github.com/jinmang2/boostcamp_ai_tech_2/blob/main/assets/ppt/palettai.pdf
- [x] Transformer based model
- [x] CNN based model(CLIP, EfficientNet, Nfnet, ResNet, ResNext)
- [x] Age-specific model
- [x] Three-head model
- [x] External Dataset
- [x] Data Augmentation (Centorcrop, Resize)
- [x] Focal loss
- [x] Weighted Sampling
- [x] Ensemble
- [x] Out of fold
- [x] Test time augmentation
- [x] Stacking
- [x] Pseudo Labeling
- [x] Noise Label Modification 
- [x] Cutmix, cutout
- [x] StyleGAN v2 + Mask Synthesis
- [ ] Ray
- [ ] MC-Dropout
- [ ] Fixmatch
- [ ] Semi-supervised learning

### Evaluation

| Method | F-score |
| --- | --- |
| Synthetic Dataset + EfficientLite0 | 69.0 |
| Synthetic Dataset + non-prtrained BEIT | 76.9 |
| Synthetic Dataset + EfficientNet + Age-speicific | 76.9 |
| Synthetic Dataset + NFNet (Pseudo Labeling + Weighted Sampling)| 78.5 |
| Stacking BEIT + NFNet | 77.1 |

# 4. How to Use
- External dataset을 이용하기 위해서는 kaggle 의 https://www.kaggle.com/tapakah68/medical-masks-p4 에서 추가적으로 다운로드 받으셔야 합니다. 
```
.
├──input/data/train
├──input/data/eval
├──input/data/images(external kaggle data)
├──image-classification-level1-08
│   ├── configs
│   ├── solution
│         ├── cnn_engine
│         ├── hugging
│         ├── jisoo
│         ├── hugging
│         └── moon
```

- `soloution`안에는 각각 **train** •  **test** •  **inference**가 가능한 라이브러리가 들어있습니다  
- 사용자는 전체 코드를 내려받은 후, 옵션을 지정하여 개별 라이브러리의 모델을 활용할 수 있습니다
- 각 라이브러리의 구성요소는 `./solution/__main__.py`에서 확인할 수 있습니다  

### How to make Synthetic Dataset
- Use the repo Mask the face(https://github.com/aqeelanwar/MaskTheFace)
- Use the deepface to label age and gender(https://github.com/serengil/deepface)


```bash
git clone https://github.com/boostcampaitech2/image-classification-level1-08.git
```
```bash
$python __main__.py -m {module} -s {script} -c {config}

```
