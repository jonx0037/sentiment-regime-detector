[[Ferrell_ComprehensiveSurveyIntegrationReinforcementLearning_2025]]

# A Comprehensive Survey on the Integration of Reinforcement Learning and NLP for Stock Market Trading

## [[Brian J. Ferrell]]

## Abstract

The integration of Reinforcement Learning (RL) and Natural Language Processing (NLP) has emerged as a powerful approach in stock market trading, enabling agents to leverage both numerical and textual data for informed financial decision-making. Traditional strategies often overlook the contextual insights available in financial news, social media, and corporate disclosures. By combining RL’s iterative learning capabilities with NLP’s ability to process unstructured text, modern trading systems can potentially optimize for higher profitability and risk management. This survey synthesizes findings from 22 research papers published between 2018 and 2024, analyzing methodologies, data sources, evaluation metrics, and other relevant aspects within an integrated RL–NLP framework for stock trading. A detailed review of foundational RL and NLP concepts is provided to contextualize these advancements. Challenges such as the lack of standardized datasets, limited use of random seeds for reproducibility, the simplicity of state representations and NLP methods, insufficient evaluation procedures, and limited real-world adaptability are explored, alongside opportunities for future research, including leveraging large language models and advancing textually-aware RL systems. This study aims to offer a comprehensive resource for researchers and practitioners to advance the field of RL and NLP in financial decision-making.

## Key concepts

# st_v; #deep_reinforcement_learning; #natural_language_processing; #dynamic_programming; #deep_deterministic_policy_gradient; #reinforcement_learning

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

## Builds on previous research

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

[^18]: J. Moody, L. Wu, Y. Liao, M. Saffell, Performance functions and reinforcement learning for trading systems and portfolios, Journal of forecasting 17 (1998) 441–470.  [OA](https://engine.scholarcy.com/oa_version?query=Moody%2C%20J.%20Wu%2C%20L.%20Liao%2C%20Y.%20Saffell%2C%20M.%20Performance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998&author=Moody&title=Performance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios&year=1998) [GScholar](https://scholar.google.co.uk/scholar?q=Moody%2C%20J.%20Wu%2C%20L.%20Liao%2C%20Y.%20Saffell%2C%20M.%20Performance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998) [Scite](/scite_tallies?query=author%3AMoody%2Ctitle%3APerformance%20functions%20and%20reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%2Cyear%3A1998)

[^19]: J. E. Moody, M. Saffell, Y. Liao, L. Wu, Reinforcement learning for trading systems and portfolios., in: KDD, 1998, pp. 279–283.  [OA](https://scholar.google.co.uk/scholar?q=Moody%2C%20J.E.%20Saffell%2C%20M.%20Liao%2C%20Y.%20Wu%2C%20L.%20Reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998) [GScholar](https://scholar.google.co.uk/scholar?q=Moody%2C%20J.E.%20Saffell%2C%20M.%20Liao%2C%20Y.%20Wu%2C%20L.%20Reinforcement%20learning%20for%20trading%20systems%20and%20portfolios%201998)

[^20]: J. Sadighian, Extending deep reinforcement learning frameworks in cryptocurrency market making, arXiv preprint arXiv:2004.06985 (2020).  [OA](https://arxiv.org/abs/2004.06985)  

[^44]: OpenAI, Trpo - spinning up documentation, Blog post, 2018. URL: <https://spinningup.openai.com/en/latest/algorithms/ddpg.html>.  [OA](https://spinningup.openai.com/en/latest/algorithms/ddpg.html)  

[^66]: W. A. Qader, M. M. Ameen, B. I. Ahmed, An overview of bag of words; importance, implementation, applications, and challenges, in: 2019 international engineering conference (IEC), IEEE, 2019, pp. 200–204.  [OA](https://scholar.google.co.uk/scholar?q=W%20A%20Qader%20M%20M%20Ameen%20B%20I%20Ahmed%20An%20overview%20of%20bag%20of%20words%20importance%20implementation%20applications%20and%20challenges%20in%202019%20international%20engineering%20conference%20IEC%20IEEE%202019%20pp%20200204) [GScholar](https://scholar.google.co.uk/scholar?q=W%20A%20Qader%20M%20M%20Ameen%20B%20I%20Ahmed%20An%20overview%20of%20bag%20of%20words%20importance%20implementation%20applications%20and%20challenges%20in%202019%20international%20engineering%20conference%20IEC%20IEEE%202019%20pp%20200204)
