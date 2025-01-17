@echo off

REM 在 WSL 中启动 CosyVoice API 服务
echo 正在启动 CosyVoice API 服务...
wsl -d ubuntu -e bash -c "source ~/miniconda3/etc/profile.d/conda.sh && conda activate Cosyvoice && cd ~/CosyVoice && python cosyvoice-api.py --port 50001 --model_dir pretrained_models/CosyVoice-300M-SFT"
