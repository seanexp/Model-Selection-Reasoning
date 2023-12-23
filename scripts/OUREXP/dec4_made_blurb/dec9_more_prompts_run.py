import subprocess as sb 

PROMPTS = [
# 'RIMS/99_7_no_refl_rims_cotpal_inference_prompt_k2_DEC9.txt', 

# dec 9
# 'RIMS/99_7_rims_cotpal_inference_prompt_k2_DEC9.txt',
# 'RIMS/99_7_rims_cotpal_inference_prompt_k2_DEC9_noformat.txt',
# 'RIMS/99_7_no_refl_rims_cotpal_inference_prompt_k4_DEC9.txt', 
# 'RIMS/99_7_rims_cotpal_inference_prompt_k4_DEC9.txt', 
# 'RIMS/99_7_rims_cotpal_inference_prompt_k4_DEC9_noformat.txt', 
# 'RIMS/99_7_no_refl_rims_cotpal_inference_prompt_k6_DEC9.txt', 
# 'RIMS/99_7_rims_cotpal_inference_prompt_k6_DEC9.txt',
# 'RIMS/99_7_rims_cotpal_inference_prompt_k6_DEC9_noformat.txt',

# dec 22: attempt --> attempt 1,2,3...
'RIMS/modif_no_refl_rims_cotpal_inference_prompt_k2_DEC9.txt',
# 'RIMS/modif_rims_cotpal_inference_prompt_k2_DEC9_noformat.txt',
# 'RIMS/modif_no_refl_rims_cotpal_inference_prompt_k6_DEC9.txt',
# 'RIMS/modif_rims_cotpal_inference_prompt_k6_DEC9_noformat.txt',
# 'RIMS/modif_no_refl_rims_cotpal_inference_prompt_k4_DEC9.txt',
# 'RIMS/modif_rims_cotpal_inference_prompt_k4_DEC9_noformat.txt',
]


# run exps
for promptf in PROMPTS:
    # cmd = f"bash dec9_run_a_prompt.sh {promptf}"
    cmd = f"bash dec22_run_a_prompt_modif.sh {promptf}"
    print(cmd)
    sb.call(cmd, shell=True)


# evaluate to a table
ecmd = "python dec_evaluates_all_and_combine_to_a_table.py"
sb.call(ecmd, shell=True)
