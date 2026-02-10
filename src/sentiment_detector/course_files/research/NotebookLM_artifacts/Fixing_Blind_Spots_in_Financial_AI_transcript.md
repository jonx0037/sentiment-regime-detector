# Transcript: Fixing_Blind_Spots_in_Financial_AI.m4a

[00:00] We're looking at a fascinating submission today, a suite of three papers on NLP and financial markets.
[00:06] They cover using Twitter for stock trends, LLMs for crypto, and a big literature review on what's next.
[00:13] It's an ambitious package for sure.
[00:14] It is. But there's this massive tension right from the start between the theory they lay out and the actual experiments they run.
[00:24] And that brings us to the first big issue, multimodal data.
[00:28] The research establishes a strong theoretical case for multimodal analysis, but stops short of applying it to the empirical studies.
[00:36] Yeah, this is a big one.
[00:38] I mean, the literature review that taught at Allpaper, it's fantastic.
[00:42] It explicitly flags this as the future.
[00:45] They even drop that stat, you know, that 38% of human emotion comes through vocal attributes.
[00:50] Not what you say, but how you say it.
[00:52] Exactly. So they build this incredible case, this theoretical Ferrari.
[00:57] But then in the actual studies, the Amin and Romeliotti's papers...
[01:01] They leave it in the garage.
[01:02] They leave it in the garage and ride a bicycle. It's all text.
[01:05] Just hashtags, news articles.
[01:08] They completely ignore the very data they just told us was critical.
[01:12] Right. And you have to ask why.
[01:14] I mean, to play devil's advocate, text is clean.
[01:17] You know, it's structured.
[01:19] You feed it to GPT-4, you get a number back.
[01:22] Audio is...
[01:23] Messy.
[01:24] It's messy, yeah.
[01:25] But by ignoring it, you're ignoring the signal.
[01:28] You're ignoring those paralinguistic cues they talked about.
[01:32] The pitch, the intensity.
[01:33] The jitter, the shimmer.
[01:34] All of it.
[01:35] I mean, think about an earnings conference call.
[01:37] It's the perfect example they bring up.
[01:39] The transcript might say, we are confident in our Q4 outlook.
[01:43] Uh-huh.
[01:43] Sounds positive.
[01:44] But if you listen to the audio, the CEO's voice cracks.
[01:48] The pitch goes way up.
[01:49] He's stuttering.
[01:50] A human hears fear.
[01:52] A text model just reads confident.
[01:54] You're buying right before the crash.
[01:56] And they even have that Tesla example in there with Elon Musk.
[01:59] The boring, bonehead questions moment.
[02:02] Yes, the text is rude, sure.
[02:04] But the audio?
[02:05] The audio is pure hostility.
[02:08] The paper notes the share drop that followed, but then their own models?
[02:11] Don't try to capture that.
[02:12] They're still just reading the transcript.
[02:14] Exactly.
[02:15] So, okay.
[02:16] A suggestion for improvement.
[02:18] How do we get them to bridge that gap?
[02:20] Well, it's actually pretty straightforward.
[02:22] They have the advanced model from the Romaliotis paper, the fine-tuned GPT-4.
[02:26] And they have the data source from the Todd paper, the earnings calls.
[02:30] So, combine them.
[02:31] Just combine them.
[02:32] Propose an experiment.
[02:34] Run the call transcripts through GPT-4 for a sentiment score.
[02:37] Then run the audio files through a separate model that's designed to quantify vocal stress.
[02:42] The jitter, the intensity.
[02:44] And then fuse the results.
[02:46] Fuse them.
[02:46] And see if angry voice plus dismissive text predicts that Tesla's share drop more accurately than the text alone.
[02:53] My money says it does.
[02:54] And if they prove that, they've shown a real market inefficiency.
[02:58] That takes it from just another model comparison to something exploitable.
[03:03] That's a huge leap.
[03:04] But that leads to another blind spot, doesn't it?
[03:08] It's not just the data.
[03:09] It's the whole economic environment.
[03:11] The vacuum problem.
[03:12] The methodology for normalizing external economic factors is inconsistently applied across the different asset classes presented.
[03:20] In the stock market paper, the Amin study.
[03:23] They are so rigorous.
[03:24] They harmonize everything with macro variables.
[03:27] They've got the Twitter economic uncertainty index, CPI, unemployment.
[03:31] Standard.
[03:32] Robust econometrics.
[03:33] You have to do it.
[03:34] You have to.
[03:36] But then you turn to the Rumeliotis crypto paper and all of that just evaporates.
[03:41] It's gone.
[03:42] No control variables.
[03:43] It's just a cage match.
[03:44] GPT-4 versus FinBert.
[03:46] It treats crypto like it exists in a completely different universe.
[03:50] Which is so dangerous.
[03:51] Because now you have to ask, is GPT-4 actually better at understanding crypto sentiment?
[03:57] Or is it just better at riding a macro wave that you're not controlling for?
[04:01] Right.
[04:01] If the whole study took place during a bull run when inflation was low, any model that just says buy is going to look like a genius.
[04:09] Or worse, what if crypto is actually more sensitive to that Twitter uncertainty index?
[04:15] You know, when people get scared, they dump risk on assets like Bitcoin first.
[04:19] So if you aren't controlling for that...
[04:21] You have no idea if your model is picking up on subtle sentiment or just reacting to widespread economic panic.
[04:27] The whole comparison is contaminated.
[04:29] So how do they fix it?
[04:31] This is probably the easiest fix in the whole critique.
[04:34] It's a copy-paste job.
[04:35] Steal from yourself.
[04:36] Steal from yourself.
[04:37] Steal from the Amin paper.
[04:40] Grab those variables.
[04:41] The TEU index.
[04:42] The CPI data.
[04:44] And just drop them in as features into the Rumeliadis crypto dataset.
[04:47] And then rerun the showdown.
[04:49] Rerun the showdown.
[04:50] But add a twist.
[04:52] Don't just give me the overall accuracy.
[04:54] I want a stress test.
[04:56] Filter the results.
[04:57] Show me how GPT-4 performs against FinBert when the consumer confidence index is in the toilet versus when it's sky high.
[05:04] Oh, that's interesting.
[05:05] So if GPT-4's edge disappears when the economy is bad...
[05:09] Then it tells you the model isn't smarter.
[05:11] It's just fair-weather smart.
[05:13] And that's a much more valuable insight.
[05:15] It goes from GPT-4 is 86% accurate to GPT-4 is superior in stable markets but vulnerable to macro shocks.
[05:23] That level of nuance is key.
[05:26] Which brings us to the third big issue.
[05:27] The material relies heavily on quantitative accuracy scores without providing sufficient linguistic analysis of why specific models outperform others.
[05:37] Yes.
[05:37] The black box problem.
[05:39] This is my biggest pet peeve.
[05:41] I mean, we see these impressive numbers, right?
[05:43] 86.7% accuracy.
[05:46] 100% recall for bullish Microsoft trends.
[05:49] But there's zero analysis of why.
[05:52] They give you a scoreboard but they never show you the game tape.
[05:55] We know that it works but not how.
[05:57] Why did FinBert fail on that one headline?
[05:59] Why did GPT-4 get it right?
[06:01] And without that why, you can't really trust it, can you?
[06:04] Because what if it's right for the wrong reason?
[06:06] Like overfitting.
[06:07] Look at that 100% recall number for random forest on bullish Microsoft trends.
[06:12] 100%.
[06:13] That immediately makes me suspicious.
[06:16] Yeah, that feels too good to be true.
[06:17] Is it really understanding nuanced bullish sentiment or did it just learn that the hashtag hashtag chat GPT means buy?
[06:24] Because if that's all it is, it's not sentiment analysis.
[06:27] It's a simple keyword search.
[06:29] And it's brittle.
[06:30] So the suggestion here is to what?
[06:32] Look under the hood?
[06:33] Exactly.
[06:34] Do a granular qualitative error analysis.
[06:37] I want them to pull the false positives and false negatives and dissect them.
[06:41] And what are they looking for?
[06:43] For the linguistic tripping wires.
[06:45] They mention those domain-specific dictionaries in the Todd paper.
[06:49] You know, words like liability, bad and normal conversation, totally neutral in accounting.
[06:54] Maybe GPT-4 gets that context.
[06:57] Okay, so you want them to show their work.
[07:00] I want them to show me 5 to 10 specific crypto headlines where FinBert said neutral and GPT-4 correctly said positive.
[07:08] Put them side by side.
[07:09] Look for patterns.
[07:10] Like what kind of patterns?
[07:11] Look for what linguists call irrealist moods, hypothetical statements.
[07:16] Words like could, might, potential.
[07:19] Older models choke on those.
[07:20] They see uncertainty and default to neutral.
[07:23] LLMs are much better at understanding that a potential partnership is a bullish signal.
[07:28] Or even just slang.
[07:30] Crypto Twitter is full of it.
[07:31] Hodl.
[07:32] Paperhands.
[07:33] Right.
[07:34] If FinBert thinks Paperhands is an office supply company, that explains a lot.
[07:38] But they have to show us that.
[07:40] There's that chart in the Rumi Liatis paper, Figure 1, that shows the base GPT-4 model struggled with neutral labels.
[07:47] But the fine-tuned one nailed them.
[07:50] That's the perfect place to do this analysis.
[07:52] Show us an example of a tweet the base model got wrong that the fine-tuned model got right.
[07:57] Show us what the fine-tuning process actually taught the model about the language of the market.
[08:02] That's so much more powerful than just saying, accuracy went up 2%.
[08:06] It proves learning, not just memorization.
[08:10] Okay.
[08:10] So, let's say they do all that.
[08:12] They add audio.
[08:13] They add macro controls.
[08:15] They open the black box.
[08:17] We're still left with the biggest question of all.
[08:20] Causality.
[08:20] The argument for the predictive power of social sentiment needs to move beyond correlation to establish stronger causal links.
[08:28] The chicken and the egg.
[08:30] And right now, the submission is very, very weak on this.
[08:34] The Amin paper literally admits they found, and I'm quoting,
[08:38] intriguing indications suggesting a plausible correlation.
[08:42] Plausible correlation is not something you bet the farm on.
[08:44] No, it's weak.
[08:46] And their own literature review warns about this.
[08:49] It talks about reverse causality.
[08:51] The stock price moves, and then people tweet about it.
[08:54] If your model just picks that up, it's not a predictor.
[08:57] It's a rear-view mirror.
[08:59] And you will crash.
[09:00] So they have to prove their model is looking out the windshield.
[09:04] So, how do they do that?
[09:05] They have to get much more aggressive with time.
[09:08] Time-lagged analysis.
[09:09] The Todd paper mentions looking at intraday data.
[09:13] Don't just match today's tweets to today's closing price.
[09:17] That's too blunt an instrument.
[09:18] Go tighter.
[09:19] Much tighter.
[09:21] Take those 500K chat GPT tweets, analyze the sentiment at 10 a.m., and compare it to the price at 10.30 a.m.
[09:28] Then compare it to the price at 10.30 a.m. the next day.
[09:32] If the signal is strong at 30 minutes, but gone by 24 hours, you've found something.
[09:37] But if the sentiment at 10 o'clock just matches the price move from 9.55...
[09:41] Then you've found nothing.
[09:43] It's a reaction.
[09:44] It's reverse causality.
[09:45] But I think there's an even better way to test for this.
[09:48] The quiet day test.
[09:50] Use their uncertainty index or just a corporate calendar to find days where there were zero major announcements for a company.
[09:58] No earnings.
[09:59] No press releases.
[10:00] A boring day.
[10:01] A day the stock shouldn't move much.
[10:03] Exactly.
[10:03] Now, on one of those quiet days, if their sentiment model picks up a big surge in positive tweets, rumors, leaks, whatever, and then the stock moves up...
[10:15] That's the holy grail.
[10:16] That's the golden ticket.
[10:17] Because that proves the social chatter contains information that isn't yet in the official news.
[10:24] It separates the real signal from the noise of everyone reacting to an earnings report.
[10:28] This has been a really comprehensive teardown, but in a constructive way.
[10:34] Absolutely.
[10:35] The potential here is incredible.
[10:38] They have the models.
[10:39] They have the data.
[10:40] They just need to tighten the methodology.
[10:42] So, to recap for the authors.
[10:45] Four clear pillars to rebuild on.
[10:48] Pillar 1.
[10:49] Go multimodal.
[10:50] Don't just talk about audio.
[10:52] Use it.
[10:53] Run that earnings call study.
[10:55] Fuse the vocal cues with the text.
[10:57] Pillar 2.
[10:59] Harmonize your variables.
[11:00] Apply those same macro controls from the stock paper to the crypto paper.
[11:04] And stress test the models against a bad economy.
[11:08] Pillar 3.
[11:09] Explain the why.
[11:10] Open that black box.
[11:12] Give us a real linguistic error analysis.
[11:15] Show us the tweets and the headlines that separate the good models from the great ones.
[11:19] And finally, Pillar 4.
[11:21] Prove causality.
[11:22] Get aggressive with time lags and use that quiet day test to prove your model is a headlight, not a taillight.
[11:29] If they do those four things, this isn't just a strong submission.
[11:32] This is the kind of work that gets cited by hedge funds.
[11:35] That's the goal.
[11:35] There is a fantastic idea here.
[11:38] It just needs to be refined.
[11:40] Tighten up the methodology.
[11:40] Run the new experiments.
[11:42] And please send it back to us.
[11:44] We would love to see version 2.0.
[11:46] Thanks for listening.
[11:47] Now go fix your models.
