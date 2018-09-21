# CLI

import sys,re,json,time

def log(msg):
    print(f'LOG:::{msg}')

class FNote(object):

    def readdata(self):
        log(f'Generating notebook from {self.file}')
        with open(self.file, mode='r') as fp:
            return json.load(fp)
    
    def writedata(self):
        log(f'closing and saving to {self.file}')
        with open(file=self.file, mode='w') as fp:
            return json.dump(self.notebook,fp)

    def __init__(self,file):
        super(FNote, self).__init__()
        self.file = file
        self.notebook = self.readdata()

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
            self.add_note(args[0], ''.join(args[1:]))
        else:
            heading = args[0] if len(args) == 1 else input('Enter heading: ')
            while True:
                txt = input('Enter Text or \'stop\' to exit: ')
                if txt.lower() == 'stop':
                    break
                self.add_note(heading, txt)

def listen(file):
    # todo: move cmd executions to new method
    fnote = FNote(file)
    switch = {
        'save' : lambda args: fnote.save(args)
    }
    exitcmds = set(['stop','exit','end'])
    while True:
        try:
            tokens = re.split(r'\\s+',input('Enter cmd: '))
            cmd = tokens[0].lower()
            if cmd in exitcmds or not cmd in switch:
                return
            else:
                switch[cmd](tokens[1:]) 
        except EOFError | IndexError:
            return
        finally:
            fnote.writedata()

def main():
    # todo: Ask first time, then save in config file
    basedir = r'C:\\Users\\gluo7\\Desktop\\Shared Projects\\FNote'
    notebook = r'NoteBook.json'
    notebook = basedir + r'\\' + notebook
    args = sys.argv[1:] # Exclude execution
    log(f'Arguments=[{" ".join(args)}]')
    if len(args) == 0:
        listen(notebook)

if __name__ == '__main__':
    main()