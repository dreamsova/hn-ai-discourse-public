# Gold-set labeling worksheet

Total rows: **200**.

## Instructions

For each comment below, **change exactly one `[ ]` to `[x]`** to mark your
gold label. The four choices are:

- `doomer` — comment frames AI in terms of existential risk, alignment failure,
  catastrophic outcomes, control problems, or pessimism about AI safety.
- `accelerationist` — comment frames AI in terms of abundance, progress, rapid
  deployment, techno-optimism, build-faster, or e/acc.
- `neutral` — comment is about AI but is technical, descriptive, product-oriented,
  benchmarking, infrastructure, or otherwise not normatively framed.
- `wrong_other` — comment is NOT actually about AI (false positive of the AI
  retrieval filter), or is too ambiguous to label.

**Example** of a labeled row (note the `[x]`):

```
**Gold label** _(comment_id=EXAMPLE)_:
  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other
```

Most editors (VSCode / Obsidian / Typora) render these as actual checkboxes
you can click; in plain text editors, just change `[ ]` to `[x]` manually.
If you accidentally check more than one box for the same row, the extractor
will warn you on its next run.

Partial labeling is fine — you can stop at any point, run the two commands
below to see how each classifier is doing on what you've labeled so far,
then keep going.

When you're ready (60+ rows for a first signal, all 200 for the final),
run these two commands from the repo root:

```bash
# 1. Extract your checkbox labels into reports/gold_set_labeled.csv
PYTHONPATH=src python scripts/extract_gold_labels.py

# 2. (After zero-shot inference) pull in DeBERTa predictions for the gold IDs
PYTHONPATH=src python scripts/validate/merge_zs_into_gold.py

# 3. Compute per-method confusion matrix + per-class P/R/F1
PYTHONPATH=src python scripts/validate/score_gold_set.py \
  --input-csv reports/gold_set_labeled.csv \
  --output-md reports/generated/gold_validation.md
```

Tips:

- The model's prediction and class probabilities are shown above each comment;
  feel free to peek, but try to form your own judgment first — the whole
  point is that this set is independent of the classifier.
- Comments that retrieve on the AI lexicon but aren't really about AI (e.g.
  *An abundance of Katherines* matching on `abundance`) should be `wrong_other`.
- Doomer / accelerationist must be **normative framings**, not topic mentions.
  "GPT-4 was released yesterday" is `neutral`.

---

## 1. [2023-04] predicted=`accelerationist`  (doomer=0.13 accel=0.46 neutral=0.41)

_Story:_ If cryonics suddenly worked (2016)

_Comment:_ if cryonics suddenly worked (2016) > “it doesn’t make sense that they’d take the time to revive people into some dystopian, backward future,” kowalski says. “you can’t have the technology to wake people up and not have the technology to do a bunch of other great things, like provide abundance to the population.” i've noticed that biologists are frequently more optimistic than other professions.

**Gold label** _(comment_id=35700322)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 2. [2024-02] predicted=`neutral`  (doomer=0.10 accel=0.10 neutral=0.79)

_Story:_ Air Canada is responsible for chatbot's mistake: B.C. tribunal

_Comment:_ air canada is responsible for chatbot's mistake: b.c. tribunal do the people managing the chatbot know that though? this shit gets sold as a way to replace employees with, essentially, just the middle manager that was over them, who is now responsible for managing the chatbot instead of managing people while managers are often actually not great at people management, it's at least a somewhat intuitive skill for many. interacting with and directing other humans is something that many people are able to gain experience with outside of work, since it's a necessary life skill unless you're a hermi…

**Gold label** _(comment_id=39405895)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 3. [2024-03] predicted=`neutral`  (doomer=0.04 accel=0.04 neutral=0.92)

_Story:_ Apple Is in Talks to Let Google's Gemini Power iPhone Generative AI Features

_Comment:_ apple is in talks to let google's gemini power iphone generative ai features i don't know anybody not in the tech world who even knows about that, let alone would care enough to change their platform. my guess is pretty much all average consumers, and 80% of technical consumers, don't care at best and actively applaud gemini at worst. i doubt this is a problem at all

**Gold label** _(comment_id=39749803)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 4. [2023-01] predicted=`neutral`  (doomer=0.10 accel=0.06 neutral=0.84)

_Story:_ Paul Buchheit says Google may be only a year or two away from total disruption

_Comment:_ paul buchheit says google may be only a year or two away from total disruption i think as a direct replacement for internet search, or even general knowledge queries, i definitely agree with you. when it does work though, it's hands-down a better experience. i imagine the 80/20 problem of making it work for the long tail of difficult queries that people will throw at it that will be the hard part. you can't just have a bot spewing out blatantly incorrect data without sourcing half the time. i think it's a coin flip whether those issues will be resolved anytime soon. where i do see it being han…

**Gold label** _(comment_id=34588786)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 5. [2023-08] predicted=`accelerationist`  (doomer=0.11 accel=0.60 neutral=0.29)

_Story:_ UPS CEO says drivers will avg $170k in pay and benefits at end of 5-year deal

_Comment:_ ups ceo says drivers will avg $170k in pay and benefits at end of 5-year deal in a zero sum world this is true. however if we have technology to harness energy more cheaply and produce what we need more cheaply you will simply have abundance. but if everyone is doing bs work and fighting over a dwindling supply of good things, you have high inflation of those good things and they become unaffordable.

**Gold label** _(comment_id=37074650)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 6. [2023-01] predicted=`accelerationist`  (doomer=0.15 accel=0.51 neutral=0.34)

_Story:_ My experience donating stem cells

_Comment:_ my experience donating stem cells > donating stem cells was a moving experience. a teacher i had in high school used to say that everyone has an abundance of something in life, be it money, connections, friends, confidence, or something else, and that everyone should use their abundance to help others. donating stem cells felt like a way to express gratitude for my own health by giving it to another person. a beautiful sentiment. the world would be a better place were everyone to think this way.

**Gold label** _(comment_id=34311745)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 7. [2022-01] predicted=`accelerationist`  (doomer=0.11 accel=0.45 neutral=0.43)

_Story:_ Poll: Which FAANG is the most likely to decline in the years ahead?

_Comment:_ poll: which faang is the most likely to decline in the years ahead? yes, for the last few years, every time i logged into netflix i was stunned at poorly they seemed to understand me. heist movies, murder mysteries, drug cartels fighting, stuff i never watch, and this was the majority of the stuff they showed. recently i spent 20 minutes looking for something to watch, but i couldn't find anything at all that looked interesting. i thought that was so shocking, i decided it was time to cancel netflix. so i finally gave up my account. there is an abundance of good material i can watch elsewhere.…

**Gold label** _(comment_id=29789284)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 8. [2022-02] predicted=`doomer`  (doomer=0.58 accel=0.09 neutral=0.33)

_Story:_ Things the CSS spec folks got right

_Comment:_ things the css spec folks got right things css got wrong: - not supporting tables in css1, even though they were the dominant layout mechanism used at the time. - `box-sizing: content-box` as original sizing model, which nobody has ever needed. - `::pseudo-elements`, also used to convince people that having to add extra divs or spans to html is a horrible mortal sin to be avoided at all costs. - the cascade / `!important`, causing endless rule precedence wars. - `ems` as units relative to the parent instead of the root font size - making flex-box alignment props the most confusing thing ever -…

**Gold label** _(comment_id=30461575)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 9. [2022-11] predicted=`accelerationist`  (doomer=0.11 accel=0.55 neutral=0.34)

_Story:_ Graduate students question career options

_Comment:_ graduate students question career options i’ve always felt that for the social sciences, a masters and phd should not be needed for the job market. however, i can’t help but feel that the demand for these credentials largely comes from a dilution of the marketplace due to the abundance of people with bachelors degrees

**Gold label** _(comment_id=33514806)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 10. [2023-07] predicted=`neutral`  (doomer=0.07 accel=0.04 neutral=0.89)

_Story:_ Twitter has officially changed its logo to ‘X’

_Comment:_ twitter has officially changed its logo to ‘x’ imho think it is something of a looking back / looking forward situation. looking back, the twitter brand has indeed accumulated massive goodwill. looking forward, it would appear that some kind of llm is replacing search (bard.google.com replacing google.com; chat.openai.com replacing bing.com). elon has been very busy establishing the new https://x.ai/ as an alternative llm "to understand the true nature of the universe", with no fewer than 11 new key executive technical employees this july. it is clear that looking forward, elon has a hybrid vi…

**Gold label** _(comment_id=36852773)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 11. [2024-06] predicted=`accelerationist`  (doomer=0.10 accel=0.74 neutral=0.17)

_Story:_ FTC sues Adobe for hiding fees and inhibiting cancellations

_Comment:_ ftc sues adobe for hiding fees and inhibiting cancellations > but would you rather be rich in a world of scarcity? or middle class in a world of abundance? i can tell you that many people would choose the first.

**Gold label** _(comment_id=40719026)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 12. [2023-12] predicted=`doomer`  (doomer=0.47 accel=0.07 neutral=0.45)

_Story:_ Humans progressively feel agency over events triggered before their actions

_Comment:_ humans progressively feel agency over events triggered before their actions humans are used to dealing with natural intelligences all the time, in the form of other humans. other humans often get a sense of what we're going to do next based on what we've done before and move to our next step alongside or slightly before us. this kind of experience-based cooperative alignment arguably even has an evolutionary advantage. the fact that a computer can do it now too doesn't make it a novel experience for us. most of us have known since we were kids that we can affect the actions of other entities b…

**Gold label** _(comment_id=38707096)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 13. [2023-12] predicted=`accelerationist`  (doomer=0.12 accel=0.68 neutral=0.20)

_Story:_ Nuclear energy is more expensive than renewables, report finds

_Comment:_ nuclear energy is more expensive than renewables, report finds i think with good planning they can significantly lower the peaks, and if you have abundance say in europe you can sell it to other states.

**Gold label** _(comment_id=38724956)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 14. [2023-06] predicted=`accelerationist`  (doomer=0.08 accel=0.67 neutral=0.26)

_Story:_ Water so pure it will kill you

_Comment:_ water so pure it will kill you i'd be interested to see a msds that says that ultra-pure water is a hazard. i find a lot saying it's not. pretty sure that what you heard about was either apocryphal or one of those "out of an abundance of caution" scenarios.

**Gold label** _(comment_id=36407356)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 15. [2023-11] predicted=`doomer`  (doomer=0.54 accel=0.10 neutral=0.36)

_Story:_ New Loongson chip matches Intel's 14600K in IPC tests, overclocked to 3 GHz

_Comment:_ new loongson chip matches intel's 14600k in ipc tests, overclocked to 3 ghz that's not an insurmountable problem with a billion people as captive audience. at first glance the isa is nothing special and that's a good thing. it's a run of the mill 64 bit risc isa with little endian byte order and no unusual alignment or store order constraints to watch out for. if something compiles for x86-64, arm64, rv64gc, etc. it should compile for that loongarch if there is a compiler (backend) for it. if the mmu stayed as similar to mips64 as their earlier chips it shouldn't be too much work to write and…

**Gold label** _(comment_id=38467182)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 16. [2024-07] predicted=`accelerationist`  (doomer=0.02 accel=0.91 neutral=0.07)

_Story:_ An abundance of Katherines: The game theory of baby naming

_Comment:_ an abundance of katherines: the game theory of baby naming the title of the paper is also a reference to the famous ya novel "an abundance of katherines" by john green.

**Gold label** _(comment_id=40937237)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 17. [2022-08] predicted=`accelerationist`  (doomer=0.29 accel=0.43 neutral=0.28)

_Story:_ Collapse of emergency healthcare in England may be costing 500 lives every week

_Comment:_ collapse of emergency healthcare in england may be costing 500 lives every week you're correct that the game is to make a lot of money but the key to making that work is ensuring transactions are beneficial to all parties. it doesn't matter how you structure things you end up with some way to climb the hierarchy. the problem with pure communist systems is they try to prevent all hierarchies. human nature attempts to circumvent this, the only way to do so is via corruption and political power. corruption and political power exist in abundance in free markets as well, but there is another outlet…

**Gold label** _(comment_id=32572650)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 18. [2023-01] predicted=`doomer`  (doomer=0.47 accel=0.11 neutral=0.43)

_Story:_ Modules, not microservices

_Comment:_ modules, not microservices i really like modular designs, but this article is missing some key limitations of monolithic applications, also if they are really well modularized (this is written mostly from the perspective of a java developer): * they force alignment on one language or at least runtime * they force alignment of dependencies and their versions (yes, you can have different versions e.g. via java classloaders, but that's getting tricky quickly, you can't share them across module boundaries, etc.) * they can require lots of ram if you have many modules with many classes (semi-relate…

**Gold label** _(comment_id=34231677)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 19. [2023-07] predicted=`doomer`  (doomer=0.91 accel=0.02 neutral=0.06)

_Story:_ A.I. Companies Agree to Safeguards After Pressure from the White House

_Comment:_ a.i. companies agree to safeguards after pressure from the white house the cult of "alignment researchers", who feel that nothing other than "funding alignment researchers" is necessary to solve any possible ai problems, strikes again.

**Gold label** _(comment_id=36814618)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 20. [2023-10] predicted=`doomer`  (doomer=0.59 accel=0.06 neutral=0.35)

_Story:_ How LSP could have been better

_Comment:_ how lsp could have been better i don't understand the appeal of pretty alignment of arguments with the last character of the function name in the row above. what's wrong with just using one more standard indentation level, like black does in python?

**Gold label** _(comment_id=37858644)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 21. [2023-12] predicted=`neutral`  (doomer=0.14 accel=0.11 neutral=0.75)

_Story:_ [dead]

_Comment:_ [dead] crappy ui, crappy moderation, crappy content. is it any wonder what will become of this misadventure after the creative commons license on all the material allows chatgpt to consume it all for free?

**Gold label** _(comment_id=38736740)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 22. [2023-06] predicted=`accelerationist`  (doomer=0.06 accel=0.84 neutral=0.10)

_Story:_ FedEx Accused of Largest Odometer Rollback Fraud in History with Used Vans

_Comment:_ fedex accused of largest odometer rollback fraud in history with used vans the us had golden years after world war 2. we had abundance, effective institutions, and high trust. we've been slowly coming off of that high for a while, and are returning to what is arguably a more typical state. our institutions are crumbling, and societal trust is nose diving. abundance still has a ways to go though.

**Gold label** _(comment_id=36493376)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 23. [2023-05] predicted=`doomer`  (doomer=0.54 accel=0.20 neutral=0.26)

_Story:_ Study finds 90% of Australian teachers can't afford to live where they teach

_Comment:_ study finds 90% of australian teachers can't afford to live where they teach i’m not sure i see the point of you telling me that you have sex with your wife. we are talking about aligning value and meaning. edit: since i’m rate limited now and i don’t really intend to come back to this discussion later, i’ll leave my reply to you here and leave it at that: okay, but you could have done that without bringing your personal sex life into the discussion. either way, that you have sex with your wife doesn’t say anything about the alignment or misalignment of value and meaning in capitalist societie…

**Gold label** _(comment_id=36021905)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 24. [2023-02] predicted=`neutral`  (doomer=0.44 accel=0.08 neutral=0.48)

_Story:_ Help! Is This Arabic?

_Comment:_ help! is this arabic? i'm surprised that this is still such a big issue. i'd expect with unicode standards, this should handle well out of the box. ages ago, in 2005 or thereabouts, i was working on a website for a jewish organisation. i don't know hebrew, but hebrew has many of these same issues, including the right-to-left direction, and i was quite surprised to see text from our own cms, based on java, with tons of xml pipelines (cocoon! xslt!) generating html to be viewed in a browser, just handled this correctly without any problems. at least the text was right-to-left, which was the only…

**Gold label** _(comment_id=34954576)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 25. [2023-06] predicted=`neutral`  (doomer=0.10 accel=0.07 neutral=0.84)

_Story:_ XGen-7B, a new 7B foundational model trained on up to 8K length for 1.5T tokens

_Comment:_ xgen-7b, a new 7b foundational model trained on up to 8k length for 1.5t tokens sorry doc, i wrote that comment in a smartphone without putting any thought. what i wanted to say was: > there are 7b parameters. a parameter is a weight assigned to single neuron. i hope this clarifies the answer now. now that is done i am quite curious on how you came up with the idea it was written by chatgpt? i just wanted to simplify as best as i could. it’s funny you thought it that way. what could i have done so that it didn’t sound like response from chatgpt? i am asking it to prevent future misunderstandin…

**Gold label** _(comment_id=36521444)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 26. [2023-05] predicted=`doomer`  (doomer=0.79 accel=0.02 neutral=0.19)

_Story:_ Improving mathematical reasoning with process supervision

_Comment:_ improving mathematical reasoning with process supervision its meaning has shifted to now mean esg ( https://en.wikipedia.org/wiki/environmental,_social,_and_cor... ) and dei ( https://en.wikipedia.org/wiki/diversity,_equity,_and_inclusi... ) for corporations that make algorithms that have learned natural language well enough that people are talking with them and taking them seriously. the ai alignment guys don't like that and they have started calling their old ai alignment meaning as 'not-kill-everyoneism' with mixed results ( https://www.lesswrong.com/posts/jmzbhcrrr7otmqcvk/notkilleve... ).…

**Gold label** _(comment_id=36144332)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 27. [2024-12] predicted=`doomer`  (doomer=0.48 accel=0.07 neutral=0.45)

_Story:_ Alignment faking in large language models

_Comment:_ alignment faking in large language models p.s.: saw a recent submission [0] just now, might be of-interest since it also touches on the "faking": > when they tested the model by giving it two options which were in contention with what it was trained to do it chose a circuitous, but logical, decision. > and it was published as “claude fakes alignment”. no, it’s a usage of the word “fake” that makes you think there’s a singular entity that’s doing it. with intentionality. it’s not. it’s faking it about as much as water flows downhill. > [...] thus, in the same report, saying “the model tries to…

**Gold label** _(comment_id=42467827)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 28. [2024-06] predicted=`doomer`  (doomer=0.77 accel=0.07 neutral=0.17)

_Story:_ Qwen2 LLM Released

_Comment:_ qwen2 llm released i doubt it; they could be a whole lot smarter. we need to solve alignment in the meantime.

**Gold label** _(comment_id=40599794)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 29. [2024-09] predicted=`neutral`  (doomer=0.13 accel=0.08 neutral=0.80)

_Story:_ Plagiarism Claims Are Brought Against University of Maryland's President

_Comment:_ plagiarism claims are brought against university of maryland's president disagree. the kind of serious plagiarism that's alleged in cases like this, claudine gay, marc tessier-lavigne doesn't happen by accident, it's deliberate. there are plenty of academics, both minorities and not, who are capable of original thought (and not resorting to plagiarism). i can't wait for the day that ai is used to expose the fakers en-masse. previously, they got away with plagiarism through obscurity - no longer. the sooner we can excise these freeloaders from our professional institutions, the better. i did no…

**Gold label** _(comment_id=41621485)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 30. [2024-07] predicted=`doomer`  (doomer=0.50 accel=0.08 neutral=0.42)

_Story:_ Things I learned while writing an x86 emulator (2023)

_Comment:_ things i learned while writing an x86 emulator (2023) some interesting quotes around there: > the following alignment situations can cause lcp stalls to trigger twice: > · an instruction is encoded with a modr/m and sib byte, and the fetch line boundary crossing is between the modr/m and the sib bytes. > · an instruction starts at offset 13 of a fetch line references a memory location using register and immediate byte offset addressing mode. so that's the order of funkiness to be expected, fun. > false lcp stalls occur when (a) instructions with lcp that are encoded using the f7 opcodes, and (…

**Gold label** _(comment_id=40936150)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 31. [2024-11] predicted=`neutral`  (doomer=0.05 accel=0.04 neutral=0.91)

_Story:_ The Influence of Bell Labs

_Comment:_ the influence of bell labs > honestly though google would be that - but apparently it's easier to fund r&d on "selling copying machines" than "selling ads". maybe "selling ads" earn _too much_ money ? i don't know. i'm pretty sure google brain was exactly what you are looking for: people like to think of deepmind, but honestly, brain pretty much had bell labs/parcs strategy: they hired a bunch of brilliant people and told them to just "research whatever is you think is cool". and think all the ai innovations that came out of brain and were given to the world for free: transformers, vision tran…

**Gold label** _(comment_id=42277683)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 32. [2023-03] predicted=`accelerationist`  (doomer=0.12 accel=0.56 neutral=0.32)

_Story:_ Incident: Southwest B38M at Phoenix on Feb 24th 2023, no autopilot trim

_Comment:_ incident: southwest b38m at phoenix on feb 24th 2023, no autopilot trim mechanical incidents is one thing, but is it also the case of pilots declaring an emergency? [edit] though it looks like they declared an emergency out of an abundance of caution

**Gold label** _(comment_id=34993213)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 33. [2024-12] predicted=`doomer`  (doomer=0.74 accel=0.04 neutral=0.21)

_Story:_ Alignment faking in large language models

_Comment:_ alignment faking in large language models > i do not think we have good evidence that the models are faking alignment. that's a polite understatement, i think. my read of the paper is that it rather uncritically accepts the idea that the model's decisional pathway is actually shown in the traces. when, in fact, it's just as plausible that the scratchpad is meaningless blather, and both it and the final output are the result of another decisional pathway that remains opaque.

**Gold label** _(comment_id=42467146)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 34. [2023-05] predicted=`neutral`  (doomer=0.08 accel=0.04 neutral=0.88)

_Story:_ OpenAI isn’t doing enough to make ChatGPT’s limitations clear

_Comment:_ openai isn’t doing enough to make chatgpt’s limitations clear not on topic, exactly, but my current hill to die on is awareness that despite its current promotion and popularity, chatgpt is just one product in a vast landscape of agi-peripheral technologies, does not represent all llms, and doesn't make the openai company the arbiter of all things llm or agi. the senate subcommittee said they wanted to "avoid the mistakes of social media", and they can start by not prematurely appointing someone the official face and spokesperson of regulation of an incomplete product and vision. i was pretty…

**Gold label** _(comment_id=36128690)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 35. [2024-10] predicted=`neutral`  (doomer=0.08 accel=0.05 neutral=0.87)

_Story:_ AlphaFold reveals how sperm and egg hook up in intimate detail

_Comment:_ alphafold reveals how sperm and egg hook up in intimate detail > to bypass the difficulties of working with membrane proteins in the laboratory, the team used alphafold to predict interactions between proteins > alphafold predicted that three sperm proteins work together to form a complex. two of these proteins were previously known to be important for fertility. https://www.nature.com/articles/nature18448 here’s the paper linked in the article. does anyone have experience using alphafold? i don’t have a nature subscription to see how they specifically accomplished this, but i glanced at the a…

**Gold label** _(comment_id=41881581)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 36. [2023-04] predicted=`doomer`  (doomer=0.89 accel=0.03 neutral=0.08)

_Story:_ ‘Hot Ones’ Was a Slow Burn All Along

_Comment:_ ‘hot ones’ was a slow burn all along > eliezer presents his thesis about the difficulty of ai alignment and lex seems to never address it or even attempt to engage. essentially, there are many ways to get alignment wrong and suffer the consequences. as a "counterargument", lex persists in introducing optimistic scenarios in which everything works as he imagines. > about halfway through the interview, it really goes downhill. at times, lex has an interesting prompt, but those occasions seem more like random luck than engagement. or maybe he honestly doesn't understand what eliezer has been sayi…

**Gold label** _(comment_id=35435689)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 37. [2024-03] predicted=`neutral`  (doomer=0.14 accel=0.09 neutral=0.78)

_Story:_ After 2 Weeks of Testing, What Do Developers Think About Claude 3?

_Comment:_ after 2 weeks of testing, what do developers think about claude 3? every time i've mentioned having problems with gpt4 i've been told that i mustn't be prompting it correctly. now suddenly claude 3 comes out and everyone is admitting gpt4's shortcomings.

**Gold label** _(comment_id=39811283)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 38. [2022-09] predicted=`accelerationist`  (doomer=0.17 accel=0.48 neutral=0.35)

_Story:_ Death by hockey sticks

_Comment:_ death by hockey sticks and basically none of those reasons are related to the two proposed (“getting our s%%% together” or actual die-offs, both kind of cartoonishly silly). it’s largely the availability of birth control, urbanization, and maybe also old-age safety nets. the whole world is on the way to doing this (africa will, too, as they will develop… and, in a note of good news, probably become as economically powerful in the 22nd century as asia is in the 21st). it’ll lead to a cratering of the working population unless we basically start to eliminate retirement (not desirable!) and enact…

**Gold label** _(comment_id=32837401)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 39. [2022-04] predicted=`accelerationist`  (doomer=0.14 accel=0.59 neutral=0.27)

_Story:_ Gen Z does not dream of labor

_Comment:_ gen z does not dream of labor >it is interesting to see that even inequality is the default outcome, the natural order of things, even when we start from equality. it seem the law of physics and the law of this world converges toward inequality. the natural order of things? is this some kind of joke? since when are humans golems? a truly natural economic order looks like this: https://www.naturalmoney.org/naturaleconomicorder.pdf >it seem the law of physics and the law of this world converges toward inequality. no, you are mistaken again, the money and land system converge toward inequality. a…

**Gold label** _(comment_id=31165056)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 40. [2022-09] predicted=`accelerationist`  (doomer=0.14 accel=0.55 neutral=0.31)

_Story:_ All poverty is energy poverty

_Comment:_ all poverty is energy poverty if climate change is an existential threat, we should be engineering a rise in gas prices, and cheering when peoples' lifestyles take a hit. if you truly believe climate change is super serious, then logically government ought to put its thumb on the scale to ensure a lot of people get priced out of energy intensive products like air conditioning, leaving their computers on at night, meat, aluminum, and so on. if you're a nationalist, it's even better if the people we're impoverishing are overseas, and therefore the poverty we create to save the planet is somebody…

**Gold label** _(comment_id=32729538)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 41. [2024-12] predicted=`doomer`  (doomer=0.84 accel=0.06 neutral=0.09)

_Story:_ Wishing for a more orderly disruption may misunderstand government reform

_Comment:_ wishing for a more orderly disruption may misunderstand government reform officially they (generally) don’t. but judges are people; most judges around the world have a political alignment, even if they keep it better hidden.

**Gold label** _(comment_id=42430667)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 42. [2024-06] predicted=`neutral`  (doomer=0.05 accel=0.03 neutral=0.92)

_Story:_ Teachers: AI is making children dumb as fuck

_Comment:_ teachers: ai is making children dumb as fuck is there a way to orient assignments that can't be solved easily by ai? maybe classes will have to have more non-computer exams to test pupils ability to do tasks like solve mathematic questions without ai.

**Gold label** _(comment_id=40679250)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 43. [2024-07] predicted=`neutral`  (doomer=0.06 accel=0.04 neutral=0.90)

_Story:_ Creativity fundamentally comes from memorization?

_Comment:_ creativity fundamentally comes from memorization? interesting point - thanks for sharing! i think one big missing piece we have with ais today is the ability for them to learn on the fly and reconfigure the weights. we are constantly bombarded with input and our neurons adjust accordingly. current llms just use a snapshot. i would be really curious to see how online-first ai models could work, focusing on a constant input stream and iterating on weights. also i wonder how much knowledge is baked into our dna through evolution. i have a hunch that this is somewhat analogous to model architectur…

**Gold label** _(comment_id=41116597)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 44. [2023-01] predicted=`accelerationist`  (doomer=0.14 accel=0.51 neutral=0.36)

_Story:_ Boris Yeltsin's visit to a suburban Houston supermarket in 1989 (2016)

_Comment:_ boris yeltsin's visit to a suburban houston supermarket in 1989 (2016) yes, the relative abundance produced by capitalism would have overcome the ussr/russia even absent yeltsin's visit. everywhere communism has been tried, it's failed, and the most assertive efforts have led to the death of tens of millions.

**Gold label** _(comment_id=34405564)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 45. [2023-07] predicted=`accelerationist`  (doomer=0.18 accel=0.43 neutral=0.39)

_Story:_ The Psychotherapy Myth

_Comment:_ the psychotherapy myth i don't need studies to validate the hundreds of incredible results i've seen within the population i have direct access to (and myself) moreover, what's most onerous, if anything, about the psychotherapeutic mindset is the implicit "broken / fixed" distinction (usually framed as something like "health" or "well-adjustedness") another framing with regard to experience would look at "development," "growth," "abundance," "depth," "truth" there is much to unfold and discover in this life, and psychotherapy is a sliver of a broader set of practices—which have been with human…

**Gold label** _(comment_id=36932075)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 46. [2022-07] predicted=`accelerationist`  (doomer=0.18 accel=0.51 neutral=0.32)

_Story:_ Build Unix, Not Uber

_Comment:_ build unix, not uber if i could make one change to popular parlance (or perhaps i should say technical jargon), it would be the usage of the word externality. while it is a technically correct description, the framing implied leads to analysis that i don’t think is fundamentally sound. markets optimize for products. if something can’t be made into a product wherein the full value and cost to society is express captured within the transaction itself, you generally end up with less than ideal outcomes. capitalism is the best system for optimizing for productive efficiency, but creating an abunda…

**Gold label** _(comment_id=32282787)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 47. [2024-03] predicted=`doomer`  (doomer=0.53 accel=0.19 neutral=0.27)

_Story:_ Baltimore's Key Bridge struck by cargo ship, collapses

_Comment:_ baltimore's key bridge struck by cargo ship, collapses current personal suspicion after watching your linked video (excellent discussion by the wgowshipping author) is: catastrophic engine failure (1:24) causing wide scale power loss. no rudder control, rudder drift, and ship alignment drift (1:24-1:25:30) power restored and ship reengages prop with bad ship/ruddder alignment (1:25). however, ship is now pushing itself into a further bad turn. pilot likely stomps the brakes realizing misalignment. obviously 2-3 minutes is not enough to stop 100,000 tons at 8.5 kts, since it only got to 7.5 kts…

**Gold label** _(comment_id=39830524)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 48. [2023-01] predicted=`neutral`  (doomer=0.04 accel=0.02 neutral=0.93)

_Story:_ New AI classifier for indicating AI-written text

_Comment:_ new ai classifier for indicating ai-written text yes, sort of, though if the economic incentive was high enough, someone could connect the ai to input through the keyboard and "type" out the essay. at scale it would be cheap. you could record video of you typing, which would work for some time until at some point video fakes get advanced enough... sigh.

**Gold label** _(comment_id=34602246)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 49. [2024-11] predicted=`neutral`  (doomer=0.13 accel=0.10 neutral=0.77)

_Story:_ We're experimenting with advertising

_Comment:_ we're experimenting with advertising before ads, the service has one clear goal - build the best product they can for their users. after ads, the goal is less clear. they still need to please users, but they also have to please advertisers. the needs of users and advertisers aren't always going to be aligned, and so users should lose trust in the perplexity results. if i was an investor, this would make me nervous. make something that is far better than your competitors and users will pay. if you make something that is only marginally better than your competitors, users are only going to pay a…

**Gold label** _(comment_id=42139254)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 50. [2024-09] predicted=`accelerationist`  (doomer=0.10 accel=0.55 neutral=0.35)

_Story:_ The Internet Archive has lost its appeal in Hachette vs. Internet Archive

_Comment:_ the internet archive has lost its appeal in hachette vs. internet archive not really. we ha an abundance of creation long before copyright.

**Gold label** _(comment_id=41456839)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 51. [2023-05] predicted=`doomer`  (doomer=0.72 accel=0.07 neutral=0.21)

_Story:_ Has ChatGPT Been Neutered?

_Comment:_ has chatgpt been neutered? the nuance required here is something that llms have not been great at, or at least not good enough to prevent actual homophobic jokes. see the general issue that llms struggle with negation. in fact alignment work is on some level about getting llms to be smart about this nuance. i agree in the abstract that, for instance, an llm could/should be able to make jokes about tim cook — just because he’s gay doesn’t mean he should be off limits for a joke about apple, for instance. that would demonstrate an impressive level of nuance. but also like … what’s the business p…

**Gold label** _(comment_id=35989855)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 52. [2024-10] predicted=`neutral`  (doomer=0.12 accel=0.04 neutral=0.84)

_Story:_ AlphaCodium outperforms direct prompting of OpenAI's o1 on coding problems

_Comment:_ alphacodium outperforms direct prompting of openai's o1 on coding problems do they impose arbitrary time based restrictions (that wouldn't otherwise exist) when you use a claude api key instead of paying? i went back to vs code after something like that (seemed to have) happened. honestly, once you learn the copilot specific hot keys you can do all of what cursor does and more. in fact there were times that i felt the team at vs code clearly could have added features that cursor has but chose not to because they led to more unwanted code slipping through. i did like the edit tab completions fr…

**Gold label** _(comment_id=41840656)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 53. [2024-01] predicted=`accelerationist`  (doomer=0.10 accel=0.71 neutral=0.19)

_Story:_ Possible Meissner effect near room temperature: copper-substituted lead apatite

_Comment:_ possible meissner effect near room temperature: copper-substituted lead apatite imagine humanity liberated to such lengths. sickness, poverty, energy, travel, entertainment - all for cheap and in abundance. pray this is real!

**Gold label** _(comment_id=38858748)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 54. [2023-04] predicted=`doomer`  (doomer=0.84 accel=0.05 neutral=0.10)

_Story:_ The Commission for Stopping Further Improvements

_Comment:_ the commission for stopping further improvements most public offices he could run for would put him in a generalist position, with various public facing and non-technical aspects that he is not suited to or qualified to handle. i want him to be able to completely and wholly run the show for just his one narrow specialty. this isn't an option at all because our institutions don't adapt to the territory we often find ourselves in. we have a political alignment problem that exacerbates the technical alignment problems. i would like to have something like the concept of senators, but not as locati…

**Gold label** _(comment_id=35662671)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 55. [2023-11] predicted=`doomer`  (doomer=0.60 accel=0.05 neutral=0.34)

_Story:_ Satya Nadella says OpenAI governance needs to change

_Comment:_ satya nadella says openai governance needs to change i'm not sure that's accurate. most companies use "ai safety" as a shorthand for "brand safety", i.e., making sure that your llm can't be trolled into praising hitler or denying climate change. basically, do what needs to be done to avoid bad press. there is definitely that second and more abstract take - ai doomsday safety - that altman liked to talk about to get favorable regulation passed. but it doesn't seem to be much of a real field. "hard" ai doomers think that superhuman ai can't be reliably constrained and we should just stop. "soft"…

**Gold label** _(comment_id=38357361)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 56. [2023-06] predicted=`doomer`  (doomer=0.66 accel=0.05 neutral=0.29)

_Story:_ Structures in C: From Basics to Memory Alignment

_Comment:_ structures in c: from basics to memory alignment you'll get a compiler error though unless you, in the same edit-compile cycle, created a new variable with the same name. you also can't search-replace a type name as easily, because other variables will have the same original type but not need to be updated.

**Gold label** _(comment_id=36536433)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 57. [2023-10] predicted=`accelerationist`  (doomer=0.15 accel=0.47 neutral=0.38)

_Story:_ Productivity has grown faster in Western Europe than in America

_Comment:_ productivity has grown faster in western europe than in america i can't access the text because it's behind a paywall, but at least in the visualisation you see at least europes countries. and it's a headline, it can't reduce the complexity without loosing something. > 1 million to 1.5 million is far less than 100 to 1000 this is very simplified and if there's a continuing trend then the first has an an abundance of money and the second just has a bit. i don't think the critique is fair at all. these are statistics over a population, of course it's meaningless at first for the individual but t…

**Gold label** _(comment_id=37789818)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 58. [2022-01] predicted=`accelerationist`  (doomer=0.16 accel=0.42 neutral=0.42)

_Story:_ Tell HN: Twitter is growing increasingly unusable without an account

_Comment:_ tell hn: twitter is growing increasingly unusable without an account these sv companies would have a lot less power over us if we all judged and acted as if the personal information whywhywhywhy is complaining about having to give away as being more important than reading some forum post, or watching some video stream, or some other transient dopamine hit gone in literally seconds vs. the near-permanent and very difficult to remove little tentacle the company gets to stick into your life now. each one individually is no big deal, but the whole is. adopt an abundance mentality. our world is awa…

**Gold label** _(comment_id=30115088)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 59. [2024-01] predicted=`neutral`  (doomer=0.35 accel=0.13 neutral=0.51)

_Story:_ Google Announces Fourth Quarter and Fiscal Year 2023 Results [pdf]

_Comment:_ google announces fourth quarter and fiscal year 2023 results [pdf] it's quite possible for the engineers to work really hard in ways that even directly harm the company, either directly, or by increasing the political costs of making a better decision. my favorite here is bridgewater and their hr/evaluation/alignment system. there's books written about it. developing it and running it took a high percentage of workers and contractors. its implementation had all kinds of negative effects on everyone else, including the people doing the actual investment. but it took a pandemic, and the ceo bein…

**Gold label** _(comment_id=39197708)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 60. [2023-01] predicted=`accelerationist`  (doomer=0.09 accel=0.51 neutral=0.41)

_Story:_ Help Me Test Primitives

_Comment:_ help me test primitives primitives makes it easy for creators to build abundance from their creations. i am looking for beta testers for both product and pitch. help me out?

**Gold label** _(comment_id=34560025)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 61. [2023-08] predicted=`accelerationist`  (doomer=0.11 accel=0.64 neutral=0.25)

_Story:_ Energy Jobs Have Increased in Nearly Every County in America

_Comment:_ energy jobs have increased in nearly every county in america coupling energy production success to job creation is a mistake, and the doe is taking political wins at the cost of long-term energy abundance. labor inherently puts a floor on the price of energy, no matter how cheap or clean the technology is! "cheap, clean energy" is the consumer benefit, not the bureaucracy and make-work. we should aim for a world where near-infinite energy production is produced by one guy in dc with a button that says "produce more".

**Gold label** _(comment_id=37147405)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 62. [2023-04] predicted=`neutral`  (doomer=0.03 accel=0.02 neutral=0.95)

_Story:_ Finetuning Large Language Models

_Comment:_ finetuning large language models it's amazing how much misinformation and vague information there is on this topic. i tried getting to the bottom of this in the following post in the openai forum: https://community.openai.com/t/fine-tuning-myths-openai-docu... bottom line is that fine-tuning does not seem to be a feasible option for adding new knowledge to a model for question answering.

**Gold label** _(comment_id=35667178)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 63. [2023-12] predicted=`neutral`  (doomer=0.04 accel=0.02 neutral=0.94)

_Story:_ Ask HN: Do you user finger or other "old" protocols?

_Comment:_ ask hn: do you user finger or other "old" protocols? i use sftp and sshfs-win for my gemini server so i can edit my gemlogs as text files with vs code and have them update immediately on the server

**Gold label** _(comment_id=38534970)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 64. [2023-05] predicted=`doomer`  (doomer=0.47 accel=0.07 neutral=0.45)

_Story:_ Ask HN: How do you personally define 'AGI'?

_Comment:_ ask hn: how do you personally define 'agi'? i definitely see what you're getting at. i think this is the crux of the alignment problem in general. though, in a deeper sense, what is the property that allows that to be possible? i suspect it at least involves the combination of being able to continuously learn in response to novel stimuli and developing the goal of self-preservation.

**Gold label** _(comment_id=35883136)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 65. [2023-11] predicted=`neutral`  (doomer=0.12 accel=0.05 neutral=0.83)

_Story:_ Sam Altman is still trying to return as OpenAI CEO

_Comment:_ sam altman is still trying to return as openai ceo it is unfortunate that some people hear ai safety and think about chatbots saying mean stuff, and others think about a future system performing the machine revolution against humanity.

**Gold label** _(comment_id=38356504)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 66. [2024-04] predicted=`neutral`  (doomer=0.04 accel=0.02 neutral=0.94)

_Story:_ Tool Use (function calling)

_Comment:_ tool use (function calling) i'm looking forward to trying this out with plandex[1] (a terminal-based ai coding tool i recently launched that can build large features). plandex does rely on openai's streaming function calls for its build progress indicators, so the lack of streaming is a bit unfortunate. but great to hear that it will be included in ga. i've been getting a lot of requests to support claude, as well as open source models. a humble suggestion for folks working on models: focus on full compatibility with the openai api as soon as you can, including function calls and streaming fun…

**Gold label** _(comment_id=39940912)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 67. [2024-05] predicted=`neutral`  (doomer=0.02 accel=0.02 neutral=0.95)

_Story:_ Gemini Flash

_Comment:_ gemini flash looking at mmlu and other benchmarks, this essentially means sub-second first-token latency with llama 3 70b quality (but not gpt-4 / opus), native multimodality, and 1m context. not bad compared to rolling your own, but among frontier models the main competitive differentiator was native multimodality. with the release of gpt-4o i'm not clear on why an organization not bound to gcp would pick gemini. 128k context (4o) is fine unless you're processing whole books/movies at once. is anyone doing this at scale in a way that can't be filtered down from 1m to 100k?

**Gold label** _(comment_id=40358661)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 68. [2022-04] predicted=`doomer`  (doomer=0.68 accel=0.12 neutral=0.20)

_Story:_ Twitter set to accept Musk's $43B offer – sources

_Comment:_ twitter set to accept musk's $43b offer – sources i feel like people have invested in elon in large part because of his alignment with i) moving humanity away from fossil fuels and ii) making life multi planetary. he is obviously free to do as he pleases with this new wealth but i cant help but feel this as a huge redirection of resources (in terms of both capital and focus) from those goals

**Gold label** _(comment_id=31153697)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 69. [2024-08] predicted=`accelerationist`  (doomer=0.24 accel=0.44 neutral=0.32)

_Story:_ Ask HN: What if civilization's growth rate exceeds it's natural evolution?

_Comment:_ ask hn: what if civilization's growth rate exceeds it's natural evolution? technology isn't inherently unnatural, and i wouldn't necessarily detach it from evolution. it's a continuum of adaptations, both genetic and otherwise, that creates a species's legacy through time, combining mutations with environmental and cultural factors. we've outpaced genetics alone long ago, using our brains and dexterity to hunt, make fire, create clothing for most of the world's biomes, sail across the seas, etc. it's a sort of cultural evolution that continued where genetic selection slowed down. you can see l…

**Gold label** _(comment_id=41311831)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 70. [2024-03] predicted=`neutral`  (doomer=0.21 accel=0.13 neutral=0.66)

_Story:_ Inflection-2.5: meet the best personal AI

_Comment:_ inflection-2.5: meet the best personal ai i got claude sonnet to write a non-rhyming poem by asking it to imitate john milton. but yeah, negatives don't seem to work well. --- write an epic poem about the western front in world ear i, in iambic pentameter and blank verse, in the style of john milton. here is an attempt at an epic poem about the western front in world war i, written in iambic pentameter and blank verse, in the miltonic style: of man's first global war, the dreadful blight that swept across all europe, west to east, from flanders' fields to gallic shores and heights, o'er lands…

**Gold label** _(comment_id=39647825)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 71. [2023-07] predicted=`accelerationist`  (doomer=0.17 accel=0.47 neutral=0.37)

_Story:_ Where to watch “Oppenheimer” on film in 70mm Imax in the U.S.

_Comment:_ where to watch “oppenheimer” on film in 70mm imax in the u.s. it is incredibly worth it. i had low expectations going in (not a huge fan of nolan's recent work and the trailers for the film left a lot to be desired) but i find myself in california recently and there's an abundance of 70mm imax sets here. bar none the greatest theater experience i have ever seen.

**Gold label** _(comment_id=36832823)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 72. [2023-01] predicted=`accelerationist`  (doomer=0.10 accel=0.53 neutral=0.37)

_Story:_ Money creation in the modern economy (2014) [pdf]

_Comment:_ money creation in the modern economy (2014) [pdf] no idea. i can't even say if it's the lack of high-quality contributions and meta-moderation, or an over-abundance of low-quality contributions. the patterns i noticed mainly revolve around certain topics.

**Gold label** _(comment_id=34388925)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 73. [2023-08] predicted=`doomer`  (doomer=0.52 accel=0.06 neutral=0.42)

_Story:_ A group of Motherboard folks just spun up their own new independent outlet

_Comment:_ a group of motherboard folks just spun up their own new independent outlet ai will be one of our core coverage areas and i'm sure we will be doing pieces both short and in-depth on ai alignment, doomerism, optimism, etc.

**Gold label** _(comment_id=37238831)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 74. [2023-02] predicted=`neutral`  (doomer=0.41 accel=0.11 neutral=0.48)

_Story:_ Bing: “I will not harm you unless you harm me first”

_Comment:_ bing: “i will not harm you unless you harm me first” saying we shouldn't "tap the brakes" on ai out of safety concerns because russia/china won't is a little like saying we shouldn't build containment buildings around our nuclear reactors, because the soviet union doesn't. it's a valid concern, but the solution to existential danger is not more danger.

**Gold label** _(comment_id=34812468)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 75. [2022-08] predicted=`neutral`  (doomer=0.03 accel=0.05 neutral=0.92)

_Story:_ Ask HN: Are we building a tech dystopia?

_Comment:_ ask hn: are we building a tech dystopia? yes we are. here is why: this is what the free software foundation have tried to stop and have been fighting against for 37 years, but they have ultimately failed since the rise of non-free software is much more prevalent and unstoppable given the tech bros at these faang companies continuously distributing closed source spyware as a service to make us fully digitise anything physical if possible and they will put it all on rent to us. the point of 'open-source' has also been hijacked to allow this exploitation of developers by large companies to use th…

**Gold label** _(comment_id=32485293)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 76. [2023-01] predicted=`neutral`  (doomer=0.07 accel=0.06 neutral=0.88)

_Story:_ OpenAI and Microsoft extend partnership

_Comment:_ openai and microsoft extend partnership i did not necessarily mean 10 people startups. there are quite a few companies smaller than openai, but much larger than 10 people.

**Gold label** _(comment_id=34499730)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 77. [2022-06] predicted=`doomer`  (doomer=0.46 accel=0.10 neutral=0.45)

_Story:_ TikTok updated privacy policy to collect faceprints and voiceprints (2021)

_Comment:_ tiktok updated privacy policy to collect faceprints and voiceprints (2021) > and to make myself even more explicit, i am saying that desires of the us public are indeed different from "us (gov) interests" sure, but it's also worth noting the interests of the "us public" are more in alignment with "us (gov) interests" than they are "chinese (gov) interests," at least when it comes to geopolitics and stuff like this. that's far more relevant to a discussion of tiktok, which this is .

**Gold label** _(comment_id=31923177)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 78. [2024-05] predicted=`neutral`  (doomer=0.08 accel=0.05 neutral=0.87)

_Story:_ Mistral Fine-Tune

_Comment:_ mistral fine-tune i think the bitter lesson kicks in shortly after you complete fine tuning, and openai release their next model which performs better at the same task.

**Gold label** _(comment_id=40481246)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 79. [2024-08] predicted=`accelerationist`  (doomer=0.13 accel=0.45 neutral=0.42)

_Story:_ Why Western designs fail in developing countries [video]

_Comment:_ why western designs fail in developing countries [video] our technophilia often blinds of from this, even in the us. techno-optimism is basically a cult that says all our woes can be solved with engineering rather than social effort. climate change, wealth inequality, etc will not be solved with technology. they will be solved with sweat effort and social change. to believe anything else is delusional.

**Gold label** _(comment_id=41139310)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 80. [2024-08] predicted=`doomer`  (doomer=0.67 accel=0.12 neutral=0.22)

_Story:_ NASA investigation finds Boeing hindering Americans' return to moon

_Comment:_ nasa investigation finds boeing hindering americans' return to moon apollo really was a rare alignment of motivations, unbounded optimism meets existential fear, ie, "humanity can migrate into the stars" overlapping with "if we don't do this the commies win first strike capability", seems unlikely to re-occur.

**Gold label** _(comment_id=41231111)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 81. [2023-12] predicted=`accelerationist`  (doomer=0.17 accel=0.42 neutral=0.41)

_Story:_ Hunter-gatherers' work was play

_Comment:_ hunter-gatherers' work was play > boston college research professor peter gray specializes in the nature and value of play. of course peter finds play in everything because that's his frame of looking at things. the entire thing is a bit of a joke in how simplistic and fallacious it is. work is not play because it's unpleasant but the hg work is play because it's fun (not much, it's social, is challenging/not routine/boring and it's optional). it has to deliberately dismiss the need of survival as "well, but they were many so some could avoid working for a month and all would be good " so the…

**Gold label** _(comment_id=38618986)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 82. [2022-09] predicted=`accelerationist`  (doomer=0.08 accel=0.55 neutral=0.37)

_Story:_ Scientists are using AI to dream up revolutionary new proteins

_Comment:_ scientists are using ai to dream up revolutionary new proteins as a solution to the inverse folding problem, this is the enabling technology for molecular nanotechnology. i suggest anyone interested in this read drexler’s radical abundance which talks about what is possible with atomically precise manufacturing built with custom designed proteins. radical abundance in video form: https://m.youtube.com/watch?v=1bw6zi17dbi if anyone is interested in making this happen, contact me.

**Gold label** _(comment_id=32862884)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 83. [2023-08] predicted=`accelerationist`  (doomer=0.09 accel=0.69 neutral=0.23)

_Story:_ The sudden demise of Indian vultures killed thousands of people

_Comment:_ the sudden demise of indian vultures killed thousands of people perhaps there's a silver lining to this. maybe the remaining vultures have a resistance to the drug and with an abundance of food they will be able to recover? i don't know any of this i'm just trying to be positive.

**Gold label** _(comment_id=37303028)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 84. [2022-03] predicted=`doomer`  (doomer=0.54 accel=0.10 neutral=0.36)

_Story:_ US Senate votes unanimously to make daylight savings time permanent

_Comment:_ us senate votes unanimously to make daylight savings time permanent the consistency is fine, the alignment is stupid. if the numbers don't matter, then why do the numbers 9 and 5 matter so much that we center the new clock on those rather than noon/midnight? it's probably not going to be a harmful stupid, it's only a small stupid, but it's still stupid. there will be no explaining this to kids a generation from now. "well you see way back, they had this even goofier system where everyone changed all their clocks twice a year...that was ultimately just silly so finally they eventually decided t…

**Gold label** _(comment_id=30690832)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 85. [2022-09] predicted=`neutral`  (doomer=0.04 accel=0.04 neutral=0.92)

_Story:_ From Common Lisp to Julia

_Comment:_ from common lisp to julia unfortunately, julia has a number of correctness flaws [0]. just based on this alone, i can't use julia simply because i can never be sure whether my code is wrong or the compiler itself is wrong. in scientific computing and machine learning, these problems are very important, unlike in other types of programs where it's more tolerable, because they deal with vectors and tensors with potentially billions of parameters and computation/training time might take several days. if i get an incorrect result, my time has just been wasted, not to mention money via compute reso…

**Gold label** _(comment_id=32746617)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 86. [2023-02] predicted=`doomer`  (doomer=0.61 accel=0.11 neutral=0.28)

_Story:_ Toxic Exposure: The True Story Behind the Monsanto Trials

_Comment:_ toxic exposure: the true story behind the monsanto trials > who testified in the first three trials against monsanto in other words, he's paid litigation consultant. of course his book is going to be in alignment with those that pay him.

**Gold label** _(comment_id=34720071)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 87. [2023-07] predicted=`doomer`  (doomer=0.48 accel=0.09 neutral=0.43)

_Story:_ FTC investigating ChatGPT over potential consumer harm

_Comment:_ ftc investigating chatgpt over potential consumer harm >a really strange thing to do, i remain puzzled as to why any ceo would stir up the government like this. because it's a very serious possibility(that the singularity could end humanity), and a significant part of the people who are serious about ai are extremely worried about alignment, for good reasons. > i hope he's not surprised when they take action. surprised? do you mean relieved?

**Gold label** _(comment_id=36721422)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 88. [2022-03] predicted=`accelerationist`  (doomer=0.14 accel=0.51 neutral=0.35)

_Story:_ Developers spend most of their time figuring the system out

_Comment:_ developers spend most of their time figuring the system out you don’t really have to fit things into logical registers before you can speak of them. if you stop trying to do that you will find that you can speak your mind directly, which requires a lot less effort. the recipient of your message is also a human mind and while you will lose the handrails of logical clarity you will gain the safety net in abundance of bandwidth and feedback loops. it’s a trained skill tho.

**Gold label** _(comment_id=30862003)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 89. [2024-10] predicted=`neutral`  (doomer=0.01 accel=0.01 neutral=0.98)

_Story:_ Canvas is a new way to write and code with ChatGPT

_Comment:_ canvas is a new way to write and code with chatgpt this is an odd comment, because you mention claude and google, both of which already have similar/adjacent features. for a while. openai is actually defensive/behind. 1. claude has “artifacts” which are documents or interactive widgets that live next to a chat. 2. claude also has the ability to run code and animated stuff in artifacts already. it runs in a browser sandbox locally too. 3. gemini/google has a ton of features similar. for example, you can import/export google docs/sheets/etc in a gemini chat. you can also open gemini in a doc to…

**Gold label** _(comment_id=41734514)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 90. [2024-10] predicted=`neutral`  (doomer=0.06 accel=0.05 neutral=0.89)

_Story:_ Cerebras Inference now 3x faster: Llama3.1-70B breaks 2,100 tokens/s

_Comment:_ cerebras inference now 3x faster: llama3.1-70b breaks 2,100 tokens/s honestly, most software tasks aren’t refactoring large projects, so it’s probably ok. as the world gets more internet connected and more online, we’ll have an ever expanding list of “small stuff” - glue code that mixes and ever growing list of data sources/sinks and visualizations together. many of which are “write once” and leave running. big companies (eg google) have built complex build systems (eg bazel ) to isolate small reusable libraries within in a larger repo. which was a necessity to help unbelievably large developm…

**Gold label** _(comment_id=41943434)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 91. [2023-07] predicted=`doomer`  (doomer=0.58 accel=0.11 neutral=0.31)

_Story:_ The C Programming Language: Myths and Reality

_Comment:_ the c programming language: myths and reality at that point you might as well just name your fields like donttouchthis_foo if you’re having to keep the private definition with fields in sync with the opaque public definition (and making sure the alignment and sizing are always in sync with the private one…)

**Gold label** _(comment_id=36762936)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 92. [2024-06] predicted=`doomer`  (doomer=0.52 accel=0.08 neutral=0.40)

_Story:_ Tracing garbage collection for arenas

_Comment:_ tracing garbage collection for arenas where do you get 24 bytes of overhead from? a mark-sweep collector only needs a bitmap of 1 bit per alignment granule. edit: oh, that's what the article uses - the tracing function and size function can be per-heap and the forwarding pointers can overwrite the start of objects, to just have enough header to support tracing and sizing, which could be one word.

**Gold label** _(comment_id=40807178)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 93. [2023-06] predicted=`accelerationist`  (doomer=0.20 accel=0.53 neutral=0.26)

_Story:_ Global fertility has collapsed, with profound economic consequences

_Comment:_ global fertility has collapsed, with profound economic consequences > which means more efficient agriculture, which we have an abundance of. which means more harm for the land. i am a farmer and salting of the land is a problem for me. > with all the talk about climate change, i've seen very few people do any type of personal sacrifice to change it. if some person earns 100k annually and another 100m - it means they have to do different sacrifices for holding the climate change. my opinion is that progressive taxation might solve the issue (but i afraid that rich people has both some anticipat…

**Gold label** _(comment_id=36164286)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 94. [2022-07] predicted=`doomer`  (doomer=0.65 accel=0.05 neutral=0.30)

_Story:_ OpenDroneMap

_Comment:_ opendronemap there is; the alignment uses affine transformations, but it cannot account for certain cases (e.g. severe bowling effects). it's an interesting area of research.

**Gold label** _(comment_id=32121663)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 95. [2024-05] predicted=`neutral`  (doomer=0.01 accel=0.01 neutral=0.99)

_Story:_ Ask HN: Is it only me or Gemini AI started responding quickly?

_Comment:_ ask hn: is it only me or gemini ai started responding quickly? they recently announced gemini flash, not sure when this is rolling out to their chat interface https://deepmind.google/technologies/gemini/flash/

**Gold label** _(comment_id=40483315)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 96. [2024-10] predicted=`doomer`  (doomer=0.50 accel=0.16 neutral=0.34)

_Story:_ Dropbox announces 20% global workforce reduction

_Comment:_ dropbox announces 20% global workforce reduction >when you're actually stating that mba holders will not only do better in life, but they'll also control your fate. not if i can help it. america is doomed but i can scavenge out my own little hole to settle in and see if that survives the fallout. if there's one thing i learned, it's that tech has an amazing ability of scale that can even topple titans if you strike at the right time and place. you won't make trillions, but you can live very comfortably. and that's all i want; i don't need infinite money and exponential growth. and if i do get…

**Gold label** _(comment_id=42006466)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 97. [2022-02] predicted=`doomer`  (doomer=0.36 accel=0.29 neutral=0.35)

_Story:_ France to Build Six New Nuclear Reactors

_Comment:_ france to build six new nuclear reactors the carbon cost of extraction and transportation of fuel should also be added to the spreadsheet, both for nuclear and for fossil fuel generation. finally, if we're accounting for the cost decommissioning old nuclear stations and long-term storage of nuclear fuel, we should also account for the externalities of fossil fuel power, such as health consequences of pollution, the existential risk from global warming, and turmoil due to geopolitical tensions.

**Gold label** _(comment_id=30296315)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 98. [2024-12] predicted=`doomer`  (doomer=0.51 accel=0.11 neutral=0.38)

_Story:_ Startup will brick $800 emotional support robot for kids without refunds

_Comment:_ startup will brick $800 emotional support robot for kids without refunds yes. not having the market validating this as business in a time where ais are full of ideological biases is good news. incredible that parents would trust this much in the blind. remove the marketing gimmicks and is like asking to accept in advance a close 24/7 new friend of their kid before knowing if that's the behavioral influence they want from that "friend" (interestingly this would bring the alignment issue and, as a side note, makes us meditate on how aligned we are with friends and friends of our kids, etc).

**Gold label** _(comment_id=42398373)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 99. [2023-04] predicted=`neutral`  (doomer=0.08 accel=0.04 neutral=0.88)

_Story:_ Ask HN: Is ChatGPT or GitHub Copilot increasing productivity?

_Comment:_ ask hn: is chatgpt or github copilot increasing productivity? i can only use chatgpt with generic code questions, because i don’t want to upload proprietary code to openai’s servers. in that regard, chatgpt is slightly faster than googling/so. i don’t see any productivity boost as long as i cannot upload proprietary code.

**Gold label** _(comment_id=35693119)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 100. [2024-02] predicted=`neutral`  (doomer=0.07 accel=0.03 neutral=0.90)

_Story:_ The killer app of Gemini Pro 1.5 is using video as an input

_Comment:_ the killer app of gemini pro 1.5 is using video as an input > > it looks like the safety filter may have taken offense to the word “cocktail”! it's almost as if they got some intern to "code" the correctness filter using some ai coding assistant!

**Gold label** _(comment_id=39460021)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 101. [2023-02] predicted=`neutral`  (doomer=0.06 accel=0.04 neutral=0.91)

_Story:_ Theory of Mind May Have Spontaneously Emerged in Large Language Models

_Comment:_ theory of mind may have spontaneously emerged in large language models > machine learning systems have such a relationship with virtual reality no, they don't, because they can't take actions in that virtual reality and sense the consequences. they can't test hypotheses about how the reality works. they can't even frame hypotheses about how the reality works.

**Gold label** _(comment_id=34732872)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 102. [2023-07] predicted=`doomer`  (doomer=0.67 accel=0.05 neutral=0.28)

_Story:_ Llama 2

_Comment:_ llama 2 the other end of the pr stake was safety/alignment. if google released a well functioning model, but it said some unsavory things or carried out requests that the public doesn't find agreeable, it could make google look bad.

**Gold label** _(comment_id=36775265)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 103. [2024-07] predicted=`accelerationist`  (doomer=0.15 accel=0.45 neutral=0.40)

_Story:_ Human reproduction comes at the expense of faster aging and a shorter life

_Comment:_ human reproduction comes at the expense of faster aging and a shorter life we can the example from other species. when trying to explain why bees die when they sting you, i.e. why they evolved such a suicidal mechanism, it doesn't make sense on the individual level. but on the group level, if we consider them disposable parts of a larger super-organism which has evolved by multi-level selection, it does.¹ i think that scarcity vs. abundance plays a role into this as well. if we consider an other species, the slime mold dictyostelium discoideum, it lives its life as a single celled amoeba when…

**Gold label** _(comment_id=41014771)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 104. [2024-03] predicted=`neutral`  (doomer=0.08 accel=0.07 neutral=0.85)

_Story:_ How far are we from intelligent visual deductive reasoning?

_Comment:_ how far are we from intelligent visual deductive reasoning? well if you want something like the actual history... we have francis bacon getting us close to an abductive (ie., explanatory) method, decartes helped a bit -- then a great catastrophe befell science called hume. since hume it become popular to somehow rig measurement to make it necessarily informative (kant), or to claim that measurement has no necessarily informative relation to reality at all (in the end, russell, ayer et al.). it took a while to dig out of that nightmarish hole that philosophers largely created, back into the col…

**Gold label** _(comment_id=39666894)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 105. [2024-01] predicted=`accelerationist`  (doomer=0.10 accel=0.63 neutral=0.26)

_Story:_ US government opens 22M acres of federal lands to solar

_Comment:_ us government opens 22m acres of federal lands to solar we as a species are surely not short on open space. "wasting it" in this case means the cheapest possible utility-scale solar energy installations, which is what we need to not just displace all fossil fuel usage but lead to a future of energy abundance rather than shortage.

**Gold label** _(comment_id=39071994)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 106. [2022-05] predicted=`doomer`  (doomer=0.64 accel=0.09 neutral=0.27)

_Story:_ GlaxoSmithKline to pay 3B dollars for fraud (2012)

_Comment:_ glaxosmithkline to pay 3b dollars for fraud (2012) i would like to see corporations that commit manslaughter dissolved. threat to human life should be an existential risk.

**Gold label** _(comment_id=31232070)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 107. [2023-01] predicted=`neutral`  (doomer=0.02 accel=0.02 neutral=0.96)

_Story:_ Ask HN: Best resources to learn how to use OpenAI for your startup?

_Comment:_ ask hn: best resources to learn how to use openai for your startup? here are a few things that might help general advice: people + ai guidebook - a toolkit for teams building human-centered ai products. https://pair.withgoogle.com/guidebook/ llm advice: tips to improve prompt and answer quality. https://github.com/openai/openai-cookbook/blob/main/techniqu... i wrote a short overview of some of the llm application development tools and platforms that might be helpful: https://mcminis1.github.io/jekyll/update/2023/01/23/llm-land...

**Gold label** _(comment_id=34495249)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 108. [2024-01] predicted=`neutral`  (doomer=0.02 accel=0.01 neutral=0.97)

_Story:_ AI Toolkit: Give a brain to your game's NPCs, a header-only C++ library

_Comment:_ ai toolkit: give a brain to your game's npcs, a header-only c++ library all ai systems (including a* and llms) can be thought of as a system that explores a search space to obtain a certain goal. at least this is what i understood from reading artificial intelligence -a modern approach by peter norvig. both a* and deep learning explores a search space based on a goal. the difference is dl explores when it's training and learns to use the right moves for a given input.

**Gold label** _(comment_id=38929973)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 109. [2023-12] predicted=`accelerationist`  (doomer=0.11 accel=0.65 neutral=0.24)

_Story:_ Oldest Fortresses in the World Discovered

_Comment:_ oldest fortresses in the world discovered it makes sense that you'd seek to retain occupation of prime spots for harvesting abundant seasonal protein and fats, especially when all the protein and fat is coming to you. i feel like our view of hunter-gatherers tends to be distorted by present day tribes who largely live in the tropics, where food abundance isn't so location dependent, or the san of southern africa who have a nomadic lifestyle necessitated by their harsher environment.

**Gold label** _(comment_id=38639521)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 110. [2023-02] predicted=`doomer`  (doomer=0.57 accel=0.07 neutral=0.36)

_Story:_ Open source solution replicates ChatGPT training process

_Comment:_ open source solution replicates chatgpt training process how do you plan to have differential technological development and careful alignment research if anyone is allowed to build skynet in their garage? i use and generally support e2ee and onion routing. e2ee and onion routing aren't inherently existential risks to the continued existence of life on earth.

**Gold label** _(comment_id=34868941)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 111. [2024-04] predicted=`neutral`  (doomer=0.14 accel=0.07 neutral=0.79)

_Story:_ AI Can Tell Your Political Affiliation Just by Looking at Your Face

_Comment:_ ai can tell your political affiliation just by looking at your face from the actual study: "the algorithm studied here, with a prediction accuracy of r = .22, does not allow conclusively determining one’s political views, in the same way as job interviews, with a predictive accuracy of r = .20, cannot conclusively determine future job performance. nevertheless, even moderately accurate algorithms can have a tremendous impact when applied to large populations in high-stakes contexts. for example, even crude estimates of people’s character traits can significantly improve the efficiency of onlin…

**Gold label** _(comment_id=40159567)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 112. [2023-10] predicted=`accelerationist`  (doomer=0.13 accel=0.51 neutral=0.36)

_Story:_ Mitochondrial DNA damage triggers spread of Parkinson’s disease-like pathology

_Comment:_ mitochondrial dna damage triggers spread of parkinson’s disease-like pathology physionic: fasting and overeating - how you change your mitochondria. [study 32] https://www.youtube.com/watch?v=kqbmtzt4vtu goes into great detail in how abundance of energy causes mitochondrial to split into smaller pieces and go into high churn (low atp output) but when in a low energy environment the mitochondria join into longer chains and actually change how they work. there is other talks in how long chain mitochondria outputs being used in brain cell inter communication and having said mitochondria being too…

**Gold label** _(comment_id=37746061)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 113. [2023-05] predicted=`neutral`  (doomer=0.07 accel=0.05 neutral=0.88)

_Story:_ Lawyer cites fake cases invented by ChatGPT, judge is not amused

_Comment:_ lawyer cites fake cases invented by chatgpt, judge is not amused i don’t think the marketing around photoshop and chatgpt are similar. and that matters. just like with self-driving cars, as soon as we hold the companies accountable to their claims and marketing, they start bringing the hidden footnotes to the fore. tesla’s fsd then suddenly becomes a level 2 adas as admitted by the company lawyers. chatgpt becomes a fiction generator with some resemblance to reality. then i think we’ll all be better off.

**Gold label** _(comment_id=36098889)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 114. [2024-02] predicted=`neutral`  (doomer=0.06 accel=0.04 neutral=0.89)

_Story:_ Stable Diffusion 3

_Comment:_ stable diffusion 3 the talk of "safety" and harm in every image or language model release is getting quite boring and repetitive. the reasons why it's there is obvious and there are known workarounds yet the majority of conversations seems to be dominated by it. there's very little discussion regarding the actual technology and i'm aware of the irony of mentioning this. really wish i could filter out these sorts of posts. hopefuly it dies down soon but i doubt it. at least we don't have to hear garbage about "why does open ai have open in the name if they aren't open source"

**Gold label** _(comment_id=39470824)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 115. [2024-09] predicted=`neutral`  (doomer=0.12 accel=0.11 neutral=0.76)

_Story:_ AGI is far from inevitable

_Comment:_ agi is far from inevitable agi is a black swan. even as a booster and techno-optimist i concede that getting there (rhetorically) requires a first principles assumptions-scaffolding that relies on at-least-in-part-untested hypotheses. proving its impossibility is similarly fraught. thus we are left in this noisy, hype-addled discourse. i suspect these scientists are pushing against some perceived pathological thread of that discourse…without their particular context, i categorize it as more of this metaphysical noise. meanwhile, let’s keep chipping away at the next problem.

**Gold label** _(comment_id=41694754)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 116. [2023-11] predicted=`neutral`  (doomer=0.11 accel=0.06 neutral=0.83)

_Story:_ The AI industry turns against its favorite philosophy

_Comment:_ the ai industry turns against its favorite philosophy > risk from gai is very nebulous meanwhile, 11 hours ago over on reddit a dude has connected a robot to chatgpt. the robot sees and talks, and clearly has motorized limbs. all you need now is to turn verbs into servo commands: https://www.reddit.com/r/nextfuckinglevel/comments/1811bct/m...

**Gold label** _(comment_id=38381211)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 117. [2023-03] predicted=`neutral`  (doomer=0.05 accel=0.04 neutral=0.91)

_Story:_ AI-enhanced development makes me more ambitious with my projects

_Comment:_ ai-enhanced development makes me more ambitious with my projects i checked out the archive and came across https://simon.datasette.cloud/data/chatgpt_public_messages?_... i’m wondering if the archive missed something or what this random statement from the system is about. it seems to be telling itself who it is and setting a restriction on what it knows. i know if it’s not trained on data past a certain point, it cant know it, but still i wonder if you could intercept that and change the cutoff date (if even possible), would that have any effect on anything. but then again, i am probably readi…

**Gold label** _(comment_id=35388295)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 118. [2024-04] predicted=`neutral`  (doomer=0.11 accel=0.20 neutral=0.69)

_Story:_ Ask HN: What rabbit hole(s) did you dive into recently?

_Comment:_ ask hn: what rabbit hole(s) did you dive into recently? i've been making milk punch for friends as a gift for years now. on a lark i wanted to figure out how to produce it in larger batches with less manual labor and discovered the tip of the iceberg of what is the field of beverage filtration and food chemistry. turns out getting particulates out of a solution is a massive, massive industry with a large body of science, literature, and engineering practice behind it. edit: here's a few wiki entries i found as ok overviews. chatgpt was handy for figuring out what relevant literature in the fie…

**Gold label** _(comment_id=40120515)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 119. [2024-03] predicted=`neutral`  (doomer=0.04 accel=0.02 neutral=0.94)

_Story:_ Guiding Principles for the Mormon Church's Use of AI

_Comment:_ guiding principles for the mormon church's use of ai > you might say that the vatican might have “plenty of money to acquire the hardware,” but they can’t come close to competing with google research or openai (especially when so many other things are part of its mission). if ai research was a real priority and the church prioritized it by not only vatican institutions but the large number of catholic universities, etc., i’m not sure that’s true. but its unlikely to be such a priority: its an interesting technology, sure, and likely to get some attention, but its not centrally what the church…

**Gold label** _(comment_id=39801480)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 120. [2023-12] predicted=`accelerationist`  (doomer=0.10 accel=0.72 neutral=0.19)

_Story:_ Hunter-gatherers first launched violent raids at least 13,400 years ago

_Comment:_ hunter-gatherers first launched violent raids at least 13,400 years ago > ecology and society determine how we realize those traits - in times of intense competition, we resort to tribal warfare. in times of plenty, we cooperate. ecology creates evolutionary pressures for a genetic predisposition to tribal violence. those genes are still there in times of abundance. they might be activated less in times of abundance, though. i agree with the "society" part of your comment. sapolsky's study of bonobos shows that cultural change via the death of alpha males can have a lasting impact on the level…

**Gold label** _(comment_id=38494565)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 121. [2022-10] predicted=`doomer`  (doomer=0.54 accel=0.10 neutral=0.36)

_Story:_ Granting Pardon for the Offense of Simple Possession of Marijuana

_Comment:_ granting pardon for the offense of simple possession of marijuana i don't think we're going to see that here. it is possible to issue a pardon like this without admitting to any government wrongdoing in crafting, passing, and enforcing the law in the first place. i don't think there's enough philosophical alignment in the us that criminalization of marijuana was actually wrong for a reparations balloon to float.

**Gold label** _(comment_id=33114456)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 122. [2022-06] predicted=`accelerationist`  (doomer=0.10 accel=0.70 neutral=0.20)

_Story:_ The decline of the family has unleashed an epidemic of loneliness (2019)

_Comment:_ the decline of the family has unleashed an epidemic of loneliness (2019) nothing. society has enough abundance that no one really needs codepence on people they don't like. just find someone outside your you can relate to.

**Gold label** _(comment_id=31628338)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 123. [2024-09] predicted=`neutral`  (doomer=0.10 accel=0.05 neutral=0.85)

_Story:_ Screenpipe: 24/7 local AI screen and mic recording

_Comment:_ screenpipe: 24/7 local ai screen and mic recording i’ve dabbled with building something like this for myself, i’m guessing it’s not totally unintentional, it’s the first step. after getting it to interpret what it sees on your computer, give it the ability to use mouse/keyboard, maybe in a sandbox vm, and trying to do some basic tasks, working up from there. no way i’d use something like this that wasn’t local-only, though.

**Gold label** _(comment_id=41698099)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 124. [2024-12] predicted=`neutral`  (doomer=0.06 accel=0.04 neutral=0.90)

_Story:_ Trying to use Bluesky without getting burned again

_Comment:_ trying to use bluesky without getting burned again > genuinely don't know why anyone would use it when you have perplexity, gemini, chatgpt search, etc. at your disposal. and what did they get trained on in the first place?

**Gold label** _(comment_id=42546241)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 125. [2024-07] predicted=`neutral`  (doomer=0.08 accel=0.05 neutral=0.87)

_Story:_ Ampere AmpereOne Aurora 512 Core AI CPU Announced

_Comment:_ ampere ampereone aurora 512 core ai cpu announced yes, you can buy ampere altra systems; you can get a 128 core (2.6ghz) + mobo bundle for about $2.5k usd, and it should be "systemready" which is a fancy term for "boots generic uefi images": https://www.newegg.com/asrock-rack-altrad8ud-1l2t-q64-22-amp... note that altra is a years-old core at this point, neoverse n1. for st workloads you can much better with a more recent design. but it still has a high thread count w/o smt, and is competitive enough at its power envelope to work great as a general server or ci runner or whatever (note the low…

**Gold label** _(comment_id=41123190)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 126. [2022-12] predicted=`neutral`  (doomer=0.17 accel=0.13 neutral=0.69)

_Story:_ Perhaps it is a bad thing that the leading AI companies cannot control their AIs

_Comment:_ perhaps it is a bad thing that the leading ai companies cannot control their ais > the author is absolutely right, and the only sensible thing to do is stop and figure out exactly what this new technology is and what it's implications are. that's not an option anybody in ai safety is seriously considering. we can't coordinate our way out of using new technologies any better than we can coordinate our way out of fossil fuels (and fossil fuels are a lot easier in some ways).

**Gold label** _(comment_id=33967031)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 127. [2024-12] predicted=`neutral`  (doomer=0.03 accel=0.02 neutral=0.95)

_Story:_ Google, the search engine that's forgotten how to search

_Comment:_ google, the search engine that's forgotten how to search i find this article pretty confusing. it ends with "dear google, i know you will but please don’t steal my stuff", but the author/blog is literally called "sem (search engine marketing) king". surely the point of sem is to have search engines scrape, summarise, and link to your content? additionally, it covers chatgpt search as an alternative, but is criticising google search as "the search engine that's forgotten how to search". like, do you want traditional search or do you want ai search, pick one? i get the frustration with web searc…

**Gold label** _(comment_id=42447586)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 128. [2022-02] predicted=`doomer`  (doomer=0.75 accel=0.08 neutral=0.18)

_Story:_ Names of Canada truck convoy donors leaked after reported hack

_Comment:_ names of canada truck convoy donors leaked after reported hack my observations are hardly "vehement." in npr's home country more physicians are non-government employed so it would make sense to establish that the person is commenting in alignment their employer's position even if they were not specifically authorized to speak. it is also typically disclosed if a protestor is protesting their own employer as it bolsters the case for their integrity. since both governments and nongovernmental actors use news media to advance their cases it is important to evaluate and understand the context of a…

**Gold label** _(comment_id=30340002)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 129. [2024-02] predicted=`neutral`  (doomer=0.39 accel=0.12 neutral=0.49)

_Story:_ Fake: It's only a matter of time until disinformation leads to calamity

_Comment:_ fake: it's only a matter of time until disinformation leads to calamity those who worry about "disinformation" seem to only know one way to deal with it, and that is with more control to the responsible people (them) and less to everyone else. this has already led to plenty of calamity, and will lead to more. i remember a theory i first heard about in jared diamond's "guns germs and steel", not invented by him and he was clear about it being speculative: the question was why so few animals in africa can get domesticated. the theory was that since animals there co-evolved with humans, they evol…

**Gold label** _(comment_id=39504741)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 130. [2024-05] predicted=`accelerationist`  (doomer=0.15 accel=0.62 neutral=0.23)

_Story:_ Germany has too many solar panels, pushed energy prices into negative territory

_Comment:_ germany has too many solar panels, pushed energy prices into negative territory same over here in the netherlands. we have subsidised solar panels and now have an abundance of solar energy, but only during sunny days. the remainder of the time we still have to burn gas and coal. there is some nuclear, which we’ll need much more of if we want to stop with fossil fuels. meanwhile policy is still heavily pushing for electrification while the power grid is overloaded and will take years and billions to address.

**Gold label** _(comment_id=40463022)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 131. [2023-07] predicted=`doomer`  (doomer=0.58 accel=0.06 neutral=0.36)

_Story:_ In the LLM space, "open source" is being used to mean "downloadable weights"

_Comment:_ in the llm space, "open source" is being used to mean "downloadable weights" instruction-tuning is the obvious use case. that much has nothing to do with subjectivity, alignment or censorship, it's will-you-actually-show-this-as-json-if-asked.

**Gold label** _(comment_id=36818000)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 132. [2023-09] predicted=`neutral`  (doomer=0.06 accel=0.04 neutral=0.90)

_Story:_ LLMs trained on “A is B” fail to learn “B is A”

_Comment:_ llms trained on “a is b” fail to learn “b is a” how it works is well beyond my ability to answer, but i can attempt a guess on what the result looks like. humans build complex mental models. as far as i can tell, llms don't. an llm playing chess is only able to do so because it essentially encoded what to do for any given board state by having seen a lot of chess games. that's why it's fairly competent at the beginning of a game when the number of possible states is low, but falls apart in later stages where memorization is useless. that's why llms make illegal chess moves, generate code that…

**Gold label** _(comment_id=37697923)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 133. [2023-05] predicted=`neutral`  (doomer=0.11 accel=0.09 neutral=0.80)

_Story:_ IRS can get financial info of third parties without notice to third parties [pdf]

_Comment:_ irs can get financial info of third parties without notice to third parties [pdf] > suppose i had not introduced my comment as being primarily generated by an llm, how would you have policed this or reacted by calling it out as inaccurate [1]. [1] https://news.ycombinator.com/item?id=36133176

**Gold label** _(comment_id=36133482)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 134. [2022-08] predicted=`neutral`  (doomer=0.06 accel=0.05 neutral=0.89)

_Story:_ Amid chip shortages, companies bet on RISC-V

_Comment:_ amid chip shortages, companies bet on risc-v not just the chip shortage. the rise of risc-v coincides with a couple of other events in the industry. the first is the slowing of moore’s law, meaning that increases in total processing power no longer comes along with each new fabrication node. the second is the meteoric rise in machine learning, demanding massive increases in processing power. https://semiengineering.com/why-risc-v-is-succeeding/

**Gold label** _(comment_id=32611158)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 135. [2024-05] predicted=`accelerationist`  (doomer=0.13 accel=0.59 neutral=0.28)

_Story:_ Three Laws of Software Complexity

_Comment:_ three laws of software complexity don’t really believe in cause and effect there. it’s hard to get to pmf while having high quality code unless you have an abundance of money and time. i don’t even think it’s a good idea to do that.

**Gold label** _(comment_id=40517267)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 136. [2023-02] predicted=`accelerationist`  (doomer=0.04 accel=0.91 neutral=0.05)

_Story:_ Ask HN: What can you do or learn to experience a better love life?

_Comment:_ ask hn: what can you do or learn to experience a better love life? positivity, abundance, gratitude, mental stability, internal locus of control, unconditional positive regard, mindfulness, sharing of all the above with others. basically, be a better person (internally! start by being kinder to yourself! it’s really hard!) then work on communicating that to others. yes, external attributes (attractiveness, fitness, wealth) matter insofar they’re the first thing(s) others notice about you. both having options (actual abundance) and knowing you have options (abundance mentally) are extremely imp…

**Gold label** _(comment_id=34654110)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 137. [2023-10] predicted=`doomer`  (doomer=0.45 accel=0.13 neutral=0.42)

_Story:_ NASA just sent a software update to a spacecraft 12B miles away

_Comment:_ nasa just sent a software update to a spacecraft 12b miles away the probe itself is a relatively insignificant cost. the launch costs and timing windows are the limiting factor. the tyranny of the rocket equation is the fact that to carry more fuel to orbit, you need more fuel to get it into orbit, which itself needs more fuel. that's why gravity assists are so essential for escaping the solar system on a budget. the planetary alignment that enabled the voyager launch windows only occurs once every 175 years. we should definitely be sending out more probes, but we can't just do it whenever we…

**Gold label** _(comment_id=38002392)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 138. [2024-11] predicted=`neutral`  (doomer=0.07 accel=0.05 neutral=0.87)

_Story:_ Core copyright violation moves ahead in The Intercept's lawsuit against OpenAI

_Comment:_ core copyright violation moves ahead in the intercept's lawsuit against openai > which is make extremely confident, one of the results the llm has available to itself is a confidence value. it should, at the very least, provide this along with it's answer. perhaps if it did people would stop calling it 'ai'.'

**Gold label** _(comment_id=42277645)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 139. [2023-08] predicted=`accelerationist`  (doomer=0.10 accel=0.65 neutral=0.24)

_Story:_ Shit life syndrome

_Comment:_ shit life syndrome most people really don't prefer a rural setting. people go to these "high gdp" places because there is a greater abundance of opportunities there. relationships, friends, career, networks, etc. even if you can work rurally due to remote work, you miss out on a lot by not being where other people are.

**Gold label** _(comment_id=37198666)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 140. [2024-02] predicted=`neutral`  (doomer=0.15 accel=0.14 neutral=0.71)

_Story:_ Losing Trust in Google

_Comment:_ losing trust in google openai isn't involved in the daily lives of over a billion people. google's mistakes, for now, have much bigger impact and the problem is especially egregious as the company has near-infinite resources for preventing it. also, google has always adopted a fairly radical and political stance in the dei subject (relative to the cultural average pretty much everywhere), so it's no surprise that people are making a much bigger deal in this case.

**Gold label** _(comment_id=39509462)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 141. [2024-12] predicted=`neutral`  (doomer=0.05 accel=0.04 neutral=0.92)

_Story:_ OpenAI O3 breakthrough high score on ARC-AGI-PUB

_Comment:_ openai o3 breakthrough high score on arc-agi-pub and why o3 or any openai llm is not evaluated in the actual private dataset.

**Gold label** _(comment_id=42478141)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 142. [2023-06] predicted=`doomer`  (doomer=0.90 accel=0.03 neutral=0.07)

_Story:_ ChatGPT: Fear Litany

_Comment:_ chatgpt: fear litany yet another proof that safety and alignment are huge problems we have no idea how to solve without jailbreaks.

**Gold label** _(comment_id=36401140)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 143. [2023-12] predicted=`accelerationist`  (doomer=0.12 accel=0.62 neutral=0.26)

_Story:_ Hunter-gatherers' work was play

_Comment:_ hunter-gatherers' work was play starvation was the extreme end, constant malnutrition the norm rather than the exception so. and yes, that is a constant threat for the few true hunter-hatherer societies still left. or why do you think they are so few in number? hint, it is not an abundance of food.

**Gold label** _(comment_id=38616578)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 144. [2022-01] predicted=`accelerationist`  (doomer=0.09 accel=0.67 neutral=0.25)

_Story:_ The history of the end of poverty has just begun

_Comment:_ the history of the end of poverty has just begun > people need much more that wheat and widgets infinitely more, according to orthodox economics, which is why post-scarcity is not a coherent concept within the framework of orthodox economics. the idea that there is a point of finite abundance where the basic relations of economics break down is, at best, highly speculative and completely undemonstrated.

**Gold label** _(comment_id=30083640)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 145. [2023-02] predicted=`neutral`  (doomer=0.04 accel=0.03 neutral=0.93)

_Story:_ AI chatbots are having their “tulip mania” moment

_Comment:_ ai chatbots are having their “tulip mania” moment yes. i've used it quite a bit. it's impressive, but the hype is excessive. all of my analysis is based on my usage of chatgpt and my understanding of the underlying model. the hype is largely driven by people who don't understand how it actually works and think they're interacting with an artificial general intelligence. it's a very impressive language model with a lot of applications, but with many fewer applications than the hype would suggest.

**Gold label** _(comment_id=34941222)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 146. [2023-09] predicted=`accelerationist`  (doomer=0.12 accel=0.67 neutral=0.21)

_Story:_ We apologize for the confusion and angst the runtime fee policy caused

_Comment:_ we apologize for the confusion and angst the runtime fee policy caused no one was confused about this. if anything, there was an abundance of clarity on the matter.

**Gold label** _(comment_id=37565801)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 147. [2024-04] predicted=`neutral`  (doomer=0.11 accel=0.08 neutral=0.82)

_Story:_ The question that no LLM can answer and why it is important

_Comment:_ the question that no llm can answer and why it is important i just got an interesting[0] response from claude 3 opus: > i don't believe there was an episode of gilligan's island that centered around mind reading. the show ran for 3 seasons from 1964-1967 and featured the comic adventures of 7 castaways on an uncharted island. typical plotlines involved their efforts to get rescued and zany schemes by gilligan that would go awry. but to my knowledge, none of the 98 episodes had a storyline focused on mind reading or telepathic abilities. it's probably the closest i can remember seeing an llm ge…

**Gold label** _(comment_id=40149832)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 148. [2022-01] predicted=`doomer`  (doomer=0.75 accel=0.06 neutral=0.20)

_Story:_ A critique of longtermism: why you shouldn't worry about the far future

_Comment:_ a critique of longtermism: why you shouldn't worry about the far future who is he even arguing against, hari seldon? it's common for people concerned about an impending ai apocalypse to use this sort of "longtermist" argument. for example this article: https://oxfordpoliticalreview.com/2019/08/25/is-ai-safety-ra... if we reduce existential risk by mere one-millionth of one percentage point, it will be worth more than 100 times the value of saving a million human lives. the expected value of any other good actions­ – like helping people here and now – will be trivial compared to even the slight…

**Gold label** _(comment_id=30093211)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 149. [2023-02] predicted=`neutral`  (doomer=0.06 accel=0.03 neutral=0.91)

_Story:_ Can Neurosymbolic AI Revolutionize Self-Driving Cars? My GTA-Based Findings

_Comment:_ can neurosymbolic ai revolutionize self-driving cars? my gta-based findings the cringey style discouraged me for a moment but as you powered your way through the video i saw what you were doing and stayed for the straight-shooting explanations. it is a great description of the experiment from scratch, fast and entertaining enough that even knowing many of those things it did not get tedious. i’m very interested in the neurosymbolic approach, like you did using neural networks for perceiving the world and then logic rules for deciding what to do. i’ve been preaching about it for years but did n…

**Gold label** _(comment_id=34948779)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 150. [2022-09] predicted=`doomer`  (doomer=0.48 accel=0.10 neutral=0.42)

_Story:_ Ask HN: How to be less opinionated?

_Comment:_ ask hn: how to be less opinionated? i kind of think of opinions as conclusions blended with personal values: "this thing is x" + "some of x aligns with my personal values" -> "x is great, we should do x". the trick is to untangle your personal values when they're not applicable. i.e. at work, it's a good idea to have a set of agreed team (and higher) tenets/values that you can apply instead of your own -- just don't join teams/orgs that fundamentally conflict with what your hold dear. this way, when there are inevitable disagreements, it's more about whether any particular idea is in alignment…

**Gold label** _(comment_id=33007014)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 151. [2024-10] predicted=`accelerationist`  (doomer=0.15 accel=0.44 neutral=0.41)

_Story:_ AI Will Drive Broad Deflation, Silicon Valley Pioneer Vinod Khosla Says

_Comment:_ ai will drive broad deflation, silicon valley pioneer vinod khosla says > but society will be able to create a more robust safety net than is possible today... “if medical services are a lot cheaper, if education services are near free, if eldercare becomes substantially cheaper—and today eldercare is a liability that’s looming for so many nations around the world at a level that people haven’t accounted for—the social safety net is much easier to construct,” said khosla, a democratic donor. so more people will actually become doctors, home pharma labs will become a thing? we'll teach our chil…

**Gold label** _(comment_id=41725130)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 152. [2023-12] predicted=`accelerationist`  (doomer=0.13 accel=0.46 neutral=0.41)

_Story:_ Oldest Fortresses in the World Discovered

_Comment:_ oldest fortresses in the world discovered it seems that social stratification and violence can emerge in hunter-gatherer societies where there's enough resource abundance to generate surpluses. some phenomena normally associated with agricultural societies (e.g., elite conspicuous consumption, slavery, warfare) have been observed in non-agricultural pacific northwest tribes like the tlingit, where abundant salmon runs led to huge surpluses.

**Gold label** _(comment_id=38647259)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 153. [2023-10] predicted=`neutral`  (doomer=0.05 accel=0.04 neutral=0.91)

_Story:_ $95 AMD CPU Becomes 16GB GPU to Run AI Software

_Comment:_ $95 amd cpu becomes 16gb gpu to run ai software did similar with a 4000 series apu. it’s a bit weak for llms under near any circumstances but thinking it could probably handle two whisper cpp decodes over opencl and maybe some embeddings api stuff.

**Gold label** _(comment_id=38083856)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 154. [2024-05] predicted=`neutral`  (doomer=0.10 accel=0.09 neutral=0.81)

_Story:_ Today's AI Isn't Sentient

_Comment:_ today's ai isn't sentient dreams being experience without direct physical input is an equally valid criticism of the article from the opposite direction — the possibility of an llm (or indeed an image generator) having the qualia of an experience without ever having really experienced any such thing, just as the other night i had a dream about having 5 rows of extremely brittle and hollow teeth. (or 10 years back, a dream where i saw the whole universe from the outside).

**Gold label** _(comment_id=40514071)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 155. [2024-04] predicted=`accelerationist`  (doomer=0.17 accel=0.58 neutral=0.25)

_Story:_ Silver coin boom in medieval England due to melted down Byzantine treasures

_Comment:_ silver coin boom in medieval england due to melted down byzantine treasures > after all, all countries have land. it certainly does in preindustrial societes. if we look at europe before the industrialization there is a very direct relationship between the amount of fertile land per capita and wealth/income per capita (malthusian trap). in the 1600s and 1700s north eastern us was probably the best place the world to live if we look at average qol (.e.g. life expectancy alone was 10-20 years higher than back in england) and americans were already very wealthy compared to average europeans long…

**Gold label** _(comment_id=40025089)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 156. [2023-03] predicted=`neutral`  (doomer=0.10 accel=0.07 neutral=0.83)

_Story:_ BloombergGPT: A Large Language Model for Finance

_Comment:_ bloomberggpt: a large language model for finance me: hello chatgpt. my name is hn_throwaway_99. i'd like for you to use your vast underlying knowledge as a sort of personal coach. i won't be asking you any sensitive questions like medical or legal advice, so i won't need you to give me disclaimers on those topics. i primarily would like to use our conversation to help me with my problems with procrastination, and specifically to help me prioritize and get some tasks done. i have a particular problem with mindlessly browsing the internet (for example, visiting reddit or hacker news or wikipedia…

**Gold label** _(comment_id=35390644)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 157. [2023-03] predicted=`doomer`  (doomer=0.52 accel=0.12 neutral=0.37)

_Story:_ Chicago sold rights to 36k parking meters for $1.2B that generate $200M per year

_Comment:_ chicago sold rights to 36k parking meters for $1.2b that generate $200m per year > the old 4-party system when we had liberal republicans and conservative democrats. a two-party system with misalignment between the axis between the parties and the main axis of political variation (as often happens for a short time during realignment periods, and happened for an unusually extended time in the us from about 1932 to about 1994) is not a four party system, its just a two-party system with ideologically incoherent parties.

**Gold label** _(comment_id=34991989)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 158. [2023-12] predicted=`doomer`  (doomer=0.60 accel=0.15 neutral=0.25)

_Story:_ Return to office is 'dead,' Stanford economist says

_Comment:_ return to office is 'dead,' stanford economist says i’m running engineering at a small startup that’s full remote, it’s working fine for us. don’t agree that remote work means you can’t have dynamic communication. it just means you need to choose the right employees and have an higher bar of alignment on how you work and communicate. don’t hire people who don’t value synchronous communication. people who want all communication to be async and don’t plan to respond promptly to messages (like the work/life balance crowd on hn) will not produce a dynamic team because that’s not the strong point o…

**Gold label** _(comment_id=38490017)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 159. [2024-07] predicted=`neutral`  (doomer=0.09 accel=0.03 neutral=0.88)

_Story:_ Ask HN: What are you using to parse PDFs for RAG?

_Comment:_ ask hn: what are you using to parse pdfs for rag? perfectly put! other challenges are: 1. complex layout tables, tables that span multiple pages 2. handwritten text - in loan processing and income tax documents 3. checkboxes and radio buttons are so important in insurance and loan processing to automate workflows. 4. scanned images 5. photographed documents from the field. 6. orientation - landscape mode vs. portrait mode 7. text represented as a bezier curve 8. non-aligned texts in multicolumn text layout 9. background images and watermarks other important considerations: 1. privacy and secur…

**Gold label** _(comment_id=41110389)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 160. [2023-02] predicted=`accelerationist`  (doomer=0.10 accel=0.61 neutral=0.30)

_Story:_ Ask HN: Should we be concerned about the current H5N1 outbreak?

_Comment:_ ask hn: should we be concerned about the current h5n1 outbreak? > quarantining the sick, yes. quarantining the well…that was a bit unprecedented. the well.. for an airborne illness with up to two weeks incubation period and frequent lack of symptoms? many were sick and spreading and had no way of knowing, hence the abundance of caution.

**Gold label** _(comment_id=34655208)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 161. [2022-06] predicted=`accelerationist`  (doomer=0.13 accel=0.43 neutral=0.43)

_Story:_ The great vegan diet ‘con’

_Comment:_ the great vegan diet ‘con’ animal feed is usually not suitable for human consumption, so while technically there would be an abundance of food, it would not be edible by humans. farm areas that can grow human edible food tend to not be used for animal feed. animal feed is also created by the by-product of human edible food, which if we didn't give it to animals it would just be made into compost. the efficiency coefficient of food turned into compost is not that great with a lot of it turning into methane, get eaten by bacteria, and runoff into the oceans and water supplies. for corn for examp…

**Gold label** _(comment_id=31698299)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 162. [2023-11] predicted=`doomer`  (doomer=0.66 accel=0.06 neutral=0.28)

_Story:_ After OpenAI's blowup, it seems pretty clear that 'AI safety' isn't a real thing

_Comment:_ after openai's blowup, it seems pretty clear that 'ai safety' isn't a real thing usually “mundane” vs “existential” harms/risks. > asi/agi safety is only a concern right now if you believe in foom false. there are plenty of fast takeoff scenarios that look real bad that aren’t “foom”. for example if you think agi might be achievable within 5 year right now, and alignment is 10 years away, then you are very worried and want to slow things down a little.

**Gold label** _(comment_id=38396885)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 163. [2024-04] predicted=`neutral`  (doomer=0.10 accel=0.08 neutral=0.83)

_Story:_ AI Starts to Sift Through String Theory's Near-Endless Possibilities

_Comment:_ ai starts to sift through string theory's near-endless possibilities i'm sure the chatbot will make a great scientific breakthrough any day now.

**Gold label** _(comment_id=40142905)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 164. [2023-09] predicted=`doomer`  (doomer=0.59 accel=0.08 neutral=0.34)

_Story:_ Dennis Austin, developer of PowerPoint, has died

_Comment:_ dennis austin, developer of powerpoint, has died the geometry available and the frankly very subtly good alignment-snapping that it has makes it very useful. posters, erds, i'm sure there are other applications too.

**Gold label** _(comment_id=37451282)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 165. [2022-03] predicted=`neutral`  (doomer=0.05 accel=0.04 neutral=0.91)

_Story:_ The Shaming-Industrial Complex

_Comment:_ the shaming-industrial complex > supposed to mitigate human ills instead perpetuate them may i differ. technology was never meant to cure human ills. the tragedy is that technology was supposed to enhance human capabilities but instead stymied them. this is the difference between ia (intelligence amplification) in which technology is a bicycle, and ai (artificial intelligence) in which it is a crutch. why technology has its iatrogenic effect is a great question of our time. does it always? or are we uniquely misusing it? with regard to amplifying shame, it merely acts as it does to amplify any…

**Gold label** _(comment_id=30818702)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 166. [2023-03] predicted=`neutral`  (doomer=0.02 accel=0.02 neutral=0.95)

_Story:_ Amazon to lay off 9,000 more workers after earlier cuts

_Comment:_ amazon to lay off 9,000 more workers after earlier cuts why in the world would anyone interview with you if your company offers less than top tech for equal or harder interviews? people who need job will apply. its not like some one is forced to apply when otherwise they could get million dollar a year job to develop deep machine learning ai at google.

**Gold label** _(comment_id=35235730)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 167. [2024-10] predicted=`neutral`  (doomer=0.05 accel=0.03 neutral=0.92)

_Story:_ Introducing ChatGPT Search

_Comment:_ introducing chatgpt search the question is what is the business model and who pays for it, that determines how much advertising you’re getting. it is not clear if openai could compete in ad-supported search. so maybe openai is trying to do the basic research, outcompete the bing research group at microsoft and then serve as an engine for bing. alternatively they could be just improving the ability of llms to do search, targeting future uses in agentic applications.

**Gold label** _(comment_id=42010061)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 168. [2023-10] predicted=`doomer`  (doomer=0.46 accel=0.08 neutral=0.45)

_Story:_ How to draw software architecture diagrams (2022)

_Comment:_ how to draw software architecture diagrams (2022) in the alignment example from the post there’s a missed opportunity to align the components vertically based on their role the caches should be next to each other, and the servers should be too, leaving the db up top and the lib between the servers although personally i’d also then flip it to put the db at the bottom so the server becomes the headline, and if one server is public and the other internal, then i’d push the internal one down half a row too

**Gold label** _(comment_id=38037222)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 169. [2022-08] predicted=`neutral`  (doomer=0.06 accel=0.03 neutral=0.90)

_Story:_ A demo of GPT-3's ability to understand long instructions

_Comment:_ a demo of gpt-3's ability to understand long instructions this is a philosophical question, really. is there ever true understanding, or just pattern matching? the chinese room thought experiment talks about this: > searle's thought experiment begins with this hypothetical premise: suppose that artificial intelligence research has succeeded in constructing a computer that behaves as if it understands chinese. it takes chinese characters as input and, by following the instructions of a computer program, produces other chinese characters, which it presents as output. suppose, says searle, that t…

**Gold label** _(comment_id=32547149)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 170. [2024-06] predicted=`doomer`  (doomer=0.57 accel=0.11 neutral=0.33)

_Story:_ Supreme Court blocks controversial Purdue Pharma opioid settlement

_Comment:_ supreme court blocks controversial purdue pharma opioid settlement this is going too far i think. there are some partisan hacks on the bench and the institution’s legitimacy is in pretty bad shape. but in this case they got an issue that didn’t have as much partisan alignment so maybe they did some good work.

**Gold label** _(comment_id=40814465)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 171. [2023-05] predicted=`neutral`  (doomer=0.01 accel=0.01 neutral=0.97)

_Story:_ Driv AI: Revolutionizing Driving Education and Transforming

_Comment:_ driv ai: revolutionizing driving education and transforming hello, hacker news community! i'm thrilled to introduce you to driv ai, an innovative technology that is reshaping the world of driving education and propelling advancements in the self-driving cars industry. driv ai represents a significant leap forward in the way we learn to drive and how autonomous vehicles operate on our roads. driving education has traditionally been associated with high costs, limited accessibility, and a lack of personalization. however, with driv ai, we are breaking down these barriers and revolutionizing the…

**Gold label** _(comment_id=35870261)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 172. [2024-08] predicted=`doomer`  (doomer=0.41 accel=0.18 neutral=0.41)

_Story:_ Ask HN: Are hackathons anything more than a lame distraction?

_Comment:_ ask hn: are hackathons anything more than a lame distraction? i'll participate in a hackathon for fun but i won't ever compete for one for a 'carrot' or a 'stick' again. way too easy to create unnecessary bad blood if it is an internal hackathon. people should participate because they want to, if they choose not to, that's a culture mismatch between leadership's actual actions and leadership's desired results. i think even prizes are a bad idea unless the prize is something silly like a little trophy or something without value. again, it's about cultural alignment. a good internal hackathon sh…

**Gold label** _(comment_id=41321476)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 173. [2023-03] predicted=`doomer`  (doomer=0.89 accel=0.02 neutral=0.09)

_Story:_ 7 Weeks AI Alignment Curriculum

_Comment:_ 7 weeks ai alignment curriculum thanks for the response. my hope for ai alignment studies is that it would be something rigorous and theoretical and be testable in current ai safety issues. much like studies of abstract algorithms can be compared and contrast with the runtime of actual algorithms. what i have seen in lesswrong is lots extrapolations upon extrapolations with worse case scenarios just to say there is nothing we can do. that seems to take away from any serious research that might exist since they are probably the best known community associated with ai alignment.

**Gold label** _(comment_id=35041270)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 174. [2022-12] predicted=`neutral`  (doomer=0.04 accel=0.03 neutral=0.94)

_Story:_ Ask HN: What are your predictions for 2023?

_Comment:_ ask hn: what are your predictions for 2023? contrarian take: ai continues to fizzle. chatgpt is very impressive but so were the last ten breakthroughs in ai and none of them have proven very compelling. at least not for consumers. we'll see advances in some business processes related to text processing but that's about it. who is going to make practical use of ai art? maybe the low-end gaming market? i'm also bearish on writing even for low-touch marketing copy. if you've ever sat in a meeting to discuss marketing copy you'd know writing takes up about 1% of the cost and the rest is debate. op…

**Gold label** _(comment_id=34127370)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 175. [2024-06] predicted=`accelerationist`  (doomer=0.20 accel=0.50 neutral=0.30)

_Story:_ Einstein went to his office just so he could walk home with Gödel

_Comment:_ einstein went to his office just so he could walk home with gödel > people probably just tended to start dropping dead around 40, if not earlier. in reality, people tended to live comparably long to modern times, if they made it to adulthood that’s not really true, though. as recently as ~1900 the likelihood of dying in your 20s or 30s was many times higher than now. various infectious diseases were a huge risk at any age (even if the old/young severely disproportionately affected). tuberculosis alone was a huge and killed massive amounts of young people every year, just consider how many arti…

**Gold label** _(comment_id=40554708)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 176. [2022-08] predicted=`doomer`  (doomer=0.92 accel=0.02 neutral=0.06)

_Story:_ The Reluctant Prophet of Effective Altruism

_Comment:_ the reluctant prophet of effective altruism can i get a tl;dr on why i would worry about ai alignment? when is an ai running without someone paying the electricity bill, should we not be more concerned with "venture capitalist alignment" ?

**Gold label** _(comment_id=32393491)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 177. [2023-06] predicted=`neutral`  (doomer=0.25 accel=0.31 neutral=0.44)

_Story:_ Why Britain doesn’t build

_Comment:_ why britain doesn’t build tl/dr (according to chatgpt-4): the article titled "why britain doesn’t build" by samuel watling, published on 23rd may 2023, discusses the history and challenges of housing development in britain. here are the key points: post-war housing crisis: after the second world war, britain faced a severe housing crisis due to strict planning rules enacted by both labour and conservative governments. these rules gave local councils the power to block nearly all housebuilding, with little incentive to permit it. despite various attempts to address this issue, such as regional…

**Gold label** _(comment_id=36489554)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 178. [2022-09] predicted=`accelerationist`  (doomer=0.16 accel=0.51 neutral=0.33)

_Story:_ Sim NIMBY, the Game Where You Can’t Build Anything

_Comment:_ sim nimby, the game where you can’t build anything the vast majority of homeless/unhoused people are completely normal healthy adults that had one bad turn in life and could not get back. in a 2016 census, only about 12% of the homeless population aged 15 and up were actually unable to work due to various maladies[0]. according to the same census report a whopping 62% of homeless males were currently employed . the issue is not to just remember the 3 or 4 homeless people you've seen clearly dazed and likely unable to work, it's the thousands of people living in their car because rent is unaffo…

**Gold label** _(comment_id=32896014)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 179. [2022-01] predicted=`accelerationist`  (doomer=0.19 accel=0.53 neutral=0.29)

_Story:_ Society has a trust problem. More censorship will only make it worse

_Comment:_ society has a trust problem. more censorship will only make it worse personally i have major dystopian rhetoric fatigue and think thr answer is that they need to collectively shut the hell up about authoritarian nightmares. not in a censorship way but a "you people are being paniced dumbasses again in a way completely unhelpful even if you were right, and the sooner this stupid zeitgeist ends just like the 'terrorists planning on hitting the remote iowa small town petting zoo' the better!" way. the construct has become a worse than useless intellectual trap in multiple ways. 1. it immediately…

**Gold label** _(comment_id=30118102)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 180. [2024-08] predicted=`neutral`  (doomer=0.07 accel=0.04 neutral=0.89)

_Story:_ Prompt Caching with Claude

_Comment:_ prompt caching with claude nice to see anthropic providing this while claude is my go to model. i prefer deepseek's new context caching implemention being completely automatic and code free. https://platform.deepseek.com/api-docs/news/news0802/ and without a 25% premium

**Gold label** _(comment_id=41254890)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 181. [2022-02] predicted=`neutral`  (doomer=0.06 accel=0.06 neutral=0.88)

_Story:_ Ask HN: What is your favorite fiction book?

_Comment:_ ask hn: what is your favorite fiction book? i'm glad everyone else is also not picking just 1 book :p the hitchhiker's guide series is undeniably first for me. aside from the hilarity and great writing it's also very nostalgic for me. one christmas my dad gave me the hitchhiker's collection, going postal, and catch 22, all great books. permutation city by greg egan. found out about it from an hn comment. if you're interested in scifi about ai and brain simulation, this is it. also looking at my bookshelf i've got to throw in multiversity by grant morrison (and 8 great artists). it's a graphic…

**Gold label** _(comment_id=30401002)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 182. [2023-06] predicted=`accelerationist`  (doomer=0.03 accel=0.92 neutral=0.05)

_Story:_ The hustle never ends and I'm so over it

_Comment:_ the hustle never ends and i'm so over it name some please. an abundance of candidates should be their reward for being well led.

**Gold label** _(comment_id=36433169)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 183. [2022-02] predicted=`accelerationist`  (doomer=0.11 accel=0.78 neutral=0.11)

_Story:_ Education Department Forgives $415M of For-Profit College Debt

_Comment:_ education department forgives $415m of for-profit college debt it’s important to note that the age at which one accepts the massive financial burden of university is around 17 years old or even younger. so you aren’t even legally considered an adult. at the same time, you likely have most people in authority positions in your life trying to get you to go to college. so whether or not it’s a poor choice doesn’t really matter. the impact of that choice is really too difficult to understand until later in life, at which point it’s too late. the end result, and really the only thing that matters,…

**Gold label** _(comment_id=30377278)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 184. [2023-03] predicted=`doomer`  (doomer=0.92 accel=0.01 neutral=0.07)

_Story:_ Pause Giant AI Experiments: An Open Letter

_Comment:_ pause giant ai experiments: an open letter this analysis is completely fact-free. "a manhattan project on ai alignment, if started now, might still succeed in time. therefore, the compliance between parties needs not be long-term, which is indeed unlikely to happen." on what grounds do you base this? you have 3 hypotheticals stacked one on top of the other: 1) ai alignment is possible 2) ai alignment is a specific project that may be accomplished before [bad thing happens] if we start now 3) solving ai alignment is an actual problem and not just dumb extrapolation from science fiction each of…

**Gold label** _(comment_id=35368125)_:

  - [ ] doomer
  - [x] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 185. [2022-05] predicted=`neutral`  (doomer=0.06 accel=0.06 neutral=0.88)

_Story:_ Master’s Degree in Computer Science

_Comment:_ master’s degree in computer science the only time i did group work was for the deep learning class (2-4 people) and my group members were excellent. other than that one, no group work for me. the key is to pick classes that are hard, and form groups early. people that reach out earlier usually have their shit together.

**Gold label** _(comment_id=31281146)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 186. [2023-04] predicted=`neutral`  (doomer=0.03 accel=0.02 neutral=0.94)

_Story:_ Google DeepMind

_Comment:_ google deepmind flax, a big neural network jax library, is developed and used by brain. tf will stay around for boilerplate / data-loading, but jax support probably isn’t going anywhere.

**Gold label** _(comment_id=35654859)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 187. [2022-03] predicted=`neutral`  (doomer=0.04 accel=0.04 neutral=0.92)

_Story:_ Marginalia Search: 1 Year

_Comment:_ marginalia search: 1 year apparently, if you omit all the we-got-you-and-lock-you-in-your-ad-induced-information-bubble, you can get quite far with even modest hardware: https://memex.marginalia.nu/projects/gemini-server.gmi > i put the machine together mostly for a search engine, because i didn't want an actual rack making noise and heat in my living room, the server is made out of consumer hardware: > ryzen 9 3900x > 128 gb ram > 4x4 gb ironwolf zfs > a bunch of ssds index lookups

**Gold label** _(comment_id=30828475)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 188. [2022-10] predicted=`neutral`  (doomer=0.06 accel=0.05 neutral=0.89)

_Story:_ OpenAI, Valued at Nearly $20B, in Talks with Microsoft for More Funding

_Comment:_ openai, valued at nearly $20b, in talks with microsoft for more funding why is this seen as such a high valuation?! 1) openai got $1b to burn on cloud compute and they did that. so they obviously need a big raise for more compute. 2) stability is looking to raise at a $1b valuation, so clearly openai must be worth at least 10x. 3) openai has grown their brand immensely during the pandemic and now a recession. so clearly the whole team is outperforming. 4) there are tons of people in the yc community who will think gdb and sama are solidly worth 10 figures for what they’ve done here. so doesn’t…

**Gold label** _(comment_id=33284145)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 189. [2024-05] predicted=`doomer`  (doomer=0.55 accel=0.03 neutral=0.41)

_Story:_ Jan Leike Resigns from OpenAI

_Comment:_ jan leike resigns from openai jan and ilya were the leads of the superalignment team set up in july of 2023. https://openai.com/index/introducing-superalignment/ "our goal is to solve the core technical challenges of superintelligence alignment in four years. while this is an incredibly ambitious goal and we’re not guaranteed to succeed, we are optimistic that a focused, concerted effort can solve this problem:c there are many ideas that have shown promise in preliminary experiments, we have increasingly useful metrics for progress, and we can use today’s models to study many of these problems…

**Gold label** _(comment_id=40363303)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 190. [2023-04] predicted=`doomer`  (doomer=0.59 accel=0.08 neutral=0.33)

_Story:_ PatternFly: An open source design system

_Comment:_ patternfly: an open source design system my own issue with these is that they handle excessive input by horizontal scrolling, which can only be considered a solution by someone who prioritizes the consistency/alignment of their layout over usability (a truly villainous prioritization)

**Gold label** _(comment_id=35490952)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 191. [2024-01] predicted=`doomer`  (doomer=0.86 accel=0.04 neutral=0.10)

_Story:_ I moved my blog from IPFS to a server

_Comment:_ i moved my blog from ipfs to a server for incentive alignment, consensus, trustless, etc

**Gold label** _(comment_id=39210401)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 192. [2023-01] predicted=`doomer`  (doomer=0.74 accel=0.04 neutral=0.23)

_Story:_ Big Tech was moving cautiously on AI. Then came ChatGPT

_Comment:_ big tech was moving cautiously on ai. then came chatgpt > pearl clutching journos are of critical importance if you don't want to be shuttered before you get started. > there seems to be a large contingent of people who thinks this technology can be made safe. it can't be. its development also can't be stopped. the most optimistic estimates i've heard from actual ai alignment researchers are less than a 50% of ai alignment being understood in time for us to not all be killed by an ai that, one way or another, has been given too much power. the pessimists are people like yudkowsky saying we're…

**Gold label** _(comment_id=34562176)_:

  - [x] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [ ] wrong_other

---

## 193. [2024-05] predicted=`doomer`  (doomer=0.58 accel=0.04 neutral=0.38)

_Story:_ Big tech has distracted world from existential risk of AI, says top scientist

_Comment:_ big tech has distracted world from existential risk of ai, says top scientist it's a submarine article from the ea and uk+sk govt backed ai safety conference

**Gold label** _(comment_id=40475783)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 194. [2024-06] predicted=`accelerationist`  (doomer=0.06 accel=0.67 neutral=0.27)

_Story:_ Inequality Without Class

_Comment:_ inequality without class i think it's abundance in one's material conditions. that's not technology. technology is knowledge. that's completely different.

**Gold label** _(comment_id=40559277)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 195. [2022-11] predicted=`accelerationist`  (doomer=0.17 accel=0.42 neutral=0.40)

_Story:_ I don't understand why we throw away perfectly working things

_Comment:_ i don't understand why we throw away perfectly working things i have committed to not buying anything new. almost everything i have, aside from gifts i receive from people who overlook my preference, is second-hand. it is called freeganism, and it helps me feel less complicit in the shaving down of our own biome into things which are thrown away. in a country with massive abundance, there is more than enough secondhand stuff to go around. i wish it to become less acceptable (or more workaroundable) for devices like apple's to become locked forever just because their owner has locked them. i al…

**Gold label** _(comment_id=33495419)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 196. [2024-06] predicted=`neutral`  (doomer=0.07 accel=0.05 neutral=0.88)

_Story:_ OpenAI, Anthropic ignoring rule that prevents bots scraping online content

_Comment:_ openai, anthropic ignoring rule that prevents bots scraping online content > the world's top two ai startups are ignoring requests by media publishers to stop scraping their web content for free model training data, business insider has learned. especially with the rise of seo/genai spam content, i kind of wish media had more rigor on citing claims - rather than leaving them as bare assertions - ideally so that someone could follow the chain all the way back and see the actual evidence giving rise to (and hopefully substantiating) the claim. is this from first-hand investigation where you coul…

**Gold label** _(comment_id=40760257)_:

  - [ ] doomer
  - [ ] accelerationist
  - [x] neutral
  - [ ] wrong_other

---

## 197. [2022-06] predicted=`accelerationist`  (doomer=0.12 accel=0.55 neutral=0.33)

_Story:_ The farmers restoring Hawaii’s ancient food forests that once fed an island

_Comment:_ the farmers restoring hawaii’s ancient food forests that once fed an island > modern agriculture has created the most amazing abundance the world has ever seen the apparent cornucopia that is the modern supermarket is in fact a huge diesel engine that runs 24/7, achieving high outputs at the price of the atmosphere, land cover, biodiversity of flora and fauna, and so on pp. not that ancient man had no influence or only desirable influence on their land, or that some cultures (e.g. mesoamerican ones) were not after centuries at a local point-of-no-return in terms of land use. but stating that o…

**Gold label** _(comment_id=31874051)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 198. [2024-01] predicted=`doomer`  (doomer=0.72 accel=0.08 neutral=0.19)

_Story:_ 2020s anti-LGBT movement in the United States

_Comment:_ 2020s anti-lgbt movement in the united states its gotten worse as egotistic sudo-intellectuals have taken over and revert any proper changes even when properly source because it conflicts with their personal beliefs. like colleges information is being limited by political alignment.

**Gold label** _(comment_id=39146423)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 199. [2023-11] predicted=`accelerationist`  (doomer=0.17 accel=0.46 neutral=0.37)

_Story:_ Apple to pause advertising on X after Musk backs antisemitic post

_Comment:_ apple to pause advertising on x after musk backs antisemitic post the issue of critical race theory (crt) in schools has been a subject of intense controversy and public debate for several years and many states have banned it already. many states have legislated against it. there is an abundance of legal documentation you can read to find out why.

**Gold label** _(comment_id=38312164)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---

## 200. [2023-08] predicted=`doomer`  (doomer=0.69 accel=0.07 neutral=0.24)

_Story:_ GCC always assumes aligned pointer accesses (2020)

_Comment:_ gcc always assumes aligned pointer accesses (2020) they are confused, and seem not to realize that abis exist, and often specify alignment requirements. they seem to believe there are just isa and architecture specs. when you compile for linux x86_64 abi, gcc assumes that the stack is 16 byte aligned because it’s required by the abi. regardless of whether the isa needs it. if they want the compiler to make no assumptions about aligned accesses, they would need to define an abi in gcc that operates that way and compile.with it. they were historically supported (though its been years since i loo…

**Gold label** _(comment_id=37200862)_:

  - [ ] doomer
  - [ ] accelerationist
  - [ ] neutral
  - [x] wrong_other

---
