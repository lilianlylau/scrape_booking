call C:\Users\Alex\miniconda3\Scripts\activate.bat C:\Users\Alex\miniconda3\
call activate scrape
python scrape_tracer.py > test_%date:~10%%date:~4,2%%date:~7,2%-%time:~0,2%%time:~3,2%%time:~6,2%.log 2>&1
call conda deactivate