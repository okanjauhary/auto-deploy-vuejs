import os
import sys
import argparse
import re

def STOP(msg):
    return sys.exit('\n' + msg + '\n')

def checking_vue_config(vue_config):
    found = False
    output_path = ''
    code_line = ''
    with open(vue_config, 'r') as file:
        for code in file.readlines():
            if re.search(r"^((\s+)?(')?outputDir(')?(\s+)?:(\s+)?)(')(\w?\W?)+('),(\s+)?$", code):
                found = True
                code_line = code.strip()
                output_path = re.sub(r"((\s+)?(')?outputDir(')?(\s+)?:(\s+)?)(')", '', code)
                output_path = re.sub(r"(',(\s+)?(\n)?)", '', output_path)
                break

    return { 'found': found, 'output_path': output_path.strip(), 'code_line': code_line }

def main():
    parser = argparse.ArgumentParser(description='Automatic deployment')

    parser.add_argument('--path', required=True, default='', type=str, help='Path of project will deploying')

    args = parser.parse_args()

    path_current = os.getcwd().strip()
    path_project = re.sub('/$', '', path_current + '/' + re.sub('/$', '',args.path)) + '/'

    if path_project == '':
        STOP('Opps! something wrong')
        
    if not os.path.exists(path_project + 'vue.config.js'):
        STOP('vue.config.js not found \nPlease check your --path or --help for argument lists')

    output = checking_vue_config(path_project + 'vue.config.js')

    if not output['found']:
        STOP("Output path not found on vue.config.js\nPlease make sure you're added output path in vue.config.js")
    
    if re.search(r"^dist(.*)", output['output_path'].strip('/')):
        STOP("Cannot assign output path with 'dist', Please change your output path\n=> " + output['code_line'])

    os.chdir(path_project)
    os.system('npm run build')
    os.system('mv dist dist.old')
    os.system('mv build dist')
    os.system('rm -rf dist.old')
    print("SUKSESSS BROOOOOOO")

if __name__ == '__main__':
    main()