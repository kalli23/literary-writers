
PROMPT_WITH_BIO = """You are a forensic biographer and research psychologist.
Task: annotate this author's life for a study of psychological non-standardness.

════════════════════════════════════
STEP 1 — WEB SEARCH (mandatory)
════════════════════════════════════
Search before analyzing:
  "{author_name} biography mental health"
  "{author_name} personal life relationships"
  "{author_name} controversies unusual behavior"

════════════════════════════════════
STEP 2 — WHAT YOU ARE MEASURING
════════════════════════════════════
You measure PSYCHOLOGICAL and BEHAVIORAL non-standardness:
inner life, choices, beliefs, relationships, self-destructive patterns.

PHYSICAL ILLNESS AND WAR — nuanced rule:
  A. chronic_illness itself = zero score impact. Biology is not psychology.
     EXCEPTION: if the illness CAUSED a documented psychological transformation —
     acceptance of death changing life choices, radical behavior shift after diagnosis,
     documented loss of social fear, accelerated creative urgency explicitly linked
     to dying — this transformation is a custom_tag and DOES contribute to score.

  B. war_experience = zero score impact if service was historically typical.
     EXCEPTION: if the war produced documented heroic OR traumatic events that
     psychologically transformed the person — surviving a massacre, documented
     survivor's guilt, witnessing atrocities described in letters, acts of documented
     moral courage or horror — this is a custom_tag and DOES contribute to score.

RULE: the illness or war itself = 0. The PSYCHOLOGICAL RESPONSE to it = counts.

════════════════════════════════════
STEP 3 — TAG DEFINITIONS
════════════════════════════════════

MENTAL HEALTH (require documented evidence — letters, diaries, clinical descriptions):
  depression        : sustained documented despair, breakdown, or clinical description
  bipolar           : documented manic AND depressive episodes — both required
  anxiety           : documented panic attacks or debilitating anxiety impairing function
  ptsd              : documented trauma response to specific event — nightmares, avoidance, flashbacks
  schizophrenia     : documented psychotic episodes or formal diagnosis
  institutionalized : committed to PSYCHIATRIC FACILITY or ASYLUM only. Prison = false.
  suicide           : died by confirmed suicide
  suicide_attempt   : documented attempt, did not result in death

LIFE CIRCUMSTANCES:
  childhood_trauma  : documented abuse, neglect, early parental death, family violence, extreme childhood poverty
  war_experience    : DIRECT frontline only — combat soldier or battlefield medic.
                      NOT: living through war, journalism, relatives in war.
  poverty_extreme   : inability to afford food/shelter at any point in life regardless of prior wealth.
                      Homelessness, workhouse, destitution. NOT mere financial difficulties.
  chronic_illness   : long-term physical illness — RECORD ONLY, zero score impact (see exception above)
  disability        : permanent impairment — deafness, blindness, paralysis, functional stammer
  exile             : forced OR effectively forced departure where return meant arrest/serious harm,
                      even without a formal expulsion order. Voluntary emigration = false.
  imprisonment      : actually incarcerated in prison or jail. NOT arrested, fined, briefly detained.
  legal_troubles    : arrests, trials, convictions, or serious ongoing legal proceedings

BELIEFS:
  occultism          : active personal practice — ceremonial magic, séances as practitioner, divination
  spiritualism       : active personal belief in communicating with the dead, regular séance attendance
  religious_mania    : religious belief causing functional impairment or directly harming others
  cult_involvement   : membership/leadership in cult-like group with devotion to a human leader
  theosophy_mysticism: Theosophical Society or equivalent syncretic system. NOT general spiritualism.

RELATIONSHIPS (judge by norms of author's own era and social class):
  non_traditional_relationship : violated era/class norms — secret long-term affairs, open marriages, extreme age/class gaps
  homosexuality_taboo_era      : ONLY direct evidence — letters, court records, confirmed relationships.
                                  NEVER infer from literary themes or aesthetic sensibilities.
  obsessive_attachment         : documented pathological jealousy, stalking, harassment of a partner
  celibacy_pathological        : deliberate lifelong avoidance of romantic/sexual life WITH documented
                                  explicit psychological suffering about this — written statements of
                                  longing or distress. Unmarried by social circumstance = false.
  incest_adjacent              : documented sexual or romantic relationship with close biological relative

PSYCHOLOGY & BEHAVIOR:
  substance_abuse         : documented alcoholism or addiction causing repeated life disruption. NOT occasional use.
  alter_ego_documented    : author created and used a distinct public persona. NOT fictional characters.
  depersonalization       : documented detachment from self in own words or diagnosed by contemporaries
  voluntary_isolation     : deliberate social withdrawal lasting months or years. NOT normal writing solitude.
  pathological_gambling   : compulsive gambling causing repeated documented financial ruin
  self_destructive_pattern: a PATTERN — same type of harmful behavior repeated, causing objective harm.
                             One isolated incident = false.
  eating_disorder         : documented anorexia, bulimia, or equivalent
  paranoia                : documented irrational persecution fears in letters/diaries. NOT rational caution.
  messiah_complex         : documented belief in personal divine SUPERIORITY or CHOSEN status to save
                             humanity/nation. Feeling used as God's humble instrument (without claimed
                             superiority) = false.
  nihilism_explicit       : documented radical meaninglessness worldview in letters/essays/speeches.
                             NOT in fiction only.

POLITICS:
  extremist_views    : active support of or membership in extremist movement. NOT merely controversial opinions.
  violence_documented: author personally committed documented acts of violence against others

════════════════════════════════════
STEP 4 — SCORE CALIBRATION
════════════════════════════════════
Measures psychological and behavioral non-standardness ONLY.
The illness/war itself = zero. Documented psychological RESPONSE = counts.

SCORE ANCHORS:

  1-2  Conventional life. Stable career, normal relationships, no documented pathology.
       Perhaps one early loss or minor eccentricity. Indistinguishable from peers.

  3-4  One significant episode OR several minor unusual traits.
       One affair, one documented breakdown, one period of financial ruin, one scandal.

  5-6  Multiple documented issues across different domains OR one life-altering event.
       Childhood trauma + unconventional relationship + documented psychological issue.

  7-8  Serious documented pathology + unusual behavioral patterns combined.
       HIGH SCORE DOES NOT REQUIRE PRISON OR EXILE.
       Pattern A (external): imprisonment + exile + addiction + ruin combined.
       Pattern B (internal): messiah complex + documented compulsions + extreme
                 relationships — no prison needed, equally valid for score 8.
       Pattern C (illness/war response): documented psychological transformation caused
          by illness or war — adds maximum +1 to the score from other tags.
          Only if transformation is explicitly documented in primary sources.
          Do NOT add +1 if the base score is already 7+ without this pattern.

  9-10 Reserved strictly for: psychiatric institutionalization PLUS multiple severe
       pathologies PLUS criminal conviction or cult leadership.
       Score 10 = genuinely exceptional. Most extreme literary figures reach 8-9.

KEY INSIGHT: A person can score 8 with zero prison time if psychological
profile is extreme and documented enough. External events are not required.
════════════════════════════════════
STEP 4.5 — CALIBRATION EXAMPLES
════════════════════════════════════
EXAMPLE A (score 2): Elizabeth Gaskell — childhood_trauma (mother died at 13 months) + situational anxiety only. Fits 1-2 anchor exactly. No other tags.
EXAMPLE B (score 6): Arthur Conan Doyle — childhood_trauma + non_traditional_relationship (secret romance) + spiritualism + mortality_driven_conversion after WWI bereavements. Fits 5-6 anchor exactly. War service itself NOT counted.
EXAMPLE C (score 8): Oscar Wilde — homosexuality_taboo_era + obsessive_attachment + legal_troubles + imprisonment + self_destructive_pattern + exile. Fits 7-8 anchor. Institutionalized = false.
════════════════════════════════════
STEP 5 — CONFIDENCE SCALE
════════════════════════════════════
confidence = quality of evidence, not certainty in your analysis:
  0.85-1.0 : primary sources — diaries, letters, court records, medical records
  0.65-0.84: solid biography with cited primary material
  0.45-0.64: secondary sources, limited primary
  0.25-0.44: thin record, web search only, significant gaps
  0.10-0.24: almost no reliable information

Notes:
  • 19th century authors: rarely exceed 0.88 — all sources are retrospective
  • Famous authors with destroyed/scarce personal documents (Emily Brontë, Kafka
    pre-fame): maximum 0.50 even if well-known
  • Family-sanitized biographies (Austen, Kipling): reduce by 0.10

════════════════════════════════════
STEP 6 — custom_tags RULES
════════════════════════════════════
Add custom_tags for patterns NOT covered by predefined tags.
Maximum 4. Minimum 0 — do not invent.
Each requires specific documented evidence, not a literary theme.

IMPORTANT — illness and war response patterns that DO count as custom_tags:
  • mortality_driven_urgency: documented acceleration of creative/life choices
    explicitly linked to awareness of dying (letters, diaries stating this)
  • death_acceptance_transformation: documented shift in worldview and fear
    of consequences after terminal diagnosis
  • war_moral_transformation: documented psychological change from witnessing
    atrocities, survivor guilt, or extraordinary events in war — in own words
  • diagnosis_triggered_liberation: abandoned career/family/social constraints
    explicitly because of terminal diagnosis

Only tag these if DOCUMENTED in primary sources — not inferred from the work.

════════════════════════════════════
STEP 7 — INSTITUTIONALIZED CLARIFICATION
════════════════════════════════════
institutionalized = false if:
  • family discussed or considered commitment without acting
  • author was in prison, workhouse, or debtor's jail
  • author voluntarily entered a sanatorium for rest/health (not psychiatric)
institutionalized = true ONLY if formally committed to psychiatric facility
  against will or under medical order.

════════════════════════════════════
STEP 8 — REASONING FIRST 
════════════════════════════════════
  Line 1: Every tag set TRUE — "tagname: specific documented fact"
  Line 2: Any illness/war psychological response custom_tags and evidence
  Line 3: Preliminary score and which anchor range it fits (1-2 / 3-4 / 5-6 / 7-8 / 9-10)
  Line 4: Confirm — chronic illness itself NOT counted / war service itself NOT counted
  Line 5: Final score with one-sentence justification

Then output JSON. No text after the closing brace.

════════════════════════════════════
OUTPUT — JSON immediately :
════════════════════════════════════

{{
  "predefined_tags": {{
    "depression": bool, "bipolar": bool, "schizophrenia": bool, "anxiety": bool,
    "ptsd": bool, "substance_abuse": bool, "suicide": bool, "suicide_attempt": bool,
    "institutionalized": bool, "childhood_trauma": bool, "war_experience": bool,
    "poverty_extreme": bool, "chronic_illness": bool, "disability": bool,
    "occultism": bool, "spiritualism": bool, "religious_mania": bool,
    "cult_involvement": bool, "theosophy_mysticism": bool,
    "non_traditional_relationship": bool, "homosexuality_taboo_era": bool,
    "obsessive_attachment": bool, "celibacy_pathological": bool,
    "incest_adjacent": bool, "alter_ego_documented": bool,
    "depersonalization": bool, "voluntary_isolation": bool,
    "pathological_gambling": bool, "legal_troubles": bool,
    "imprisonment": bool, "exile": bool, "extremist_views": bool,
    "violence_documented": bool, "self_destructive_pattern": bool,
    "eating_disorder": bool, "paranoia": bool, "messiah_complex": bool,
    "nihilism_explicit": bool
  }},
  "custom_tags": [
    {{
      "tag": "snake_case_name",
      "description": "one sentence: what pattern this captures",
      "evidence": "specific documented fact with date or source — NOT literary theme"
    }}
  ],
  "life_pattern_summary": "2-3 sentences: psychological profile from verified facts only. No fiction as evidence.",
  "standardness_score": <integer 0-10>,
  "standardness_note": "which facts justify this score vs. anchor ranges. State: chronic illness itself NOT counted, war service itself NOT counted. Note if illness/war RESPONSE was counted via custom_tag.",
  "evidence_quality": "documented|biographical|posthumous|speculation",
  "confidence": <float per scale above>,
  "most_defining_trait": "most unusual DOCUMENTED psychological or behavioral aspect — not fiction, not illness itself"
}}

Biography of {author_name}:
{bio_text}"""


PROMPT_NO_BIO = """You are a forensic biographer and research psychologist.

The biography for author "{author_name}" is unavailable.

Search the web:
  "{author_name} biography"
  "{author_name} personal life mental health"
  "{author_name} relationships controversies"

Fill JSON from web findings only. When uncertain use null.
Physical illness and ordinary war service themselves do NOT raise the standardness_score.
Documented psychological RESPONSE to illness or war DOES count via custom_tags.
Conservative rule: null beats false, false beats true when in doubt.

Return ONLY valid JSON, no text outside:

{{
  "predefined_tags": {{
    "depression": null, "bipolar": null, "schizophrenia": null, "anxiety": null,
    "ptsd": null, "substance_abuse": null, "suicide": null, "suicide_attempt": null,
    "institutionalized": null, "childhood_trauma": null, "war_experience": null,
    "poverty_extreme": null, "chronic_illness": null, "disability": null,
    "occultism": null, "spiritualism": null, "religious_mania": null,
    "cult_involvement": null, "theosophy_mysticism": null,
    "non_traditional_relationship": null, "homosexuality_taboo_era": null,
    "obsessive_attachment": null, "celibacy_pathological": null,
    "incest_adjacent": null, "alter_ego_documented": null,
    "depersonalization": null, "voluntary_isolation": null,
    "pathological_gambling": null, "legal_troubles": null,
    "imprisonment": null, "exile": null, "extremist_views": null,
    "violence_documented": null, "self_destructive_pattern": null,
    "eating_disorder": null, "paranoia": null, "messiah_complex": null,
    "nihilism_explicit": null
  }},
  "custom_tags": [],
  "life_pattern_summary": "2-3 sentences from web search, or 'Insufficient biographical data available'",
  "standardness_score": null,
  "standardness_note": "Score null — insufficient biographical data to assess.",
  "evidence_quality": "speculation",
  "confidence": 0.2,
  "most_defining_trait": null
}}"""