import db_editor as db
import execution_history_parser
import finalize_parser
import magic
import mimetypes
import os
import pandas as pd
import plan_parser
import run_parser
import shutil
import sqlite3
import tarfile
import task_parser

def create_csv(html_file):
    conn = db.create_connection('/tmp/disect/disect.sqlite.db')
    db_df = pd.read_sql_query("SELECT * FROM tasks", conn)
    db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_tasks.csv', index=False)
    db_df = pd.read_sql_query("SELECT * FROM plan", conn)
    db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_plan.csv', index=False)
    db_df = pd.read_sql_query("SELECT * FROM run", conn)
    db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_run.csv', index=False)
    db_df = pd.read_sql_query("SELECT * FROM finalize", conn)
    db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_finalize.csv', index=False)
    db_df = pd.read_sql_query("SELECT * FROM exe_history", conn)
    db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_exe-history.csv', index=False)
    #db_df = pd.read_sql_query("select t.*, e.*, p.*, r.*, f.* from plan as p, run as r, tasks as t, exe_history as e, finalize as f where p.task_id = r.task_id and p.task_id = t.id and p.task_id = e.task_id and p.task_id = f.task_id", conn)
    #db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_join_all.csv', index=False)
    db_df = pd.read_sql_query("select t.*, e.* from tasks as t, exe_history as e where t.id = e.task_id", conn)
    db_df.to_csv('/tmp/disect/'+html_file[:-5]+'_join_tasks_exehistory.csv', index=False)

def call_parsers(html_file):
    task = task_parser.main(html_file)
    plan_parser.main(html_file,task)
    run_parser.main(html_file,task)
    finalize_parser.main(html_file,task)
    execution_history_parser.main(html_file,task)

def arg_type(argv):
    print('determining the argument type...')
    ftype = magic.from_file(argv,mime=True)
    #If gzip, decompress and drop me in the folder with the html files
    if ftype == 'application/gzip':
        print('detected gzip file')
        shutil.rmtree('/tmp/disect')
        with tarfile.open(argv, 'r|gz') as tar:
            tar.extractall('/tmp/disect')
        os.chdir('/tmp/disect/tmp/'+os.listdir('/tmp/disect/tmp')[0])
        files = os.listdir()
        for html_file in files:
            if html_file[-5:] == '.html' and html_file != 'index.html':
                print('parsing ' + html_file)
                call_parsers(html_file)
            else:
                print(html_file + ' is not html, skipping')
        create_csv(html_file)
    #If HTML, parse it
    elif ftype == 'text/html':
        try:
            print('detecting html file')
            print('parsing ' + argv)
            call_parsers(argv)
            create_csv(argv)
        except:
            print('exception html')
    else:
        print('The file type is %s', mimetypes.guess_extension(argv))
        print('Please use an dynflow html file, or a non-csv task-export')