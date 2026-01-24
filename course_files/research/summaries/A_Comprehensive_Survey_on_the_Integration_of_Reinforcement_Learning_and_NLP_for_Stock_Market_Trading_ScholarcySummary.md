[[Ferrell_ComprehensiveSurveyIntegrationReinforcementLearning_2025]]

# [A Comprehensive Survey on the Integration of Reinforcement Learning and NLP for Stock Market Trading]()

## [[Brian J. Ferrell]]

## Abstract
The integration of Reinforcement Learning (RL) and Natural Language Processing (NLP) has emerged as a powerful approach in stock market trading, enabling agents to leverage both numerical and textual data for informed financial decision-making. Traditional strategies often overlook the contextual insights available in financial news, social media, and corporate disclosures. By combining RL’s iterative learning capabilities with NLP’s ability to process unstructured text, modern trading systems can potentially optimize for higher profitability and risk management. This survey synthesizes findings from 22 research papers published between 2018 and 2024, analyzing methodologies, data sources, evaluation metrics, and other relevant aspects within an integrated RL–NLP framework for stock trading. A detailed review of foundational RL and NLP concepts is provided to contextualize these advancements. Challenges such as the lack of standardized datasets, limited use of random seeds for reproducibility, the simplicity of state representations and NLP methods, insufficient evaluation procedures, and limited real-world adaptability are explored, alongside opportunities for future research, including leveraging large language models and advancing textually-aware RL systems. This study aims to offer a comprehensive resource for researchers and practitioners to advance the field of RL and NLP in financial decision-making.

## Key concepts
#st_v; #deep_reinforcement_learning; #natural_language_processing; #dynamic_programming; #deep_deterministic_policy_gradient; #reinforcement_learning

## Quote
The integration of Reinforcement Learning (RL) and Natural Language Processing (NLP) has emerged as a powerful approach in stock market trading, enabling agents to leverage both numerical and textual data for informed financial decision-making.

## Key points
- The integration of Reinforcement Learning (RL) and Natural Language Processing (NLP) represents a transformative approach in stock market trading, where decision-making is informed by both structured numerical data and unstructured textual information
- Throughout this section, we explored a range of RL algorithms, highlighting their diverse mechanisms, applications, and infinitely tunable parameters
- A critical distinction in RL is the timing of updates: whether they occur after every timestep, episode, or batch of episodes, which significantly impacts learning dynamics and stability
- Despite the stochastic nature of RL experiments, relatively few studies emphasized multiple random seed trials to ensure robust, reproducible results. These findings provide a structured view of how RL models for stock trading are trained and evaluated, highlighting the methodologies and tools employed across the reviewed literature
- Dynamic Evaluation Metrics: Develop evaluation metrics that balance risk and return based on specific trading styles, such as high-risk strategies or conservative portfolio management
- Sliding window attention operates within a block, random attention connects distant blocks, and global attention spans the entire sequence. This block sparse design ensures that the model maintains strong connectivity across the sequence while significantly reducing computational overhead
- Many existing studies could broaden their scope by experimenting with multiple RL architectures, adopting robust evaluation metrics, and ensuring reproducibility via multiple random seeds


## Summary

### Introduction
The integration of Reinforcement Learning (RL) and Natural Language Processing (NLP) has emerged as a powerful approach in stock market trading, enabling agents to leverage both numerical and textual data for informed financial decision-making.
This survey synthesizes findings from 22 research papers published between 2018 and 2024, analyzing methodologies, data sources, evaluation metrics, and other relevant aspects within an integrated RL–NLP framework for stock trading.

### Challenges
Challenges such as the lack of standardized datasets, limited use of random seeds for reproducibility, the simplicity of state representations and NLP methods, insufficient evaluation procedures, and limited real-world adaptability are explored.
The non-stationarity of financial markets, the inherent noise in textual data, and the high computational demands of these models create significant barriers to real-world adoption and generalization.

### Future Directions
Opportunities for future research include leveraging large language models and advancing textually-aware RL systems.
The survey aims to offer a comprehensive resource for researchers and practitioners to advance the field of RL and NLP in financial decision-making.
Future directions emphasize standardized evaluation metrics, systematic hyperparameter tuning, and the use of AutoML techniques to streamline RL model development and improve accessibility.
Future research directions in RL for financial markets include leveraging alternative data sources, such as text, improving generalization via transfer learning and meta-RL, and developing robust, interpretable, and reproducible RL frameworks.
The use of advanced RL techniques, such as hierarchical RL and meta-RL, is proposed to develop nuanced trading strategies.
Additionally, developing realistic market simulators, testing live-trading platforms, and understanding RL behavior in volatile markets are emerging priorities.

### RL Applications
The integration of sentiment analysis into Reinforcement Learning (RL) for financial trading is a growing trend, leveraging advanced NLP techniques such as Long Short-Term Memory (LSTM) networks and transformer models.
RL methods like Q-learning and Deep Q-Networks (DQN) dominate current applications, while Twin Delayed Deep Deterministic Policy Gradient (TD3) is identified as a promising algorithm for future sentiment-based trading systems.
The application of RL in financial markets includes portfolio management, algorithmic trading, and market making, with a focus on balancing profitability with risk management.

### RL Challenges
Challenges in RL applications in financial markets include the lack of standardized datasets, insufficient exploration of multi-agent scenarios, limited market realism in simulations, and underdeveloped ethical and regulatory frameworks.
The complexity of real-world environments, such as the stochastic nature of financial markets, makes them difficult to predict, making it challenging to train an RL agent.
Additionally, deploying a trained agent into a real-world trading system requires consideration of operational intricacies, including integration with real-time data streams and managing the potential market impact of trade execution.

### MDPs
Markov Decision Processes (MDPs) serve as the cornerstone mathematical framework for understanding and designing RL systems, offering a theoretical foundation for modeling decision-making in uncertain environments.
The Markov property states that the future depends only on the present, not the past, and is expressed as P[St+1|St] = P[St+1|S1, ..., St].
An MDP is characterized by a set of states S, a set of actions A, and a transition probability function P, which together describe the environment in which the agent operates.

### Value Functions
Value functions estimate the expected return from being in a given state or taking a specific action in that state, serving as a critical tool for evaluating the desirability of various states and actions.
The state value function, Vπ(s), calculates the expected return starting from state s and following a policy π, while the action value function, Qπ(s, a), evaluates the expected return after taking an action a in state s under the same policy.
The Bellman Equation represents the recursive relationships between value functions.

### RL Algorithms
Reinforcement Learning algorithms can be classified into two strategies: Dynamic Programming (DP) and Monte Carlo (MC) methods.
DP is used in environments where every aspect is completely known to compute optimal policies for finite MDPs, and involves two main phases: Policy Evaluation and Policy Improvement.
MC methods provide an alternative approach to solving RL problems and can be used to estimate the value functions and policies.

### Monte Carlo Methods
Monte Carlo methods estimate value functions without requiring a detailed model of the environment.
They rely on repeated sampling of complete interaction episodes to learn from empirical experience.
The value of a state is estimated as the average return observed across all visits to that state across multiple episodes.
This approach leverages the law of large numbers, ensuring that the estimated values converge to their true values with sufficient sampling.
Monte Carlo methods are particularly useful in environments with complex dynamics.

### Temporal-Difference Learning
Temporal-Difference (TD) learning combines the strengths of both Monte Carlo and Dynamic Programming methods.
Like Monte Carlo methods, TD learning does not require a model of the environment’s dynamics.
However, unlike Monte Carlo methods, TD learning incorporates the bootstrapping concept from Dynamic Programming, allowing it to update value estimates immediately.
TD methods update their estimates after observing the next state, leveraging the reward and the estimated value of the subsequent state.
This makes TD learning highly efficient for many real-world applications.

### Function Approximation
Function approximation methods are used to efficiently find near-optimal policies in environments with large or infinite state spaces.
These methods replace explicit tables with parameterized models, such as linear combinations of state features or deep neural networks.
Function approximation enables the model to represent a broad range of functions, allowing it to generalize effectively across large state spaces.
Deep Reinforcement Learning (DRL) has transformed RL applications by leveraging deep neural networks for function approximation, enabling RL systems to address challenges in high-dimensional and dynamic environments.

### Policy Optimization
Policy Optimization methods focus on directly optimizing the policy that the agent follows, rather than learning state/action value functions and deriving policies from them.
The policy is parameterized by θ and updated via gradient ascent to maximize expected return.
The policy gradient theorem provides a way to compute the gradient of the expected return with respect to the policy parameters.

### Policy Gradient Algorithms
Several policy gradient algorithms are discussed, including TRPO, PPO, and A3C/A2C.
TRPO restricts the update step to a "trust region" to ensure that the new policy does not deviate too much from the old policy.
PPO introduces a surrogate objective function that restricts the new policy from deviating too far from the old policy, using techniques such as PPO-Clip and PPO-Penalty.
A3C and A2C leverage parallel computing and efficient software engineering practices to update the policy.

### Q-Learning Algorithms
Q-learning methods focus on learning an approximate action-value function, Qθ(s, a), that converges to the optimal action-value function, Q*(s, a).
Deep Q-Network (DQN) is a popular Q-learning algorithm that combines Q-learning with deep neural networks to solve complex reinforcement learning problems.
DQN introduces two key mechanisms to stabilize training: experience replay and periodically updated target networks.
Other Q-learning algorithms, such as Double DQN, Dueling DQN, and Rainbow DQN, are also discussed.

### DQN
The Deep Q-Network (DQN) algorithm uses a loss function based on the mean-squared error between predicted and target Q-values.
The epsilon-greedy strategy balances exploration and exploitation.
DQN suffers from overestimation bias, which occurs when the max operator selects actions with overestimated Q-values due to noise and approximation errors.

### Double And Dueling DQN
Double DQN addresses overestimation bias by separating action selection from action evaluation using the target network.
Dueling DQN estimates the state value and the advantage function separately, enabling more efficient learning and better generalization.
The Dueling DQN architecture consists of two streams: the state value function V(s) and the advantage function A(s, a).

### Rainbow DQN
Rainbow DQN combines six extensions, including Double DQN, Dueling DQN, Prioritized Experience Replay, Multi-Step Learning, Distributional RL, and Noisy Nets.
Prioritized Experience Replay prioritizes experiences with higher learning potential, while Multi-Step Learning considers cumulative rewards over multiple steps.
Distributional RL models the entire distribution of returns, and Noisy Nets introduce parameterized noise into the network's weights for exploration.

### DDPG
DDPG updates its target networks gradually via Polyak averaging, which slowly updates the target values, providing greater stability during training.
Polyak averaging reduces the risk of divergence.
DDPG achieves exploration by adding noise directly to the actions suggested by the policy, originally using the Ornstein-Uhlenbeck process, but more recent results suggest that uncorrelated, mean-zero Gaussian noise is equally effective and simpler to implement.

### TD3
TD3 addresses the challenges of DDPG by introducing three key components: clipped double Q-learning, delayed policy updates, and target policy smoothing.
Clipped double Q-learning learns two Q-functions to reduce overestimation bias.
Delayed policy updates reduce volatility caused by rapid policy changes.
Target policy smoothing adds noise to the target actions, preventing the policy from overfitting to sharp peaks in the Q-function.

### SAC
SAC is an off-policy reinforcement learning algorithm that extends DDPG-style methods with a maximum entropy framework.
The key components of SAC include entropy regularization, clipped double Q-learning, and the reparameterization trick.
SAC enhances exploration by combining expected return maximization with entropy regularization.
The reparameterization trick allows for backpropagation through the policy's stochasticity, balancing reward maximization and exploration.

### RL Best Practices
Log arbitrary metrics and track detailed statistics on a per-step or per-episode basis.
Periodically visualize agent behavior to identify unexpected actions and learning anomalies.
Monitor loss curves to detect healthy learning patterns.
Normalization of inputs, rewards, and target values is critical in stabilizing training.
RL algorithms are highly sensitive to hyperparameters, and effective tuning strategies include random and grid search, as well as cyclical learning rates.
Designing effective reward functions and managing exploration-exploitation trade-offs are crucial for RL success.

### NLP Evolution
NLP has evolved from rule-based systems to sophisticated deep learning models, with key milestones including the introduction of statistical methods, word embeddings, and the Transformer architecture.
The Transformer revolutionized NLP with self-attention mechanisms and contextual embeddings, enabling large-scale pre-trained language models like BERT.
Today, NLP continues to evolve rapidly, driven by advancements in model architectures, optimization techniques, and the increasing availability of vast amounts of data.

### NLP Methods
Traditional methods in NLP include Bag-of-Words, TF-IDF, N-grams, and word embeddings like Word2Vec, GloVe, and FastText.
These methods remain relevant for information retrieval and preprocessing, especially when computational simplicity, interpretability, and low resource consumption are priorities.
Word embeddings capture the semantic meaning of words and their contextual relationships and have been further improved by the introduction of contextual embeddings and large language models like ChatGPT.

### Word Embeddings
FastText extends Word2Vec by incorporating subword information into word embeddings, enabling it to better capture word morphology and meaning.
This feature is especially useful for languages with complex forms or for small datasets, where rare words may not have sufficient representation.
Word2Vec, GloVe, and FastText improved on earlier methods by encoding semantic relationships, but are limited by their inability to capture a word's multiple meanings in context.

### Transformer Model
The Transformer model introduced self-attention mechanisms that dynamically adjust word representations based on their context within a sentence.
The model follows an encoder-decoder architecture, utilizing stacked self-attention layers and point-wise, fully connected layers for both the encoder and decoder.
The self-attention mechanism allows the model to weigh the importance of each word or token relative to others, capturing dependencies and relationships across the entire sequence.

### Attention Mechanism
The attention mechanism was introduced to address the limitations of sequence-to-sequence models in handling long-range dependencies.
The Transformer uses multi-head attention, running the self-attention mechanism multiple times in parallel, each with a different set of learned weights.
This allows the model to capture different types of relationships and patterns between words in parallel, ultimately enhancing the richness and quality of the word representations.
The self-attention layer assigns different weights to each word, determining how much focus each should receive based on its relevance to the current word.

### Model Architecture
The Transformer model uses 512-dimensional word embeddings, which are learned during training.
Each word is represented as a 512-dimensional vector that captures various aspects of the word.
The model processes input tokens in parallel, using positional encodings to capture the order of the words in a sentence.
The positional encodings have the same dimensionality as the word embeddings and are generated using sinusoidal functions.

### Training Process
The training process involves encoding the input sentence into contextual representations, decoding one word at a time, and predicting the next word in the target language by sampling from a target vocabulary.
The model continuously updates its weights based on feedback, improving prediction accuracy over time.
The process uses techniques such as teacher forcing, label smoothing, and beam search to improve performance.

### BERT And Variants
BERT (Bidirectional Encoder Representations from Transformers) is a variant of the Transformer model that uses bidirectional training of Transformer encoders and novel pre-training objectives.
BERT introduces Masked Language Modeling (MLM) and Next Sentence Prediction (NSP) tasks to improve upon bidirectional representation learning.
BERT comes in two main variants: BERTBASE and BERTLARGE, with different model capacities and computational expenses.
BERT's ability to be pre-trained on large amounts of text and later fine-tuned on specific downstream tasks makes it a highly versatile and efficient model for many NLP applications.

### Pre-training
BERT's pre-training involves two tasks: Masked Language Modeling (MLM) and Next Sentence Prediction (NSP).
In MLM, 15% of tokens are masked, and the model predicts them.
Of the masked tokens, 80% are replaced with the [MASK] token, 10% with a random token, and 10% remain unchanged.
NSP involves predicting whether two sentences are adjacent in the original text.
The input sequence includes a special [CLS] token at the beginning of the first sentence and a [SEP] token separating the two sentences.
The model is trained to predict whether the second sentence logically follows the first or is a random sentence.

### Model Variants
Several BERT variants have been developed to improve efficiency, model size, and representation capabilities.
DistilBERT is a lighter, faster variant of BERT created via knowledge distillation.
It has 40% fewer parameters and 60% faster inference times than BERT, while retaining approximately 97% of BERT's performance on the GLUE benchmark.
ALBERT reduces the number of parameters by sharing weights across layers and using factorized embeddings, making it highly parameter-efficient while achieving comparable or superior performance to BERT on many NLP benchmarks.

### Fine-tuning
After pre-training, BERT can be fine-tuned for specific downstream tasks such as question answering, text classification, or sentiment analysis.
Fine-tuning is relatively simple and cost-effective because BERT retains the general language understanding learned during pre-training.
The [CLS] token's output is used as the sequence's aggregate representation and passed through a task-specific classification layer.
The model can adapt quickly to new tasks because fine-tuning typically involves fewer steps than pre-training.

### Models
Longformer and BigBird are two models designed to address the limitations of traditional transformer models in processing long sequences.
Longformer modifies the self-attention mechanism to scale linearly with sequence length, while BigBird introduces a sparse attention mechanism that replaces quadratic complexity with linear complexity.
Both models achieve state-of-the-art results on tasks involving long documents.

### Attention Mechanisms
Longformer's attention mechanism includes sliding-window local attention, dilated sliding-window attention, and global attention for task-specific tokens.
These mechanisms enable the models to efficiently capture both local and global contextual information.

### Training And Representation
RoBERTa and DeBERTa are models that refine BERT's pre-training strategies, resulting in improved performance across various NLP benchmarks.
RoBERTa introduces dynamic masking, increased batch size, and an expanded vocabulary, while DeBERTa separates the representations of word meaning and position, allowing for disentangled attention and improved contextual understanding.
These refinements enable the models to outperform BERT on several NLP benchmarks.

### DeBERTa Model
DeBERTa captures nuanced relationships between words by combining three terms: content-to-content, content-to-position, and position-to-content.
This allows the model to effectively capture complex linguistic relationships, especially for tasks where word order and sentence structure are crucial.
DeBERTa also incorporates absolute positional embeddings in the mask decoder, enabling the model to leverage both content and absolute positional information of words to predict masked tokens.

### DeBERTa Variants
DeBERTa v2 introduces several structural and architectural refinements, including an expanded vocabulary size, n-gram induced encoding, shared content and position projection matrices, and bucketed relative position encoding.
DeBERTa v3 introduces notable improvements, including the Replaced Token Detection (RTD) objective, Gradient-Disentangled Embedding Sharing (GDES), and improved cross-lingual capabilities with multilingual DeBERTa (mDeBERTa).
These enhancements refine the model's training efficiency and generalization, providing a highly optimized architecture for natural language understanding tasks.

### Large Language Models
The field of NLP has experienced a transformative leap with the advent of Large Language Models (LLMs), which have achieved remarkable scalability and generative capabilities.
Models like OpenAI's GPT series, Meta's LLaMA, Google's PaLM, and Hugging Face's BLOOM have redefined the landscape, positioning LLMs as general-purpose AI systems capable of tackling tasks far beyond the scope of their predecessors.
These models have unlocked emergent abilities such as few-shot learning, step-by-step reasoning, and cross-domain generalization, and are becoming increasingly specialized and versatile.

### Optimization
Techniques like pruning, quantization, and knowledge distillation are critical for optimizing models, especially in edge deployments with limited memory, processing power, and energy efficiency.
Lightweight models such as DistilBERT and MobileBERT retain the performance of larger models while reducing size and power consumption.
Optimization techniques enable large language models (LLMs) to be deployed across diverse settings, from high-performance cloud environments to low-power edge devices.

### Adaptability
Pre-trained language models can be fine-tuned for specific tasks and domains, allowing them to specialize in tasks such as sentiment analysis, topic modeling, and named entity recognition.
Domain-specific fine-tuning further enhances this adaptability by training models on specialized datasets to address the unique challenges of particular industries.
Embeddings provide robust representations of language for downstream applications, enabling tasks such as semantic search, clustering, and topic modeling.

### Ethics
The increasing deployment of NLP models has brought concerns about biases inherent in these systems and their potential societal implications.
Addressing these biases requires a multifaceted approach, including fair data curation, adversarial training, and transparency and accountability in the responsible deployment of NLP models.
Prioritizing fairness and ethical practices is critical, especially in sensitive domains like hiring, healthcare, and law, where a precise understanding of specialized terminology is essential.

### Sentiment Analysis
Sentiment analysis is used to guide more profitable trading, with sentiment scores helping to make buy, sell, and hold decisions.
The sentiment classifier includes an embedding layer, a CNN, an LSTM, and an output layer for robust feature extraction and binary sentiment prediction.
VADER is used for sentiment polarity scoring, and sentiment analysis is integrated with price data using LSTMs.
Sentiment correlation signals are also used to enhance trading strategies.

### Reinforcement Learning
Reinforcement learning (RL) is used to develop trading systems, with various architectures such as DQN, DDPG, and PPO being employed.
The action space includes Buy, Sell, and Hold, with a focus on discounted rewards to optimize trading strategies.
RL is combined with sentiment analysis to automate and enhance portfolio decisions, outperforming traditional methods in returns and risk management.
The gradient of the expected reward with respect to the policy parameters θ is given by the expectation of the sum over all time steps of the return Ψt times the gradient of the log-probability of the action at given state st.
The objective function J(θ) represents the expected sum of future rewards from time step t onward.
The log-derivative trick is used to convert the gradient of the expectation into the expectation of the gradient, involving the log-probability of the policy.

### Trading Systems
Trading systems are developed using a combination of RL and sentiment analysis, with some systems incorporating additional features such as knowledge graphs, technical indicators, and news embeddings.
These systems are designed to improve trading performance and address challenges such as overfitting and market unpredictability.
The systems are evaluated using various metrics, including profit and loss, Sharpe ratios, and portfolio value, and are compared to baseline methods to demonstrate their effectiveness.

### Methods
Integrated frameworks improve profitability, risk management, and adaptability in stock trading.
Various baseline methods are considered, including regression, classification, ranking, and reinforcement learning (RL) models.
These models are compared to sentiment-free RL models and traditional methods, highlighting the benefits of integrated frameworks.
Different RL models are used, such as DQN, DDQN, and DDPG, and are compared to their community-aware sentiment-enhanced counterparts.

### Data
The input data for RL models in stock trading includes prices, portfolio data, technical indicators, sentiment from news articles or social media, and broader market signals.
Preprocessing techniques, such as normalization, tokenization, and sentiment scoring, are used to structure the data for integration into RL models.
Various data sources are employed, including Yahoo Finance, the stocknet-dataset, the China & Hong Kong dataset, and news data from Reuters, Bloomberg, and Twitter.

### Environment
The context of stock market trading varies depending on the exchanges, assets, and timeframes under consideration.
Different exchanges, such as NASDAQ, Shanghai, and Shenzhen, are used, and various stocks are traded, including AAPL, GOOG, and MSFT.
The frequency of the data also varies, with some studies using daily data and others using intraday data, such as minutes or hours.
The specific exchanges, stocks, and ticker data frequencies used in the reviewed papers are detailed in Table 4.

### Training Setups
The reviewed papers reveal common patterns in model training and evaluation, including the use of grid search for hyperparameter tuning, weight initialization methods, and learning rate schedulers.
Data preparation involves temporal splits, with training sets spanning several years of historical data and validation and test sets covering more recent periods.
Some studies use rolling-window approaches to split data into overlapping training and test sets.
Models incorporating sentiment analysis or prediction input stages usually follow a two-stage training process.

### Evaluation Metrics
The studies use a variety of financial and statistical metrics to evaluate the performance of RL models, including the Sharpe Ratio, Sortino Ratio, Cumulative Return, and Maximum Drawdown.
Additional metrics include Annualized Return, Final Portfolio Value, and Portfolio Value, which track changes in asset value over time.
Risk-related metrics, such as the Calmar Ratio and Mean Absolute Drawdown, are also reported.

### Challenges And Future Directions
The reviewed literature highlights several challenges, including data quality and preprocessing, algorithmic complexity, and evaluation methodologies.
Future research should prioritize advanced NLP techniques, such as transformer-based models, and experiment with multiple RL architectures.
The development of benchmark datasets and standardized evaluation frameworks is also crucial for advancing the field.
Additionally, incorporating richer data sources, such as macroeconomic indicators and high-frequency price data, can enhance the realism and robustness of trading simulations.

### Self-Attention Mechanism
The self-attention mechanism is used to build context-aware representations of words in a sentence.
It involves creating query, key, and value vectors for each word, calculating attention scores by taking the dot product of each word's query vector with every other word's key vector, and then using these scores to weight the value vectors.
The weighted value vectors are then summed to get the final representation for each word.

### Disentangled Attention Mechanism
The disentangled attention mechanism, used in DeBERTa, calculates attention scores by incorporating relative positions within a specified range and uses special embeddings for positions beyond that range.
It involves computing content queries, keys, and values, as well as position queries and keys, and then combining these to get the final attention scores.
This approach allows the model to focus on relevant nearby tokens while efficiently handling distant tokens.


## Study subjects

### 22 research papers
- By combining RL’s iterative learning capabilities with NLP’s ability to process unstructured text, modern trading systems can potentially optimize for higher profitability and risk management. This survey synthesizes findings from 22 research papers published between 2018 and 2024, analyzing methodologies, data sources, evaluation metrics, and other relevant aspects within an integrated RL–NLP framework for stock trading. A detailed review of foundational RL and NLP concepts is provided to contextualize these advancements

### 22 research papers
- Despite its simplicity, BoW can effectively capture the presence of important terms in text data and can be used in tasks like text classification/information retrieval [^66], and basic sentiment analysis, where context is less critical. This survey synthesizes findings from 22 research papers published from 2018 onward, including a few additions from 2024, to explore the integration of RL with NLP for stock market trading. The search strategy was carefully designed to ensure relevance and focus, employing Google Scholar with keywords such as "text embeddings reinforcement learning stock trading", "trading stocks ’reinforcement learning NLP," and "Deep Reinforcement Learning NLP Stock Trading."

## Data analysis
- #method/arg_max
- #method/monte_carlo_methods
- #method/welchs_t_test
- #method/finbert_model
- #method/conjugate_gradient_method
- #method/large_language_models
- #method/citation_baseline_methods
- #method/ddpg_algorithm
- #method/actor_critic_methods
- #method/dqn_algorithm

## Findings
- With 40% fewer parameters and 60% faster inference times than BERT, DistilBERT is optimized for resource-constrained environments, including mobile devices and on-device applications
- Specifically, sliding window attention operates within a block, random attention connects distant blocks, and global attention spans the entire sequence. <mark class="claim"><mark class="fact">This block sparse design ensures that the model maintains strong connectivity across the sequence</mark> while significantly reducing computational overhead</mark>

##  Builds on previous research
- In the case of this paper, for stock market trading, an agent may learn to execute buy, sell, or hold actions with the goal of maximizing financial returns or managing risk exposure. Here, the reward could be quantified through profit or another risk-adjusted performance metric [^18], [^19], [^20].

## Differs from previous work
- where Nt is the noise generated by the OU process. However, more recent results suggest that uncorrelated, mean-zero Gaussian noise is equally effective and much simpler to implement [^44].

## Contributions
- In summary, the training process involves encoding the input sentence into contextual representations, decoding one word at a time, and predicting the next word in the target language by sampling from a target vocabulary. The model continuously updates its weights based on feedback, improving the accuracy of predictions over time.

## Limitations
- Challenges such as the lack of standardized datasets, limited use of random seeds for reproducibility, the simplicity of state representations and NLP methods, insufficient evaluation procedures, and limited real-world adaptability are explored. Common gaps include the lack of standardized datasets, insufficient exploration of multi-agent scenarios, limited market realism in simulations, and underdeveloped ethical and regulatory frameworks.
- The limitations of the studies include the lack of standardization in evaluation methodologies, the omission of complexities such as transaction costs and liquidity constraints, and the need for more rigorous treatment of environmental complexities.
- The study acknowledges existing limitations in the field of NLP in financial decision-making.

## Future work
- Future research directions include exploring Transformer-based models for financial text, combining diverse data sources for robust predictions, and leveraging transfer learning for cross-market analysis. Future directions focus on advancing multi-agent RL (MARL) to model agent interactions in financial markets, extending Deep Reinforcement Learning (DRL) applications to practical trading environments, and integrating DRL with big data and AI platforms to enhance scalability and adaptability for tasks like investment research, risk management, and high-frequency trading.
- The future work includes exploring advanced NLP techniques, such as transformer-based models, experimenting with multiple RL architectures, and creating benchmark datasets for financial RL research.
- The study proposes directions for future research to advance RL-NLP systems in financial decision-making.


## References
[^1]: R. Sawhney, A. Wadhwa, S. Agarwal, R. Shah, Quantitative day trading from natural language using reinforcement learning, in: Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, 2021, pp. 4018–4030.  [OA](https://scholar.google.co.uk/scholar?q=Sawhney%2C%20R.%20Wadhwa%2C%20A.%20Agarwal%2C%20S.%20Shah%2C%20R.%20Quantitative%20day%20trading%20from%20natural%20language%20using%20reinforcement%20learning%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Sawhney%2C%20R.%20Wadhwa%2C%20A.%20Agarwal%2C%20S.%20Shah%2C%20R.%20Quantitative%20day%20trading%20from%20natural%20language%20using%20reinforcement%20learning%202021) 

[^2]: B. Hambly, R. Xu, H. Yang, Recent advances in reinforcement learning in finance, Mathematical Finance 33 (2023) 437–503.  [OA](https://engine.scholarcy.com/oa_version?query=Hambly%2C%20B.%20Xu%2C%20R.%20Yang%2C%20H.%20Recent%20advances%20in%20reinforcement%20learning%20in%20finance%202023&author=Hambly&title=Recent%20advances%20in%20reinforcement%20learning%20in%20finance&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Hambly%2C%20B.%20Xu%2C%20R.%20Yang%2C%20H.%20Recent%20advances%20in%20reinforcement%20learning%20in%20finance%202023) [Scite](/scite_tallies?query=author%3AHambly%2Ctitle%3ARecent%20advances%20in%20reinforcement%20learning%20in%20finance%2Cyear%3A2023)

[^3]: B. Huang, Y. Huan, L. D. Xu, L. Zheng, Z. Zou, Automated trading systems, statistical and machine learning methods, and hardware implementation: a survey, Enterprise Information Systems 13 (2019) 132–144.  [OA](https://engine.scholarcy.com/oa_version?query=Huang%2C%20B.%20Huan%2C%20Y.%20Xu%2C%20L.D.%20Zheng%2C%20L.%20Automated%20trading%20systems%20statistical%20and%20machine%20learning%20methods%20and%20hardware%20implementation%3A%20a%20survey%202019&author=Huang&title=Automated%20trading%20systems%20statistical%20and%20machine%20learning%20methods%20and%20hardware%20implementation%3A%20a%20survey&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20B.%20Huan%2C%20Y.%20Xu%2C%20L.D.%20Zheng%2C%20L.%20Automated%20trading%20systems%20statistical%20and%20machine%20learning%20methods%20and%20hardware%20implementation%3A%20a%20survey%202019) [Scite](/scite_tallies?query=author%3AHuang%2Ctitle%3AAutomated%20trading%20systems%20statistical%20and%20machine%20learning%20methods%20and%20hardware%20implementation%3A%20a%20survey%2Cyear%3A2019)

[^4]: L. Kanashiro Felizardo, F. Caio Lima Paiva, A. H. Reali Costa, E. Del-Moral-Hernandez, Reinforcement learning applied to trading systems: A survey, arXiv e-prints (2022) arXiv–2212.  [OA](https://scholar.google.co.uk/scholar?q=Felizardo%2C%20L.Kanashiro%20Paiva%2C%20F.Caio%20Lima%20Costa%2C%20A.H.Reali%20Del-Moral-Hernandez%2C%20E.%20Reinforcement%20learning%20applied%20to%20trading%20systems%3A%20A%20survey%2C%20arXiv%20e-prints%202022) [GScholar](https://scholar.google.co.uk/scholar?q=Felizardo%2C%20L.Kanashiro%20Paiva%2C%20F.Caio%20Lima%20Costa%2C%20A.H.Reali%20Del-Moral-Hernandez%2C%20E.%20Reinforcement%20learning%20applied%20to%20trading%20systems%3A%20A%20survey%2C%20arXiv%20e-prints%202022) 

[^5]: R. Sawhney, A. Wadhwa, S. Agarwal, R. Shah, Fast: Financial news and tweet-based time-aware network for stock trading, in: Proceedings of the 16th conference of the European Chapter of the Association for Computational Linguistics: main volume, 2021, pp. 2164–2175.  [OA](https://scholar.google.co.uk/scholar?q=Sawhney%2C%20R.%20Wadhwa%2C%20A.%20Agarwal%2C%20S.%20Shah%2C%20R.%20Fast%3A%20Financial%20news%20and%20tweet%20based%20time%20aware%20network%20for%20stock%20trading%202021) [GScholar](https://scholar.google.co.uk/scholar?q=Sawhney%2C%20R.%20Wadhwa%2C%20A.%20Agarwal%2C%20S.%20Shah%2C%20R.%20Fast%3A%20Financial%20news%20and%20tweet%20based%20time%20aware%20network%20for%20stock%20trading%202021) 

[^6]: N. E. Huang, M.-L. Wu, W. Qu, S. R. Long, S. S. Shen, Applications of Hilbert–Huang transform to non-stationary financial time series analysis, Applied stochastic models in business and industry 19 (2003) 245–268.  [OA](https://engine.scholarcy.com/oa_version?query=Huang%2C%20N.E.%20Wu%2C%20M.-L.%20Qu%2C%20W.%20Long%2C%20S.R.%20Applications%20of%20hilbert%E2%80%93huang%20transform%20to%20non-stationary%20financial%20time%20series%20analysis%202003&author=Huang&title=Applications%20of%20hilbert%E2%80%93huang%20transform%20to%20non-stationary%20financial%20time%20series%20analysis&year=2003) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20N.E.%20Wu%2C%20M.-L.%20Qu%2C%20W.%20Long%2C%20S.R.%20Applications%20of%20hilbert%E2%80%93huang%20transform%20to%20non-stationary%20financial%20time%20series%20analysis%202003) [Scite](/scite_tallies?query=author%3AHuang%2Ctitle%3AApplications%20of%20hilbert%E2%80%93huang%20transform%20to%20non-stationary%20financial%20time%20series%20analysis%2Cyear%3A2003)

[^7]: H. Xu, L. Chai, Z. Luo, S. Li, Stock movement prediction via gated recurrent unit network based on reinforcement learning with incorporated attention mechanisms, Neurocomputing 467 (2022) 214–228.  [OA](https://engine.scholarcy.com/oa_version?query=Xu%2C%20H.%20Chai%2C%20L.%20Luo%2C%20Z.%20Li%2C%20S.%20Stock%20movement%20prediction%20via%20gated%20recurrent%20unit%20network%20based%20on%20reinforcement%20learning%20with%20incorporated%20attention%20mechanisms%202022&author=Xu&title=Stock%20movement%20prediction%20via%20gated%20recurrent%20unit%20network%20based%20on%20reinforcement%20learning%20with%20incorporated%20attention%20mechanisms&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Xu%2C%20H.%20Chai%2C%20L.%20Luo%2C%20Z.%20Li%2C%20S.%20Stock%20movement%20prediction%20via%20gated%20recurrent%20unit%20network%20based%20on%20reinforcement%20learning%20with%20incorporated%20attention%20mechanisms%202022) [Scite](/scite_tallies?query=author%3AXu%2Ctitle%3AStock%20movement%20prediction%20via%20gated%20recurrent%20unit%20network%20based%20on%20reinforcement%20learning%20with%20incorporated%20attention%20mechanisms%2Cyear%3A2022)

[^8]: W. Dabney, G. Ostrovski, A. Barreto, Temporally-extended {∖epsilon}-greedy exploration, arXiv preprint arXiv:2006.01782 (2020).  [OA](https://arxiv.org/abs/2006.01782)  

[^9]: A. Millea, Deep reinforcement learning for trading—a critical survey, Data 6 (2021) 119.  [OA](https://engine.scholarcy.com/oa_version?query=Millea%2C%20A.%20Deep%20reinforcement%20learning%20for%20trading%E2%80%94a%20critical%20survey%202021&author=Millea&title=Deep%20reinforcement%20learning%20for%20trading%E2%80%94a%20critical%20survey&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Millea%2C%20A.%20Deep%20reinforcement%20learning%20for%20trading%E2%80%94a%20critical%20survey%202021) [Scite](/scite_tallies?query=author%3AMillea%2Ctitle%3ADeep%20reinforcement%20learning%20for%20trading%E2%80%94a%20critical%20survey%2Cyear%3A2021)

[^10]: S. Sun, R. Wang, B. An, Reinforcement learning for quantitative trading, ACM Transactions on Intelligent Systems and Technology 14 (2023) 1–29.  [OA](https://engine.scholarcy.com/oa_version?query=Sun%2C%20S.%20Wang%2C%20R.%20An%2C%20B.%20Reinforcement%20learning%20for%20quantitative%20trading%202023&author=Sun&title=Reinforcement%20learning%20for%20quantitative%20trading&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Sun%2C%20S.%20Wang%2C%20R.%20An%2C%20B.%20Reinforcement%20learning%20for%20quantitative%20trading%202023) [Scite](/scite_tallies?query=author%3ASun%2Ctitle%3AReinforcement%20learning%20for%20quantitative%20trading%2Cyear%3A2023)

[^11]: V. Singh, S.-S. Chen, M. Singhania, B. Nanavati, A. Gupta, et al., How are reinforcement learning and deep learning algorithms used for big data-based decision making in financial industries–a review and research agenda, International Journal of Information Management Data Insights 2 (2022) 100094.  [OA](https://engine.scholarcy.com/oa_version?query=Singh%2C%20V.%20Chen%2C%20S.-S.%20Singhania%2C%20M.%20Nanavati%2C%20B.%20How%20are%20reinforcement%20learning%20and%20deep%20learning%20algorithms%20used%20for%20big%20data%20based%20decision%20making%20in%20financial%20industries%E2%80%93a%20review%20and%20research%20agenda%202022&author=Singh&title=How%20are%20reinforcement%20learning%20and%20deep%20learning%20algorithms%20used%20for%20big%20data%20based%20decision%20making%20in%20financial%20industries%E2%80%93a%20review%20and%20research%20agenda&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Singh%2C%20V.%20Chen%2C%20S.-S.%20Singhania%2C%20M.%20Nanavati%2C%20B.%20How%20are%20reinforcement%20learning%20and%20deep%20learning%20algorithms%20used%20for%20big%20data%20based%20decision%20making%20in%20financial%20industries%E2%80%93a%20review%20and%20research%20agenda%202022) [Scite](/scite_tallies?query=author%3ASingh%2Ctitle%3AHow%20are%20reinforcement%20learning%20and%20deep%20learning%20algorithms%20used%20for%20big%20data%20based%20decision%20making%20in%20financial%20industries%E2%80%93a%20review%20and%20research%20agenda%2Cyear%3A2022)

[^12]: W. Jiang, Applications of deep learning in stock market prediction: recent progress, Expert Systems with Applications 184 (2021) 115537.  [OA](https://engine.scholarcy.com/oa_version?query=Jiang%2C%20W.%20Applications%20of%20deep%20learning%20in%20stock%20market%20prediction%3A%20recent%20progress%202021&author=Jiang&title=Applications%20of%20deep%20learning%20in%20stock%20market%20prediction%3A%20recent%20progress&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Jiang%2C%20W.%20Applications%20of%20deep%20learning%20in%20stock%20market%20prediction%3A%20recent%20progress%202021) [Scite](/scite_tallies?query=author%3AJiang%2Ctitle%3AApplications%20of%20deep%20learning%20in%20stock%20market%20prediction%3A%20recent%20progress%2Cyear%3A2021)

[^13]: P. C. Soon, T.-P. Tan, H. Y. Chan, K. H. Gan, A review on sentiment analysis in reinforcement learning model for stock market analysis, International Journal of Asian Language Processing 32 (2022) 2330001.  [OA](https://engine.scholarcy.com/oa_version?query=Soon%2C%20P.C.%20Tan%2C%20T.-P.%20Chan%2C%20H.Y.%20Gan%2C%20K.H.%20A%20review%20on%20sentiment%20analysis%20in%20reinforcement%20learning%20model%20for%20stock%20market%20analysis%202022&author=Soon&title=A%20review%20on%20sentiment%20analysis%20in%20reinforcement%20learning%20model%20for%20stock%20market%20analysis&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Soon%2C%20P.C.%20Tan%2C%20T.-P.%20Chan%2C%20H.Y.%20Gan%2C%20K.H.%20A%20review%20on%20sentiment%20analysis%20in%20reinforcement%20learning%20model%20for%20stock%20market%20analysis%202022) [Scite](/scite_tallies?query=author%3ASoon%2Ctitle%3AA%20review%20on%20sentiment%20analysis%20in%20reinforcement%20learning%20model%20for%20stock%20market%20analysis%2Cyear%3A2022)

[^14]: S. K. Sahu, A. Mokhade, N. D. Bokde, An overview of machine learning, deep learning, and reinforcement learning-based techniques in quantitative finance: recent progress and challenges, Applied Sciences 13 (2023) 1956.  [OA](https://engine.scholarcy.com/oa_version?query=Sahu%2C%20S.K.%20Mokhade%2C%20A.%20Bokde%2C%20N.D.%20An%20overview%20of%20machine%20learning%2C%20deep%20learning%2C%20and%20reinforcement%20learning-based%20techniques%20in%20quantitative%20finance%3A%20recent%20progress%20and%20challenges%202023&author=Sahu&title=An%20overview%20of%20machine%20learning%2C%20deep%20learning%2C%20and%20reinforcement%20learning-based%20techniques%20in%20quantitative%20finance%3A%20recent%20progress%20and%20challenges&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Sahu%2C%20S.K.%20Mokhade%2C%20A.%20Bokde%2C%20N.D.%20An%20overview%20of%20machine%20learning%2C%20deep%20learning%2C%20and%20reinforcement%20learning-based%20techniques%20in%20quantitative%20finance%3A%20recent%20progress%20and%20challenges%202023) [Scite](/scite_tallies?query=author%3ASahu%2Ctitle%3AAn%20overview%20of%20machine%20learning%2C%20deep%20learning%2C%20and%20reinforcement%20learning-based%20techniques%20in%20quantitative%20finance%3A%20recent%20progress%20and%20challenges%2Cyear%3A2023)

[^15]: T. G. Fischer, Reinforcement learning in financial markets-a survey, Technical Report, FAU discussion papers in economics, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Fischer%2C%20T.G.%20Reinforcement%20learning%20in%20financial%20markets-a%20survey%2C%20Technical%20Report%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Fischer%2C%20T.G.%20Reinforcement%20learning%20in%20financial%20markets-a%20survey%2C%20Technical%20Report%202018) 

[^16]: R. S. Sutton, A. G. Barto, Reinforcement learning: An introduction, MIT Press, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Sutton%2C%20R.S.%20Barto%2C%20A.G.%20Reinforcement%20learning%3A%20An%20introduction%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Sutton%2C%20R.S.%20Barto%2C%20A.G.%20Reinforcement%20learning%3A%20An%20introduction%202018) 

[^17]: L. Weng, An overview of reinforcement learning: Theory and applications, Blog post, 2018. URL: https://lilianweng.github.io/posts/2018-02-19-rl-overview/.  [OA](https://lilianweng.github.io/posts/2018-02-19-rl-overview/)  

[^18]: J. Moody, L. Wu, Y. Liao, M. Saffell, Performance functions and reinforcement learning for trading systems and portfolios, Journal of forecasting 17 (1998) 441–470.  [OA](https://engine.scholarcy.com/oa_version?query=Moody%2C%20J.%20Wu%2C%20L.%20Liao%2C%20Y.%20Saffell%2C%20M.%20Performance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998&author=Moody&title=Performance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios&year=1998) [GScholar](https://scholar.google.co.uk/scholar?q=Moody%2C%20J.%20Wu%2C%20L.%20Liao%2C%20Y.%20Saffell%2C%20M.%20Performance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998) [Scite](/scite_tallies?query=author%3AMoody%2Ctitle%3APerformance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%2Cyear%3A1998)

[^19]: J. E. Moody, M. Saffell, Y. Liao, L. Wu, Reinforcement learning for trading systems and portfolios., in: KDD, 1998, pp. 279–283.  [OA](https://scholar.google.co.uk/scholar?q=Moody%2C%20J.E.%20Saffell%2C%20M.%20Liao%2C%20Y.%20Wu%2C%20L.%20Reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998) [GScholar](https://scholar.google.co.uk/scholar?q=Moody%2C%20J.E.%20Saffell%2C%20M.%20Liao%2C%20Y.%20Wu%2C%20L.%20Reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998) 

[^20]: J. Sadighian, Extending deep reinforcement learning frameworks in cryptocurrency market making, arXiv preprint arXiv:2004.06985 (2020).  [OA](https://arxiv.org/abs/2004.06985)  

[^21]: N.-F. Chen, R. Roll, S. A. Ross, Economic forces and the stock market, Journal of business (1986) 383–403.  [OA](https://engine.scholarcy.com/oa_version?query=Chen%2C%20N.-F.%20Roll%2C%20R.%20Ross%2C%20S.A.%20Economic%20forces%20and%20the%20stock%20market%201986&author=Chen&title=Economic%20forces%20and%20the%20stock%20market&year=1986) [GScholar](https://scholar.google.co.uk/scholar?q=Chen%2C%20N.-F.%20Roll%2C%20R.%20Ross%2C%20S.A.%20Economic%20forces%20and%20the%20stock%20market%201986) [Scite](/scite_tallies?query=author%3AChen%2Ctitle%3AEconomic%20forces%20and%20the%20stock%20market%2Cyear%3A1986)

[^22]: S. R. Parvin, N. Panakaje, Factors influencing stock market participation: A review, International Journal of Case Studies in Business, IT and Education (IJCSBE) 6 (2022) 831–861.  [OA](https://engine.scholarcy.com/oa_version?query=Parvin%2C%20S.R.%20Panakaje%2C%20N.%20Factors%20influencing%20stock%20market%20participation%3A%20A%20review%202022&author=Parvin&title=Factors%20influencing%20stock%20market%20participation%3A%20A%20review&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Parvin%2C%20S.R.%20Panakaje%2C%20N.%20Factors%20influencing%20stock%20market%20participation%3A%20A%20review%202022) [Scite](/scite_tallies?query=author%3AParvin%2Ctitle%3AFactors%20influencing%20stock%20market%20participation%3A%20A%20review%2Cyear%3A2022)

[^23]: A. Mahida, Reinforcement learning for real-world applications-a comprehensive review (2019).  [OA](https://scholar.google.co.uk/scholar?q=Mahida%2C%20A.%20Reinforcement%20learning%20for%20real-world%20applications-a%20comprehensive%20review%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Mahida%2C%20A.%20Reinforcement%20learning%20for%20real-world%20applications-a%20comprehensive%20review%202019) 

[^24]: C. J. Watkins, P. Dayan, Q-learning, Machine learning 8 (1992) 279–292.  [OA](https://scholar.google.co.uk/scholar?q=C%20J%20Watkins%20P%20Dayan%20Qlearning%20Machine%20learning%208%201992%20279292) [GScholar](https://scholar.google.co.uk/scholar?q=C%20J%20Watkins%20P%20Dayan%20Qlearning%20Machine%20learning%208%201992%20279292) 

[^25]: H. R. Maei, C. Szepesvári, S. Bhatnagar, R. S. Sutton, Toward off-policy learning control with function approximation, in: ICML, volume 10, 2010, pp. 719–726.  [OA](https://scholar.google.co.uk/scholar?q=Maei%2C%20H.R.%20Szepesv%C3%A1ri%2C%20C.%20Bhatnagar%2C%20S.%20Sutton%2C%20R.S.%20Toward%20off-policy%20learning%20control%20with%20function%20approximation%202010) [GScholar](https://scholar.google.co.uk/scholar?q=Maei%2C%20H.R.%20Szepesv%C3%A1ri%2C%20C.%20Bhatnagar%2C%20S.%20Sutton%2C%20R.S.%20Toward%20off-policy%20learning%20control%20with%20function%20approximation%202010) 

[^26]: S. Bhatnagar, R. S. Sutton, M. Ghavamzadeh, M. Lee, Naturalgradient actor-critic algorithms, Automatica  [OA](https://scholar.google.co.uk/scholar?q=Bhatnagar%2C%20S.%20Sutton%2C%20R.S.%20Ghavamzadeh%2C%20M.%20Lee%2C%20M.%20Naturalgradient%20actor-critic%20algorithms) [GScholar](https://scholar.google.co.uk/scholar?q=Bhatnagar%2C%20S.%20Sutton%2C%20R.S.%20Ghavamzadeh%2C%20M.%20Lee%2C%20M.%20Naturalgradient%20actor-critic%20algorithms) 

[^27]: J. Schulman, P. Moritz, S. Levine, M. Jordan, P. Abbeel, High-dimensional continuous control using generalized advantage estimation, arXiv preprint arXiv:1506.02438 (2015).  [OA](https://arxiv.org/abs/1506.02438)  

[^28]: J. Schulman, S. Levine, P. Abbeel, M. Jordan, P. Moritz, Trust region policy optimization, in: International conference on machine learning, PMLR, 2015, pp. 1889–1897.  [OA](https://scholar.google.co.uk/scholar?q=Schulman%2C%20J.%20Levine%2C%20S.%20Abbeel%2C%20P.%20Jordan%2C%20M.%20Trust%20region%20policy%20optimization%202015) [GScholar](https://scholar.google.co.uk/scholar?q=Schulman%2C%20J.%20Levine%2C%20S.%20Abbeel%2C%20P.%20Jordan%2C%20M.%20Trust%20region%20policy%20optimization%202015) 

[^29]: J. Achiam, Advanced policy gradient methods, Berkeley, RAIL Lab, 2017. URL: http://rail.eecs.berkeley.  [OA](http://rail.eecs.berkeley)  

[^30]: OpenAI, Trpo - spinning up documentation, Blog post, 2019. URL: https://spinningup.openai.com/en/  [OA](https://spinningup.openai.com/en/)  

[^31]: J. Schulman, F. Wolski, P. Dhariwal, A. Radford, O. Klimov, Proximal policy optimization algorithms, arXiv preprint arXiv:1707.06347 (2017).  [OA](https://arxiv.org/abs/1707.06347)  

[^32]: OpenAI, Ppo - spinning up documentation, Blog post, 2019. URL: https://spinningup.openai.com/en/  [OA](https://spinningup.openai.com/en/)  

[^33]: V. Mnih, A. P. Badia, M. Mirza, A. Graves, T. Lillicrap, T. Harley, D. Silver, K. Kavukcuoglu, Asynchronous methods for deep reinforcement learning, in: International conference on machine learning, PMLR, 2016, pp. 1928–1937.  [OA](https://scholar.google.co.uk/scholar?q=Mnih%2C%20V.%20Badia%2C%20A.P.%20Mirza%2C%20M.%20Graves%2C%20A.%20Asynchronous%20methods%20for%20deep%20reinforcement%20learning%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Mnih%2C%20V.%20Badia%2C%20A.P.%20Mirza%2C%20M.%20Graves%2C%20A.%20Asynchronous%20methods%20for%20deep%20reinforcement%20learning%202016) 

[^34]: V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. Riedmiller, A. K. Fidjeland, G. Ostrovski, et al., Human-level control through deep reinforcement learning, Nature 518 (2015) 529–533.  [OA](https://engine.scholarcy.com/oa_version?query=Mnih%2C%20V.%20Kavukcuoglu%2C%20K.%20Silver%2C%20D.%20Rusu%2C%20A.A.%20Human-level%20control%20through%20deep%20reinforcement%20learning%202015&author=Mnih&title=Human-level%20control%20through%20deep%20reinforcement%20learning&year=2015) [GScholar](https://scholar.google.co.uk/scholar?q=Mnih%2C%20V.%20Kavukcuoglu%2C%20K.%20Silver%2C%20D.%20Rusu%2C%20A.A.%20Human-level%20control%20through%20deep%20reinforcement%20learning%202015) [Scite](/scite_tallies?query=author%3AMnih%2Ctitle%3AHuman-level%20control%20through%20deep%20reinforcement%20learning%2Cyear%3A2015)

[^35]: V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wierstra, M. Riedmiller, Playing atari with deep reinforcement learning, arXiv preprint arXiv:1312.5602 (2013).  [OA](https://arxiv.org/abs/1312.5602)  

[^36]: H. Van Hasselt, A. Guez, D. Silver, Deep reinforcement learning with double Q-learning, in: Proceedings of the AAAI conference on artificial intelligence, volume 30, 2016.  [OA](https://scholar.google.co.uk/scholar?q=Hasselt%2C%20H.%20Guez%2C%20A.%20Silver%2C%20D.%20Deep%20reinforcement%20learning%20with%20double%20q-learning%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Hasselt%2C%20H.%20Guez%2C%20A.%20Silver%2C%20D.%20Deep%20reinforcement%20learning%20with%20double%20q-learning%202016) 

[^37]: Z. Wang, T. Schaul, M. Hessel, H. Hasselt, M. Lanctot, N. Freitas, Dueling network architectures for deep reinforcement learning, in: International conference on machine learning, PMLR, 2016, pp. 1995–2003.  [OA](https://scholar.google.co.uk/scholar?q=Wang%2C%20Z.%20Schaul%2C%20T.%20Hessel%2C%20M.%20Hasselt%2C%20H.%20Dueling%20network%20architectures%20for%20deep%20reinforcement%20learning%202016) [GScholar](https://scholar.google.co.uk/scholar?q=Wang%2C%20Z.%20Schaul%2C%20T.%20Hessel%2C%20M.%20Hasselt%2C%20H.%20Dueling%20network%20architectures%20for%20deep%20reinforcement%20learning%202016) 

[^38]: M. Hessel, J. Modayil, H. Van Hasselt, T. Schaul, G. Ostrovski, W. Dabney, D. Horgan, B. Piot, M. Azar, D. Silver, Rainbow: Combining improvements in deep reinforcement learning, in: Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Hessel%2C%20M.%20Modayil%2C%20J.%20Hasselt%2C%20H.%20Schaul%2C%20T.%20Rainbow%3A%20Combining%20improvements%20in%20deep%20reinforcement%20learning%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Hessel%2C%20M.%20Modayil%2C%20J.%20Hasselt%2C%20H.%20Schaul%2C%20T.%20Rainbow%3A%20Combining%20improvements%20in%20deep%20reinforcement%20learning%202018) 

[^39]: T. Schaul, J. Quan, I. Antonoglou, D. Silver, Prioritized experience replay, arXiv preprint arXiv:1511.05952 (2015).  [OA](https://arxiv.org/abs/1511.05952)  

[^40]: J. Weng, H. Chen, D. Yan, K. You, A. Duburcq, M. Zhang, Y. Su, H. Su, J. Zhu, Tianshou: A highly modularized deep reinforcement learning library, Journal of Machine Learning Research 23 (2022) 1–6. URL: http://jmlr.org/papers/v23/21-1127.html.  [OA](http://jmlr.org/papers/v23/21-1127.html)  [Scite](/scite_tallies?query=author%3AWeng%2Ctitle%3ATianshou%3A%20A%20highly%20modularized%20deep%20reinforcement%20learning%20library%2Cyear%3A2022)

[^41]: M. G. Bellemare, W. Dabney, R. Munos, A distributional perspective on reinforcement learning, in: International conference on machine learning, PMLR, 2017, pp. 449–458.  [OA](https://scholar.google.co.uk/scholar?q=Bellemare%2C%20M.G.%20Dabney%2C%20W.%20Munos%2C%20R.%20A%20distributional%20perspective%20on%20reinforcement%20learning%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Bellemare%2C%20M.G.%20Dabney%2C%20W.%20Munos%2C%20R.%20A%20distributional%20perspective%20on%20reinforcement%20learning%202017) 

[^42]: T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, D. Wierstra, Continuous control with deep reinforcement learning, arXiv preprint arXiv:1509.02971 (2015).  [OA](https://arxiv.org/abs/1509.02971)  

[^43]: D. Silver, G. Lever, N. Heess, T. Degris, D. Wierstra, M. Riedmiller, Deterministic policy gradient algorithms, in: International conference on machine learning, Pmlr, 2014, pp. 387–395.  [OA](https://scholar.google.co.uk/scholar?q=Silver%2C%20D.%20Lever%2C%20G.%20Heess%2C%20N.%20Degris%2C%20T.%20Deterministic%20policy%20gradient%20algorithms%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Silver%2C%20D.%20Lever%2C%20G.%20Heess%2C%20N.%20Degris%2C%20T.%20Deterministic%20policy%20gradient%20algorithms%202014) 

[^44]: OpenAI, Trpo - spinning up documentation, Blog post, 2018. URL: https://spinningup.openai.com/en/latest/algorithms/ddpg.html.  [OA](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)  

[^45]: S. Fujimoto, H. Hoof, D. Meger, Addressing function approximation error in actor-critic methods, in: International conference on machine learning, PMLR, 2018, pp. 1587–1596.  [OA](https://scholar.google.co.uk/scholar?q=Fujimoto%2C%20S.%20Hoof%2C%20H.%20Meger%2C%20D.%20Addressing%20function%20approximation%20error%20in%20actor-critic%20methods%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Fujimoto%2C%20S.%20Hoof%2C%20H.%20Meger%2C%20D.%20Addressing%20function%20approximation%20error%20in%20actor-critic%20methods%202018) 

[^46]: OpenAI, Td3 - spinning up documentation, Blog post, 2018. URL: https://spinningup.openai.com/en/latest/algorithms/td3.html.  [OA](https://spinningup.openai.com/en/latest/algorithms/td3.html)  

[^47]: T. Haarnoja, A. Zhou, P. Abbeel, S. Levine, Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor, in: International conference on machine learning, PMLR, 2018, pp. 1861–1870.  [OA](https://scholar.google.co.uk/scholar?q=Haarnoja%2C%20T.%20Zhou%2C%20A.%20Abbeel%2C%20P.%20Levine%2C%20S.%20Soft%20actor-critic%3A%20Off-policy%20maximum%20entropy%20deep%20reinforcement%20learning%20with%20a%20stochastic%20actor%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Haarnoja%2C%20T.%20Zhou%2C%20A.%20Abbeel%2C%20P.%20Levine%2C%20S.%20Soft%20actor-critic%3A%20Off-policy%20maximum%20entropy%20deep%20reinforcement%20learning%20with%20a%20stochastic%20actor%202018) 

[^48]: T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, et al., Soft actor-critic algorithms and applications, arXiv preprint arXiv:1812.05905 (2018).  [OA](https://arxiv.org/abs/1812.05905)  

[^49]: R. U. Community, Deep reinforcement learning practical tips, 2018. URL: https://www.reddit.com/r/reinforcementlearning/comments/7s8px9/deep_reinforcement_learning_practical_tips/, accessed:202408-31.  [OA](https://www.reddit.com/r/reinforcementlearning/comments/7s8px9/deep_reinforcement_learning_practical_tips/)  

[^50]: A. Fish, Reproducing deep rl, 2018. URL: http://amid.fish/reproducing-deep-rl, accessed:2024-08-31.  [OA](http://amid.fish/reproducing-deep-rl)  

[^51]: P. Henderson, R. Islam, P. Bachman, J. Pineau, D. Precup, D. Meger, Deep reinforcement learning that matters, in: Proceedings of the AAAI Conference on Artificial Intelligence, volume 32, 2018.  [OA](https://scholar.google.co.uk/scholar?q=Henderson%2C%20P.%20Islam%2C%20R.%20Bachman%2C%20P.%20Pineau%2C%20J.%20Deep%20reinforcement%20learning%20that%20matters%202018) [GScholar](https://scholar.google.co.uk/scholar?q=Henderson%2C%20P.%20Islam%2C%20R.%20Bachman%2C%20P.%20Pineau%2C%20J.%20Deep%20reinforcement%20learning%20that%20matters%202018) 

[^52]: P. Abbeel, J. Schulman, S. Levine, Deep rl bootcamp: Nuts and bolts of deep rl experimentation, 2017. URL: https://www.youtube.com/watch?v=8EcdaCk9KaQ, slides available at https://rll.berkeley.edu/deeprlcourse/docs/nuts-and-bolts.pdf.  [OA](https://www.youtube.com/watch?v=8EcdaCk9KaQ)  

[^53]: A. Irpan, Deep reinforcement learning doesn’t work yet, 2018. URL: https://www.alexirpan.com/2018/02/14/rl-hard.html, accessed:2024-08-31.  [OA](https://www.alexirpan.com/2018/02/14/rl-hard.html)  

[^54]: S. Ivanov, 37 reasons why your neural network is not working, 2018. URL: https://blog.slavv.com/37-reasons-why-your-neural-network-is-not-working-4020854bd607, accessed:2024-08-31.  [OA](https://blog.slavv.com/37-reasons-why-your-neural-network-is-not-working-4020854bd607)  

[^55]: O. Flowers, How many random seeds should I use? Statistical power analysis in deep reinforcement learning experiments, 2020. URL: https://openlab-flowers.inria.fr/t/how-many-random-seeds-should-i-use-statistical-power-analysis-in-deep-reinforcement-learning-experiments/457, accessed:2024-08-31.  [OA](https://openlab-flowers.inria.fr/t/how-many-random-seeds-should-i-use-statistical-power-analysis-in-deep-reinforcement-learning-experiments/457)  

[^56]: A. Hill, Others, Problem in evaluation methodology in ddpg, 2018. URL: https://github.com/hill-a/stable-baselines/issues/199, accessed:2024-08-31.  [OA](https://github.com/hill-a/stable-baselines/issues/199)  

[^57]: D. Jurafsky, J. H. Martin, Speech and Language Processing, Prentice Hall, 2000.  [OA](https://scholar.google.co.uk/scholar?q=Jurafsky%2C%20D.%20Martin%2C%20J.H.%20Speech%20and%20Language%20Processing%202000) [GScholar](https://scholar.google.co.uk/scholar?q=Jurafsky%2C%20D.%20Martin%2C%20J.H.%20Speech%20and%20Language%20Processing%202000) 

[^58]: W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, et al., A survey of large language models, arXiv preprint arXiv:2303.18223 (2023).  [OA](https://arxiv.org/abs/2303.18223)  

[^59]: T. Winograd, Understanding Natural Language, Academic Press, 1972.  [OA](https://scholar.google.co.uk/scholar?q=Winograd%2C%20T.%20Understanding%20Natural%20Language%201972) [GScholar](https://scholar.google.co.uk/scholar?q=Winograd%2C%20T.%20Understanding%20Natural%20Language%201972) 

[^60]: C. D. Manning, H. Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999.  [OA](https://scholar.google.co.uk/scholar?q=Manning%2C%20C.D.%20Sch%C3%BCtze%2C%20H.%20Foundations%20of%20Statistical%20Natural%20Language%20Processing%201999) [GScholar](https://scholar.google.co.uk/scholar?q=Manning%2C%20C.D.%20Sch%C3%BCtze%2C%20H.%20Foundations%20of%20Statistical%20Natural%20Language%20Processing%201999) 

[^61]: T. Mikolov, K. Chen, G. Corrado, J. Dean, Efficient estimation of word representations in vector space, in: Proceedings of the International Conference on Learning Representations (ICLR), 2013.  [OA](https://scholar.google.co.uk/scholar?q=Mikolov%2C%20T.%20Chen%2C%20K.%20Corrado%2C%20G.%20Dean%2C%20J.%20Efficient%20estimation%20of%20word%20representations%20in%20vector%20space%202013) [GScholar](https://scholar.google.co.uk/scholar?q=Mikolov%2C%20T.%20Chen%2C%20K.%20Corrado%2C%20G.%20Dean%2C%20J.%20Efficient%20estimation%20of%20word%20representations%20in%20vector%20space%202013) 

[^62]: J. Pennington, R. Socher, C. D. Manning, Glove: Global vectors for word representation, in: Proceedings of the Conference on Empirical Methods in Natural Language Processing (EMNLP), 2014, pp. 1532–1543.  [OA](https://scholar.google.co.uk/scholar?q=Pennington%2C%20J.%20Socher%2C%20R.%20Manning%2C%20C.D.%20Glove%3A%20Global%20vectors%20for%20word%20representation%202014) [GScholar](https://scholar.google.co.uk/scholar?q=Pennington%2C%20J.%20Socher%2C%20R.%20Manning%2C%20C.D.%20Glove%3A%20Global%20vectors%20for%20word%20representation%202014) 

[^63]: S. Hochreiter, J. Schmidhuber, Long short-term memory, Neural Computation 9 (1997) 1735–1780.  [OA](https://engine.scholarcy.com/oa_version?query=Hochreiter%2C%20S.%20Schmidhuber%2C%20J.%20Long%20short-term%20memory%201997&author=Hochreiter&title=Long%20short-term%20memory&year=1997) [GScholar](https://scholar.google.co.uk/scholar?q=Hochreiter%2C%20S.%20Schmidhuber%2C%20J.%20Long%20short-term%20memory%201997) [Scite](/scite_tallies?query=author%3AHochreiter%2Ctitle%3ALong%20short-term%20memory%2Cyear%3A1997)

[^64]: A. Vaswani, Attention is all you need, Advances in Neural Information Processing Systems (2017).  [OA](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Attention%20is%20all%20you%20need%202017) [GScholar](https://scholar.google.co.uk/scholar?q=Vaswani%2C%20A.%20Attention%20is%20all%20you%20need%202017) 

[^65]: J. Devlin, Bert: Pre-training of deep bidirectional transformers for language understanding, arXiv preprint arXiv:1810.04805 (2018).  [OA](https://arxiv.org/abs/1810.04805)  

[^66]: W. A. Qader, M. M. Ameen, B. I. Ahmed, An overview of bag of words; importance, implementation, applications, and challenges, in: 2019 international engineering conference (IEC), IEEE, 2019, pp. 200–204.  [OA](https://scholar.google.co.uk/scholar?q=W%20A%20Qader%20M%20M%20Ameen%20B%20I%20Ahmed%20An%20overview%20of%20bag%20of%20words%20importance%20implementation%20applications%20and%20challenges%20in%202019%20international%20engineering%20conference%20IEC%20IEEE%202019%20pp%20200204) [GScholar](https://scholar.google.co.uk/scholar?q=W%20A%20Qader%20M%20M%20Ameen%20B%20I%20Ahmed%20An%20overview%20of%20bag%20of%20words%20importance%20implementation%20applications%20and%20challenges%20in%202019%20international%20engineering%20conference%20IEC%20IEEE%202019%20pp%20200204) 

[^67]: M. Grootendorst, Bertopic: Neural topic modeling with a class-based tf-idf procedure, arXiv preprint arXiv:2203.05794 (2022).  [OA](https://arxiv.org/abs/2203.05794)  

[^68]: K. Lee, D. Ippolito, A. Nystrom, C. Zhang, D. Eck, C. Callison-Burch, N. Carlini, Deduplicating training data makes language models better, arXiv preprint arXiv:2107.06499 (2021).  [OA](https://arxiv.org/abs/2107.06499)  

[^69]: A. L. Awad, S. M. Elkaffas, M. W. Fakhr, Stock market prediction using deep reinforcement learning, Applied System Innovation 6 (2023) 106.  [OA](https://engine.scholarcy.com/oa_version?query=Awad%2C%20A.L.%20Elkaffas%2C%20S.M.%20Fakhr%2C%20M.W.%20Stock%20market%20prediction%20using%20deep%20reinforcement%20learning%202023&author=Awad&title=Stock%20market%20prediction%20using%20deep%20reinforcement%20learning&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Awad%2C%20A.L.%20Elkaffas%2C%20S.M.%20Fakhr%2C%20M.W.%20Stock%20market%20prediction%20using%20deep%20reinforcement%20learning%202023) [Scite](/scite_tallies?query=author%3AAwad%2Ctitle%3AStock%20market%20prediction%20using%20deep%20reinforcement%20learning%2Cyear%3A2023)

[^70]: K. A. Hambarde, H. Proenca, Information retrieval: recent advances and beyond, IEEE Access (2023).  [OA](https://engine.scholarcy.com/oa_version?query=Hambarde%2C%20K.A.%20Proenca%2C%20H.%20Information%20retrieval%3A%20recent%20advances%20and%20beyond%202023&author=Hambarde&title=Information%20retrieval%3A%20recent%20advances%20and%20beyond&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Hambarde%2C%20K.A.%20Proenca%2C%20H.%20Information%20retrieval%3A%20recent%20advances%20and%20beyond%202023) [Scite](/scite_tallies?query=author%3AHambarde%2Ctitle%3AInformation%20retrieval%3A%20recent%20advances%20and%20beyond%2Cyear%3A2023)

[^71]: P. Bojanowski, E. Grave, A. Joulin, T. Mikolov, Enriching word vectors with subword information, Transactions of the Association for Computational Linguistics 5 (2017) 135–146.  [OA](https://engine.scholarcy.com/oa_version?query=Bojanowski%2C%20P.%20Grave%2C%20E.%20Joulin%2C%20A.%20Mikolov%2C%20T.%20Enriching%20word%20vectors%20with%20subword%20information%202017&author=Bojanowski&title=Enriching%20word%20vectors%20with%20subword%20information&year=2017) [GScholar](https://scholar.google.co.uk/scholar?q=Bojanowski%2C%20P.%20Grave%2C%20E.%20Joulin%2C%20A.%20Mikolov%2C%20T.%20Enriching%20word%20vectors%20with%20subword%20information%202017) [Scite](/scite_tallies?query=author%3ABojanowski%2Ctitle%3AEnriching%20word%20vectors%20with%20subword%20information%2Cyear%3A2017)

[^72]: Y. Ye, H. Pei, B. Wang, P.-Y. Chen, Y. Zhu, J. Xiao, B. Li, Reinforcement-learning based portfolio management with augmented asset movement prediction states, in: Proceedings of the AAAI conference on artificial intelligence, volume 34, 2020, pp. 1112–1119.  [OA](https://scholar.google.co.uk/scholar?q=Ye%2C%20Y.%20Pei%2C%20H.%20Wang%2C%20B.%20Chen%2C%20P.-Y.%20Reinforcement-learning%20based%20portfolio%20management%20with%20augmented%20asset%20movement%20prediction%20states%202020) [GScholar](https://scholar.google.co.uk/scholar?q=Ye%2C%20Y.%20Pei%2C%20H.%20Wang%2C%20B.%20Chen%2C%20P.-Y.%20Reinforcement-learning%20based%20portfolio%20management%20with%20augmented%20asset%20movement%20prediction%20states%202020) 

[^73]: D. Bahdanau, Neural machine translation by jointly learning to align and translate, arXiv preprint arXiv:1409.0473 (2014).  [OA](https://arxiv.org/abs/1409.0473)  

[^74]: M.-T. Luong, Effective approaches to attention-based neural machine translation, arXiv preprint arXiv:1508.04025 (2015).  [OA](https://arxiv.org/abs/1508.04025)  

[^75]: L. Weng, Attention? attention!, Blog post, 2018. URL: https://lilianweng.github.io/posts/2018-06-24-attention/.  [OA](https://lilianweng.github.io/posts/2018-06-24-attention/)  

[^76]: J. Lei Ba, J. R. Kiros, G. E. Hinton, Layer normalization, ArXiv e-prints (2016) arXiv–1607.  [OA](https://scholar.google.co.uk/scholar?q=J%20Lei%20Ba%20J%20R%20Kiros%20G%20E%20Hinton%20Layer%20normalization%20ArXiv%20eprints%202016%20arXiv1607) [GScholar](https://scholar.google.co.uk/scholar?q=J%20Lei%20Ba%20J%20R%20Kiros%20G%20E%20Hinton%20Layer%20normalization%20ArXiv%20eprints%202016%20arXiv1607) 

[^77]: K. He, X. Zhang, S. Ren, J. Sun, Deep residual learning for image recognition, in: Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.  [OA](https://scholar.google.co.uk/scholar?q=He%2C%20K.%20Zhang%2C%20X.%20Ren%2C%20S.%20Sun%2C%20J.%20Deep%20residual%20learning%20for%20image%20recognition%202016) [GScholar](https://scholar.google.co.uk/scholar?q=He%2C%20K.%20Zhang%2C%20X.%20Ren%2C%20S.%20Sun%2C%20J.%20Deep%20residual%20learning%20for%20image%20recognition%202016) 

[^78]: Y. Wu, Google’s neural machine translation system: Bridging the gap between human and machine translation, arXiv preprint arXiv:1609.08144 (2016).  [OA](https://arxiv.org/abs/1609.08144)  

[^79]: V. Sanh, Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter, arXiv preprint arXiv:1910.01108 (2019).  [OA](https://arxiv.org/abs/1910.01108)  

[^80]: C. Bucilua, R. Caruana, A. Niculescu-Mizil, Model compression, in: Proceedings of the 12th ACM SIGKDD international conference on Knowledge discovery and data mining, 2006, pp. 535–541.  [OA](https://scholar.google.co.uk/scholar?q=Bucilua%2C%20C.%20Caruana%2C%20R.%20Niculescu-Mizil%2C%20A.%20Model%20compression%202006) [GScholar](https://scholar.google.co.uk/scholar?q=Bucilua%2C%20C.%20Caruana%2C%20R.%20Niculescu-Mizil%2C%20A.%20Model%20compression%202006) 

[^81]: G. Hinton, Distilling the knowledge in a neural network, arXiv preprint arXiv:1503.02531 (2015).  [OA](https://arxiv.org/abs/1503.02531)  

[^82]: Z. Lan, Albert: A lite bert for self-supervised learning of language representations, arXiv preprint arXiv:1909.11942 (2019).  [OA](https://arxiv.org/abs/1909.11942)  

[^83]: I. Beltagy, M. E. Peters, A. Cohan, Longformer: The long-document transformer, arXiv preprint arXiv:2004.05150 (2020).  [OA](https://arxiv.org/abs/2004.05150)  

[^84]: M. Zaheer, G. Guruganesh, K. A. Dubey, J. Ainslie, C. Alberti, S. Ontanon, P. Pham, A. Ravula, Q. Wang, L. Yang, et al., Big bird: Transformers for longer sequences, Advances in neural information processing systems 33 (2020) 17283–17297.  [OA](https://engine.scholarcy.com/oa_version?query=Zaheer%2C%20M.%20Guruganesh%2C%20G.%20Dubey%2C%20K.A.%20Ainslie%2C%20J.%20Big%20bird%3A%20Transformers%20for%20longer%20sequences%202020&author=Zaheer&title=Big%20bird%3A%20Transformers%20for%20longer%20sequences&year=2020) [GScholar](https://scholar.google.co.uk/scholar?q=Zaheer%2C%20M.%20Guruganesh%2C%20G.%20Dubey%2C%20K.A.%20Ainslie%2C%20J.%20Big%20bird%3A%20Transformers%20for%20longer%20sequences%202020) [Scite](/scite_tallies?query=author%3AZaheer%2Ctitle%3ABig%20bird%3A%20Transformers%20for%20longer%20sequences%2Cyear%3A2020)

[^85]: Y. Liu, Roberta: A robustly optimized BERT pretraining approach, arXiv preprint arXiv:1907.11692 364 (2019).  [OA](https://arxiv.org/abs/1907.11692)  

[^86]: P. He, X. Liu, J. Gao, W. Chen, Deberta: Decoding-enhanced bert with disentangled attention, in: International Conference on Learning Representations, 2021. URL: https://openreview.net/forum?id= XPZIaotutsD.  [OA](https://openreview.net/forum?id=)  

[^87]: P. He, J. Gao, W. Chen, Debertav3: Improving deberta using electra-style pre-training with gradientdisentangled embedding sharing, arXiv preprint arXiv:2111.09543 (2021).  [OA](https://arxiv.org/abs/2111.09543)  

[^88]: K. Clark, Electra: Pre-training text encoders as discriminators rather than generators, arXiv preprint arXiv:2003.10555 (2020).  [OA](https://arxiv.org/abs/2003.10555)  

[^89]: T. B. Brown, Language models are few-shot learners, arXiv preprint arXiv:2005.14165 (2020).  [OA](https://arxiv.org/abs/2005.14165)  

[^90]: J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al., Gpt-4 technical report, arXiv preprint arXiv:2303.08774 (2023).  [OA](https://arxiv.org/abs/2303.08774)  

[^91]: H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T., Lacroix, B., Rozière, N., Goyal, E., Hambro, F., Azhar, F., et al., Llama: Open and efficient foundation language models, arXiv preprint arXiv:2302.13971 (2023).  [OA](https://arxiv.org/abs/2302.13971)  

[^92]: A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung, C. Sutton, S. Gehrmann, et al., Palm: Scaling language modeling with pathways, Journal of Machine Learning Research 24 (2023) 1–113.  [OA](https://engine.scholarcy.com/oa_version?query=Chowdhery%2C%20A.%20Narang%2C%20S.%20Devlin%2C%20J.%20Bosma%2C%20M.%20Palm%3A%20Scaling%20language%20modeling%20with%20pathways%202023&author=Chowdhery&title=Palm%3A%20Scaling%20language%20modeling%20with%20pathways&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Chowdhery%2C%20A.%20Narang%2C%20S.%20Devlin%2C%20J.%20Bosma%2C%20M.%20Palm%3A%20Scaling%20language%20modeling%20with%20pathways%202023) [Scite](/scite_tallies?query=author%3AChowdhery%2Ctitle%3APalm%3A%20Scaling%20language%20modeling%20with%20pathways%2Cyear%3A2023)

[^93]: T. Le Scao, A. Fan, C. Akiki, E. Pavlick, S. Ilić, D. Hesslow, R. Castagné, A. S. Luccioni, F. Yvon, M. Gallé, et al., Bloom: A 176b-parameter open-access multilingual language model (2023).  [OA](https://scholar.google.co.uk/scholar?q=Scao%2C%20T.Le%20Fan%2C%20A.%20Akiki%2C%20C.%20Pavlick%2C%20E.%20Bloom%3A%20A%20176b-parameter%20open-access%20multilingual%20language%20model%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Scao%2C%20T.Le%20Fan%2C%20A.%20Akiki%2C%20C.%20Pavlick%2C%20E.%20Bloom%3A%20A%20176b-parameter%20open-access%20multilingual%20language%20model%202023) 

[^94]: L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al., Training language models to follow instructions with human feedback, Advances in neural information processing systems 35 (2022) 27730–27744.  [OA](https://engine.scholarcy.com/oa_version?query=Ouyang%2C%20L.%20Wu%2C%20J.%20Jiang%2C%20X.%20Almeida%2C%20D.%20Training%20language%20models%20to%20follow%20instructions%20with%20human%20feedback%202022&author=Ouyang&title=Training%20language%20models%20to%20follow%20instructions%20with%20human%20feedback&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Ouyang%2C%20L.%20Wu%2C%20J.%20Jiang%2C%20X.%20Almeida%2C%20D.%20Training%20language%20models%20to%20follow%20instructions%20with%20human%20feedback%202022) [Scite](/scite_tallies?query=author%3AOuyang%2Ctitle%3ATraining%20language%20models%20to%20follow%20instructions%20with%20human%20feedback%2Cyear%3A2022)

[^95]: OpenAI, GPT-4V(ision) System Card, 2023. URL: https://cdn.openai.com/papers/GPTV_System_Card.pdf. M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al., Evaluating large language models trained on code, arXiv preprint arXiv:2107.03374 (2021). Z. Sun, H. Yu, X. Song, R. Liu, Y. Yang, D. Zhou, Mobilebert: a compact task-agnostic bert for resource-limited devices, arXiv preprint arXiv:2004.02984 (2020). A. H. Huang, H. Wang, Y. Yang, Finbert: A large language model for extracting information from financial text, Contemporary Accounting Research 40 (2023) 806–841.  [OA](https://cdn.openai.com/papers/GPTV_System_Card.pdf)  

[^96]: I. Beltagy, K. Lo, A. Cohan, Scibert: A pretrained language model for scientific text, arXiv preprint arXiv:1903.10676 (2019). N. Reimers, I. Gurevych, Sentence-bert: Sentence embeddings using siamese bert-networks, in: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing, Association for Computational Linguistics, 2019. URL: https://arxiv.org/abs/1908.10084. Y.  [OA](https://arxiv.org/abs/1908.10084)  

[^97]: Gao, Y., Xiong, X., Gao, K., Jia, J., Pan, Y., Bi, Y., Dai, Y., Sun, J., Wang, H. Wang, Retrieval-augmented generation for large language models: A survey, arXiv preprint arXiv:2312.10997 (2023). Y. Zhu, H. Yuan, S. Wang, J. Liu, W. Liu, C. Deng, H. Chen, Z. Liu, Z. Dou, J.-R. Wen, Large language models for information retrieval: A survey, arXiv preprint arXiv:2308.07107 (2023). A. Petukhova, J. P. Matos-Carvalho, N. Fachada, Text clustering with llm embeddings, arXiv preprint arXiv:2403.15112 (2024). V. Devarajan, R. Subramanian, Analyzing semantic similarity amongst textual documents to suggest near duplicates, Indonesian Journal of Electrical Engineering and Computer Science 25 (2022) 1703–1711.  [OA](https://arxiv.org/abs/2312.10997)  

[^98]: H. Guo, S. Yuan, X. Wu, Logbert: Log anomaly detection via BERT, in: 2021 International Joint Conference on Neural Networks (IJCNN), IEEE, 2021, pp. 1–8.  [OA](https://scholar.google.co.uk/scholar?q=H%20Guo%20S%20Yuan%20X%20Wu%20Logbert%20Log%20anomaly%20detection%20via%20bert%20in%202021%20international%20joint%20conference%20on%20neural%20networks%20IJCNN%20IEEE%202021%20pp%2018) [GScholar](https://scholar.google.co.uk/scholar?q=H%20Guo%20S%20Yuan%20X%20Wu%20Logbert%20Log%20anomaly%20detection%20via%20bert%20in%202021%20international%20joint%20conference%20on%20neural%20networks%20IJCNN%20IEEE%202021%20pp%2018) 

[^99]: A. Akbik, T. Bergmann, D. Blythe, K. Rasul, S. Schweter, R. Vollgraf, Flair: An easy-to-use framework for state-of-the-art NLP, in: Proceedings of the 2019 conference of the North American chapter of the association for computational linguistics (demonstrations), 2019, pp. 54–59. I. Garrido-Muñoz, A., Montejo-Ráez, F., Martínez-Santiago, L. A., Ureña-López, A., A survey on bias in deep NLP, Applied Sciences 11 (2021) 3184.  [OA](https://engine.scholarcy.com/oa_version?query=A%20Akbik%20T%20Bergmann%20D%20Blythe%20K%20Rasul%20S%20Schweter%20R%20Vollgraf%20Flair%20An%20easytouse%20framework%20for%20stateoftheart%20nlp%20in%20Proceedings%20of%20the%202019%20conference%20of%20the%20North%20American%20chapter%20of%20the%20association%20for%20computational%20linguistics%20demonstrations%202019%20pp%205459%20I%20GarridoMu%C3%B1oz%20A%20MontejoR%C3%A1ez%20F%20Mart%C3%ADnezSantiago%20L%20A%20Ure%C3%B1aL%C3%B3pez%20A%20survey%20on%20bias%20in%20deep%20nlp%20Applied%20Sciences%2011%202021%203184&author=Akbik&title=Vollgraf%2C%20Flair%3A%20An%20easy-to-use%20framework%20for%20state-of-the-art%20nlp%2C%20in%3A%20Proceedings%20of%20the%202019%20conference%20of%20the%20North%20American%20chapter%20of%20the%20association%20for%20computational%20linguistics%20%28demonstrations&year=2019) [GScholar](https://scholar.google.co.uk/scholar?q=A%20Akbik%20T%20Bergmann%20D%20Blythe%20K%20Rasul%20S%20Schweter%20R%20Vollgraf%20Flair%20An%20easytouse%20framework%20for%20stateoftheart%20nlp%20in%20Proceedings%20of%20the%202019%20conference%20of%20the%20North%20American%20chapter%20of%20the%20association%20for%20computational%20linguistics%20demonstrations%202019%20pp%205459%20I%20GarridoMu%C3%B1oz%20A%20MontejoR%C3%A1ez%20F%20Mart%C3%ADnezSantiago%20L%20A%20Ure%C3%B1aL%C3%B3pez%20A%20survey%20on%20bias%20in%20deep%20nlp%20Applied%20Sciences%2011%202021%203184) [Scite](/scite_tallies?query=author%3AAkbik%2Ctitle%3AVollgraf%2C%20Flair%3A%20An%20easy-to-use%20framework%20for%20state-of-the-art%20nlp%2C%20in%3A%20Proceedings%20of%20the%202019%20conference%20of%20the%20North%20American%20chapter%20of%20the%20association%20for%20computational%20linguistics%20%28demonstrations%2Cyear%3A2019)

[^100]: B. Hutchinson, V. Prabhakaran, E. Denton, K. Webster, Y. Zhong, S. Denuyl, Social biases in NLP models as barriers for persons with disabilities, arXiv preprint arXiv:2005.00813 (2020). P. Kumar, Adversarial attacks and defenses for large language models (llms): methods, frameworks &amp; challenges, International Journal of Multimedia Information Retrieval 13 (2024) 26.  [OA](https://arxiv.org/abs/2005.00813)  

[^1]: A. K. Veldanda, F. Grob, S. Thakur, H. Pearce, B. Tan, R. Karri, S. Garg, Investigating hiring bias in large language models, in: R0-FoMo: Robustness of Few-shot and Zero-shot Learning in Large Foundation Models, 2023.  [OA](https://scholar.google.co.uk/scholar?q=Veldanda%2C%20A.K.%20Grob%2C%20F.%20Thakur%2C%20S.%20Pearce%2C%20H.%20Investigating%20hiring%20bias%20in%20large%20language%20models%202023) [GScholar](https://scholar.google.co.uk/scholar?q=Veldanda%2C%20A.K.%20Grob%2C%20F.%20Thakur%2C%20S.%20Pearce%2C%20H.%20Investigating%20hiring%20bias%20in%20large%20language%20models%202023) 

[^2]: W. A. Khattak, F. Rabbi, Ethical considerations and challenges in the deployment of natural language processing systems in healthcare, International Journal of Applied Health Care Analytics 8 (2023) 17–36.  [OA](https://engine.scholarcy.com/oa_version?query=Khattak%2C%20W.A.%20Rabbi%2C%20F.%20Ethical%20considerations%20and%20challenges%20in%20the%20deployment%20of%20natural%20language%20processing%20systems%20in%20healthcare%202023&author=Khattak&title=Ethical%20considerations%20and%20challenges%20in%20the%20deployment%20of%20natural%20language%20processing%20systems%20in%20healthcare&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Khattak%2C%20W.A.%20Rabbi%2C%20F.%20Ethical%20considerations%20and%20challenges%20in%20the%20deployment%20of%20natural%20language%20processing%20systems%20in%20healthcare%202023) [Scite](/scite_tallies?query=author%3AKhattak%2Ctitle%3AEthical%20considerations%20and%20challenges%20in%20the%20deployment%20of%20natural%20language%20processing%20systems%20in%20healthcare%2Cyear%3A2023)

[^3]: L. Wang, X. Zhang, H. Su, J. Zhu, A comprehensive survey of continual learning: theory, method, and application, IEEE Transactions on Pattern Analysis and Machine Intelligence (2024). H. Zhao, H. Chen, F. Yang, N. Liu, H. Deng, H. Cai, S. Wang, D. Yin, M. Du, Explainability for large language models: A survey, ACM Transactions on Intelligent Systems and Technology 15 (2024) 1–38.  [OA](https://engine.scholarcy.com/oa_version?query=Wang%2C%20L.%20Zhang%2C%20X.%20Su%2C%20H.%20Zhu%2C%20J.%20A%20comprehensive%20survey%20of%20continual%20learning%3A%20theory%2C%20method%20and%20application%202024&author=Wang&title=A%20comprehensive%20survey%20of%20continual%20learning%3A%20theory%2C%20method%20and%20application&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Wang%2C%20L.%20Zhang%2C%20X.%20Su%2C%20H.%20Zhu%2C%20J.%20A%20comprehensive%20survey%20of%20continual%20learning%3A%20theory%2C%20method%20and%20application%202024) [Scite](/scite_tallies?query=author%3AWang%2Ctitle%3AA%20comprehensive%20survey%20of%20continual%20learning%3A%20theory%2C%20method%20and%20application%2Cyear%3A2024)

[^4]: A. Bhakar, P. S. Deori, Y. V. Gautam, K. Srinivasa, Maximizing returns with reinforcement learning: A paradigm shift in stock market portfolio management, in: TENCON 2023-2023 IEEE Region 10 Conference (TENCON), IEEE, 2023, pp. 393–398.  [OA](https://scholar.google.co.uk/scholar?q=A%20Bhakar%20P%20S%20Deori%20Y%20V%20Gautam%20K%20Srinivasa%20Maximizing%20returns%20with%20reinforcement%20learning%20A%20paradigm%20shift%20in%20stock%20market%20portfolio%20management%20in%20TENCON%2020232023%20IEEE%20Region%2010%20Conference%20TENCON%20IEEE%202023%20pp%20393398) [GScholar](https://scholar.google.co.uk/scholar?q=A%20Bhakar%20P%20S%20Deori%20Y%20V%20Gautam%20K%20Srinivasa%20Maximizing%20returns%20with%20reinforcement%20learning%20A%20paradigm%20shift%20in%20stock%20market%20portfolio%20management%20in%20TENCON%2020232023%20IEEE%20Region%2010%20Conference%20TENCON%20IEEE%202023%20pp%20393398) 

[^5]: C. Zhang, Sentiment analysis and deep reinforcement learning for algorithmic trading, Semantic Scholar (2019). A. Nan, A. Perumal, O. R. Zaiane, Sentiment and knowledge-based algorithmic trading with deep reinforcement learning, in: International Conference on Database and Expert Systems Applications, Springer, 2022, pp. 167–180. R. F. d. Silva, Automated stock trading system using deep reinforcement learning and price and sentiment prediction modules. Dissertação de Doutorado, Universidade de São Paulo, 2021.  [OA](https://scholar.google.co.uk/scholar?q=Zhang%2C%20C.%20analysis%2C%20Sentiment%20trading%20Scholar%2C%20Semantic%20Sentiment%20and%20knowledge%20based%20algorithmic%20trading%20with%20deep%20reinforcement%20learning%2C%20in%3A%20International%20Conference%20on%20Database%20and%20Expert%20Systems%20Applications%202019) [GScholar](https://scholar.google.co.uk/scholar?q=Zhang%2C%20C.%20analysis%2C%20Sentiment%20trading%20Scholar%2C%20Semantic%20Sentiment%20and%20knowledge%20based%20algorithmic%20trading%20with%20deep%20reinforcement%20learning%2C%20in%3A%20International%20Conference%20on%20Database%20and%20Expert%20Systems%20Applications%202019) 

[^6]: L. Avramelou, P. Nousi, N. Passalis, A. Tefas, Deep reinforcement learning for financial trading using multi-modal features, Expert Systems with Applications 238 (2024) 121849. A. R. Azhikodan, A. G. Bhat, M. V. Jadhav, Stock trading bot using deep reinforcement learning, in: Innovations in Computer Science and Engineering: Proceedings of the Fifth ICICSE 2017, Springer, 2019, pp. 41–49.  [OA](https://scholar.google.co.uk/scholar?q=Avramelou%2C%20L.%20Nousi%2C%20P.%20Passalis%2C%20N.%20Tefas%2C%20A.%20Deep%20reinforcement%20learning%20for%20financial%20trading%20using%20multi-modal%20features%2C%20Expert%20Systems%20with%20Applications%20238%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Avramelou%2C%20L.%20Nousi%2C%20P.%20Passalis%2C%20N.%20Tefas%2C%20A.%20Deep%20reinforcement%20learning%20for%20financial%20trading%20using%20multi-modal%20features%2C%20Expert%20Systems%20with%20Applications%20238%202024) 

[^7]: Z. Huang, F. Tanaka, Mspm: A modularized and scalable multi-agent reinforcement learning-based system for financial portfolio management, Plos one 17 (2022) e0263689. T. Kabbani, E. Duman, Deep reinforcement learning approach for trading automation in the stock market, IEEE Access 10 (2022) 93564–93574. M. Yang, M. Zhu, Q. Liang, X. Zheng, M. Wang, Spotlight news-driven quantitative trading based on trajectory optimization, in: IJCAI, 2023, pp. 4930–4939. F. C. Lima Paiva, L. K. Felizardo, R. A. d. C. Bianchi, A. H. R. Costa, Intelligent trading systems: A sentiment-aware reinforcement learning approach, in: Proceedings of the second ACM international conference on AI in finance, 2021, pp. 1–9.  [OA](https://engine.scholarcy.com/oa_version?query=Huang%2C%20Z.%20Tanaka%2C%20F.%20Kabbani%2C%20T.%20Duman%2C%20E.%20Mspm%3A%20A%20modularized%20and%20scalable%20multi-agent%20reinforcement%20learning-based%20system%20for%20financial%20portfolio%20management%2C%20Plos%20one%2017%202022&author=Huang&title=Mspm%3A%20A%20modularized%20and%20scalable%20multi-agent%20reinforcement%20learning-based%20system%20for%20financial%20portfolio%20management%2C%20Plos%20one%2017&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Huang%2C%20Z.%20Tanaka%2C%20F.%20Kabbani%2C%20T.%20Duman%2C%20E.%20Mspm%3A%20A%20modularized%20and%20scalable%20multi-agent%20reinforcement%20learning-based%20system%20for%20financial%20portfolio%20management%2C%20Plos%20one%2017%202022) [Scite](/scite_tallies?query=author%3AHuang%2Ctitle%3AMspm%3A%20A%20modularized%20and%20scalable%20multi-agent%20reinforcement%20learning-based%20system%20for%20financial%20portfolio%20management%2C%20Plos%20one%2017%2Cyear%3A2022)

[^8]: S. Feuerriegel, H. Prendinger, News-based trading strategies, Decision Support Systems 90 (2016) 65–74.  [OA](https://engine.scholarcy.com/oa_version?query=Feuerriegel%2C%20S.%20Prendinger%2C%20H.%20News-based%20trading%20strategies%202016&author=Feuerriegel&title=News-based%20trading%20strategies&year=2016) [GScholar](https://scholar.google.co.uk/scholar?q=Feuerriegel%2C%20S.%20Prendinger%2C%20H.%20News-based%20trading%20strategies%202016) [Scite](/scite_tallies?query=author%3AFeuerriegel%2Ctitle%3ANews-based%20trading%20strategies%2Cyear%3A2016)

[^9]: A. B. Altuner, Z. H. Kilimci, A novel deep reinforcement learning based stock price prediction using knowledge graph and community-aware sentiments, Turkish Journal of Electrical Engineering and Computer Sciences 30 (2022) 1506–1524.  [OA](https://engine.scholarcy.com/oa_version?query=Altuner%2C%20A.B.%20Kilimci%2C%20Z.H.%20A%20novel%20deep%20reinforcement%20learning%20based%20stock%20price%20prediction%20using%20knowledge%20graph%20and%20community%20aware%20sentiments%202022&author=Altuner&title=A%20novel%20deep%20reinforcement%20learning%20based%20stock%20price%20prediction%20using%20knowledge%20graph%20and%20community%20aware%20sentiments&year=2022) [GScholar](https://scholar.google.co.uk/scholar?q=Altuner%2C%20A.B.%20Kilimci%2C%20Z.H.%20A%20novel%20deep%20reinforcement%20learning%20based%20stock%20price%20prediction%20using%20knowledge%20graph%20and%20community%20aware%20sentiments%202022) [Scite](/scite_tallies?query=author%3AAltuner%2Ctitle%3AA%20novel%20deep%20reinforcement%20learning%20based%20stock%20price%20prediction%20using%20knowledge%20graph%20and%20community%20aware%20sentiments%2Cyear%3A2022)

[^10]: P. Koratamaddi, K. Wadhwani, M. Gupta, S. G. Sanjeevi, Market sentiment-aware deep reinforcement learning approach for stock portfolio allocation, Engineering Science and Technology, an International Journal 24 (2021) 848–859.  [OA](https://engine.scholarcy.com/oa_version?query=Koratamaddi%2C%20P.%20Wadhwani%2C%20K.%20Gupta%2C%20M.%20Sanjeevi%2C%20S.G.%20Market%20sentiment-aware%20deep%20reinforcement%20learning%20approach%20for%20stock%20portfolio%20allocation%202021&author=Koratamaddi&title=Market%20sentiment-aware%20deep%20reinforcement%20learning%20approach%20for%20stock%20portfolio%20allocation&year=2021) [GScholar](https://scholar.google.co.uk/scholar?q=Koratamaddi%2C%20P.%20Wadhwani%2C%20K.%20Gupta%2C%20M.%20Sanjeevi%2C%20S.G.%20Market%20sentiment-aware%20deep%20reinforcement%20learning%20approach%20for%20stock%20portfolio%20allocation%202021) [Scite](/scite_tallies?query=author%3AKoratamaddi%2Ctitle%3AMarket%20sentiment-aware%20deep%20reinforcement%20learning%20approach%20for%20stock%20portfolio%20allocation%2Cyear%3A2021)

[^11]: A. L. Awad, S. M. Elkaffas, M. W. Fakhr, Stock market prediction using deep reinforcement learning, Applied System Innovation 6 (2023) 106.  [OA](https://engine.scholarcy.com/oa_version?query=Awad%2C%20A.L.%20Elkaffas%2C%20S.M.%20Fakhr%2C%20M.W.%20Stock%20market%20prediction%20using%20deep%20reinforcement%20learning%202023&author=Awad&title=Stock%20market%20prediction%20using%20deep%20reinforcement%20learning&year=2023) [GScholar](https://scholar.google.co.uk/scholar?q=Awad%2C%20A.L.%20Elkaffas%2C%20S.M.%20Fakhr%2C%20M.W.%20Stock%20market%20prediction%20using%20deep%20reinforcement%20learning%202023) [Scite](/scite_tallies?query=author%3AAwad%2Ctitle%3AStock%20market%20prediction%20using%20deep%20reinforcement%20learning%2Cyear%3A2023)

[^12]: S. Gangopadhyay, P. Majumder, Examining the effect of news context on algorithmic trading, in: Proceedings of the Eighth Financial Technology and Natural Language Processing and the 1st Agent AI for Scenario Planning, 2024, pp. 33–41.  [OA](https://scholar.google.co.uk/scholar?q=Gangopadhyay%2C%20S.%20Majumder%2C%20P.%20Examining%20the%20effect%20of%20news%20context%20on%20algorithmic%20trading%202024) [GScholar](https://scholar.google.co.uk/scholar?q=Gangopadhyay%2C%20S.%20Majumder%2C%20P.%20Examining%20the%20effect%20of%20news%20context%20on%20algorithmic%20trading%202024) 

[^13]: W. Liu, Y. Gu, Y. Ge, Multi-factor stock trading strategy based on DQN with multi-bigru and multi-head probsparse self-attention, Applied Intelligence (2024) 1–24.  [OA](https://engine.scholarcy.com/oa_version?query=Liu%2C%20W.%20Gu%2C%20Y.%20Ge%2C%20Y.%20Multi-factor%20stock%20trading%20strategy%20based%20on%20dqn%20with%20multi-bigru%20and%20multi-head%20probsparse%20self-attention%202024&author=Liu&title=Multi-factor%20stock%20trading%20strategy%20based%20on%20dqn%20with%20multi-bigru%20and%20multi-head%20probsparse%20self-attention&year=2024) [GScholar](https://scholar.google.co.uk/scholar?q=Liu%2C%20W.%20Gu%2C%20Y.%20Ge%2C%20Y.%20Multi-factor%20stock%20trading%20strategy%20based%20on%20dqn%20with%20multi-bigru%20and%20multi-head%20probsparse%20self-attention%202024) [Scite](/scite_tallies?query=author%3ALiu%2Ctitle%3AMulti-factor%20stock%20trading%20strategy%20based%20on%20dqn%20with%20multi-bigru%20and%20multi-head%20probsparse%20self-attention%2Cyear%3A2024)

[^2]: Variance Reduction: High variance in gradient estimates can occur when running the agent on a batch of episodes (trajectories from start to finish) and using the empirical expectation of the total reward at the end of each trajectory, leading to wide-ranging and unreliable performance outcomes, which makes learning unstable and slow. By subtracting the baseline b(st), we reduce the variability of the estimate. The baseline is typically chosen to be the value function V (st), which estimates the expected return from state st. By subtracting this baseline, we are effectively focusing on the advantage of taking a specific action over the average action. This subtraction reduces the fluctuations in the estimate, making the learning process more stable and efficient: Var(Ψt − b(st)) &lt; Var(Ψt).  [OA](https://scholar.google.co.uk/scholar?q=Variance%20Reduction%20High%20variance%20in%20gradient%20estimates%20can%20occur%20when%20running%20the%20agent%20on%20a%20batch%20of%20episodes%20trajectories%20from%20start%20to%20finish%20and%20using%20the%20empirical%20expectation%20of%20the%20total%20reward%20at%20the%20end%20of%20each%20trajectory%20leading%20to%20wideranging%20and%20unreliable%20performance%20outcomes%20which%20makes%20learning%20unstable%20and%20slow%20By%20subtracting%20the%20baseline%20bst%20we%20reduce%20the%20variability%20of%20the%20estimate%20The%20baseline%20is%20typically%20chosen%20to%20be%20the%20value%20function%20V%20st%20which%20estimates%20the%20expected%20return%20from%20state%20st%20By%20subtracting%20this%20baseline%20we%20are%20effectively%20focusing%20on%20the%20advantage%20of%20taking%20a%20specific%20action%20over%20the%20average%20action%20This%20subtraction%20reduces%20the%20fluctuations%20in%20the%20estimate%20making%20the%20learning%20process%20more%20stable%20and%20efficient%20Var%CE%A8t%20%20bst%20%20Var%CE%A8t) [GScholar](https://scholar.google.co.uk/scholar?q=Variance%20Reduction%20High%20variance%20in%20gradient%20estimates%20can%20occur%20when%20running%20the%20agent%20on%20a%20batch%20of%20episodes%20trajectories%20from%20start%20to%20finish%20and%20using%20the%20empirical%20expectation%20of%20the%20total%20reward%20at%20the%20end%20of%20each%20trajectory%20leading%20to%20wideranging%20and%20unreliable%20performance%20outcomes%20which%20makes%20learning%20unstable%20and%20slow%20By%20subtracting%20the%20baseline%20bst%20we%20reduce%20the%20variability%20of%20the%20estimate%20The%20baseline%20is%20typically%20chosen%20to%20be%20the%20value%20function%20V%20st%20which%20estimates%20the%20expected%20return%20from%20state%20st%20By%20subtracting%20this%20baseline%20we%20are%20effectively%20focusing%20on%20the%20advantage%20of%20taking%20a%20specific%20action%20over%20the%20average%20action%20This%20subtraction%20reduces%20the%20fluctuations%20in%20the%20estimate%20making%20the%20learning%20process%20more%20stable%20and%20efficient%20Var%CE%A8t%20%20bst%20%20Var%CE%A8t) 

[^2]: Gradient of the Objective Function:  [OA](https://scholar.google.co.uk/scholar?q=Gradient%20of%20the%20Objective%20Function) [GScholar](https://scholar.google.co.uk/scholar?q=Gradient%20of%20the%20Objective%20Function) 

[^4]: Final Gradient Expression:   [OA](https://scholar.google.co.uk/scholar?q=Final%20Gradient%20Expression) [GScholar](https://scholar.google.co.uk/scholar?q=Final%20Gradient%20Expression) 

