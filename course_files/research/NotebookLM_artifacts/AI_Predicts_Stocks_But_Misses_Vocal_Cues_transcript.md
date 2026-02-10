# Transcript: AI_Predicts_Stocks_But_Misses_Vocal_Cues.m4a

[00:00] Welcome to The Debate. Today, we're tackling a question that has migrated from computer science labs directly to the heart of Wall Street.
[00:09] Can an algorithm actually read the news better than a human trader?
[00:13] We're looking at the explosion of large language models and asking if they can, you know, really predict market movements based on public sentiment.
[00:20] And on the other side, I'm asking if we're maybe mistaking correlation for comprehension.
[00:25] I mean, we are trying to reduce fear, greed and hesitation into a vector of numbers.
[00:31] And I believe the current high accuracy scores are masking some pretty dangerous blind spots.
[00:39] So to set the table, I'll be arguing that recent evidence specifically regarding these fine tuned LLMs proves we have crossed a certain threshold.
[00:48] These models are no longer discounting happy or sad words.
[00:52] They are parsing complex context to deliver actionable, high accuracy predictions for assets ranging from tech stocks to cryptocurrency.
[01:01] And I'm taking the position that while the processing power is, of course, impressive, the methodology is fundamentally flawed because it's un-unimodal.
[01:09] It relies entirely on text.
[01:11] By ignoring the vocal cues and facial expressions that drive human communication, these models are missing the deception and nuance that, frankly, define financial markets.
[01:20] Let's dive right into the evidence because the leap in performance is, well, it's hard to ignore.
[01:27] I want to start with the Harmonizing Macro Financial Factors study by Amin and his colleagues.
[01:32] They didn't just look at stock prices.
[01:34] They analyzed half a million tweets about chat GPT between late 2022 and early 2023 to predict the movement of tech giants like Microsoft and Google.
[01:45] Right, right.
[01:45] The AI boom period.
[01:47] Exactly.
[01:48] But here's the key insight.
[01:49] They didn't just look at the text.
[01:51] They integrated macro factors like the Consumer Price Index.
[01:55] When they applied a random forest model, which is, you know, essentially a way of averaging multiple decision trees to improve accuracy, the results were staggering.
[02:05] They achieved 100% accuracy and identifying bullish trends for Microsoft.
[02:10] For Google, they hit 98% accuracy on bearish trends.
[02:13] They effectively quantified the hype cycle.
[02:15] Okay.
[02:16] But I have to push back on the, let's say, universality of that finding.
[02:22] You're looking at a singular, massive hype event.
[02:25] Microsoft investing in open AI created a mechanical link.
[02:30] People tweet, chat GPT, and Microsoft stock goes up.
[02:33] It's almost a self-fulfilling prophecy.
[02:36] But the model distinguished between the companies.
[02:39] It wasn't just a blanket rule.
[02:40] True.
[02:41] True.
[02:41] But look at the controls they used.
[02:43] The study included the Twitter Economic Uncertainty Index.
[02:47] My argument is that during a period of high volatility, the model might just be picking up on broader economic anxiety rather than genuine insight into the company.
[02:56] Plus, you know, random forest is a robust tool, but it's still traditional machine learning.
[03:02] Are we predicting market sentiment or are we just correlating high volume noise with a stock that was probably destined to skyrocket anyway because of a corporate deal?
[03:10] I think dismissing it as noise is a bit too easy.
[03:14] If we move to a messier, more volatile arena, cryptocurrency, the signal still holds up.
[03:20] And this is where we see the evolution from traditional models to true large language models.
[03:24] Ruma Leotis and his colleagues were in a fascinating comparison on crypto sentiment.
[03:29] And crypto is arguably the hardest place to find a clean signal.
[03:33] Yeah.
[03:33] Which makes the results even more impressive.
[03:36] They compared older models, like BERT, against a fine-tuned GPT-4.
[03:40] In the old days, we used bag-of-words approaches, literally just counting positive adjectives.
[03:45] But GPT-4 understands context.
[03:47] It achieved an accuracy of 86.7%, beating out the specialized financial model FINBERT.
[03:54] This suggests that a general-purpose brain, when you teach it the jargon, navigates the chaos of crypto news better than models built specifically for finance.
[04:02] Yeah, I've read that study and there is a devil in the details there.
[04:06] If you look closely, the base GPT-4 model, before they spent all the time and money fine-tuning it, was terrible at one specific thing.
[04:15] Identifying neutral sentiment.
[04:17] Well, sure.
[04:18] No model is perfect right out of the box.
[04:20] That's why we fine-tune.
[04:22] But neutral is everything in finance.
[04:24] Neutral means hold.
[04:26] It implies stability.
[04:28] I mean, if the most advanced AI in the world needs heavy computational surgery just to realize a news article is noncommittal, it suggests it lacks inherent financial reasoning.
[04:37] It's forcing a binary view on a nuanced world.
[04:40] I'd argue you're focusing on the engineering hurdles rather than the final output.
[04:45] Once it was tuned, the F1 scores, which balance precision and recall, were superior.
[04:51] The architecture can learn the nuance.
[04:52] But can it learn deception?
[04:55] This is where the text-only approach just, it hits a hard wall.
[04:59] Let's talk about spin.
[05:02] The literature review by Todd and his colleagues brings up a critical point about earnings press releases versus 10K filings.
[05:08] The discrepancy in tone?
[05:10] Exactly.
[05:11] Managers know they are being watched.
[05:13] The data shows that earnings press releases contain about 1.27% optimistic words, whereas the legally binding 10K filings only have about 1.08%.
[05:22] That might sound small, but in finance, that is a massive gap.
[05:26] Managers are spinning the press release.
[05:28] If your AI only reads the text, it's being manipulated by the very people it's supposed to analyze.
[05:33] That's a valid concern, though I would probably interpret that data a bit differently.
[05:38] That discrepancy isn't a bug.
[05:40] It's a feature we can track.
[05:42] The same literature points out that analyst sentiment during the Q&A sessions has stronger predictive power than the manager's speech.
[05:50] Because the analysts are the professional skeptics.
[05:53] Precisely.
[05:53] And the models are sophisticated enough to separate the speakers.
[05:57] They can, you know, discount the CEO's spin in the press release and heavily weight the analyst's doubt in the Q&A.
[06:05] The study by Million and Smith showed that analyst's praise is significantly linked to abnormal returns.
[06:11] The algorithm identifies who was speaking.
[06:14] It filters out the noise of the spin to find the signal in the skepticism.
[06:18] That works, sure, if the skepticism is written down.
[06:22] But you and I both know that humans communicate doubt through hesitation, through pitch, through silence.
[06:29] This is the 738-55 rule mentioned in the review.
[06:33] Only 7% of communication is the actual words.
[06:36] 38% is vocal.
[06:38] Okay, but we're trading stocks here, not analyzing therapy sessions.
[06:42] The text is the legal record.
[06:44] But the market reacts to the voice.
[06:46] Research by Mew and Venica Chilam prove that a manager's affective state, their vocal cues, predicts unexpected earnings even when you control for the text.
[06:57] If a CEO sounds confident but the text is neutral, the stock moves.
[07:02] Your text-based transformers, no matter how fine-tuned, are completely deaf to that signal.
[07:07] Look, I'm not ignoring the value of voice.
[07:09] I'm really not.
[07:11] But I am looking at the reality of deployment.
[07:13] The finance literature, as Todd noted, is lagging behind computer science.
[07:20] We are just now getting Wall Street to adopt transformers like BERT and GBT-4.
[07:25] There's massive untapped potential in text analysis.
[07:29] We are seeing 90% accuracy in some sectors before we need to complicate the pipeline with complex audiovisual processing.
[07:36] To me, that sounds like optimizing a fax machine when the internet has just arrived.
[07:40] We are hitting the ceiling of what text can actually do.
[07:44] I have to disagree.
[07:45] We are seeing a quantum leap, not a ceiling.
[07:49] We've gone from, you know, looking up words in a dictionary to large language models that understand sarcasm and context.
[07:56] The evidence from Amin and Rumliadis shows that for high-velocity assets like tech and crypto, these text-based models are already outperforming human analysts.
[08:06] And I would conclude that while those models are impressive, they are brittle.
[08:11] They require specific optimizers, massive fine-tuning, and as we discussed, they struggle with the basic concept of neutrality.
[08:20] Until we have multimodal models that can listen to a CEO's hesitation and watch their facial expressions, we are looking at a two-dimensional picture of a three-dimensional market.
[08:31] So it seems we agree that AI can quantify the mood, but we disagree on how much of the picture is actually missing, whether the text itself is enough or whether we need the voice behind it.
[08:42] That seems to be the next frontier.
[08:44] Indeed.
[08:45] The question for the listener is simple.
[08:48] Would you trust your portfolio to an algorithm that can read the news but can't hear the panic in the anchor's voice?
[08:55] That is all for this debate.
[08:57] Thank you for listening.
[08:57] Thank you.
