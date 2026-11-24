# Assessment by laguna-s-2.1

# Week 03 Prompting
- Awarded: 4b out of 5b
- Commentary: The student delivered a coherent, end-to-end prompt-comparison pipeline. Task 1 cleanly defines three distinct frameworks (ICIO, RTF, CoT) found on frompting.com/frameworks, each with a well-structured prompt actually reused in Task 2. Task 3 proposes an original and defensible "Relaxed Result F1" metric, implemented and run against the Task 2 predictions, clearly complementing accuracy. Task 4 provides a thorough statistical analysis (bootstrap CIs, McNemar, Wilcoxon, SQL-feature and question-type breakdowns) with generated graphs. Task 2 is the weakest link: predictions and an inference-time comparison report are present, but the report lacks a visualization and the prediction CSVs carry no explicit model/prompt metadata. Additionally, the Task 4 report was supplied only as Report_Task_4.pdf, which this model cannot render, so the written interpretation was judged from analysis.py and the generated artifacts rather than the report text itself.

## Task 1
- Awarded: 1b   (max 1b)
- Commentary: Three valid prompting frameworks were selected (ICIO, RTF, CoT), none of which are ROSES or zero-shot. The report (Report_Task_1.md) explains why each was chosen and what it is expected to contribute, and all were sourced from https://frompting.com/frameworks as required. Three corresponding prompt files (prompts/P1_ICIO.md, P2_RTF.md, P3_CoT.md) are formulated and were subsequently reused to produce the Task 2 predictions, confirming they are genuinely intended for the downstream problem. Minor: the report is brief, but it meets all stated requirements.

## Task 2
- Awarded: 0.5b   (max 1b)
- Commentary: Predictions for all three prompts are stored (predictions/ICIO.csv, RTF.csv, CoT.csv) and a brief comparison report (Report_Task_2.md) records accuracy, inference times (ICIO 2m50s, RTF 3m15s, CoT 4m10s) and interprets the results. However, the report contains no visualization as explicitly requested, and the prediction CSVs carry only question/predicted_sql columns with no explicit model or prompt-identification metadata (prompt is implied only by filename; the underlying model is named vaguely as "GitHub Copilot"). Core deliverables are present, but the missing visualization and metadata leave the task partially incomplete.

## Task 3
- Awarded: 1b   (max 1b)
- Commentary: An original, well-justified "Relaxed Result F1" metric was proposed, executed via Claude Opus to produce relaxed_result_f1.py. The metric matches predicted rows to gold rows regardless of returned columns, penalizes missing/extra rows, and yields per-question F1 (partial credit) rather than 0/1, explicitly complementing the original accuracy rather than replacing it. The implementation is functional, per-question scores are computed for all three prompts in relaxed_f1_scores.csv (ICIO 0.284, RTF 0.897, CoT 0.994), and the report interprets how the new metric reveals differences (especially ICIO vs RTF) hidden by accuracy. All requirements are fully met.

## Task 4
- Awarded: 1.5b   (max 2b)
- Commentary: analysis.py performs a comprehensive re-analysis: bootstrapped confidence intervals for accuracy and F1, pair-wise McNemar tests (accuracy) and Wilcoxon signed-rank tests (F1) for statistical significance, overlap/accuracy tables, question-type breakdown, SQL-feature profiling, and empty-vs-non-empty result analysis, and generates three graphs (graf_metriky.png, graf_prazdne_vysledky.png, graf_rozdelenie_f1.png) plus per_question.json. The statistical-significance and graph/table requirements are clearly satisfied. Note: the required detailed report was provided only as Report_Task_4.pdf, which could not be read by this model (PDF input unsupported), so the written interpretation/explanation of the prompt/model/coding-agent factors could not be verified directly and was assessed from the code and generated artifacts. This unverifiable written-report portion is the reason for the 0.5b deduction.
