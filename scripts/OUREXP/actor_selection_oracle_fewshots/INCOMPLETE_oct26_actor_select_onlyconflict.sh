#!/bin/bash
set -x

# Specify your EXEHOME first. EXEHOME=/home/user-name/Model-Selection-Reasoning/src
EXEHOME=/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src
cd ${EXEHOME}

python selection_math.py --start 0 \
        --end -1 \
        --dataset 'gsm8k' \
        --backbone 'chatgpt' \
        --cot_temperature 0. \
        --pal_temperature 0. \
        --sc_num 1 \
        --output_dir '../output/oct26_only_conflict/actor_select' \
        # --when_only_conflict \
        # --actor_selection_prompt "/Users/seonils/dev/llm-reasoners/examples/Model-Selection-Reasoning/src/prompts/prep_reflexion/4_selection_prompt_0_1_nobiassys_modif_verbose_nomenclature.txt" 

# run evaluation at once
python evaluate.py --input_path '../output/oct26_only_conflict/actor_select/chatgpt/gsm8k*.jsonl'\
                --dataset_type 'math'