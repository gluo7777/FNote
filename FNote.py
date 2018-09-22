# CLI

import sys,re,json,time,os
from pathlib import Path

def log(msg):
    print(f'LOG:::{msg}')

def next(msg='Enter: ',default=''):
    try:
        return input(msg)
    except EOFError:
        return default

class FNote(object):

    def readdata(self):
        log(f'Generating notebook from {self.file}')
        mode = 'r' if os.path.exists(self.file) else 'x+'
        with open(self.file, mode) as fp:
            if os.stat(self.file).st_size == 0:
                return {}
            else:
                return json.load(fp)
    
    def writedata(self):
        log(f'closing and saving to {self.file}')
        with open(file=self.file, mode='w') as fp:
            return json.dump(self.notebook,fp)

    def get_heading(self,heading):
        if heading not in self.notebook:
            self.notebook[heading] = {
                "notes": []
                ,"lastModified": time.time()
            }
        return self.notebook[heading]

    def add_note(self,heading,line):
        self.get_heading(heading)['notes'].append(line)
        self.get_heading(heading)['lastModified'] = time.time()
    
    def find(self,args):
        """find [OPTION]... [h <header>] <text>"""

    def save(self,args):
        """save [OPTION]... [header [tokens]]"""
        log(f'save {args}')
        if len(args) >= 2:
            self.add_note(args[0], ' '.join(args[1:]))
        else:
            heading = args[0] if len(args) == 1 else input('Enter heading: ')
            while True:
                txt = input('Enter Text or \'stop\' to exit: ')
                if txt.lower() == 'stop':
                    break
                self.add_note(heading, txt)
    
    def __init__(self,file):
        super(FNote, self).__init__()
        self.file = file
        self.notebook = self.readdata()
        self.switch = {
            'save' : lambda args: self.save(args)
        }

    def handle(self):
        try:
            tokens = re.split(r'\s+',input('Enter cmd: '))
            cmd = tokens[0].lower()
            if not cmd in self.switch:
                return False
            else:
                self.switch[cmd](tokens[1:])
                return True
        except EOFError | IndexError:
            return False

class FConfig(object):
    def __init__(self):
        try:
            with open('FNote.json','x') as fp:
                notedir = next('Enter notes directory (empty for installation directory): ')
                notebook = next('Enter name of note book: ','NoteBook') + '.json'
                self.config = {
                    "notedir" : notedir
                    ,"notebook" : notebook
                }
                json.dump(self.config,fp)
        except FileExistsError:
            with open('FNote.json','r') as fp:
                self.config = json.load(fp)
        finally:
            self.notebook = Path(self.config['notedir'],self.config['notebook']).name

    def fnote(self):
        return FNote(self.notebook)

def main():
    fnote = FConfig().fnote()
    args = sys.argv[1:] # Exclude execution
    log(f'Arguments=[{" ".join(args)}]')
    if len(args) == 0: 
        while True and fnote.handle():  pass
    else:
        fnote.handle()
    fnote.writedata()

if __name__ == '__main__':
    main()