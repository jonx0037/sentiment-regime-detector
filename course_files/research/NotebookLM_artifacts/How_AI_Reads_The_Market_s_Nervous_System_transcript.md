# Transcript: How_AI_Reads_The_Market_s_Nervous_System.m4a

[00:00] Okay, let's unpack this.
[00:01] You know, there's this romantic image of the stock market that we all have in our heads.
[00:06] We picture the buttonwood tree in 1792, or, you know, the crowded trading floor of the NYSE in the 80s.
[00:13] Men in different colored jackets shouting, waving papers, sweating.
[00:18] Right.
[00:18] And the smartest guy in the room was the one who could literally read the room.
[00:22] He could look at the sweat on another trader's brow, hear the panic and the shouting,
[00:27] and know instinctively that a crash was coming.
[00:30] The ultimate gut feeling.
[00:31] It was biological.
[00:34] It was visceral.
[00:35] Exactly.
[00:35] But today, that room doesn't exist.
[00:38] The floor is the entire internet.
[00:40] The shouting is millions of tweets, Reddit posts, news headlines, and earnings calls all happening at the same time.
[00:45] Simultaneously.
[00:46] And the premise of today's deep dive is, how do we replicate that old school gut feeling when the room is now, well, infinite?
[00:52] And more importantly, how do we do it without going deaf from the noise?
[00:56] Right.
[00:56] Because the sources we have in front of us today, specifically this, this massive capstone research by Rocha,
[01:02] along with a bunch of supporting studies from King Meghni, Dackelbob, and others, they're telling us something pretty uncomfortable.
[01:09] They're saying that the way we've been trying to read the room for the last 10 years is basically broken.
[01:15] Broken might be a charitable word for it.
[01:18] It's definitely outdated.
[01:19] We've been obsessed with Twitter.
[01:20] For a decade, financial sentiment analysis just meant, let's scrape a million tweets and see if people are happy about Tesla.
[01:28] But the research we're unpacking today argues that looking just at Twitter, or X, as it is now, is a massive strategic error.
[01:36] Oh, it is.
[01:37] It's like trying to predict the weather by only looking out a window that faces north.
[01:41] That's a great analogy.
[01:43] Because if a storm is coming from the south, you're going to get soaked while looking at a perfectly sunny sky.
[01:49] And the core theme of all this research, and especially that Rocha capstone, is heterogeneity.
[01:55] It's, I know, a $5 word, but it's so crucial here.
[01:59] It just means the market isn't one conversation.
[02:02] It's a messy, chaotic ecosystem of distinct subcultures.
[02:06] Okay.
[02:07] You have the mean lords on Reddit, the serious suits reading Bloomberg.
[02:11] You have the outgoes parsing 10K reports, and then the crypto fanatics on Discord.
[02:15] If you aren't listening to all of them at the same time, you just aren't seeing the market.
[02:19] You're missing the big picture.
[02:20] So the mission for this deep dive is to figure out how on earth we synthesize that mess.
[02:25] We're moving beyond just counting positive or negative words.
[02:29] Way beyond that.
[02:30] We're talking about models that can distinguish between a YOLO bet on our Wall Street bets and, you know, a hedged risk in a corporate disclosure.
[02:37] We're going to look at how machines are learning to read charts, listen to the tone of a CEO's voice, and merge all of that into a single prediction.
[02:44] We are, in effect, trying to map the entire nervous system of the global economy.
[02:49] So let's start with that concept you mentioned, heterogeneity.
[02:53] Why is more sources actually different?
[02:55] I mean, why can't it just scrape more tweets to get a better signal?
[03:00] Because not all text is created equal, and maybe more importantly, not all intent is equal.
[03:05] If you just scrape more tweets, you're just getting more impulsive, performative noise.
[03:10] More of the same thing.
[03:11] Exactly.
[03:12] The Rocha Capstone highlights this beautifully.
[03:14] They propose aggregating sentiment across four totally distinct asset classes.
[03:19] Equities, crypto, forex, and commodities.
[03:22] What they found, and this is key, is that you cannot use a one-size-fits-all model.
[03:27] You can't.
[03:27] Because the people talking about these assets speak entirely different languages.
[03:31] Okay, let's drill into that.
[03:33] Take Reddit versus, say, Reuters.
[03:35] I think most listeners understand they are different, but mechanically, how does an algorithm treat them differently?
[03:40] Well, just think about the structure.
[03:42] A Reuters article is what we'd call structured and formal.
[03:45] It goes through an editorial process.
[03:46] It uses standard grammar.
[03:48] It at least attempts to be objective.
[03:51] Right.
[03:52] There are rules.
[03:53] There are rules.
[03:54] A Reddit post on rwallstreetbets is the definition of unstructured and informal.
[03:59] It's full of slang, sarcasm, emojis, typos, you name it.
[04:04] And irony.
[04:05] So much irony.
[04:06] Oh, huge amounts of irony.
[04:07] And that's a complete nightmare for standard models.
[04:09] If a user posts, you know, I am losing all my money on this stock.
[04:13] This is great.
[04:13] A standard cinema model just sees the word great and marks the whole post as positive.
[04:18] Which is the exact opposite of reality.
[04:20] Exactly.
[04:21] A human or a very highly specialized model knows that's pure sarcasm and despair.
[04:26] And then there's the whole subculture element, the diamond hands phenomenon.
[04:29] That's a perfect example.
[04:30] If you feed the phrase diamond hands into a standard English dictionary, it's just nonsense.
[04:35] It'll probably think about jewelry.
[04:36] But in the Wall Street Bets lexicon, diamond hands is an incredibly strong, bullish signal.
[04:42] It means you're holding on no matter what.
[04:45] It means high conviction to hold through extreme volatility.
[04:48] Conversely, paper hands is bearish, a sign of weakness.
[04:52] Then you have terms like bag holding.
[04:53] Which sounds pretty neutral.
[04:55] In standard English, holding a bag is neutral.
[04:59] In the trading world, being a bag holder means you're stuck with a losing asset that has collapsed and you can't sell it.
[05:05] It's a deeply negative, almost shameful term.
[05:08] So if you use a generic tool, you're misclassifying the core sentiment of the entire retail market.
[05:15] You are literally getting the signal backward.
[05:17] Precisely.
[05:18] You are getting garbage inputs.
[05:20] And the Rocha study specifically points this out.
[05:22] You need different classifiers for different communities.
[05:25] You can't use the same brain to read our cryptocurrency that you use to read the Wall Street Journal.
[05:31] They are different worlds.
[05:32] But here's the flip side that really surprised me in the King Magni study.
[05:36] We usually assume the institutional signal, you know, the Bloomberg and Reuters stuff, is the gold standard.
[05:41] It's the smart money.
[05:42] Right.
[05:42] That's the common wisdom.
[05:43] But King Magni found something really counterintuitive about where the predictive power actually comes from.
[05:48] This was a shocker, really.
[05:50] They compared the giants, Bloomberg and Reuters against what we might call tier two or more retail focused outlets, specifically Benzinga and Zacks.
[05:58] And to be clear, Benzinga isn't some tabloid, but it's definitely punchier.
[06:01] It's faster.
[06:02] It's clickier.
[06:03] It feels more aggressive.
[06:04] It is.
[06:05] And the study found that in certain contexts, Benzinga and Zacks actually showed higher predictive utility and temporal stability than the giants.
[06:14] Wait, really?
[06:15] The clickier news was more accurate for prediction.
[06:17] How is that possible?
[06:18] It's a bit open to interpretation, but there are two main theories.
[06:22] One is just raw speed.
[06:24] Benzinga is designed to push headlines instantly to day traders.
[06:28] They might be capturing that sentiment shift minutes before the more polished, detailed Reuters analysis hits the wire.
[06:35] And in modern markets, minutes are an eternity.
[06:37] An absolute eternity.
[06:38] The second theory is about filtering.
[06:42] Reuters and Bloomberg might smooth out the sentiment.
[06:44] They use more neutral journalistic language, which can actually dampen the signal.
[06:48] Benzinga might just say, stock crashes on bad news, which for an algorithm is a raw, clear, unambiguous signal.
[06:55] So the journalistic polish actually hurts the prediction.
[06:58] Sometimes.
[06:59] Yeah.
[06:59] Raw emotion can be a better predictor of immediate price action than a nuanced analysis.
[07:04] But this leads to an even bigger problem with news that King Meghny highlighted.
[07:09] What they call the agreement problem.
[07:11] I looked at that matrix in the notes.
[07:13] The sentiment sign agreement matrix.
[07:15] It's wild.
[07:17] It is startling.
[07:17] Let's do a quick thought experiment.
[07:19] Apple releases its quarterly earnings.
[07:21] It's a complex report.
[07:22] Revenue is up.
[07:24] But iPhone sales in China are a little bit down.
[07:27] How do you report that?
[07:28] Apple posts record revenue.
[07:30] Yeah.
[07:30] Or Apple shows cracks in crucial China market.
[07:32] Exactly.
[07:33] You'd expect Reuters and Bloomberg, the two titans, to broadly agree on whether the overall news is good or bad.
[07:39] But the data shows they only agree on the sentiment sign about 47 to 60 percent of the time.
[07:45] That is, that is barely better than a coin flip.
[07:48] It is a coin flip.
[07:48] So if I'm an algorithmic trader and I'm only subscribing to the Bloomberg feed, I might be buying Apple because my feed says positive.
[07:55] Meanwhile, the guy across the street using the Reuters feed is shorting it because his feed says negative on the same news.
[08:02] That is exactly what happens.
[08:03] Yeah.
[08:03] And that is precisely why the single source approach is so incredibly dangerous.
[08:08] Yeah.
[08:08] If you are relying on just one editorial voice, you are completely blind to the other half of the market's perception.
[08:17] That's a huge blind spot.
[08:18] It's massive.
[08:19] Right.
[08:19] And the Rocher research argues really strongly that you need a multi-source approach.
[08:24] You need to ingest Bloomberg, Reuters, and Benzinga and then average out the editorial bias to find something closer to the true ground truth of the sentiment.
[08:34] It's like getting a second opinion from a doctor.
[08:37] If one says you're fine and the other says you're dying, you probably want a third opinion before you celebrate.
[08:43] Or before you start planning the funeral, yes.
[08:45] And this connects to the other massive variable here, time.
[08:49] The lag factor.
[08:50] We always hear news is old news.
[08:51] By the time it's in the Wall Street Journal, the big move is already over.
[08:54] That's the efficiency of the market right there.
[08:55] Yeah.
[08:56] But social media disrupts this a bit.
[08:57] There was a great study by Kai and others looking at stock message boards, specifically East Money in China, which is pretty similar to stock twits here.
[09:05] And they were looking at really high frequency data, right?
[09:08] Yeah.
[09:09] They were breaking it down into half hourly chunks.
[09:11] And they found that the predictive power of sentiment decays incredibly fast.
[09:16] To capture what they call alpha, the real profit, you need to update your sentiment analysis every 30 minutes.
[09:22] If you are using daily summaries, you are just looking at a fossil record.
[09:26] So the tweet might predict the next 30 minutes.
[09:30] The Reuters article maybe explains the last four hours.
[09:33] And the 10K report explains the last quarter.
[09:35] You have to layer these different time frames on top of each other.
[09:38] You can't just treat them as a flat surface.
[09:40] This is a perfect segue into the how.
[09:43] We have this massive spectrum of data tweets, reports, news.
[09:48] But how do computers actually read this stuff?
[09:51] Because I remember the early days of sentiment analysis.
[09:54] It was, I mean, basically a glorified spell checker.
[09:57] It was the bag of words era.
[09:58] And it was exactly what it sounds like.
[10:01] You take a document, you metaphorically shake it up into a bag of individual words, and you just count them.
[10:06] You have a dictionary of good words and a dictionary of bad words.
[10:08] Profit is good. Loss is bad. Simple.
[10:12] Way too simple.
[10:13] This method hit a huge wall, which became known as the Laughlin and McDonald problem.
[10:18] This is a classic, classic case study in financial natural language processing.
[10:23] Explain that for us.
[10:24] So Laughlin and McDonald, they looked at these standard English dictionaries.
[10:29] They were being used for sentiment analysis.
[10:32] They found that in standard everyday English, the word liability is negative.
[10:36] It implies a burden, a fault, something wrong.
[10:41] He's liability to the team, something like that.
[10:42] Exactly. But in finance, assets and liabilities, it's just a line item on a balance sheet.
[10:48] Every single company on earth has liabilities.
[10:51] It's not bad. It's just accounting.
[10:53] But if an old school model read a balance sheet, it would see the word liability 50 times and just start screaming,
[10:58] Sell! Sell!
[11:00] This company is in terrible trouble.
[11:01] When in reality, it's just a completely standard report.
[11:04] And it was the same with the word share. In normal English, share is a positive word.
[11:08] Sharing is caring.
[11:09] In finance, a share is just a unit of stock. It's neutral.
[11:14] So these generic dictionaries were just hallucinating sentiment where there was absolutely none.
[11:18] They were misclassifying everything.
[11:20] So they had to build better dictionaries.
[11:21] I've heard of Vader. Sounds like a Star Wars villain, but it's a tool, right?
[11:25] Vader, yes.
[11:26] It stands for Valence Aware Dictionary and Sentiment Reasoner.
[11:29] And it was a big step forward. It's rule-based.
[11:33] It understands that GOOD, in all caps, is more intense than GOOD in lowercase.
[11:39] It understands that an exclamation point adds intensity. It even understands emojis.
[11:44] So it's kind of the teenager of sentiment tools. It gets the vibe.
[11:47] It gets the vibe.
[11:48] It's great for social media, but it still lacks deep context.
[11:52] It doesn't really understand the sentence.
[11:53] It just scores the individual components.
[11:55] If I say the company absolutely killed it this quarter, Vader might see the word killed and tag that as negative.
[12:02] When a human knows, that means they did great.
[12:05] Exactly. And that brings us to the modern era, the Transformers.
[12:09] This is where we stop counting words and start, well, trying to read minds.
[12:12] This is the quantum leap.
[12:13] It is. We move from dictionaries to large language models.
[12:17] And the big one here is BERT bidirectional encoder representations from Transformers.
[12:22] Okay, let's unpack BERT versus FinBERT.
[12:24] I see this distinction a lot in the Rocha paper and the FinSo study.
[12:28] What makes FinBERT so special?
[12:31] Think of the original BERT as a brilliant, brilliant student who has read the entire Internet, Wikipedia, every book, millions of blogs.
[12:40] It understands English grammar perfectly.
[12:42] It knows about cats and history and cooking.
[12:45] It's a generalist.
[12:46] A total generalist.
[12:47] But if you hand that student a dense, legalistic, financial 10K report, they might struggle with the nuance.
[12:53] They might still think liability is a bad word.
[12:55] So you send the student to business school.
[12:57] That is the perfect analogy.
[12:59] That process is called domain adaptation or fine-tuning.
[13:02] FinBERT is just BERT.
[13:03] But it has been forced to read millions of financial documents.
[13:07] The Reuters TRC2 dataset, the Financial Phrase Bank.
[13:11] It essentially relearns the language of finance.
[13:13] So FinBERT learns that earnings missed estimates is a disaster, even if the word missed isn't inherently evil in a general context like I missed the bus.
[13:22] Correct.
[13:23] It understands the context of financial disappointment.
[13:25] But, and here's the really important catch that the Rocha Capstone points out.
[13:30] FinBERT is a suit.
[13:32] It's a professional.
[13:33] It's great for formal news.
[13:34] Okay.
[13:35] But what happens if you feed it a Reddit thread full of typos, slang, and diamond hands?
[13:40] It's the banker walking into a rave.
[13:43] He's confused.
[13:43] He's uncomfortable.
[13:45] He fails miserably.
[13:46] And that is why the researchers also use another model, Roberta.
[13:49] Roberta is a robustly optimized version of BERT that really excels at handling noisy, informal grammar.
[13:58] It's much, much better at the rave.
[14:00] So the ensemble superiority hypothesis that's mentioned in the Rocha study, that's basically saying don't pick one.
[14:06] Don't choose.
[14:07] Use FinBERT to read Bloomberg.
[14:09] Use Roberta or another specialized model like FinSoCent to read stock twits.
[14:13] Then you have them vote, where you average their scores.
[14:15] This ensemble approach aligns perfectly with the heterogeneous nature of the data.
[14:20] You use the right expert for the right room.
[14:22] I want to touch on FinSoCent for a second because that sounds like a very specific tool.
[14:26] It is.
[14:26] It's a domain-specific large language model trained purely on the SSIX corpus, which is just stock twits and Twitter data.
[14:34] And the key takeaway here is all about efficiency.
[14:38] Everyone today thinks GPT-4 is the answer to everything.
[14:40] Just ask chat GPT.
[14:42] Right.
[14:42] But GPT-4 is massive.
[14:44] It's incredibly expensive to run.
[14:46] And because it knows everything about everything, it's sometimes too broad.
[14:50] The research suggests that smaller domain-specific models like FinSoCent can often outperform massive general models in these niche tasks, like predicting stock direction.
[15:01] Why is that?
[15:02] Because they are hyper-focused on that specific vocabulary.
[15:05] They don't know who the president of France is, but they know exactly what a bear trap or a short squeeze means in extreme detail.
[15:10] So we have the data, this whole mess of the internet, and we have the brains, these specialized models.
[15:15] Now for the million-dollar question, what does this actually tell us?
[15:18] Because as an investor, I don't really care if a tweet is happy.
[15:20] I care if the market is going to crash.
[15:22] And this brings us to the concept of market regimes.
[15:25] This is the so what of all of this.
[15:28] Sentiment isn't just a squiggly line on a graph.
[15:30] It defines the underlying psychology of the entire market environment.
[15:35] The Roche's study is attempting to use this multi-source sentiment to detect risk-on versus risk-off regimes.
[15:42] Let's define those terms for the listeners who might hear them on financial news but not really know the mechanics.
[15:47] Sure.
[15:47] Risk-on is a regime where investors feel brave.
[15:50] They're greedy.
[15:51] They are actively buying speculative assets, tech stocks, crypto, emerging markets.
[15:57] Risk-off is the complete opposite.
[15:59] Fear dominates the market.
[16:01] Investors sell the risky stuff, and they hide in so-called safe havens gold, U.S. treasury bonds, the Swiss franc.
[16:07] And the goal is to spot that switch before everyone else does?
[16:10] The holy grail is predicting that shift before it shows up in the price.
[16:14] The study suggests that these aggregated sentiment signals might lead the VIX, the volatility index, which is often called the fear gauge, by one to five days.
[16:22] That is huge.
[16:23] If you know the fear gauge is going to spike five days before it actually happens,
[16:27] you can make a fortune or at least save one.
[16:30] That's the theory.
[16:31] But it's not uniform.
[16:32] It varies wildly by asset class.
[16:34] And let's look at crypto versus equities, because the Trushkovsky and Dackelbob studies highlight this divide perfectly.
[16:42] Crypto has to be the most emotional market on Earth.
[16:45] It feels like it's pure psychology.
[16:47] It is the emotional market.
[16:48] Trushkovsky found very strong evidence of something called Granger causality in crypto.
[16:54] Granger causality.
[16:55] We need to break that down.
[16:56] It sounds like some kind of legal term.
[16:58] Think of it like a detective trying to figure out who shot first.
[17:01] Does A cause B or does B cause A?
[17:05] In the traditional stock market, it's usually price drives sentiment.
[17:09] The stock drops, then people get sad and angry on Twitter.
[17:11] Right.
[17:12] I see the red line on my screen and then I tweet, ouch.
[17:14] Exactly.
[17:15] But in crypto, specifically with Bitcoin, they found the reverse is often true.
[17:20] Sentiment on Twitter and Reddit frequently precedes the price move.
[17:23] The sentiment actually drives the price.
[17:25] That actually makes a lot of sense.
[17:27] I mean, Bitcoin doesn't have earnings.
[17:29] It doesn't have a CEO.
[17:30] It doesn't pay dividends.
[17:31] It basically just has belief.
[17:33] So if the belief starts to waver, the price has to move.
[17:36] That's it.
[17:37] Exactly.
[17:37] It is an asset class built almost entirely on social consensus.
[17:40] But here's where it gets even more nuanced.
[17:43] Volatility.
[17:44] In Bitcoin, negative sentiment correlates with price volatility.
[17:48] But the users often see that volatility as a speculative opportunity.
[17:52] They see the chaos and think, great, I can trade this.
[17:56] Whereas in Ethereum, the sentiment was found to be more purely emotionally driven.
[18:02] Fear led to selling, period.
[18:03] There was less of that embrace the chaos mentality.
[18:07] So Bitcoiners are adrenaline junkies.
[18:09] The data certainly suggests a much higher tolerance for chaos.
[18:12] Now, contrast that whole world with Forex, the currency market, the euro, the dollar, the yen.
[18:17] That seems like it would be way too big for Twitter to move.
[18:20] I can't crash the U.S. dollar by tweeting a mean meme about it.
[18:23] You cannot.
[18:24] Forex is the macro market.
[18:26] It's driven by huge things like interest rates, GDP growth, unemployment numbers.
[18:32] And so the Doc O'Bopp model introduces a multimodal approach here.
[18:36] They argue you have to combine the text analysis with these macro financial factors, CPI numbers, unemployment rates.
[18:42] So for Forex, you need the hard economic data plus the news about it.
[18:47] And you need precise alignment.
[18:48] This was a huge point in the Doc O'Bopp studies.
[18:50] You have to align the news timestamp exactly with the price candle.
[18:54] If the news drops at 10.03 a.m., you need to look at the 10.03 a.m. price movement.
[19:00] If you just look at the daily average, the signal is completely washed out.
[19:04] This is what they call a microstructure of the market.
[19:06] There was another concept in the notes for this section that really caught my eye.
[19:09] Asymmetric connectedness.
[19:10] This was from the Nyakurikwa and Setheram study.
[19:13] It sounds complicated, but I think it just validates something we all feel deep down.
[19:16] Bad news travels fast.
[19:19] That is exactly what it means.
[19:20] They studied the Dow Jones Industrial Average as a network, and they found that negative sentiment is more connected.
[19:26] It spreads faster.
[19:27] It influences more of its peers.
[19:29] And it lingers longer than positive sentiment does.
[19:31] Fear is more contagious than greed.
[19:33] Biologically, yes.
[19:34] We are literally wired to react more strongly to threats.
[19:39] In the market, one bad rumor about a single bank can start to drag down the whole financial sector in minutes.
[19:44] Good news comes out, and the market often goes, eh, maybe.
[19:48] Let's see.
[19:49] But here is the twist that I found fascinating.
[19:51] On social media, this dynamic can completely flip during bull runs.
[19:56] Yes.
[19:57] Think back to 2021, the GameStop era, the crypto bubble.
[20:01] During those manic episodes, FOMO, the fear of missing out, became a positive sentiment contagion that actually spread faster and more virally than fear.
[20:10] Everyone seeing their neighbor getting rich on a meme coin was a stronger viral signal than the underlying risk of losing email.
[20:15] Precisely.
[20:16] So the regime dictates the physics of the sentiment.
[20:20] In a bear market, fear spreads fastest.
[20:23] In a mania, greed spreads fastest.
[20:26] The model has to know which regime we are in to know how to properly weight the signals it's seeing.
[20:31] This is getting really deep.
[20:32] We've covered text pretty extensively.
[20:34] But let's be real.
[20:35] The internet isn't just text anymore.
[20:37] I scroll through my feed, and it's charts.
[20:39] It's memes with rocket ships.
[20:41] It's videos of CEOs talking.
[20:44] This is the multimodal frontier.
[20:46] And honestly, this is where the cutting edge of data science is right now.
[20:49] Text-only analysis is definitely hitting a ceiling.
[20:52] Because a picture is worth a thousand words, right?
[20:54] Literally.
[20:55] Source 3 in our stack discusses visual sentiment.
[20:58] If I post a picture of a bull or a rocket ship emoji or a chart with a big green arrow pointing up, that carries a massive amount of sentiment.
[21:06] But a text miner just sees a blank space.
[21:08] It misses the entire message.
[21:09] So the models are learning to see the memes.
[21:12] Yes.
[21:12] They use computer vision to analyze the images.
[21:15] But even more important, I think, is the fusion of text and technicals.
[21:18] The Dogglebub paper discusses a mechanism called cross-attention.
[21:22] I love the analogy we had in the notes for this.
[21:24] Imagine two experts sitting in a room.
[21:27] Right.
[21:27] One expert is a technical analyst.
[21:29] He doesn't read the news.
[21:30] He only looks at the price chart, the moving averages, the candlesticks.
[21:33] Yeah.
[21:33] The other expert is a fundamentalist.
[21:36] He only reads the news, the tweets, the reports.
[21:39] Cross-attention is the mechanism that allows them to whisper to each other to confirm a signal.
[21:45] So the chart guy says, hey, this looks like a textbook buy signal.
[21:48] We have a breakout.
[21:49] And the news guy whispers back, hold on a second.
[21:52] Mm-hmm.
[21:52] I'm reading a lot of anxiety about the CEO on Twitter right now.
[21:55] This might be a false breakout.
[21:57] Let's maybe wait.
[21:58] Or the chart says sell.
[22:00] But the news guy says, no, this drop is just a temporary overreaction to a rumor I saw.
[22:05] The fundamentals are still totally fine.
[22:07] Buy the dip.
[22:08] Exactly.
[22:08] The model learns to weigh these two streams of information dynamically.
[22:13] It learns when to trust the chart and when to trust the news.
[22:16] And then there's audio, the Todd et al. study.
[22:19] This is fascinating because we usually just read the transcripts of earnings calls.
[22:23] Transcripts are sanitized.
[22:24] They're cleaned up.
[22:25] They completely lose the tone.
[22:27] A CEO can say, we're confident in the next quarter.
[22:30] On paper, that's positive.
[22:32] A simple model sees confident and scores it high.
[22:34] But if they say it like, we are confident in the next quarter with a shaky voice.
[22:40] Exactly.
[22:40] A shaky voice, a hesitation, a change in pitch, a nervous cough.
[22:44] Those are all biological leakage.
[22:47] They reveal the truth that the carefully chosen words are trying to hide.
[22:51] Current research is trying to fuse audio wave analysis, literally analyzing the sound waves of the voice with the text analysis.
[22:59] Wow.
[23:00] The text says confident, but the voice says terrified.
[23:02] The model flags a massive risk.
[23:04] That is incredible.
[23:05] It's like a lie detector for earnings calls.
[23:07] It is attempting to capture the implicit sentiment that the text completely misses.
[23:11] But, and there's always a light, but on this show, we have to go to the skeptics corner.
[23:16] Because if this was easy, everyone would be a billionaire.
[23:18] We'd all be on yachts and nobody would be listening to this deep dive.
[23:21] Correct.
[23:22] And the King Meghni paper provides a very necessary, very sobering reality check.
[23:27] Despite all this incredible tech Lama 3, FinBert, multimodal, fusion-accurate next-day prediction, remains incredibly, incredibly elusive.
[23:36] Why? I mean, if we have all this data, if we have the god mode of market surveillance, why can't we just predict tomorrow?
[23:42] The Efficient Market Hypothesis, or EMH.
[23:45] It's an old idea, but it's still very powerful.
[23:48] The theory is that any new information is absorbed into the price almost instantly.
[23:52] By the time your model reads the news, processes the sentiment, and executes a trade, the market has often already moved.
[23:58] The alpha decays in milliseconds.
[24:00] So for high-frequency trading, maybe this is just too slow.
[24:03] And cost is another massive factor.
[24:05] Running a huge LLM like Roberta or Lama, it takes an enormous amount of computational power.
[24:10] It requires expensive GBUs, it burns electricity, it costs hard dollars.
[24:14] Simple dictionaries like Vader are fast and cheap.
[24:17] So King Meghni raises the economic question.
[24:19] Is that 1% or 2% accuracy boost you get from a massive brain worth the massive cost?
[24:24] If the model costs $10,000 a month to run, and it only makes you $9,000 in extra profit...
[24:30] You're losing money.
[24:31] For a retail trader, these massive models are probably complete overkill.
[24:36] For a huge hedge fund managing billions of dollars, that 1% edge could be worth millions.
[24:43] So it's a scale game.
[24:45] And there was a technical point about overfitting when you combine price and sentiment data.
[24:49] This sounded like the model getting lazy.
[24:52] This is a classic machine learning trap.
[24:54] When you give a model both sentiment data, like news, and price history, like charts, and you ask it to predict the future price,
[25:01] the model often realizes that yesterday's price is a really, really good predictor of today's price.
[25:06] Because trends tend to continue, an object in motion.
[25:10] Right.
[25:10] So the model effectively says, you know what, why should I bother reading all this complex, messy news?
[25:15] I'll just look at the chart.
[25:16] It starts to ignore the sentiment data and just predicts based on the price history.
[25:20] It overfits to the price.
[25:22] So it stops reading the news and just looks at the ticker tape.
[25:24] Exactly.
[25:25] And then when a huge news event does break the trend, like a surprise war or a pandemic or a company fraud,
[25:31] the model misses it completely because it was ignoring the news channel all along.
[25:37] Researchers have to actually force the model to pay attention to the text,
[25:41] sometimes by hiding the price data during its training.
[25:44] There's also the issue of the sources themselves.
[25:46] We talked about hedging in corporate reports earlier.
[25:49] Oh, 10-Ks are written by lawyers.
[25:50] Their entire job is to minimize liability.
[25:53] So they use hedging language constantly.
[25:56] We anticipate potential challenges.
[25:58] Forward-looking statements are subject to significant risk.
[26:01] They avoid direct negative words like the plague.
[26:04] Unlike a Redditor who just says, this stock is complete trash.
[26:07] Exactly.
[26:08] The Reddit post is blunt and clear.
[26:10] The 10-K is purposefully obfuscated.
[26:12] And this makes sentiment detection so much harder in formal documents compared to social media.
[26:17] You need a model that understands that the phrase potential material adverse effect actually means we might go bankrupt.
[26:22] So to wrap this all up, we've journeyed from just counting happy words on Twitter to these massive, multi-headed hydra models that listen to CEO voice trimmers, read Reddit memes, and analyze charts all at the same time.
[26:37] We have moved from a dictionary to a nervous system.
[26:41] That's really the best way to think about it.
[26:43] The modern approach isn't about finding one perfect source.
[26:46] It's about the ensemble.
[26:48] It's the ability to weigh a Reddit meme against a Bloomberg headline, against a CEO's tone of voice, and find the true signal in all that noise.
[26:56] It seems like the Holy Grail isn't a single magical formula.
[26:59] It's the integration of it all.
[27:01] It is the synthesis of heterogeneity.
[27:03] It is accepting that the market is messy and building a model that embraces that mess instead of trying to simplify it.
[27:09] Now, before we sign off, I want to leave our listeners with a thought.
[27:12] We're building these incredibly sophisticated systems to read the market psychology.
[27:15] We are teaching machines to understand human fear and greed.
[27:18] But as these systems get bigger, and as more and more money is traded by them, are they starting to create the psychology?
[27:25] That is the final provocative thought, isn't it?
[27:28] As these models become widespread, they begin to create the very sentiment they're designed to analyze.
[27:33] If an AI reads negative sentiment and decides to sell, its selling action lowers the price.
[27:39] That lower price scares people, or more likely other AIs, which creates more negative sentiment.
[27:45] The AI then reads that new sentiment and sells more.
[27:48] It's a feedback loop, an AI-induced panic.
[27:52] And we are definitely entering the era of agentic AI autonomous agents that don't just predict but execute trades based on these complex webs of data.
[28:01] We might be moving toward a world where market psychology is no longer entirely human.
[28:06] It's machines reading machines and getting scared of other machines.
[28:09] And on that slightly terrifying note, we'll leave you to think about who or what is really moving the market today.
[28:15] Thanks for listening to The Deep Dive.
[28:17] Always a pleasure.
[28:18] Keep questioning the data.
[28:19] See you next time.
