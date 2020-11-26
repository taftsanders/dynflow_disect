import magic
import os
import csv
import tarfile
import plan_parser
import task_parser
import run_parser
import finalize_parser
import execution_history_parser


def arg_type(argv):
    print('determining the argument type...')
    ftype = magic.from_file(argv,mime=True)
    #If gzip, decompress and drop me in the folder with the html files
    if ftype == 'application/gzip':
       # try:
        print('detected gzip file')
        with tarfile.open(argv, 'r|gz') as tar:
            tar.extractall('/tmp/disect')
        os.chdir('/tmp/disect/tmp/'+os.listdir('/tmp/disect/tmp')[0])
        files = os.listdir()
        print(files)
        for html_file in files:
            each_task = []
            if html_file[-5:] == '.html' and html_file != 'index.html':
                print('parsing ' + html_file)
                #call task parcer
                task = task_parser.main(html_file)
                each_task.append(task)
                #call plan_parser here
                plan = plan_parser.main(html_file)
                each_task.append(plan)
                #call run_parser here
                run = run_parser.main(html_file)
                each_task.append(run)
                #call finalize_parser here
                finalize = finalize_parser.main(html_file)
                each_task.append(finalize)
                #call execution_history_parser here
                execution = execution_history_parser.main(html_file)
                each_task.append(execution)
                print('Writing '+html_file+' results to /tmp/disect_results.csv')
                with open('/tmp/disect_results.csv', 'w') as csvfile:
                    wr = csv.writer(csvfile, lineterminator='\n')
                    wr.writerow(each_task)
            else:
                print(html_file + ' is not html, skipping')
        #except:
            #print('exception gzip')
    #If HTML, parse it
    elif ftype == 'text/html':
        try:
            print('detecting html file')
            #call parser here
        except:
            print('exception html')
    elif argv is str:
        if 'http' in argv:
            try:
                print('detecting URL')
            except:
                print('exception URL')