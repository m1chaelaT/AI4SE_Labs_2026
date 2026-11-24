# Assessment by mimo-2.6-flash

# Week 03 Prompting
- Awarded: 4b out of 5b
- Commentary: The submission covers all four tasks with real, reproducible artifacts: three well-formed prompting-framework prompts, full 155-question prediction sets, an implemented and argued novel metric, and a rigorous statistical analysis script. Task 1 and Task 3 are essentially complete. Task 2 lacks the explicitly required visualisation and only weakly identifies the model in its outputs, and Task 4's main deliverable is a PDF report that this model could not open, so it was judged from the accompanying code, data and graph files. Note: Report_Task_4.pdf and the three Task 4 PNG graphs could not be viewed by this model; Task 4 was graded from analysis.py and per_question.json.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three non-ROSES, non-zero-shot frameworks (ICIO, RTF, CoT) were chosen, each formulated as a separate prompt file (P1_ICIO.md, P2_RTF.md, P3_CoT.md) usable in Task 2, all targeting the text-to-SQL problem. The short report explains why each framework fits the task and cites the common source (frompting.com/frameworks). All required outputs are present.

## Task 2
- Awarded: 0.5b   (max 1b)
- Commentary: Complete prediction sets for all three prompts (155 questions each) plus an evaluation script executing queries against the database are present, and the report gives accuracies, inference times (2m50s / 3m15s / 4m10s) and a sensible comparison (each prompt run in a fresh Copilot session, as hinted). However, the explicitly required visualisation is entirely missing from Task 2, and the prediction CSVs contain only question,predicted_sql with no model/prompt metadata columns; the model is mentioned only vaguely ("GitHub Copilot with the same model", no model name). Core work done, deliverable requirements partially missed.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: The student proposes a "Relaxed Result F1" metric (row-level precision/recall tolerant of column choice/order, rewarding partially correct answers), argues why it complements rather than replaces exact-match accuracy, and defends its applicability. It is implemented in relaxed_result_f1.py, computed over all Task 2 predictions (relaxed_f1_scores.csv, 465 rows), and the report compares prompts with a genuinely insightful finding: RTF jumps from 27.7% accuracy to ~0.90 relaxed F1 while ICIO stays low, showing the new metric uncovers a difference the original accuracy hid. All outputs present.

## Task 4
- Awarded: 1.5b   (max 2b)
- Commentary: analysis.py delivers a strong quantitative re-analysis: bootstrap confidence intervals, McNemar tests on accuracy, Wilcoxon signed-rank tests on per-question F1, accuracy-overlap counts, question-type and empty-result breakdowns, SQL-feature counts (SELECT *, LIMIT, HOUSE_NUMBER, DISTINCT, MAX) as prompt-level explanations, and generation of three comparison graphs (graf_metriky, graf_prazdne_vysledky, graf_rozdelenie_f1) backed by per-question data in per_question.json. Tables and statistical-significance determination are clearly supported by the artifacts. Half a point is withheld because the actual deliverable — the detailed narrative report, incl. the required discussion of the model and coding agent as factors — exists only as Report_Task_4.pdf, which this model cannot read, so that content could not be verified from the text.