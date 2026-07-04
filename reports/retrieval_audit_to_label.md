# Retrieval-audit labeling worksheet

Total rows: **50** (out-of-gate sample for retrieval recall estimation).

## Instructions

Each row below is a comment that the lexicon retrieval gate marked
as NOT about AI (`ai_hits == 0`). For each row, **change exactly one
`[ ]` to `[x]`** to record your judgment:

- `ai` — comment IS actually about AI (lexicon missed it: retrieval false negative)
- `not_ai` — comment is correctly not about AI

We use the resulting empirical AI-rate in this sample to estimate the
lexicon retrieval recall:

```
estimated_recall = n_retrieved_ai / (n_retrieved_ai + n_missed_ai)
```

where `n_missed_ai = (estimated AI-rate in this sample) * (size of out-of-gate pool)`.

When done, extract labels with:

```bash
PYTHONPATH=src python scripts/extract_retrieval_labels.py
```

---

## 1. [2021-07] soft_hit=yes

_Story:_ Toyota is quietly pushing Congress to slow the shift to electric vehicles

_Comment:_ toyota is quietly pushing congress to slow the shift to electric vehicles that was a typo. if you look at the amount of work and research i have done on this subject i think it is pretty easy to determine "confused" is far from where i am. yes, it is 1 gw. and my math uses this number, not 1 mw. i invite you to run through your own calculations. i actually want to be wrong. i just don't see what i am missing. again, this is about developing a rom (rough order of magnitude) model. the difference between 50, 100 and 300 nuclear plants is almost irrelevant. why? because we can't even build a single nuclear plant in 10 to 25 years, which means that a rom requirement of ten, twenty or a hundred nuclear power plants might as well be a million. in the us, we are at a point in history where we can't build anything of any real scale. the best example i have of this is the failed high speed train in california. a project sold to voters as a ten billion dollar price tag. it is now at a hundred billion, only about ten miles have been built. these ten miles are unusable (not in service as far as i know) and are far from being high speed by any definition of the term. some think this thing will …

**Gold is_ai** _(comment_id=27985255)_:

  - [ ] ai
  - [ ] not_ai

---

## 2. [2020-04] soft_hit=no

_Story:_ Colleges at the breaking point, forcing ‘hard choices’ about education

_Comment:_ colleges at the breaking point, forcing ‘hard choices’ about education colleges have been peddling shoddy goods to unsophisticated buyers for years with little or no regulation or oversight. in fact, the government has propped them up with federal money, loan guarantees, and a feeder school system that conditions their potential customers and funnels them in the doors. the shoddy goods are degrees that are highly unlikely to be worth what was paid for. you can't get more unsophisticated than an 18 year old who's been fed a dream about how their life will be awesome if they get into the school of their choice.

**Gold is_ai** _(comment_id=23037292)_:

  - [ ] ai
  - [ ] not_ai

---

## 3. [2022-06] soft_hit=yes

_Story:_ MIT engineers fly first-ever plane with no moving parts (2018)

_Comment:_ mit engineers fly first-ever plane with no moving parts (2018) while hummingbirds are amazing, i think we will have to model out systems more closely to birds of prey. most birds can’t carry much extra weight, until you get to raptors and some sea birds. we would be after something that can carry a payload such as a salmon, a coconut, or a human.

**Gold is_ai** _(comment_id=31935070)_:

  - [ ] ai
  - [ ] not_ai

---

## 4. [2020-03] soft_hit=no

_Story:_ Machine translation of cortical activity to text with encoder–decoder framework

_Comment:_ machine translation of cortical activity to text with encoder–decoder framework not to swing my credentials around, but i actually record neural activity, from monkey brains, for a living. it can be unexpectedly hard in so many different ways. the dura covering the monkey brain is much tougher, the brain itself is larger, more convoluted, and moves more, even just from breathing and heartbeats). the animals have busy, clever little fingers, so the interface itself needs to be mechanically robust and durable because these implants need to last for years . i certainly want this to be true: with the exception of neuropixels, electrode technology has been depressingly stagnant. on the other hand, i need to see data before i get too excited and if i did have it, i'd be shouting it from the rooftops.

**Gold is_ai** _(comment_id=22738178)_:

  - [ ] ai
  - [ ] not_ai

---

## 5. [2020-05] soft_hit=yes

_Story:_ Evolution of Emacs Lisp [pdf]

_Comment:_ evolution of emacs lisp [pdf] > the title is pretty clear. the complaint is that the title is in fact unclear. if someone comes up to me saying they are going to talk about the evolution of monkeys they have two strategies: (1) developed protein complex a, cell mechanism b became vestigial, a sequence xyz came from a disease which became part of the cell structure, etc. (2) when they migrated from a to b abundant food sources meant that selective pressure caused c. then flooding destroyed the habitat and killed off all the monkeys that weren't d and that trait can still be seen today. etc. (1) focuses on technical mechanisms and (2) focuses on pressures and adaptions. this article has a mix of both, but it focuses in on the mechanism and a lot less on the adaptions within emacs. not the interpretation of 'evolution' that i was hoping for. take the section on concurrency - it leaves open the interesting question of "why was there pressure to make a text editor concurrent?" and "what did they want to do with that concurrency?". the article notes that use appears to still be limited - so why did they feel pressure to implement a feature people aren't using? are there issues with emacs…

**Gold is_ai** _(comment_id=23102630)_:

  - [ ] ai
  - [ ] not_ai

---

## 6. [2023-06] soft_hit=no

_Story:_ YouTube is testing a more aggressive approach against ad blockers

_Comment:_ youtube is testing a more aggressive approach against ad blockers honestly, seeing an old spice ad isn't going to make me buy old spice. and seeing a 1 hour ad for some guy telling me to stop eating what i'm eating to have no-wipe bowel movements isn't going to make me buy the stuff. there have been studies done about plumbers. the ones that pay money to get on top in the white pages have worse reviews than the ones that work by word of mouth. i go by the same thing. if you feel that your product needs an ad, it's probably overpriced and / or doesn't do what it says it does.

**Gold is_ai** _(comment_id=36537125)_:

  - [ ] ai
  - [ ] not_ai

---

## 7. [2022-07] soft_hit=yes

_Story:_ Shouldibuytwitter.com – A tiny takeover arbitrage model for TWTR

_Comment:_ shouldibuytwitter.com – a tiny takeover arbitrage model for twtr one possible scenario: he took over twitter. fire the execs. opening up all emails. you can bet at least one person out of 6000 employees disagree with how twitter counts bot number. pick that email, point out that execs discarded a concern raised by employee. change the calculation of bot number to be higher. report to sec in public earning. allude that the previous number was just plainly wrong. sue the execs for fraud... since sec accepts the new number and approach which is materially different from the old number. to be honest, just opening up all emails is already bad enough for execs.

**Gold is_ai** _(comment_id=32161466)_:

  - [ ] ai
  - [ ] not_ai

---

## 8. [2022-01] soft_hit=yes

_Story:_ Danish government makes its new economic model open source

_Comment:_ danish government makes its new economic model open source what are you a skeptic of, exactly? this is the model actually used by the danish ministry of finance to study the effects of various policy changes. i don't think there's any need to speculate about how much influence it will have: it apparently is already in use and guides policymaking. other advanced economies have their own similar models used for studying and making various aspects of economic policy. i think another poster has provided a link to the model used by the ny fed. at a high level, i, like you, am fairly persuaded by the hayekian point that its impossible to collect enough information or otherwise capture the necessary complexity to reliably model even a moderately complex economy with enough fidelity to allow central planning. but this is far short of that. and there does seem to be a need for general models to allow policymakers to make informed decisions. the only alternative would seem to be to make no decisions at all which a) is itself a decision and 2) does not seem to be an option that many people seriously advance. i guess your position could be that these efforts are doomed to failure--i.e., no mod…

**Gold is_ai** _(comment_id=30032710)_:

  - [ ] ai
  - [ ] not_ai

---

## 9. [2024-01] soft_hit=no

_Story:_ New Renderers for GTK

_Comment:_ new renderers for gtk game engines can afford to be generations ahead : they might even be targeting specific hardware (single console release), they typically assume a sandboxed environment that they are in total control of (at best, they'll make a limited and tightly controlled gui framework for modders), they might have restricted themselves to a limited number of inputs/outputs (single screen with a specific resolution, gamepad only), they don't have to worry about unknown unknown uses by other developers... none of these apply to a generalist renderer, therefore it can only "lag behind" the game ones. (unless maybe if we're talking about the "human side of the question" : what are the best designs, layouts for a generalist human/machine interface ? here it's the generalist guis that i would expect to be a couple of generations ahead (xerox' labs, apple's macintosh, ibm's common user access standard, cern's world wide web...)

**Gold is_ai** _(comment_id=39176092)_:

  - [ ] ai
  - [ ] not_ai

---

## 10. [2020-01] soft_hit=no

_Story:_ How to Exit Vim

_Comment:_ how to exit vim i am a vim user, and if i had a group leader tell me that i had to use some different editor because we are all learning how to do this job together, and that learning how to use the editor properly was part of learning how to do the job, i would do what he says. at least for as long as he stays in the room... on the other hand, we had an architect who has since retired that said, if it was up to him, all developers across the campus would use the same programming language, editor, and configuration. thankfully it was not up to him, and we still have this lovely diversity of opinions and tools that signals it is encouraged for specializations to develop, thus making sure that we are not all replaceable cogs in an exceedingly boring machine. but the memory of this man's twisted vision remains with me, and it strikes me that the leadership still would seem to prefer if we were in fact fungible units of work-capacity, without any distinctive features or unique characteristics differentiating us from other developers. imo if you learned to ensure there was no proof of different tools, you learned an equally valuable lesson; i would mark you down for example if i opened …

**Gold is_ai** _(comment_id=21995098)_:

  - [ ] ai
  - [ ] not_ai

---

## 11. [2021-01] soft_hit=yes

_Story:_ We don't need data scientists, we need data engineers

_Comment:_ we don't need data scientists, we need data engineers >are they, basically, software engineers who specialize in putting other peoples' models into production? it depends on the company. traditionally, yes, but deployment into production can be automated, so typically today it is something different. an mle is someone who specializes in tensorflow or pytorch. they write deep neural networks, reinforcement learning, and more. often times the data scientist will make a model, specializing in feature engineering and domain experience, and use a generic ml like a generic dnn or xgboost or whatever it may be. it then gets handed off to an mle who writes ml specific for the problem to get every last drop of accuracy out of the model. they then hand it off to prod. i don't think they're on call (i could be wrong on this.) so today they're not really deploying models much. they're more an inbetween. i work at small companies and startups so i've never worked with an mle, but i do have friends who are managers at google who told me about it, so that's where this information is coming from, telephone game. in other words, i'd take this with a grain of salt. ymmv. starting in 2018 big name co…

**Gold is_ai** _(comment_id=25794948)_:

  - [ ] ai
  - [ ] not_ai

---

## 12. [2021-10] soft_hit=yes

_Story:_ Bitcoin: Who owns it, who mines it, who’s breaking the law

_Comment:_ bitcoin: who owns it, who mines it, who’s breaking the law ultimately, yes. that problem is unsolvable. there will always be more of us than there is stuff to sustain us (unless you get rid of the people ;) ). our survival—and arguably, sense of meaning—is dependent on our ability to produce value for others in exchange for money. what bitcoin solves is removing the ability for that money to be manipulated. for example, in the u.s., if i'm at a bank or a large enough company, i can get 0% interest loans from the federal reserve. that would be fine if the money was backed by something, but it isn't. as the federal reserve, i can print more and more money ad infinitum and then give it away at 0% interest. this is literally money that is not backed by a commensurate amount of value (e.g., gold or some other precious asset like my time/labor). in this model, i can take resources of the table without replacing them rendering me, effectively, a parasite. the u.s. dollar (or any fiat currency) is not _real_ in the sense that it functions within a set of fixed, well-defined laws. bitcoin on the other hand functions based on the laws of mathematics and its own, publicly exposed source code …

**Gold is_ai** _(comment_id=28880292)_:

  - [ ] ai
  - [ ] not_ai

---

## 13. [2020-08] soft_hit=yes

_Story:_ Differentiable Control Problems

_Comment:_ differentiable control problems gradient descent is already about as easy a training method as can be. just a little freshman calculus and programmers can do the "state of the art" optimization of modern times. it's also scalable. if your polynomial regression gets too large because of the model complexity (for comparison, typical deep networks can have millions of parameters) you can't invert your matrix and probably end up using a similar method anyway. i would have thought a computer uses tables to compute e^x. there's also piecewise linear activation functions that are trivially easy to compute gradients of. the whole "universal approximation" perspective is pretty vague to begin with. i'd say generally people don't understand why nn's work as well as they do. previously theorists expected they would need a lot more training data to work, given their complexity. so it's driven to a large degree by empirical success. i am certainly really interested to see people accomplishing the same things with less sophisticated methods, since there is no doubt it has been overused/hyped in some areas just to make the papers and proposals sexier.

**Gold is_ai** _(comment_id=24292052)_:

  - [ ] ai
  - [ ] not_ai

---

## 14. [2021-11] soft_hit=yes

_Story:_ Why philosophers should care about computational complexity (2011)

_Comment:_ why philosophers should care about computational complexity (2011) > since my liking you is caused by my immediate environment, it isn't reducible to a weighted average of my history. it is not clear to me that this cannot be the case of a weighted average very heavily weighted to the immediate past. > the historical positions of all the molecules in some water aren't sufficient to determine its present state. it's state depends on its container (ie., the pressure & temp of its environment). afaik, given that you could determine the momenta of the molecules from a history of their positions, this would be sufficient to determine its state (maybe you need their angular momenta independently?) the relevant information about the container has been impressed on the motion of the molecules. similarly, we can suppose that the history of your environment becomes manifest in your mental states (and a predisposition towards certain state transitions) - though, on account of the complexity of that environment, in a compressed form. > we are more like water than a computer. a computer is a deterministic machine which is a deterministic function of its deterministic inputs. water is a chatoic …

**Gold is_ai** _(comment_id=29247162)_:

  - [ ] ai
  - [ ] not_ai

---

## 15. [2021-03] soft_hit=no

_Story:_ Introducing the Wikimedia Enterprise API

_Comment:_ introducing the wikimedia enterprise api i similarly require that producers of motion pictures say "nosteal" at some point in the opening credits otherwise i assume i am free to make copies of the film to share with the internet.

**Gold is_ai** _(comment_id=26485104)_:

  - [ ] ai
  - [ ] not_ai

---

## 16. [2024-07] soft_hit=no

_Story:_ CrowdStrike CEO summoned to explain epic fail to US Homeland Security committee

_Comment:_ crowdstrike ceo summoned to explain epic fail to us homeland security committee ok, do you think 1000 is way too low, or way too high? e.g., how many life-threatening emergencies do you think happen per hour across the world? how much extra time did it take to reach the average injured person over the outage period? how was the base rate of iatrogenic death affected by losing access to all electronic records for inpatients? if you come up with a fermi estimate more than two orders of magnitude lower than 1,000, i will be suspicious of your assumptions.

**Gold is_ai** _(comment_id=41055660)_:

  - [ ] ai
  - [ ] not_ai

---

## 17. [2023-10] soft_hit=no

_Story:_ Company with a 10% lifetime employee turnover shows their real secret is trust

_Comment:_ company with a 10% lifetime employee turnover shows their real secret is trust money is the wrong excuse to do your own thing. ideally you have something you really enjoy doing or something that fascinates you endlessly then find an angle to do it for a living. it doesn't really matter if you succeed. if your thing is [say] fitness and you get to fool around in your own gym for a few years you've done well. you wanted to dj and started your own club. you enjoy bowling and got to own your own bowling alley - for a while. go do those things you wanted to do when you had all that money?

**Gold is_ai** _(comment_id=38090492)_:

  - [ ] ai
  - [ ] not_ai

---

## 18. [2022-10] soft_hit=yes

_Story:_ US Supreme Court to weigh end to race-based college admissions

_Comment:_ us supreme court to weigh end to race-based college admissions so i'd consider that part of the system. you could also train your model to debias by using a cost function that incorporates race and minimizes the kl divergence between different ethnicities. (obviously it would be best to use interpretable models and/or causal ones) a mahalanobis distance might also be good here. but when training your model you might want to pca it and if race isn't an included factor then you can't see if it is a main contributing component or not. you should be training your model such that the racial variable contributes near nothing to the model's outcome (easier said than done). > in this example, i'd wonder why zip code is even an input. the school you go to is strongly correlated with zip code. so... if any of your schools are considered on your college app (hint: they are) then you have extracted the zip code (which again, points back to red lining[0]). in the crime example, the zip code is going to also correlate with the frequency and type of crime as crime (especially when broken down into types of crime) is not homogeneously distributed across a country/state/city (to be honest, not even…

**Gold is_ai** _(comment_id=33413629)_:

  - [ ] ai
  - [ ] not_ai

---

## 19. [2021-07] soft_hit=yes

_Story:_ For developers, Safari is crap and outdated

_Comment:_ for developers, safari is crap and outdated installing an app gives you a chance to consider the option first, with websites you are required to download and install it to take a look and see what is it all about. on the other hand i wouldn't have a problem with the model where pwa's notifications and other functionalities are limited to apps added to the home screen and the options to manage those is exactly the same with native apps. i don't advocate that all apps must go through the app store.

**Gold is_ai** _(comment_id=27970088)_:

  - [ ] ai
  - [ ] not_ai

---

## 20. [2023-08] soft_hit=no

_Story:_ HashiCorp switching to BSL shows a need for open charter companies

_Comment:_ hashicorp switching to bsl shows a need for open charter companies companies rarely switch from bsd to a commercial license - they are moving from a highly commercially restrictive license like (a)gplv3 to something even stronger. these are typically very unbalanced relationships between the project "owner" and any contributors - the "owner" may require clas and copyright assignment, and reserve the sole right to relicense the code under any license they see fit - but for these sorts of more restrictive relicensing exercises and for an exclusive rights to sell under non-open/copyleft "commercially friendly" licensing. the anger and frustration usually come from thinking that even though the relationship was unbalanced, there was an understanding and social contract where both a community member and the commercial enterprise got value. the relicensing is unbalanced - it removes value from the community member without providing any new benefit. sure, they can quit the community, but that also removes the sources of their value. in the most extreme cases, there have been successful attempts to create entirely new communities (strangely these are predominantly around oracle-owned proje…

**Gold is_ai** _(comment_id=37245614)_:

  - [ ] ai
  - [ ] not_ai

---

## 21. [2021-11] soft_hit=yes

_Story:_ Hubris – A small operating system for deeply-embedded computer systems

_Comment:_ hubris – a small operating system for deeply-embedded computer systems > hubris does support shared memory via leases, but i'm not sure how it manages to map them into the very limited 8 cortex-m mpu regions. what i did in a similar kernel was dynamically map them from a larger table on faults, sort of like you would with a soft fill tlb. when you turn off the mpu in supervisor mode you get a sane 'map everything' mapping, leaving all 8 entries to user code. the way ldm/stm restart after faults is amenable to this model on the m series cores.

**Gold is_ai** _(comment_id=29392999)_:

  - [ ] ai
  - [ ] not_ai

---

## 22. [2022-10] soft_hit=no

_Story:_ Do central banks’ mounting losses actually matter?

_Comment:_ do central banks’ mounting losses actually matter? i don't see the climate analogy. people live their plight. on a day to day basic they know where they stand. they have been watching costs rise and incomes not keeping pace. this is situation decades old but only breaking the narrative surface lately. they're reminded of the power of the fed. true, they might get the exact details wrong, but they have a solid enough grip on who. they also see others (i.e., 1%) doing better and better. "i'm struggling to pay my bills" is all they need to understand. because the people don't understand the nitty gritty doesn't make the fed any less accountable.

**Gold is_ai** _(comment_id=33161986)_:

  - [ ] ai
  - [ ] not_ai

---

## 23. [2023-02] soft_hit=no

_Story:_ Difficult to impossible travel across wide swaths of the U.S.

_Comment:_ difficult to impossible travel across wide swaths of the u.s. big thumbs up to noaa's weather page. i've used it for years. the hour by hour weather report has the exact detail one needs before venturing out. i dont leave home without opening this bookmark. https://forecast.weather.gov/mapclick.php?lat=40.0891&lon=-8... (needs to be set to your zip)

**Gold is_ai** _(comment_id=34906705)_:

  - [ ] ai
  - [ ] not_ai

---

## 24. [2021-05] soft_hit=yes

_Story:_ Making the hard problem of consciousness easier

_Comment:_ making the hard problem of consciousness easier is it hard though? or is the hard part ethics i.e. personhood, and because the terms are conflated that makes consciousness hard, since it means you cannot accept what consciousness is without needing to also define ethics. drop the idea that consciousness is sufficient or required for personhood in favor for something more behaviourally consistent like cuteness or power, and things become clearer. there is a part of you which simulates social interaction by learning models of various other agents it has inferred the existence of. as can be expected from something which is looking for agents based on indirect clues, we know this part does struggle with accidentally assigning agency to things which clearly lack consciousness i.e that damned sharp rock you stepped on twice. this part of you is capable of simulating a finite number of simultaneous such agents at a time, meaning it will focus on, as a whole, being able to predict the actions of the agents most often observed. it is also why we would expect it to replace groups of people you only interact with as a group as a "them". it is also very common that the most significant agent t…

**Gold is_ai** _(comment_id=27324087)_:

  - [ ] ai
  - [ ] not_ai

---

## 25. [2022-02] soft_hit=no

_Story:_ Germany aims to get 100% of energy from renewable sources by 2035

_Comment:_ germany aims to get 100% of energy from renewable sources by 2035 even with less regulation, the problem is that it takes a huge amount of capital, and you need a decade or more to get return on your investment. so it is really not that interesting for a private investor.

**Gold is_ai** _(comment_id=30502129)_:

  - [ ] ai
  - [ ] not_ai

---

## 26. [2021-08] soft_hit=no

_Story:_ T-Mobile: Breach Exposed SSN/DOB of 40M+ People

_Comment:_ t-mobile: breach exposed ssn/dob of 40m+ people > voting is not a constitutional right. yes it is. > voting rights act is statutory like most of our laws. constitutional rights are often enforced by legislation; amendments articulating rights often explicitly authorize this. see, with regard to voting rights, the 15th, 19th, and 26th amendments. (edit: also, the 14th amendment [see sec. 2 and 5], and, as noted in a sibling comment, the 24th amendment. also the 17th amendment, though that doesn’t have a congressional enforcement clause. voting rights are the single most common subject of constitutional amendments.)

**Gold is_ai** _(comment_id=28225048)_:

  - [ ] ai
  - [ ] not_ai

---

## 27. [2022-11] soft_hit=no

_Story:_ No to Spy Pixels

_Comment:_ no to spy pixels standard email marketing best practice is to use this to see if the recipient is opening emails. if the recipient doesn’t, the sender should auto unsubscribe the recipient. blocking tracking pixels means that the “good” email marketers will keep emailing until a manual unsubscribe event happen.

**Gold is_ai** _(comment_id=33755011)_:

  - [ ] ai
  - [ ] not_ai

---

## 28. [2022-05] soft_hit=no

_Story:_ Why Google is so unbearable, and how to fix it

_Comment:_ why google is so unbearable, and how to fix it refreshing layout! those apps are time saver as i don't have to search across different sources by opening up multiple tabs for every query.

**Gold is_ai** _(comment_id=31428164)_:

  - [ ] ai
  - [ ] not_ai

---

## 29. [2023-10] soft_hit=no

_Story:_ Where does my computer get the time from?

_Comment:_ where does my computer get the time from? i don't feel entitled to anything, it was just a suggestion for how they can communicate better, which they ostensibly want. i constantly get lauded for good presentations, and see others do them with unforced errors, so i thought i'd do my part to level the playing field. ironically enough, aren't you doing the same thing now, berating me for giving free information the wrong way ? how about just learning from the advice and moving on?

**Gold is_ai** _(comment_id=37786399)_:

  - [ ] ai
  - [ ] not_ai

---

## 30. [2020-08] soft_hit=yes

_Story:_ Waiting for Gödel (2016)

_Comment:_ waiting for gödel (2016) > question: can a sentence be provably true in one arithmetic system but not another? the answer is yes! zfc |- ac but zf |/- ac and both zfc and zf can encode arithmetic. but there's an issue here: no-one really talks about the "truth" of the axiom of choice as though it's a concrete thing: it's a very controversial axiom, and although most mathematicians accept it, quite a few don't. constructivist mathematicians don't accept it, and it's provably equivalent to the law of the excluded middle, so it can't be used in intuitionistic logics. now you might counter and say that ac isn't the gödel sentence for zfc, and the gödel sentence for pa is true in the intended model. but that's a different matter from whether it's provable from an axiomatic foundation. the reason i think this matters is because mathematicians work with proofs! most mathematicians aren't working in foundations, and rely on proofs to the extent that they don't even consider the truth of statements which cannot be proven. > if so that means there are provably true sentences which exist, but not provably true with the axioms that i have at my disposal right now? the issue is that provability…

**Gold is_ai** _(comment_id=24333354)_:

  - [ ] ai
  - [ ] not_ai

---

## 31. [2023-05] soft_hit=yes

_Story:_ Tell HN: YouTube download websites disappearing from Google search results

_Comment:_ tell hn: youtube download websites disappearing from google search results i think your doomsaying is a bit premature. as long as companies want us to be able to see their content, there will be ways to extract it without the drm gunk. from a security / threat model analysis perspective, drm can never be 100% secure. and remember, for drm to work, all these products have to be perfect 100% of the time. someone trying to break drm only needs to be lucky once. the idea of all software and hardware reaching some sort of perfect level of security is pretty laughable. from the hardware side, tools get cheaper and cheaper every year. even today it's a lot more feasible for a motivated group to do things like decapping chips and scanning them to extract keys. this sort of thing will only get cheaper and more accessible over time. maybe manufacturers will have to start putting hsms into their products that self-destruct when they detect tampering to try to combat this?

**Gold is_ai** _(comment_id=36144494)_:

  - [ ] ai
  - [ ] not_ai

---

## 32. [2021-02] soft_hit=yes

_Story:_ Show HN: Deploy ML Models on a Budget

_Comment:_ show hn: deploy ml models on a budget a cost effective way of deploying models on aws is to use 'zappa' (autotemplating for lambda + api gateway). this just works, and costs my team less for a year than one week of sagemaker or kubernetes architectures. https://www.corbettanalytics.com/deploy-machine-learning-mod...

**Gold is_ai** _(comment_id=25994160)_:

  - [ ] ai
  - [ ] not_ai

---

## 33. [2023-03] soft_hit=yes

_Story:_ Universal Speech Model

_Comment:_ universal speech model if cost isn’t an issue, i’d use one of the established commercial offerings. otherwise, you could try splitting into shorter chunks (20 minutes maybe?), do multiple runs on each chunk and pick out the best run according to some criteria, e.g. character count after removing repetitions. whisper isn’t deterministic so some runs can be better than others; you could also tweak parameters like compression ratio or silence thresholds between runs, but in my experience there’s not going to be an obvious winner leading to a marked improvement in quality. anyway, i’m no expert, and maybe you’ll have better luck than me. my recordings do have background music and conversations in some places that might confuse the model.

**Gold is_ai** _(comment_id=35370627)_:

  - [ ] ai
  - [ ] not_ai

---

## 34. [2023-03] soft_hit=no

_Story:_ Repeat yourself, do more than one thing, and rewrite everything (2018)

_Comment:_ repeat yourself, do more than one thing, and rewrite everything (2018) i don't think it's quite the same though... or at least i can make an argument for learning about ways not to do programming tasks because it generalizes. there are patterns between ways not to do programming related things, e.g. use the single responsibility principle, use pure functions. there are also so many ways to accomplish programming tasks, it's useful to be able to filter down that multitude of ways or notice "this stack overflow post has 5 bad patterns, maybe i shouldn't use it".

**Gold is_ai** _(comment_id=35158834)_:

  - [ ] ai
  - [ ] not_ai

---

## 35. [2023-02] soft_hit=yes

_Story:_ Mercedes-Benz previews its operating system MB.OS

_Comment:_ mercedes-benz previews its operating system mb.os i just found this presentation with technical details: https://group.mercedes-benz.com/dokumente/investoren/praesen... i guess it is not a typical os, but more like a collection of tools that build on already existing oss. this is comparable to ros (robotic operating system), which are just some programs, middleware, services and conventions to build software for robots on linux. it seems like this should integrate and abstract different "os" (linux, qnx, autosar) and run on very different platforms (high power application processor for infotaiment, microcontrollers) (slide 13). these are widely different systems: 1. linux needs a memory managing unit (mmu), which only comes with high(ish) powered application processors, e.g. arm cortex-a9. these are obviously not hard-realtime because a page fault can occur non-deterministically (except when you can lock everything to ram). this might be used for infotaiment. 2. (classic) autosar is used without a operating system on a microcontroller like the arm cortex-m or a automotive mcu like the infinion tricore, which can run two cores in lockstep to verify each computation. autosar is kind …

**Gold is_ai** _(comment_id=34905331)_:

  - [ ] ai
  - [ ] not_ai

---

## 36. [2024-10] soft_hit=yes

_Story:_ Cerebras Trains Llama Models to Leap over GPUs

_Comment:_ cerebras trains llama models to leap over gpus cerebras had less chip perimeter to hook up external memory i/o and is memory capacity limited with just sram. sram circuit size hasn't been scaling nearly as well as logic on recent nodes, but if scaling there had continued to from when cerebras started it may have worked out better. they'll probably still have to do advanced packaging putting hbm on top to save things. they could maybe enable some cool real time inference stuff like vr sora, but that doesn't seem like much of a product market for the cost yet. maybe something heavy on inference iteration like an o1 style model that trades training time for more inference, used to process earnings reports the fastest or something zero sum latency war like that will be a viable market. a real time use case that may be viable with cerebras first could be with flexible robotics in ad hoc latency sensitive environments, maybe warfare. if models keep lasting ~year timescales could we ever see people going with rom chips for the weights instead of memory? has density and speed kept up there? lots of stuff uses identical elements to help make the masks more cheaply, so i don't think you coul…

**Gold is_ai** _(comment_id=42003642)_:

  - [ ] ai
  - [ ] not_ai

---

## 37. [2022-09] soft_hit=no

_Story:_ Censorship by big tech at the behest of the U.S. government?

_Comment:_ censorship by big tech at the behest of the u.s. government? yes, you are noble and altruistic and people who disagree with you are stupid and evil. come on. downplaying, denial, misinformation, exaggeration, victim complexes, persecution complexes, every stop was pulled out, every tactic was tried. like when ron desantis was called a murderer for opening florida's beaches (when it was well established that outside activities were extremely safe), or when parents advocating for schools to open were called white supremacists (when the predictable result of closing schools was that poor and minority students suffered most)? the scariest thing i learned during the last two years is how many people are willing to throw me, you, and everyone (including themselves!) under the bus in order to avoid even mild, temporary inconvenience meanwhile, i learned how many people are willing to have governments literally lock everyone in their homes because of their inability to do any sort of rational risk assessment or cost-benefit analysis.

**Gold is_ai** _(comment_id=32945477)_:

  - [ ] ai
  - [ ] not_ai

---

## 38. [2023-12] soft_hit=no

_Story:_ Ask HN: Books you read in 2023 and recommend for 2024?

_Comment:_ ask hn: books you read in 2023 and recommend for 2024? fiction: "yumi and the nightmare painter" and "tress of the emerald sea" - two of brandon sanderson's "secret projects" that he released this year and easily my favorites of the bunch. tress is just such a fun adventure and yumi left me an emotional wreck by the end. "there is no antimemetics division" - i had a brief period where i wanted to read some stories about clandestine operations around odd anomalies, scp-adjacent if you will. this, alongside "agents of dreamland", is rather short and great for getting through in a couple sittings. it's all about taking on an entity that you actively can't remember the existence of. non-fiction: "letters to a young poet" - this is a collection of ten letters sent from the poet rainer maria rilke to a younger aspiring poet in the early 1900s. as a creative that sometimes struggles with the whole "what am i doing this for?", i found this a highly inspiring and comforting read. "on writing" - i'm sure most of you know the book, or at the least know stephen king. the info in here on writing (at least in the style of king) is fantastic, but i think the memoir portions are the killer part of…

**Gold is_ai** _(comment_id=38562337)_:

  - [ ] ai
  - [ ] not_ai

---

## 39. [2023-08] soft_hit=yes

_Story:_ ISPs should not police online speech no matter how awful it is

_Comment:_ isps should not police online speech no matter how awful it is i dont care what it is protected as, i am telling you what automatically happens once you try to poke holes into it. it shouldnt be a surprise to anyone with a functioning relationship to reality. picture it as a shared communication bus everyone uses for navigation where somebody added a hidden packet drop you cant compensate for or detect. if you try to use that thing you are going to crash. because you have no ability to determine how much gets dropped. and how much bullshit cant be challenged anymore. thats the line in the sand for cascading failure. it cant work. those blind spots cant be detected, managed or compensated for. they are like a metastasizing cancer. that blind spot is at the core of totalitarian regimes. group think sets in and suddenly your farmers are told to plant the crops closer together to utilize the proletarian solidarity between the plants. anyone who doesnt gets gulaged and the rest starves. its worth mentioning that my local constitution has a clause that simplified means anyone trying to get the society to e) can be shot by anyone. how ever much of a paper tiger this is, having had two mur…

**Gold is_ai** _(comment_id=37334270)_:

  - [ ] ai
  - [ ] not_ai

---

## 40. [2023-08] soft_hit=no

_Story:_ Ask HN: Why did Python win?

_Comment:_ ask hn: why did python win? definitely a jack of all trades language. and when you get older, and you care more about solving problems than about trying new things, and you've got more responsibilities in life and lack the time to devote to learning new language / technology du jour, then knowing and using python becomes so handy. if it is indeed the 2nd best language for the job, it is still a decent choice if you get to solve the problem.

**Gold is_ai** _(comment_id=37338045)_:

  - [ ] ai
  - [ ] not_ai

---

## 41. [2022-08] soft_hit=yes

_Story:_ Don’t call it a comeback: Java is still champ

_Comment:_ don’t call it a comeback: java is still champ > sorry, but the popularity of tools which generate boilerplate for you is, in my opinion, one of the biggest indictments of the whole ecosystem. i couldn't disagree more. i can understand disliking the fact that we need getters/setters in the first place, or perhaps dynamic things like annotations which aren't "normal" code, but static code generation is something that the industry absolutely should embrace. model driven development should be more common. for example, if you can just draw a few er diagrams and have mysql workbench forward engineer sql migrations for you to check them over (especially if you need to change 20 tables), why shouldn't you take advantage of that? having a model of your schema that you can generate from the live schema and then transform it into either a set of fresh migrations or just a delta for bringing an older schema version up to date. i've actually used these two approaches to save bunches of time for personal projects in the past, even though i took the sql output and put it into dbmate migration tool. reverse engineer: https://dev.mysql.com/doc/workbench/en/wb-reverse-engineer-create-script.html for…

**Gold is_ai** _(comment_id=32408566)_:

  - [ ] ai
  - [ ] not_ai

---

## 42. [2020-03] soft_hit=no

_Story:_ Ask HN: Books giving practical advice on starting a solo SaaS business?

_Comment:_ ask hn: books giving practical advice on starting a solo saas business? personally, i struggle finding decent advice by reading such books. what i do instead, is i am building my own product. this surfaced quite a few personal limitations - one being focus. there is no amount of times one can read deep work to cover for that moment when things click in your head. by all means read books but practical experience is what wins for me.

**Gold is_ai** _(comment_id=22716079)_:

  - [ ] ai
  - [ ] not_ai

---

## 43. [2022-01] soft_hit=no

_Story:_ Bridge collapse in Pittsburgh’s Frick Park

_Comment:_ bridge collapse in pittsburgh’s frick park what was the limit when the bridge was new?

**Gold is_ai** _(comment_id=30117858)_:

  - [ ] ai
  - [ ] not_ai

---

## 44. [2021-02] soft_hit=no

_Story:_ Fructose reprogrammes glutamine-dependent oxidative metabolism to support LPS

_Comment:_ fructose reprogrammes glutamine-dependent oxidative metabolism to support lps i suppose that depends on what you believe the point is. the opening assertion was that high-fructose corn syrup is a misnomer. this not a historically accurate statement. disregarding any erroneous conflation of high-fructose corn syrup with corn syrup (of the only type that existed prior to the invention of what is termed high-fructose corn syrup), high-fructose corn syrup is most assuredly "high" in that it contains a "high" percentage of fructose (40-90%) in comparison with the previously existing corn syrup which contain 0% fructose. it is spurious to hold to a vague definition of "high" that can only apply to concentrations somewhere in excess of 90%, lest we find ourselves unable to refer to water containing 0.5% lead by weight as having "high" levels of lead. that said, i concur with the assertion that significant consumption of fructose in any of the commonly available forms, including as a component of sucrose, that do not substantially moderate the rate of its absorption (e.g. such as a dietary fiber-based structural matrix) carry an associated negative health risk. it is accurate to say that s…

**Gold is_ai** _(comment_id=26241653)_:

  - [ ] ai
  - [ ] not_ai

---

## 45. [2020-07] soft_hit=yes

_Story:_ Datahike: Durable Datalog database powered by an efficient Datalog query engine

_Comment:_ datahike: durable datalog database powered by an efficient datalog query engine interesting, honestly speaking we have not thought about time series data a lot yet, but i think we should be able to provide custom indices and extend datalog with more efficient query primitives, if this is necessary. can you elaborate a bit? i have used hdf5 binary blobs for tensors of experimental recordings (parameter evolution in spiking neural networks) in datomic a few years ago and it is definitely possible to integrate external index data structures, but eventually the query engine will need to be aware of how to join them efficiently. w.r.t. security, our current approach is to shard access rights and encryption on a database level and just provide many databases, one for each user. this is obviously not the most space efficient, but the most general approach. if users can share access keys and data we can also do structural sharing between these instances and factorize further. we envision doing joins potentially over dozens of distributed datahike instances in a global address space during single queries. since the indices are amortized data structures it does not make too much sense to enc…

**Gold is_ai** _(comment_id=23953227)_:

  - [ ] ai
  - [ ] not_ai

---

## 46. [2022-08] soft_hit=no

_Story:_ Biden cancels $10k in student loan debts

_Comment:_ biden cancels $10k in student loan debts > so, the government got involved in student loans, encouraged people who should have entered trades to get irrelevant degrees, significantly inflated the cost of tuition, and is now not only rewarding poor decisions and debt, but is making others pay for it? if 10,000 people pay $1 each, none of them have any problems. if one person pays $10,000, it's a big problem, and possibly even life-ruining or inaccessible. "making others pay for it" is a skewed perspective on what's really happening when taxes pay for public services, or services that should be public. speaking of "should be public" -- who are you to decide whether other people "should have entered trades" instead of attending university? many people don't attend higher education because they can't afford it, and you're basically saying that means they just should go straight to work and shouldn't even try to get an education? > and who making $125k needs a $10k discount on their loans!? a friend intentionally stopped paying his a while back in anticipation. what a joke. if your friend was affording his payments, then it sounds like your friend is a selfish dick. to answer your quest…

**Gold is_ai** _(comment_id=32583458)_:

  - [ ] ai
  - [ ] not_ai

---

## 47. [2020-10] soft_hit=yes

_Story:_ Reddit’s About page doesn't include Aaron Swartz as a founder

_Comment:_ reddit’s about page doesn't include aaron swartz as a founder jess indeed said that, but also quite a few people pretty much lauded that labour was so omnipresent on social media and that the response from the users was so overwhelmingly positive not realizing that twitter and facebook showing them what they want to see (and in some cases if the leaks to be believed factions in their own party targeted party politicians with their own ads). targeted ads and bespoke feed algorithms are bad enough, but when you combine it with political campaigns it's just a recipe for disaster. and this isn't a problem that is easy to solve and honestly i don't know how and if it can be solved. targeted ads are arguably the easy one but even then how you define targeting, as well as what is clearly a political ad (e.g. a corporation making an ad that exploits a given event such as blm, ow or anything remotely political), the feed is oh boy... people want their feeds curated for them, at this point these platforms know their users better than the users know themselves they know what content keeps them engaged and what drives them away and that's the problem. the content that may be relevant for a giv…

**Gold is_ai** _(comment_id=24680391)_:

  - [ ] ai
  - [ ] not_ai

---

## 48. [2024-01] soft_hit=no

_Story:_ Helios: A distribution of Illumos powering the Oxide Rack

_Comment:_ helios: a distribution of illumos powering the oxide rack > everyone is capable of learning. i can hire someone who is capable of learning japanese. they can then try to teach the rest of the team japanese. does that mean it's a good idea to switch all our internal docs to japanese? the difference between japanese and english is much, much bigger than the difference between one unix os and one unix-like os. this is a remarkably disingenuous argument. if you really don't understand the difference in scope, there's no point in discussing anything with you because you've managed to disprove your opening sentence with yourself as the counterexample.

**Gold is_ai** _(comment_id=39184566)_:

  - [ ] ai
  - [ ] not_ai

---

## 49. [2020-03] soft_hit=yes

_Story:_ Ask HN: Why don't employers post an applicant-to-job ratio?

_Comment:_ ask hn: why don't employers post an applicant-to-job ratio? but stats like that also can signal being over-selective. i would gently suggest that it is a mistake to think in terms of unqualified vs highly-qualified candidates and ml for "callback probability". i don't want a good, but not fang-level, candidate to not apply for our standard software engineer opening just because 74 people already did. why? we had 60+ candidates for a recent posting for a junior developer role with some experience - think 1-2 years or some good school projects. somewhere around 45-50 of those applicants were easily hard-flagged don't interview at all after a quick cover-letter and resume review by a technical person using a rubric. that rubric was scoped only to weed out applicants with absolutely no meaningful experience. while i also hate the laundry-list approach for job listings (must have: expert java and c#, spring orm and activerecord skills with deep understanding of react internals), i think the best way to attack that is with a short, but focused cover letter. that should include a short paragraph or two about a candidate's hands-on experience and speculate how their experience might apply …

**Gold is_ai** _(comment_id=22627969)_:

  - [ ] ai
  - [ ] not_ai

---

## 50. [2020-12] soft_hit=yes

_Story:_ State of Common Lisp Survey 2020

_Comment:_ state of common lisp survey 2020 > i'm explaining why lisp is hard to learn. it is not hard to learn in general, there are too many counterexamples of people of all sorts and skills learning it without these issues you are having, learning it as their first, learning it later in their careers... (cl is big , i'll give you that, but each piece can be chewed one at a time and does not seem to be individually that difficult.) so i can hypothesize why it's hard to learn for you . my first guess is still that you aren't meeting lisp in its own terms and are trying to make lisp fit your mental model of some other language and its ecosystem. this isn't going to work, and the failure mode (if i'm right) has nothing to do with lisp but with biases in general heuristics of learning. you don't need to "unlearn" the way you're used to doing things, but you do need to separate yourself from it for a bit until you actually grasp the lisp (and its ecosystem's) way(s) and can then see the connections, tenuous and non-existent as some may be. i'll risk raising some of those connections below, but really, things need to be understood on their own terms first or you wind up with misconceptions. (i've…

**Gold is_ai** _(comment_id=25298127)_:

  - [ ] ai
  - [ ] not_ai

---
