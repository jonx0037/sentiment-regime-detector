[[Luo_trainedLargeLanguageModelsFinancial_2024]]

# [Pre-trained Large Language Models for Financial Sentiment Analysis](https://arxiv.org/abs/2401.05215v1)

## [[Wei Luo]]; [[Dihong Gong]]

## Abstract
Financial sentiment analysis refers to classifying financial text contents into sentiment categories (e.g. positive, negative, and neutral). In this paper, we focus on the classification of financial news title, which is a challenging task due to a lack of large amount of training samples. ==To overcome this difficulty, we propose to adapt the pretrained large language models (LLMs) [1, 2, 3] to solve this problem==. The LLMs, which are trained from huge amount of text corpora,have an advantage in text understanding and can be effectively adapted to domain-specific task while requiring very few amount of training samples. In particular, we adapt the open-source Llama2-7B model (2023) with the supervised fine-tuning (SFT) technique [4]. ==Experimental evaluation shows that even with the 7B model (which is relatively small for LLMs), our approach significantly outperforms the previous state-of-the-art algorithms==.

## Key concepts
#fine_tuning; #finding/financial_news; #financial_news; #claim/large_language_models; #large_language_models; #text_corpora

## Quote
> This paper proposes the use of a pre-trained large language model, LLaMA2-7B, with supervised fine-tuning (SFT) to achieve state-of-the-art results in financial sentiment analysis, outperforming previous methods with limited training samples.

## Key points
- Financial sentiment analysis refers to classifying financial text contents into sentiment categories
- We investigate with different methods of using few-shots, further pretraining, and supervised fine-tuning (SFT) based on the Llama2-7B model
- The base method leverages the capability of pretrained large language models (LLMs), while the SFT method further improves this capablity by fune-tuning the model use task-specific training data, and the ClassHead method models the problem as classification problem by adding a classification head at the output layer
- We can see that the SFT version improves from the base version by a clear margin, which confirms that our SFT method is effective in improving the classification accuracy of the financial news titles
- We explored the potentials of using LLMs for the financial sentiment analysis
- Our SFT algorithm significantly improves over the baseline method and achieve a new state-of-the-art performance


## Summary

### Introduction
The paper discusses financial sentiment analysis, which involves classifying financial text into sentiment categories.
The authors propose using a pretrained large language model (LLM) to solve this problem, specifically the LLaMA2-7B model with supervised fine-tuning (SFT).
The LLMs have an advantage in text understanding and can be effectively adapted to domain-specific tasks with few training samples.

### Methodology
The authors investigate different methods of using few-shots, further pretraining, and SFT based on the LLaMA2-7B model.
They achieve state-of-the-art results on the PhraseBank financial sentiment analysis benchmark.
The paper also discusses the use of the GPT model, which differs from BERT in its pre-training methodology and architectural design, and may offer a distinctive perspective and advantages in financial sentiment analysis.

### Results
The authors demonstrate the capability of LLMs for solving the financial sentiment analysis problem, and their approach significantly outperforms previous state-of-the-art algorithms.
The study is based on the Financial PhraseBank dataset, and the authors provide data and code for their approach on GitHub.
The paper also discusses related work, including the use of BERT and FinBERT for financial sentiment analysis, and highlights the potential of LLMs for this task.
The results show that the SFT method improves the classification accuracy, and the ClassHead method performs equally with the SFT method but has the advantage of outputting classification confidence scores.
The proposed method achieves a new state-of-the-art performance with an accuracy of 0.9, outperforming the current state-of-the-art accuracy of 0.86.

### Model
The model used is LLaMA-7B version 2 without SFT, trained with 5 epochs, a learning rate starting from $3e^{-5}$ and reducing to $3e^{-6}$ with cosine annealing schedule.
The micro batch size is set to $4$ with max sequence length $1024$.
The model is trained with data parallel paradigm with world size of $4$ and each GPU has RAM of 80GB.

### Dataset
The dataset used is the Financial PhraseBank, which contains 4845 English sentences randomly extracted from financial news.
The data is split into training, validation, and testing sets, with $20\%$ of the data held out for testing.
The performance of algorithms is measured with classification accuracy.


## Study subjects

### 1200 workers
- You are asked to choose the most suitable sentiment from ("postive", "negative", "neutral") with signle-choice questions. ==Please follow these examples to answer the question.News Title: Most of the permanent layoffs will be in the plywood and sawn timber sectors of the Finnish company’s operations at several domestic mills, where earlier this year it temporarily laid off some 1,200 workers to save costs==. Choices: A) positive

### 1200 workers
- Please follow these examples to answer the question. ==News Title: Most of the permanent layoffs will be in the plywood and sawn timber sectors of the Finnish company’s operations at several domestic mills, where earlier this year it temporarily laid off some 1,200 workers to save costs==. Choices: A) positive

## Data analysis
- #method/classhead_method

## Findings
- <mark class="claim">Experimental evaluation shows that even with the 7B model (which is relatively small for LLMs), our approach significantly outperforms the previous state-of-the-art algorithms</mark>
- <mark class="claim"><mark class="fact">We achieve the state-of-the-art on PhraseBank financial sentiment analysis benchmark</mark></mark>
- <mark class="fact">The base method leverages the capability of pretrained LLMs</mark>, <mark class="fact">while the SFT method further improves this capablity by fune-tuning the model use task-specific training data</mark>, and finally <mark class="fact">the ClassHead method models the problem as classification problem by adding a classification head</mark> at the output layer. The results of these three methods are show in Table 1. <mark class="claim">According to these results, <mark class="fact">we can see that the SFT version improves from the base version</mark> by a clear margin, <mark class="fact">which confirms that our SFT method is effective in improving the classification accuracy</mark> of the financial news titles</mark>
- <mark class="claim"><mark class="fact">The results show that our method has improved the current state-of-the-art accuracy</mark> from 0.86 to 0.9, which is a big improvement</mark>
- <mark class="claim"><mark class="fact">Our SFT algorithm significantly improves over the baseline method</mark> and achieve a new state-of-the-art performance</mark>

## Differs from previous work
- Based on the paper of Yang et al (2023) and Kheiri et al (2023), the GPT model differs significantly from BERT in its pre-training methodology and architectural design, primarily emphasizing its generative modeling capabilities. ==In contrast to BERT’ s bidirectional encoding, the GPT model adopts a unidirectional architecture, focusing more on context generation and coherence== [^16], [^17].

## Contributions
- In this paper, <mark class="claim"><mark class="fact"><mark class="fact">we explored the potentials of using LLMs for the financial sentiment analysis</mark></mark></mark>. We performed a systematically empirical analysis and provided novel insights on how to efficiently utilize the LLMs to improve the classification accuracy. Specifically, the few-shots only method can achieve relatively decent accuracy, <mark class="fact">while the further pretraining doesn’t provide a noticeable improvement over its baseline</mark>. Finally, <mark class="claim"><mark class="fact"><mark class="fact">our SFT algorithm significantly improves over the baseline method</mark></mark> and achieve a new state-of-the-art performance</mark>. Future work includes using LLMs with larger number of parameters (e.g. LLaMA2-70B).

## Limitations
- The limitations of this study include the use of a relatively small model (7B parameters) and the reliance on a specific dataset (Financial PhraseBank).
- The study does not explicitly mention limitations, but it notes that further pretraining does not provide a noticeable improvement over the baseline.

## Future work
- The future work includes exploring the use of larger models, investigating the use of other pre-trained models, and evaluating the model's performance on other datasets.
- The study suggests using LLMs with a larger number of parameters, such as LLaMA2-70B, for future work.


## References
[^1]: Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. Improving language understanding by generative pre-training. 2018.  [OA](https://scholar.google.co.uk/scholar?q=Radford%2C%20Alec%20Narasimhan%2C%20Karthik%20Salimans%2C%20Tim%20Sutskever%2C%20Ilya%20Improving%20language%20understanding%20by%20generative%20pre-training%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Radford%2C%20Alec%20Narasimhan%2C%20Karthik%20Salimans%2C%20Tim%20Sutskever%2C%20Ilya%20Improving%20language%20understanding%20by%20generative%20pre-training%202018) 

[^2]: Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. Language models are unsupervised multitask learners. OpenAI Blog, 1(8):9, 2019.  [OA](https://engine.scholarcy.com/oa_version?query=Radford%2C%20Alec%20Wu%2C%20Jeff%20Child%2C%20Rewon%20Luan%2C%20David%20Language%20models%20are%20unsupervised%20multitask%20learners%202019&author=Radford&title=Language%20models%20are%20unsupervised%20multitask%20learners&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Radford%2C%20Alec%20Wu%2C%20Jeff%20Child%2C%20Rewon%20Luan%2C%20David%20Language%20models%20are%20unsupervised%20multitask%20learners%202019) [Scite](/scite_tallies?query=author%3ARadford%2Ctitle%3ALanguage%20models%20are%20unsupervised%20multitask%20learners%2Cyear%3A2019)

[^3]: Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding, 2019.  [OA](https://scholar.google.co.uk/scholar?q=Devlin%2C%20Jacob%20Chang%2C%20Ming-Wei%20Lee%2C%20Kenton%20Toutanova%2C%20Kristina%20Bert%3A%20Pre-training%20of%20deep%20bidirectional%20transformers%20for%20language%20understanding%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Devlin%2C%20Jacob%20Chang%2C%20Ming-Wei%20Lee%2C%20Kenton%20Toutanova%2C%20Kristina%20Bert%3A%20Pre-training%20of%20deep%20bidirectional%20transformers%20for%20language%20understanding%202019) 

[^4]: Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lample. Llama: Open and efficient foundation language models, 2023.  [OA](https://scholar.google.co.uk/scholar?q=Touvron%2C%20Hugo%20Lavril%2C%20Thibaut%20Izacard%2C%20Gautier%20Martinet%2C%20Xavier%20Marie-Anne%20Lample%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Touvron%2C%20Hugo%20Lavril%2C%20Thibaut%20Izacard%2C%20Gautier%20Martinet%2C%20Xavier%20Marie-Anne%20Lample%202023) 

[^5]: Bing Liu. Sentiment Analysis: Mining Opinions, Sentiments, and Emotions. Studies in Natural Language Processing. Cambridge University Press, 2  [OA](https://engine.scholarcy.com/oa_version?query=Liu%2C%20Bing%20Sentiment%20Analysis%3A%20Mining%20Opinions%2C%20Sentiments%2C%20and%20Emotions&author=Liu&title=Sentiment%20Analysis%3A%20Mining%20Opinions%2C%20Sentiments%2C%20and%20Emotions&year=0000) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20Bing%20Sentiment%20Analysis%3A%20Mining%20Opinions%2C%20Sentiments%2C%20and%20Emotions) [Scite](/scite_tallies?query=author%3ALiu%2Ctitle%3ASentiment%20Analysis%3A%20Mining%20Opinions%2C%20Sentiments%2C%20and%20Emotions%2Cyear%3A0000)

[^6]: Bo Pang and Lillian Lee. Opinion Mining and Sentiment Analysis, volume 2. 2008.  [OA](https://engine.scholarcy.com/oa_version?query=Bo%20Pang%20and%20Lillian%20Lee%20Opinion%20Mining%20and%20Sentiment%20Analysis%20volume%202%202008&author=Pang&title=&year=2008) [GScholar](https://scholar.google.co.uk/scholar?q=Bo%20Pang%20and%20Lillian%20Lee%20Opinion%20Mining%20and%20Sentiment%20Analysis%20volume%202%202008) [Scite](/scite_tallies?query=%5B6%5D%20Bo%20Pang%20and%20Lillian%20Lee.%20Opinion%20Mining%20and%20Sentiment%20Analysis%2C%20volume%202.%202008.)

[^7]: Apoorv Agarwal, Boyi Xie, Ilia Vovsha, Owen Rambow, and Rebecca Passonneau. Sentiment analysis of twitter data. In Proceedings of the Workshop on Languages in Social Media, LSM ’11, page 30–38, USA, 2011. Association for Computational Linguistics.  [OA](https://scholar.google.co.uk/scholar?q=Agarwal%2C%20Apoorv%20Xie%2C%20Boyi%20Vovsha%2C%20Ilia%20Rambow%2C%20Owen%20Sentiment%20analysis%20of%20twitter%20data%202011) [GScholar](https://scholar.google.co.uk/scholar?q=Agarwal%2C%20Apoorv%20Xie%2C%20Boyi%20Vovsha%2C%20Ilia%20Rambow%2C%20Owen%20Sentiment%20analysis%20of%20twitter%20data%202011) 

[^8]: Erik Cambria and Amir Hussain. Introduction, pages 1–21. Springer International Publishing, Cham, 2015.  [OA](https://scholar.google.co.uk/scholar?q=Cambria%2C%20Erik%20Hussain%2C%20Amir%20Introduction%202015) [GScholar](https://scholar.google.co.uk/scholar?q=Cambria%2C%20Erik%20Hussain%2C%20Amir%20Introduction%202015) 

[^9]: Pekka Malo, Ankur Sinha, Pekka Korhonen, Jyrki Wallenius, and Pyry Takala. Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and Technology, 65(4):782–796, 2014.  [OA](https://engine.scholarcy.com/oa_version?query=Malo%2C%20Pekka%20Sinha%2C%20Ankur%20Korhonen%2C%20Pekka%20Wallenius%2C%20Jyrki%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014&author=Malo&title=Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts&year=2014) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%2C%20Pekka%20Sinha%2C%20Ankur%20Korhonen%2C%20Pekka%20Wallenius%2C%20Jyrki%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%202014) [Scite](/scite_tallies?query=author%3AMalo%2Ctitle%3AGood%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%2Cyear%3A2014)

[^10]: Mathias Kraus and Stefan Feuerriegel. Decision support from financial disclosures with deep neural networks and transfer learning. Decision Support Systems, 104:38–48, December 2017.  [OA](https://engine.scholarcy.com/oa_version?query=Kraus%2C%20Mathias%20Feuerriegel%2C%20Stefan%20Decision%20support%20from%20financial%20disclosures%20with%20deep%20neural%20networks%20and%20transfer%20learning%202017-12&author=Kraus&title=Decision%20support%20from%20financial%20disclosures%20with%20deep%20neural%20networks%20and%20transfer%20learning&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Kraus%2C%20Mathias%20Feuerriegel%2C%20Stefan%20Decision%20support%20from%20financial%20disclosures%20with%20deep%20neural%20networks%20and%20transfer%20learning%202017-12) [Scite](/scite_tallies?query=author%3AKraus%2Ctitle%3ADecision%20support%20from%20financial%20disclosures%20with%20deep%20neural%20networks%20and%20transfer%20learning%2Cyear%3A2017)

[^11]: Sahar Sohangir, Dingding Wang, Anna Pomeranets, and Taghi M. Khoshgoftaar. Big data: Deep learning for financial sentiment analysis. Journal of Big Data, 5, 2018.  [OA](https://engine.scholarcy.com/oa_version?query=Sohangir%2C%20Sahar%20Wang%2C%20Dingding%20Pomeranets%2C%20Anna%20Khoshgoftaar%2C%20Taghi%20M.%20Big%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis%202018&author=Sohangir&title=Big%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Sohangir%2C%20Sahar%20Wang%2C%20Dingding%20Pomeranets%2C%20Anna%20Khoshgoftaar%2C%20Taghi%20M.%20Big%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis%202018) [Scite](/scite_tallies?query=author%3ASohangir%2Ctitle%3ABig%20data%3A%20Deep%20learning%20for%20financial%20sentiment%20analysis%2Cyear%3A2018)

[^12]: Bernhard Lutz, Nicolas Pröllochs, and Dirk Neumann. Sentence-level sentiment analysis of financial news using distributed text representations and multi-instance learning, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Lutz%2C%20Bernhard%20Pr%C3%B6llochs%2C%20Nicolas%20Neumann%2C%20Dirk%20Sentence-level%20sentiment%20analysis%20of%20financial%20news%20using%20distributed%20text%20representations%20and%20multi-instance%20learning%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Lutz%2C%20Bernhard%20Pr%C3%B6llochs%2C%20Nicolas%20Neumann%2C%20Dirk%20Sentence-level%20sentiment%20analysis%20of%20financial%20news%20using%20distributed%20text%20representations%20and%20multi-instance%20learning%202018) 

[^13]: Macedo Maia, André Freitas, and Siegfried Handschuh. Finsslx: A sentiment analysis model for the financial domain using text simplification. In 2018 IEEE 12th International Conference on Semantic Computing (ICSC), pages 318–319, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Maia%2C%20Macedo%20Freitas%2C%20Andr%C3%A9%20Handschuh%2C%20Siegfried%20Finsslx%3A%20A%20sentiment%20analysis%20model%20for%20the%20financial%20domain%20using%20text%20simplification%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Maia%2C%20Macedo%20Freitas%2C%20Andr%C3%A9%20Handschuh%2C%20Siegfried%20Finsslx%3A%20A%20sentiment%20analysis%20model%20for%20the%20financial%20domain%20using%20text%20simplification%202018) 

[^14]: Dogu Araci. Finbert: Financial sentiment analysis with pre-trained language models, 2019.  [OA](https://scholar.google.co.uk/scholar?q=Araci%2C%20Dogu%20Finbert%3A%20Financial%20sentiment%20analysis%20with%20pre-trained%20language%20models%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Araci%2C%20Dogu%20Finbert%3A%20Financial%20sentiment%20analysis%20with%20pre-trained%20language%20models%202019) 

[^15]: Yi Yang, Mark Christopher Siy UY, and Allen Huang. Finbert: A pretrained language model for financial communications, 2020.  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20Yi%20UY%2C%20Mark%20Christopher%20Siy%20Huang%2C%20Allen%20Finbert%3A%20A%20pretrained%20language%20model%20for%20financial%20communications%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Yi%20UY%2C%20Mark%20Christopher%20Siy%20Huang%2C%20Allen%20Finbert%3A%20A%20pretrained%20language%20model%20for%20financial%20communications%202020) 

[^16]: Binxia Yang, Xudong Luo, Kaili Sun, and Michael Y. Luo. Recent progress on text summarisation based on bert and gpt. In Zhi Jin, Yuncheng Jiang, Robert Andrei Buchmann, Yaxin Bi, Ana-Maria Ghiran, and Wenjun Ma, editors, Knowledge Science, Engineering and Management, pages 225–241, Cham, 2023. Springer Nature Switzerland.  [OA](https://scholar.google.co.uk/scholar?q=Yang%2C%20Binxia%20Luo%2C%20Xudong%20Sun%2C%20Kaili%20Luo%2C%20Michael%20Y.%20Recent%20progress%20on%20text%20summarisation%20based%20on%20bert%20and%20gpt%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Yang%2C%20Binxia%20Luo%2C%20Xudong%20Sun%2C%20Kaili%20Luo%2C%20Michael%20Y.%20Recent%20progress%20on%20text%20summarisation%20based%20on%20bert%20and%20gpt%202023) 

[^17]: Kiana Kheiri and Hamid Karimi. Sentimentgpt: Exploiting gpt for advanced sentiment analysis and its departure from current machine learning, 2023.  [OA](https://scholar.google.co.uk/scholar?q=Kheiri%2C%20Kiana%20Karimi%2C%20Hamid%20Sentimentgpt%3A%20Exploiting%20gpt%20for%20advanced%20sentiment%20analysis%20and%20its%20departure%20from%20current%20machine%20learning%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Kheiri%2C%20Kiana%20Karimi%2C%20Hamid%20Sentimentgpt%3A%20Exploiting%20gpt%20for%20advanced%20sentiment%20analysis%20and%20its%20departure%20from%20current%20machine%20learning%202023) 

[^18]: Jürgen Schmidhuber, Sepp Hochreiter, et al. Long short-term memory. Neural Comput, 9(8):1735–1780, 1997.  [OA](https://engine.scholarcy.com/oa_version?query=Schmidhuber%2C%20J%C3%BCrgen%20Hochreiter%2C%20Sepp%20Long%20short-term%20memory%201997&author=Schmidhuber&title=Long%20short-term%20memory&year=1997) [GScholar](https://scholar.google.co.uk/scholar?q=Schmidhuber%2C%20J%C3%BCrgen%20Hochreiter%2C%20Sepp%20Long%20short-term%20memory%201997) [Scite](/scite_tallies?query=author%3ASchmidhuber%2Ctitle%3ALong%20short-term%20memory%2Cyear%3A1997)

[^19]: Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, and Luke Zettlemoyer. Deep contextualized word representations. In Marilyn Walker, Heng Ji, and Amanda Stent, editors, Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), pages 2227–2237, New Orleans, Louisiana, June 2018.  [OA](https://scholar.google.co.uk/scholar?q=Peters%2C%20Matthew%20E.%20Neumann%2C%20Mark%20Iyyer%2C%20Mohit%20Gardner%2C%20Matt%20Deep%20contextualized%20word%20representations%202018-06) [GScholar](https://scholar.google.co.uk/scholar?q=Peters%2C%20Matthew%20E.%20Neumann%2C%20Mark%20Iyyer%2C%20Mohit%20Gardner%2C%20Matt%20Deep%20contextualized%20word%20representations%202018-06) 

[^20]: Association for Computational Linguistics.  [OA](https://scholar.google.co.uk/scholar?q=Association%20for%20Computational%20Linguistics) [GScholar](https://scholar.google.co.uk/scholar?q=Association%20for%20Computational%20Linguistics) 

[^20]: Jeremy Howard and Sebastian Ruder. Universal language model fine-tuning for text classification, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Howard%2C%20Jeremy%20Ruder%2C%20Sebastian%20Universal%20language%20model%20fine-tuning%20for%20text%20classification%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Howard%2C%20Jeremy%20Ruder%2C%20Sebastian%20Universal%20language%20model%20fine-tuning%20for%20text%20classification%202018) 

[^21]: Pekka Malo, Ankur Sinha, Pekka Korhonen, Jyrki Wallenius, and Pyry Takala. Good debt or bad debt: Detecting semantic orientations in economic texts. Journal of the Association for Information Science and  [OA](https://engine.scholarcy.com/oa_version?query=Malo%2C%20Pekka%20Sinha%2C%20Ankur%20Korhonen%2C%20Pekka%20Wallenius%2C%20Jyrki%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts&author=Malo&title=Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts&year=0000) [GScholar](https://scholar.google.co.uk/scholar?q=Malo%2C%20Pekka%20Sinha%2C%20Ankur%20Korhonen%2C%20Pekka%20Wallenius%2C%20Jyrki%20Good%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts) [Scite](/scite_tallies?query=author%3AMalo%2Ctitle%3AGood%20debt%20or%20bad%20debt%3A%20Detecting%20semantic%20orientations%20in%20economic%20texts%2Cyear%3A0000)

[^22]: Srikumar Krishnamoorthy. Sentiment analysis of financial news articles using performance indicators. Knowledge and Information Systems, 56(2):373–394, 2018. Generated on Wed Jan 10 15:16:54 2024 by LATExml   [OA](https://engine.scholarcy.com/oa_version?query=Krishnamoorthy%2C%20Srikumar%20Sentiment%20analysis%20of%20financial%20news%20articles%20using%20performance%20indicators%202018&author=Krishnamoorthy&title=Sentiment%20analysis%20of%20financial%20news%20articles%20using%20performance%20indicators&year=2018) [GScholar](https://scholar.google.co.uk/scholar?q=Krishnamoorthy%2C%20Srikumar%20Sentiment%20analysis%20of%20financial%20news%20articles%20using%20performance%20indicators%202018) [Scite](/scite_tallies?query=author%3AKrishnamoorthy%2Ctitle%3ASentiment%20analysis%20of%20financial%20news%20articles%20using%20performance%20indicators%2Cyear%3A2018)

