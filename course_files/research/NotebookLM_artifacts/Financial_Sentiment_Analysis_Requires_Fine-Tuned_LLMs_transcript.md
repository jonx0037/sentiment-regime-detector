# Transcript: Financial_Sentiment_Analysis_Requires_Fine-Tuned_LLMs.m4a

[00:00] Okay, so we're looking at a comparative synthesis on financial sentiment analysis,
[00:06] which tracks the evolution from lexicons and random forest all the way to LLMs like GPT-4.
[00:12] Right. Let's jump right into the gaps in the draft.
[00:15] The first thing that jumps out is the hierarchy of model evaluation.
[00:20] The draft creates this kind of false equivalency between the traditional classifiers and the newer transformer models.
[00:27] It really does. It holds up that finding from Ahmed et al., the one where random forest hits, what, 100% recall?
[00:34] Yeah, and it presents it like it's a huge victory.
[00:37] Exactly. While the Rumiliadis study shows the far more advanced GPT-4, topping out at around 86%, it just doesn't add up.
[00:46] It reads more like a scorecard than a deep analysis.
[00:49] The suggestion here has to be to frame those perfect scores from the older models as, well, a red flag.
[00:55] A huge red flag for overfitting.
[00:58] Absolutely. The rewrite needs to clearly position the transformer architectures as the superior standard for nuance,
[01:05] you know, regardless of that raw accuracy metric.
[01:08] And to make that concrete, when the draft discusses the Microsoft and Google predictions,
[01:13] it needs to contrast those perfect random forest numbers with the Todd et al. literature review.
[01:18] Right, because that review clearly identifies BERT and GPT-3 as the actual state-of-the-art.
[01:24] Yes. So you have to tell the reader that the perfect score likely lacks generalizability.
[01:30] It's just not robust in the way the Rumiliadis study shows fine-tuned LLMs can be.
[01:35] And, you know, speaking of robustness, relying only on text to get those scores, that really hurts the search for nuance.
[01:42] Oh, definitely. The submission is so over-indexed on tweets and news headlines.
[01:47] It completely misses the whole multimodal frontier that's mentioned in the literature review.
[01:52] It just restricts the analysis so much. So our suggestion is to broaden the scope by adding a section on paralinguistic features from earnings calls.
[02:03] To increase the robustness.
[02:05] Exactly. The Todd et al review is very explicit here. You need to be analyzing vocal pitch, intensity, even the pauses and silences.
[02:14] Because that's where you find the managerial affective states. The things the transcripts alone just can't capture.
[02:21] And adding that layer is what moves this piece from a basic summary to a really strong synthesis.
[02:27] But even with better data, the way the draft talks about the models is still too broad. It says things like using GPT-4 or using BERT.
[02:36] Right. As if the off-the-shelf versions are just good to go for a specialized field like finance.
[02:42] Which is a fatal flaw in this domain.
[02:45] It really is. I mean, the Rumeliotius data shows the base GPT-4 model just flailing with neutral sentiment labels.
[02:52] It can't handle them. And the draft doesn't connect the dots that without fine-tuning, that model is fundamentally unreliable.
[02:59] So the suggestion isn't that fine-tuning is some optional optimization.
[03:04] No. It has to be framed as a hard requirement. Non-negotiable.
[03:08] And a concrete way to show that is to combine those GPT-4 error rates with a Todd et al comparison of, you know, FinBERT versus a StandardBERT.
[03:16] Yeah.
[03:16] The reader has to walk away knowing that general models fail at financial neutrality. Domain adaptation is the only path to a reliable signal.
[03:24] So to recap then, really scrutinize those perfect scores from older classifiers. They're probably a sign of overfitting.
[03:32] Then integrate that multimodal audio data from earnings calls to capture the real tone and sentiment.
[03:37] And finally, insist that fine-tuning isn't just a nice-to-have. It's absolutely essential for detecting neutral sentiment accurately.
[03:46] We look forward to seeing the rewrite.
