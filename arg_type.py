import magic
import os
import tarfile
import shutil
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
        print('detected gzip file')
        shutil.rmtree('/tmp/disect')
        with tarfile.open(argv, 'r|gz') as tar:
            tar.extractall('/tmp/disect')
        os.chdir('/tmp/disect/tmp/'+os.listdir('/tmp/disect/tmp')[0])
        files = os.listdir()
        for html_file in files:
            if html_file[-5:] == '.html' and html_file != 'index.html':
                print('parsing ' + html_file)
                #call task parcer
                task = task_parser.main(html_file)
                #call plan_parser here
                plan_parser.main(html_file,task)
                #call run_parser here
                run_parser.main(html_file,task)
                #call finalize_parser here
                finalize_parser.main(html_file,task)
                #call execution_history_parser here
                execution_history_parser.main(html_file,task)
            else:
                print(html_file + ' is not html, skipping')
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
    