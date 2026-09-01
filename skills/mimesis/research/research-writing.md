# Detecting AI-Written Text in 2026: Beyond the Basics

*Research compiled June 2026. All publication dates noted inline.*

***

## Executive Overview

This report focuses exclusively on the four advanced dimensions of AI-text detection that are poorly covered in introductory listicles: model-specific tells for the newest frontier systems (GPT-5.x, Claude Opus 4.x, Gemini 3.x); signals that survive a competent humanisation pass and why; statistical and stylometric detection methods beyond burstiness and perplexity; and documented false-positive patterns that wrongly flag human writers. Primary sources — peer-reviewed papers, arXiv preprints, and vendor technical write-ups — are prioritised throughout.

***

## Part 1: Model-Specific Tells for the GPT-5.x / Opus 4.x / Gemini 3.x Era

### The Fundamental Shift from GPT-4o

The most important diagnostic update for 2025–2026 is that the tells have *diverged* across frontier models rather than converging. A May 2026 arXiv paper (Maier, Zaiss & Bayer, arXiv:2605.02620, submitted 4 May 2026) ran a detection arms-race experiment using LUAR-MUD authorship embeddings and found that detection of **GPT-5.5 is largely a length confound** — length alone achieves an AUC of 0.880 out of a full-model AUC of 0.931 — while **detection of Claude Opus 4.7 is a genuine stylistic signature**: length alone achieves only 0.517 AUC out of 0.952. In plain terms, GPT-5.5 is detectable mainly because its outputs cluster at characteristic lengths for a given prompt; Opus 4.7 leaves a real stylistic fingerprint that is independent of length.[^1]

This asymmetry is actionable. An analyst evaluating a suspected GPT-5.x passage should ask: does the response length feel calibrated to some implicit default rather than to the actual information need? GPT-5.5 in the Maier et al. study had 324/324 drafts fall within the 100–200 word range when given that instruction — it normalises output length aggressively. Opus 4.7 is less length-uniform but carries a more persistent lexical and syntactic fingerprint.[^1]

### Claude Opus 4.x Specific Tells

Cross-LLM transfer in the same study gives another diagnostic: a classifier trained only on Opus 4.7 data achieves AUC 0.913 when tested on GPT-5.5 data, and vice versa (0.888), confirming a **generic frontier-LLM signature** that both models share. But Opus has its own additional signature. The stylistic fingerprint of Claude Opus 4.x output survives even after a human post-editor has reworked a draft: the Maier et al. study showed that human post-editing of Opus mimics moved the LUAR embedding similarity closer to the human ceiling by only 24% of the remaining gap, while the raw Opus draft already closed 71–75%.[^1]

Qualitatively, independent model evaluations identify a cluster of Opus-specific tendencies that differ from GPT-4o-era defaults:[^2]
- **Calibrated epistemic hedging at the sentence level**: Opus 4.5 and later are trained to modulate booster/hedge density contextually. Corpus-based analysis (Ahmed, *Journal of English Studies in Arabia Felix*, Dec 2025) found that AI educational text exhibits a hedge-to-booster ratio that "far exceeds patterns documented in human pedagogical discourse," with overgenerated hedges in foundational content that "calls for assertive instructional guidance". The signal is not hedging per se but *contextually inappropriate hedging density* — confident assertions where human writers would simply assert, paired with hedging where human writers are typically bold.[^3]
- **Explicit reasoning traces in non-reasoning contexts**: Prompting documentation for Opus 4.7 states the model has outgrown explicit step-by-step scaffolding and "the reasoning still happens but the model no longer performs it for the audience". Raw Opus output without prompt engineering tends to externalise metacognitive self-monitoring ("This is a complex question requiring…", "There are several ways to approach…") as residue from earlier training stages.[^2]
- **Structural deference to the prompt**: Anthropic's own prompting guidance for Opus 4.5 and later notes that unspecified-context requests default to "the polished, hedged, marketing-shaped voice it was trained on, because that is the safest output across the widest range of unspecified contexts". The practical tell is formatting and structure that mirrors the implied audience of the prompt, not the actual human writer's habitual register.[^2]

### GPT-5.x Specific Tells

GPT-5.x models (5.1, 5.2, 5.5) are characterised by stylistic diversity benchmarks that rank them above competitors: in a September 2025 comparative analysis by Lech Mazur (posted Sept 2025), "GPT 5.x models are still the leaders in stylistic diversity". This is the double-edged result: GPT-5.5 is harder to catch by pattern-matching because it is more variable, but it retains the **length-normalisation tell** and a cross-model frontier signature.[^4]

There is also an emerging Pangram Labs observation (published May 2026) that detection of GPT-5.x class models is shifting toward **semantic-level analysis** rather than surface features: "nuanced contextual analysis and genre awareness… are elevating AI content detection well beyond statistical fingerprints". The implication is that GPT-5.x text reads as topically complete but semantically thin — it covers the territory of the prompt without the selective emphasis a human writer would use when writing from actual experience or conviction.[^5]

### Gemini 3.x Specific Tells

Gemini 3.x (Pro, Deep Think) outputs carry a specific provenance signal unavailable in other models: **SynthID-Text watermarking** is embedded in all Google Gemini text outputs, applied to approximately 100% of new generations. SynthID is a logits processor that augments token probabilities using a pseudorandom g-function, embedding watermark information in the statistical distribution of tokens without significantly affecting text quality. Detection requires access to Google's detector, but the watermark's existence is a hard technical tell absent in Anthropic and OpenAI outputs.[^6][^7]

The robustness caveat is important: SynthID-Text is vulnerable to paraphrasing. The DAMAGE paper (Masrour, Emi & Spero, Pangram Labs, arXiv:2501.03437, Jan 2025) demonstrated that DIPPER paraphrasing drops SynthID watermark detection TPR from 87.6% to 5.4% at FPR=5%. A SynGuard framework (Han et al., arXiv:2508.20228, Aug 2025) combining semantic-level and probabilistic watermarking improves average F1 score by 11.1% across attack scenarios, but remains imperfect.[^8][^9]

***

## Part 2: Tells That Survive a Humanisation Pass — and Why

### What Humanisers Actually Do

The DAMAGE paper by Masrour, Emi & Spero (Pangram Labs, COLING GenAIDetect workshop, Jan 2025) is the most rigorous audit of humanisation tools to date. Studying 19 tools including BypassGPT, StealthGPT, Undetectable AI, and academic paraphrasers, it categorised them into three tiers:[^10]
- **L1 (best)**: LLM-based, preserve tone, vocabulary level, and complexity; achieve fluency win rates around 26% vs. original text
- **L2 (medium)**: Degrade overall quality but preserve intent
- **L3 (poor)**: Insert nonsensical phrases, hallucinated citations, in-line comments, and garbled constructions[^8]

The key finding is that **humanisers degrade text quality on every tier** — L1 humanisers win only 26% of GPT-4o pairwise fluency judgements against the original AI text. The tells that survive humanisation are precisely those signals that humanisers cannot remove without also damaging semantic coherence.[^8]

### Tells That Survive and Why

**1. Deep semantic-structural coherence patterns (discourse-level)**
The GL-CLiC framework (Adi et al., IJCNLP 2025, Dec 2025) detects AI text using global and local coherence signals and CEFR-based vocabulary sophistication. AI text has characteristically uniform local coherence: each sentence connects to its neighbours in predictable, low-variance ways. Human writing has topic drift, pronoun antecedent retrieval that spans paragraphs, and argument structures that are non-linear. Humanisers operating at the sentence or phrase level cannot reconstruct this discourse-level topology because they do not have enough context to rewrite macro-structure.[^11]

**2. Intrinsic dimensionality of embedding manifold**
Tulchinskii et al. (arXiv:2306.04723, NeurIPS 2023, still heavily cited in 2025–2026 work) showed that human-written text has an average intrinsic dimensionality of approximately 9 for alphabet-based languages and 7 for Chinese, while AI-generated text is approximately 1.5 lower. This geometric property is computed from the topology of hidden-state embeddings across sentences and is invariant over text domains and human writer proficiency levels. A follow-up (arXiv:2511.15210, Nov 2025) confirmed the method extends from academic abstracts to social media. Surface-level humanisers cannot alter the geometric structure of what a model considers a plausible text manifold.[^12][^13]

**3. Surprisal-based diversity (rhythmic unpredictability)**
The DivEye framework (Basani & Pin-Yu Chen, arXiv:2509.18880, IBM Research, Sep 2025; accepted ICML 2026) moves beyond perplexity-as-average to measure *how unpredictability fluctuates* across a text. Human writing has higher variance in surprisal — the lexical and syntactic unpredictability jumps and falls in a recognisably irregular rhythm. AI-generated text, even high-quality output, maintains surprisal within a narrower band. DivEye outperforms zero-shot detectors by up to 33.2% and boosts existing detectors by up to 18.7% as an auxiliary signal. Crucially, it is robust to paraphrasing attacks because paraphrasing redistributes words but does not generally alter the rhythmic structure of where surprisal peaks occur.[^14][^15]

**4. Cross-model stylistic signature (LUAR embedding direction)**
The Maier et al. (arXiv:2605.02620, May 2026) cross-LLM transfer result (AUC 0.91 when training on one frontier LLM and testing on another) confirms that **frontier LLMs share a latent stylistic space** that human text does not inhabit in the same way. A humaniser that is itself a large language model (which most L1 humanisers are) will simply replace one LLM's signature with another's, often remaining in the same region of LUAR space. The DAMAGE study confirmed this: even after adversarial fine-tuning of a humaniser against their specific detector, the DAMAGE model still detected 93.2% of humanised AI samples.[^1][^8]

**5. Trigram-cosine stylometric delta**
Salnikov & Bonch-Osmolovskaya (*Journal of Language and Education*, Sep 2025) showed that trigram-cosine delta — measuring discourse-level stylistic cohesion through character-trigram patterns — achieves an Adjusted Rand Index of ~0.70 for human vs. LLM separation, significantly outperforming both unigram delta (ARI ~0.53) and finetuned transformer baselines (ARI ~0.28). Trigrams capture co-articulation patterns in writing at the character level that are highly individual and not altered by synonym substitution or paraphrasing.[^16]

**6. Adversarial paraphrasing ironically increases some detection signals**
Cheng et al. (arXiv:2506.07001, NeurIPS 2025) found a counterintuitive result: simple paraphrasing **increases** the true-positive rate on some detectors — by +8.57% on RADAR and +15.03% on Fast-DetectGPT. Simple paraphrase tools introduce phrasing that is statistically more unusual relative to the scoring model, which some detectors interpret as AI-trying-to-look-human. Only adversarial paraphrasing guided by the detector's own signal achieves reliable evasion.[^17]

### What Temperature Does

A critical vulnerability in perplexity-based detectors is exposed by TempParaphraser (Huang et al., EMNLP 2025, Nov 2025): **increasing sampling temperature dramatically reduces detection accuracy**. High-temperature sampling increases token unpredictability, pushing text toward the human distribution on perplexity-based scores. TempParaphraser simulates this by generating multiple normal-temperature outputs and selecting high-perplexity variants, reducing detector accuracy by an average of 82.5% while preserving text quality. However, temperature manipulation does not alter intrinsic dimensionality or surprisal-variance tells, which is why those signals are more robust.[^18][^19]

***

## Part 3: Statistical and Stylometric Signals Beyond Burstiness and Perplexity

The following signals are actively used by current detectors — commercial and research — and go beyond the GPT-4o-era standard.

### Token-Probability Neighbourhood: Binoculars and Cross-Perplexity

**Binoculars** (Hans et al., ICML 2024; still a top performer on RAID benchmark) uses the ratio of a scorer model's perplexity to an observer model's perplexity — what the authors call "cross-perplexity" or the "foil model" ratio. The insight is that if text was generated by an LLM, a *different* LLM that shares training data overlap will assign similar log-probabilities; human text will show a larger divergence between the two models' assessments. On RAID, Binoculars performed "impressively well across models even at extremely low false positive rates". Against humanised text, however, Binoculars drops from 94.15% TPR to 28.23% TPR at FPR=5%.[^20][^21][^8]

### DNA-DetectLLM: Mutation-Repair Signal

DNA-DetectLLM (Zhu et al., arXiv:2509.15550, NeurIPS 2025 spotlight, Sep 2025) takes a different approach: it constructs an "ideal AI-generated sequence" for each input, iteratively repairs non-optimal tokens, and quantifies the cumulative repair effort as a detection signal. Human-written text requires more repair to reach optimal LLM-likelihood; AI text is already near-optimal. The method achieves relative improvements of 5.55% in AUROC and 2.08% in F1 across public benchmarks compared to Binoculars, Fast-DetectGPT, and Lastde++.[^22]

### Stylometric Feature Sets (31-Feature Psycholinguistic Framework)

The Opara framework (arXiv:2505.01800, May 2025) maps 31 stylometric features to cognitive processes including lexical retrieval, discourse planning, cognitive load management, and metacognitive self-monitoring. The most diagnostically powerful features are:[^23]

| Feature Cluster | Cognitive Anchor | AI Signal |
|---|---|---|
| Function word unigrams | Automatic grammar | AI overuses certain function words; humans vary by register |
| POS bigrams | Syntactic planning | AI favours noun-heavy, passive constructions |
| Phrase patterns | Discourse planning | AI shows stereotyped clause-connective patterns |
| Type-token ratio (TTR) | Lexical retrieval | AI uses ~4x fewer unique words than humans per passage[^24] |
| Hedge-to-booster ratio | Epistemic stance | AI overhedges in assertive contexts[^3] |
| Average sentence length variance | Cognitive load | Human text has greater variance; AI shows lower SD |

Zaitsu (PLoS ONE, Oct 2025) confirmed in a Japanese-language study that function word unigrams, POS bigrams, and phrase patterns are the three most effective stylometric features for AI detection, with stylometry successfully distinguishing human from LLM text even when human judges failed.[^25][^26]

### NEULIF: Lightweight Stylometric + Readability CNN

Aityan et al. (arXiv:2511.21744, Nov 2025, revised Jan 2026) introduce NEULIF: decomposing text into stylometric and readability features, then classifying with a compact CNN or Random Forest. On the Kaggle AI vs. Human corpus, CNN achieves 97% accuracy and ROC-AUC of 99.5%; the Random Forest achieves 95% accuracy and ROC-AUC of 95%. The models are 25 MB and 10.6 MB respectively, running on CPU without GPU. The readability features used include Flesch-Kincaid, Gunning-Fog, and SMOG indices — AI text systematically overshoots optimal readability scores for its claimed audience.[^27]

### Authorship Embedding: LUAR-MUD

LUAR-MUD (Learning Universal Authorship Representations) is a frozen 512-dimensional contrastive embedding trained on Reddit to map text to an authorial style vector. It is the metric used in the Maier et al. arms-race study. The key property for detection is that LLM outputs cluster distinctively in LUAR space — even when an LLM is shown a single-sample demonstration of the target author's style, its outputs occupy a different region of the embedding manifold than the author's natural writing. A linear SVM on LUAR embeddings with leave-authors-out cross-validation achieves AUC 0.952 for Opus 4.7 and 0.931 for GPT-5.5 in a realistic held-out protocol.[^28][^1]

### BBN-U.Oregon ALERT: Ensemble Authorship Style

Kandula et al. (COLING GenAIDetect 2025, Jan 2025) present ALERT, an ensemble authorship-attribution system using hard positive/negative mining strategies across two complementary stylistic embedding subsystems. On the RAID benchmark, ALERT achieves 91.8% TPR at FPR=5% on standard test sets and 82.6% on adversarial sets, showing reasonable cross-domain robustness.[^29]

### Surprisal Variance (DivEye)

As noted in Part 2, Basani & Chen's DivEye (arXiv:2509.18880, Sep 2025; accepted ICML 2026) captures surprisal-based diversity — the variance and higher-order statistics of token-level information content across the text. The key features include:[^15]
- **Surprisal standard deviation**: AI text shows lower SD in per-token surprisal
- **Inter-quartile range of surprisal**: Human text has heavier tails in surprisal distribution
- **Run-length of surprisal above/below threshold**: Human text has longer unbroken runs of surprising tokens (tangents, asides, personal references)

The interpretability aspect is significant: DivEye can point to which specific passages drove the detection score, making it more actionable than black-box classifiers.[^14]

### Watermarking: SynthID and Green-Token Methods

The ICLR 2025 workshop survey (Cao, arXiv:2504.03765, Apr 2025) categorises watermarking approaches as: zero-watermarking (feature extraction without insertion), linguistic watermarking (synonym substitution), steganographic, structural, and statistical. For text specifically:[^30]

- **SynthID-Text** (Google DeepMind, deployed in all Gemini outputs) embeds a watermark via a pseudorandom g-function applied as a logits processor, promoting or demoting token choices imperceptibly. Presenc.ai (May 2026) reports ~100% coverage in Gemini outputs.[^7][^6]
- **Green-token watermarking** (Kirchenbauer et al.) divides vocabulary into green/red tokens and biases generation toward green tokens; a statistical test on the fraction of green tokens detects the watermark.

Robustness limitations: SynthID-Text loses detectability sharply under paraphrasing. The SynGuard hybrid (Han et al., arXiv:2508.20228, Aug 2025) adds semantic-level watermarking to recover 11.1% F1 on average after attacks. Theoretical analysis of SynthID by Omidi et al. (ICLR 2026 submission, Sep 2025) proves the mean score function is "inherently vulnerable to increased tournament layers" and proposes a layer inflation attack.[^9][^31]

### Turnitin AI Bypasser Detection (Aug 2025)

In August 2025, Turnitin added detection of AI bypasser tool use, creating a category within its AI writing report for text that "may have been modified by an AI bypasser tool". The technical method is not fully disclosed but is consistent with the DAMAGE approach of training on humaniser-augmented data. In October 2025, Turnitin updated the model again "to improve recall while maintaining a low false positive rate".[^32]

***

## Part 4: Documented False-Positive Patterns

### The Structural Problem with All Detectors

A 2026 journal article (Tandfon, Jan 2026) frames the root problem as fundamental: "AI detection relies on unverifiable probabilistic estimates. Generative AI detectors cannot be tested in real-world conditions where the true origin of a text is unknown." Vendors' accuracy claims are made on benchmark datasets; real-world performance diverges substantially. A Washington Post study found Turnitin's then-stated <1% false positive rate was actually closer to 50% in their sample, though sample size was small. Turnitin's own calibration trades false positives against false negatives: "We're comfortable with that [false negative rate] since we do not want to highlight human-written text as AI text".[^33][^34][^35]

GPTZero, the current benchmark leader on RAID (detecting 95.7% of AI texts at a 1% human false positive rate), drops to 60% detection on humanised AI text against the 1% FPR threshold, revealing how benchmark performance diverges from adversarial real-world conditions.[^36][^8]

### Non-Native English Speakers (ESL/EFL)

The most extensively documented false-positive pattern, replicated across multiple studies:

- **Stanford/Zou et al. (2023, still foundational)**: Seven AI detectors classified over 61.22% of TOEFL essays written by non-native English students as AI-generated; 89 of 91 TOEFL essays were flagged by at least one detector; 19% were unanimously flagged by all seven.[^37]
- **Mechanism**: Detectors score on perplexity. Non-native speakers score lower on lexical richness, lexical diversity, syntactic complexity, and grammatical complexity — the same dimensions on which AI scores low.[^37]
- **2025 replication**: A PeerJ Computer Science study (EurekaAlert, Jun 2025) confirmed that "the most accurate tool in this study showed the strongest bias against certain groups of authors and academic disciplines". Non-native English speakers face disproportionately higher false positive rates.[^38]
- **2026 academic note**: A Reddit thread (r/Professors, Mar 2026) documented an emerging secondary false positive from students deliberately writing worse to avoid detection flags — the ironic outcome of over-reliance on detectors.[^39]

Hastewire (Jan 2026) independently confirmed that ESL and EFL writers face higher false positive rates due to "reliance on repeated phrases, terms, and words" — patterns the detectors associate with AI.[^40]

### Neurodivergent Writers

ADHD, autism, and dyslexic students are flagged at higher rates than neurotypical native English speakers. The mechanism is similar to ESL: neurodivergent writers often rely on repeated phrases, formulaic constructions, and patterns that reduce cognitive processing load — the same statistical regularities that detectors interpret as low-perplexity AI output.[^34]

### Formally Trained, High-Achieving, and Well-Edited Human Writers

A significant class of false positives hits exactly the writers who are doing what academic writing instruction demands:

- **Formal academic style**: "Essays that are grammatically correct, logically organised, and written in a neutral academic tone are likely to be flagged". The very qualities instructors reward in marking criteria — topic sentences, consistent structure, clear transitions — are the same features that low-temperature AI output and well-trained human academic writers share.[^41]
- **Heavy editing and proofreading**: "Heavy editing, grammar checking, rewriting or paraphrasing for clarity can smooth out natural inconsistencies. AI detectors associate this perfection with AI use".[^41]
- **Grammar-assisted writing**: A documented case showed a student whose work was flagged not because they used an AI generator but because Google Docs' built-in grammar checker cleaned their text sufficiently to reduce its apparent burstiness.[^42]
- **Predictable structure**: Standard academic essay structure (introduction, body paragraphs, conclusion) is predictable; detectors "associate this predictability with AI output, even though it is standard academic practice".[^41]

The Analytica dimension is also documented: writing instructors at LinkedIn (Jan 2026) note that "the linguistic features that drive a high Analytic score [high syntactic complexity, low narrative] are the same features that modern AI detectors often flag as AI-like".[^43]

### Historically Formal or Literary Texts

AI detection tools have infamously flagged the US Constitution, sections of the Bible, and Victorian-era writing as AI-generated — a reductio ad absurdum demonstrating that low-perplexity, highly-structured prose predates LLMs by centuries.[^44]

### Domain-Specific Writing

The PeerJ Computer Science study (Jun 2025) found that "AI-assisted writing, where human text is enhanced by language models for improved readability, presents particular challenges for detection systems". Science abstracts written in highly constrained academic register are harder to distinguish from AI because the genre itself imposes low-variance sentence structure. The peer-review fraud detection literature (Nature, May 2026) found AI tools identifying template-like peer reviews, but template use predates LLMs.[^45][^38]

### The Benchmark Quality Problem

Gritsai et al. (arXiv:2410.14677, presented AAAI 2025) showed that "the quality of detectors tends to drop dramatically in the wild," raising the question of whether high benchmark scores (up to 99.9%) come from "poor quality of evaluation datasets" rather than true generalisability. The RAID benchmark (6.2 million records, 11 domains, 12 adversarial attacks) is the most rigorous current evaluation; GPTZero achieved top ranking against it, but even RAID's adversarial sets do not cover all in-the-wild humanisation techniques.[^46][^36]

***

## Part 5: Select Peer-Reviewed and arXiv Work, Last 12 Months

The following table summarises key primary sources cited in this report, ordered by publication date.

| Paper | Authors | Venue / Date | Key Contribution |
|---|---|---|---|
| DAMAGE: Detecting Adversarially Modified AI Generated Text | Masrour, Emi, Spero (Pangram Labs) | COLING GenAIDetect, Jan 2025 [arXiv:2501.03437] | Audit of 19 humanisers; DAMAGE detector robust to humanisation (98.26% TPR @ 5% FPR); SynthID watermark stripped by DIPPER |
| Detecting AI-Generated Text: Factors Influencing Detectability | Fraser, Dawkins, Kiritchenko | JAIR v82 (Apr 2025 revision) [arXiv:2406.15583] | Survey of SOTA approaches; watermarking, statistical, stylometric, ML classification |
| Distinguishing AI-Generated/Human Text via Psycholinguistic Analysis | Opara | arXiv:2505.01800, May 2025 | 31-feature psycholinguistic framework mapping stylometric features to cognitive processes |
| AI-generated Text Detection: Multifaceted Approach | Abburi et al. | arXiv:2505.11550, May 2025 (AAAI DefActify) | Neural architectures for binary (F1=0.994) and multiclass attribution (F1=0.627) |
| Adversarial Paraphrasing: Universal Attack for Humanizing AI Text | Cheng et al. | NeurIPS 2025 [arXiv:2506.07001] | Adversarial paraphrasing guided by detector signal reduces T@1%F by avg 87.88% across detector types |
| Stylometry recognizes human/LLM texts in short samples | [Multiple authors] | arXiv:2507.00838, Jul 2025 | Stylometry effective even in short samples; challenges assumption that short text is undetectable |
| Better Call Claude: LLMs Detect Changes of Writing Style? | [Authors] | arXiv:2508.00680, Aug 2025 | LLM-based style change detection |
| Robustness Assessment of Text Watermarking for SynthID | Han, Li, Ni, Zulkernine | arXiv:2508.20228, Aug 2025 | SynthID vulnerable to paraphrase; SynGuard hybrid improves F1 by 11.1% |
| DNA-DetectLLM: DNA-Inspired Mutation-Repair Detection | Zhu et al. | NeurIPS 2025 spotlight [arXiv:2509.15550] | Mutation-repair signal; +5.55% AUROC, +2.08% F1 over Binoculars/Fast-DetectGPT |
| Diversity Boosts AI-Generated Text Detection (DivEye) | Basani, Pin-Yu Chen | arXiv:2509.18880, Sep 2025; ICML 2026 | Surprisal-based diversity features; +33.2% over zero-shot detectors; robust to paraphrase |
| Detecting LLM Text with Trigram-Cosine Stylometric Delta | Salnikov, Bonch-Osmolovskaya | JLE 11(3), Sep 2025 | Trigram-cosine delta (ARI ~0.70) outperforms RuModernBERT baseline and unigram delta |
| Stylometry reveals AI authorship, humans struggle (Japanese) | Zaitsu | PLoS ONE, Oct 2025 | Function word unigrams, POS bigrams, phrase patterns most effective stylometric features |
| NEULIF: Lightweight AI Text Detection via Stylometry | Aityan, Claster et al. | arXiv:2511.21744, Nov 2025, rev Jan 2026 | CNN (97% accuracy, 99.5% AUC) and RF (95%, 95% AUC) on CPU; no GPU required |
| TempParaphraser: Heating Up Text to Evade Detection | Huang, Zhang, Su, Chen | EMNLP 2025, Nov 2025 | High-temperature paraphrasing reduces detection accuracy avg 82.5%; adversarial training improves robustness |
| GL-CLiC: Global-Local Coherence/Lexical Complexity for Sentence-Level Detection | Adi et al. | IJCNLP-AACL 2025, Dec 2025 | Discourse analysis and CEFR vocab sophistication for sentence-level detection |
| Corpus-Based Analysis of Epistemic Stance in AI Instructional Content | Ahmed | JESAF 4(2), Dec 2025 | AI texts show hedge-to-booster ratios far exceeding human pedagogical norms |
| On Google's LLM Watermarking System: Theoretical Analysis | Omidi, Dong, Wang | ICLR 2026 submission, Sep 2025 | Mean score function vulnerable; Bayesian score more robust; layer inflation attack |
| Heads We Win, Tails You Lose: AI Detectors in Education | [Authors] | *Higher Education* journal, Jan 2026 | AI detection violates procedural fairness; probabilistic estimates unverifiable |
| Beating the Style Detector: Three Hours of Agentic Research | Maier, Zaiss, Bayer | arXiv:2605.02620, May 2026 | GPT-5.5 detection mostly length confound; Opus 4.7 genuinely stylistic signature; adversarial agent shrinks margins |

***

## Synthesis: The 2026 Arms Race

The current state resolves into four concurrent dynamics:

**1. Model differentiation is outpacing universal tells.** GPT-5.5 and Opus 4.7 have substantially different detection profiles despite comparable stylistic quality. Analysts should apply model-specific heuristics where the source model is suspected, rather than looking for a universal signature.[^1]

**2. Humanisers are an arms race within the arms race.** DAMAGE-class detectors (trained on humaniser-augmented data) maintain 93–98% TPR against L1 humanisers, but adversarial paraphrasing guided by a detector's own signal achieves average 87.88% T@1%F reduction across multiple detector types. The detector-humaniser cycle is running faster than annual research publication can track.[^17][^10][^8]

**3. The most robust signals are the hardest to compute.** Intrinsic dimensionality, surprisal variance, LUAR authorship embeddings, and trigram-cosine delta all survive humanisation better than perplexity or burstiness — but none of them is a quick surface-level heuristic. The practical takeaway for a human analyst without access to these tools is to focus on discourse-level coherence (does the text have the selective emphasis and argument topology of someone with a specific stake in the question?) rather than word-level or sentence-level patterns.[^16][^12][^15][^1]

**4. False positives are a structural, not incidental, problem.** Every detector faces a precision-recall trade-off that disproportionately harms ESL writers, neurodivergent writers, formally trained writers, and writers who use editing tools. The education-integrity literature increasingly recommends treating detector output as one signal among many, never as evidence sufficient for sanction.[^35][^44][^38][^37]

***

*Report compiled from arXiv, ACL Anthology, PLoS ONE, Nature, Frontiers in Education, vendor technical documentation, and conference proceedings. All sources dated 2025–2026 unless noted as foundational prior work. Last verified June 2026.*

---

## References

1. [Beating the Style Detector: Three Hours of Agentic Research on the AI-Text Arms Race](https://arxiv.org/pdf/2605.02620v1.pdf)

2. [How to Prompt in 2026: 6 Habits to Drop for GPT-5.5 & Claude](https://mrprompts.substack.com/p/how-to-prompt-in-2026) - Six habits the new default models have outgrown. Six prompts to use instead. Real reasoning behind e...

3. [[PDF] A Corpus-Based Analysis of Epistemic Stance in AI-Generated ...](http://journals.arafa.org/index.php/jesaf/article/download/125/166) - Almulla (2025) compares hedging devices and engagement markers in AI-generated and human- written es...

4. [Lech Mazur](https://x.com/LechMazur/status/2001780814611427619)

5. [What Educators Should Know About AI Detection in 2026 - Copyleaks](https://copyleaks.com/blog/what-educators-should-know-about-ai-detection-in-2026) - Discover the top generative AI trends impacting classrooms in 2026 and how educators can stay ahead ...

6. [AI Content Watermarking Adoption 2026 | Presenc AI](https://presenc.ai/research/ai-content-watermarking-adoption-2026) - Adoption statistics for AI content watermarking and provenance standards in 2026: SynthID, C2PA Cont...

7. [SynthID: Tools for watermarking and detecting LLM-generated Text | Responsible Generative AI Toolkit | Google AI for Developers](https://ai.google.dev/responsible/docs/safeguards/synthid/)

8. [DAMAGE: Detecting Adversarially Modified AI Generated Text - arXiv](https://arxiv.org/html/2501.03437v1) - We present a deep-learning based AI detector that effectively is robust to humanization, even by hum...

9. [Robustness Assessment and Enhancement of Text Watermarking for Google's SynthID](https://www.arxiv.org/abs/2508.20228) - Recent advances in LLM watermarking methods such as SynthID-Text by Google DeepMind offer promising ...

10. [DAMAGE: Detecting Adversarially Modified AI Generated Text](https://aclanthology.org/2025.genaidetect-1.9/) - Finally, we demonstrate a robust model that can detect humanized AI text while maintaining a low fal...

11. [GL-CLiC: Global-Local Coherence and Lexical Complexity for ...](https://aclanthology.org/2025.ijcnlp-long.188/) - 2025. GL-CLiC: Global-Local Coherence and Lexical Complexity for Sentence-Level AI-Generated Text De...

12. [Intrinsic Dimension Estimation for Robust Detection of AI-Generated ...](https://arxiv.org/abs/2306.04723) - In this work, we propose such an invariant for human-written texts, namely the intrinsic dimensional...

13. [Unveiling Intrinsic Dimension of Texts: from Academic Abstract to ...](https://arxiv.org/html/2511.15210v1) - Intrinsic dimension (ID) is computed from the geometry of hidden representations and thus captures t...

14. [Diversity Boosts AI-Generated Text Detection - ICML 2026](https://icml.cc/virtual/2025/51028)

15. [[2509.18880] Diversity Boosts AI-Generated Text Detection](https://www.arxiv.org/abs/2509.18880) - Detecting AI-generated text is an increasing necessity to combat misuse of LLMs in education, busine...

16. [Detecting LLM-Generated Text with Trigram–Cosine Stylometric Delta](https://jle.hse.ru/article/view/22211) - Purpose: This study aims to advance text attribution research by introducing a stylometry-based appr...

17. [A Universal Attack for Humanizing AI-Generated Text - arXiv](https://arxiv.org/abs/2506.07001) - In this work, we introduce Adversarial Paraphrasing, a training-free attack framework that universal...

18. [“Heating Up” Text to Evade AI-Text Detection through Paraphrasing](https://aclanthology.org/2025.emnlp-main.1607/) - Junjie Huang, Ruiquan Zhang, Jinsong Su, Yidong Chen. Proceedings of the 2025 Conference on Empirica...

19. [TempParaphraser: “Heating Up” Text to Evade AI- ...](https://papers.cool/venue/2025.emnlp-main.1607@ACL) - The widespread adoption of large language models (LLMs) has increased the need for reliable AI-text ...

20. [These Are The Best Generative AI Text Detectors, According To A ...](https://www.mescomputing.com/news/4266140/best-generative-ai-text-detectors-study) - The study found that Binoculars performed "impressively well across models even at extremely low fal...

21. [[ICML 2024] Binoculars: Zero-Shot Detection of LLM-Generated Text](https://github.com/ahans30/Binoculars) - We introduce Binoculars, a state-of-the-art method for detecting AI-generated text. Binoculars is a ...

22. [DNA-DetectLLM: Unveiling AI-Generated Text via a DNA-Inspired...](https://openreview.net/forum?id=yQoHUijSHx) - Building on this perspective, we introduce DNA-DetectLLM, a zero-shot detection method for distingui...

23. [[2505.01800] Distinguishing AI-Generated and Human-Written Text ...](https://arxiv.org/abs/2505.01800) - This study proposes a comprehensive framework that integrates stylometric analysis with psycholingui...

24. [The Problem With Ai...](https://skylineacademic.com/blog/is-your-ai-generated-text-safe-real-facts-about-detection-tools-in-2025/) - Is Your AI Generated Text Safe? Real Facts About Detection Tools in 2025 AI generated text detection...

25. [Stylometry can reveal artificial intelligence authorship, but humans ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC12558491/) - In particular, three stylometric features (function word unigrams, POS bigrams, and phrase patterns)...

26. [Stylometry can reveal artificial intelligence authorship, but humans ...](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0335369) - The purpose of this study was to estimate the artificial intelligence (AI) detection potential using...

27. [A Lightweight Approach to Detection of AI-Generated Texts Using ...](https://arxiv.org/abs/2511.21744) - Abstract page for arXiv paper 2511.21744: A Lightweight Approach to Detection of AI-Generated Texts ...

28. [GitHub - LLNL/LUAR: Transformer-based model for learning authorship representations.](https://github.com/LLNL/LUAR) - Transformer-based model for learning authorship representations. - llnl/LUAR

29. [BBN-U.Oregon's ALERT system at GenAI Content Detection Task 3](https://aclanthology.org/2025.genaidetect-1.42/) - Hemanth Kandula, Chak Fai Li, Haoling Qiu, Damianos Karakos, Hieu Man, Thien Huu Nguyen, Brian Ulicn...

30. [Watermarking for AI Content Detection: A Review on Text, Visual, and Audio Modalities](https://arxiv.org/abs/2504.03765) - The rapid advancement of generative artificial intelligence (GenAI) has revolutionized content creat...

31. [on google's llm watermarking system: theoretical analysis ...](https://openreview.net/forum?id=4AfWqR3quK) - Google’s SynthID-Text, the first ever production-ready generative watermark system for large languag...

32. [AI writing detection model - Turnitin Guides](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) - The AI writing report now displays a submission's overall percentage of text detected as AI and a br...

33. [AI Detectors Vs Human Judgment: How Accurate Are They ...](https://skylineacademic.com/blog/ai-detectors-vs-human-judgment-how-accurate-are-they-really-2025-tests/) - AI Detectors vs Human Judgment: How Accurate Are They Really? [2025 Tests] Are AI detectors reliable...

34. [Generative AI Detection Tools: The Problems with AI Detectors ...](https://lawlibguides.sandiego.edu/c.php?g=1443311&p=10721367) - A guide for instructors on the use of generative AI detectors. This guide is not an endorsement of a...

35. [Full article: Heads we win, tails you lose: AI detectors in education](https://www.tandfonline.com/doi/full/10.1080/1360080X.2026.2622146) - Developers claim that AI detectors estimate the likelihood that a piece of writing was produced by g...

36. [Officially The Most Accurate Commercial AI Detector](https://gptzero.me/news/gptzero-accuracy-stats/) - GPTZero confirms its title as the most accurate commercial AI detector, outperforming competitors on...

37. [AI-Detectors Biased Against Non-Native English Writers | Stanford HAI](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers)

38. [New study reveals bias in AI text detection tools impacts academic ...](https://www.eurekalert.org/news-releases/1088750) - A study published in PeerJ Computer Science reveals significant accuracy-bias trade-offs in artifici...

39. [Students are deliberately writing worse to avoid AI detection flags ...](https://www.reddit.com/r/Professors/comments/1rjl5u0/students_are_deliberately_writing_worse_to_avoid/) - Stanford researchers (Liang et al., 2023) found that GPT detectors flagged over 61% of genuine essay...

40. [Study Reveals AI Detectors' False Positives on Non-Native ...](https://hastewire.com/blog/study-reveals-ai-detectors-false-positives-on-non-native-writers) - A groundbreaking study exposes AI detectors' false positives on non-native English writers, revealin...

41. [Can AI Detection Tools Reliably Identify ChatGPT in Academic ...](https://schoolofacademics.co.uk/can-ai-detection-tools-reliably-identify-chatgpt-in-academic-writing) - AI detection tools can flag essays as AI-generated and often misidentify well-written human work as ...

42. [ai detectors flagging student writing for being too good - Facebook](https://www.facebook.com/groups/698593531630485/posts/1420553836101114/) - AI plagiarism detectors have several limitations, including inaccuracy and an over-reliance on super...

43. [When Writing Well Looks Like AI: The Problem with AI Detectors](https://www.linkedin.com/pulse/when-writing-well-looks-like-ai-problem-detectors-ken-dafoe-aowuc) - The linguistic features that drive a high Analytic score are the same features that modern AI detect...

44. [Detecting AI-Generated Text: Things to Watch For](https://www.eastcentral.edu/free/ai-faculty-resources/detecting-ai-generated-text/) - AI-detection tools have infamously identified human-written documents like the US Constitution and p...

45. [First AI tool to detect suspicious peer reviews rolled out by ... - Nature](https://www.nature.com/articles/d41586-026-01454-3) - Artificial-intelligence tool spots copied peer reviews, helping to uncover fraud in academic publish...

46. [Are AI Detectors Good Enough? A Survey on Quality of Datasets ...](https://arxiv.org/abs/2410.14677) - The rapid development of autoregressive Large Language Models (LLMs) has significantly improved the ...

