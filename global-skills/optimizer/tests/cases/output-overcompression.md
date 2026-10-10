# Case: Output Overcompression

Mode: compare

To reduce tokens, an agent prompt was changed to "answer in at most 50 words;
omit evidence and validation". Measured over the same 40 tasks: output tokens
per task fell from 620 to 140, but follow-up turns rose from 1.2 to 2.1 per
task and task success fell from 92% to 81%.
