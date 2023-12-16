from subprocess import Popen, PIPE
from datetime import datetime
import shutil
import json
import tempfile
import os


class Conversation:
    """Convo interface"""

    # A dictionary of functions that can be called by the conversation
    callbacks={}

    # The messages of the conversation. Call completeAsync to populate messages
    messages=[]

    # The messages of the conversation in raw syntax form. By default syntaxMessages are not populated
    # when calling completeAsync. Set populateSyntaxMessages to true to enabled.
    syntaxMessages=[]

    populateSyntaxMessages=False

    # The shared state variables of the conversation. Call completeAsync to populate state
    state={}

    # The current conversation as a string
    convo=""

    def append(self, content):
        if content.startswith('*convo*'):
            content=content[7:].lstrip()

        self.convo+=content+'\n\n'

    def appendMessage(self, role, message):
        self.convo+='> '+role+'\n'+message+'\n\n'

    def appendUserMessage(self, message):
        self.appendMessage('user',message)

    def appendAssistantMessage(self, message):
        self.appendMessage('assistant',message)


    def completeAsync(self):

        # if not self.convoSrcTmpCreated:
        #     self.createConvoTmpSrc()

        tmp=tempfile.NamedTemporaryFile(delete=False)
        tmp.write(self.convo.encode())
        tmp.flush()
        tmp.close()

        nodePath=shutil.which('node')

        args=[
            nodePath,
            os.path.join(os.path.dirname(__file__),'convo.js'),
            '--source',tmp.name,
            '--cmdMode',
            '--prefixOutput',
            '--printState',
            '--printFlat'
        ]

        if self.populateSyntaxMessages:
            args.append('--printMessages')

        proc = Popen(
            args,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE
        )

        def writeProc(line):
            proc.stdin.write((line+'\n').encode())
            proc.stdin.flush()

        resultLines=[]
        flatLines=[]
        stateLines=[]
        syntaxLines=[]

        while True:
            line=proc.stdout.readline()
            if isinstance(line, (bytes, bytearray)):
                line=line.decode()

            if line.startswith('CALL:'):
                callObj=json.loads(line[5:].strip())
                callback=self.callbacks[callObj['fn']]
                if callback:
                    result=callback(*callObj['args'])
                    writeProc('RESULT:'+json.dumps(result))
                else:
                    writeProc('ERROR:no function found by name - '+callObj['fn'])

            elif line.startswith('END:'):
                break
            elif line.startswith(':'):
                resultLines.append(line[1:])
            elif line.startswith('f:'):
                flatLines.append(line[2:])
            elif line.startswith('s:'):
                stateLines.append(line[2:])
            elif line.startswith('m:'):
                syntaxLines.append(line[2:])

        proc.kill()

        if len(flatLines):
            self.messages=json.loads(''.join(flatLines))
        else:
            self.messages=[]

        if len(stateLines):
            self.state=json.loads(''.join(stateLines))
        else:
            self.state={}

        if len(syntaxLines):
            self.syntaxMessages=json.loads(''.join(syntaxLines))
        else:
            self.syntaxMessages=[]

        self.convo=''.join(resultLines).strip()+'\n\n'

        os.remove(tmp.name)
