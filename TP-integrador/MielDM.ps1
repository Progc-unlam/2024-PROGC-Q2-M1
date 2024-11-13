$envPath = ".\.venv"

if (Test-Path $envPath) {
    & "$envPath\Scripts\Activate.ps1"
}else{
    python -m venv $envPath
    & "$envPath\Scripts\Activate.ps1"
    pip install -r requirements.txt
}
python .\menuMielScrapping.py