#!/bin/bash
export WANDB_DISABLED=true
wandb offline

deepspeed --num_gpus 8 ../../src/train_bash.py \
    --deepspeed ../deepspeed/ds_z2_config.json \
    --stage sft \
    --do_train \
    --model_name_or_path /mnt/data/shesj/PLM/Mistral-7B-Instruct-v0.2 \
    --dataset sixlan_sft_data_unwrap \
    --dataset_dir /mnt/data/shesj/Data/RL4CoTData/sft_data \
    --template mistral \
    --finetuning_type full \
    --output_dir /mnt/data/shesj/Trained/RL4CoT/SFT/Mistral-7B_SixLang \
    --logging_dir "/mnt/data/shesj/Log/CommonAlign/SFT/Mistral-7B_SixLang" \
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 2048 \
    --preprocessing_num_workers 80 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 8 \
    --gradient_accumulation_steps 2 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --warmup_ratio 0.03 \
    --save_steps 1000 \
    --eval_steps 1000 \
    --evaluation_strategy steps \
    --learning_rate 5e-6 \
    --num_train_epochs 3.0 \
    --max_samples 1000000000000000 \
    --val_size 0.1 \
    --ddp_timeout 1800000 \
    --plot_loss \
    --bf16 \
    --tf32 True