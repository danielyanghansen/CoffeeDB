
echo "Setting up the database..."
python .\KaffeDBTestInit.py
echo "running tests..."
python .\KaffeDBUserStoryTests.py | Out-File -FilePath .\Output
echo "Results successfully stored into file: Output"