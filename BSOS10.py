## Hardware
import xml.etree.ElementTree as _ET
import os

boot = True

files = {}
folders = {}

def rawRead(fid):
    global files
    if (not fid in files):
        return False
    return files[fid]

def rawWrite(fid, pos, name, data):
    global files
    if (not fid in files): 
        return False
    files[fid] = (pos, _strnorm(name), _strnorm(data))
    _rawStore()

def rawMakeFile(pos, name, data):
    global files
    hole = 0
    while (hole in files):
        hole+=1
    files[hole] = (pos, _strnorm(name), _strnorm(data))
    files = dict(sorted(files.items()))
    _rawStore()

def rawMakeDir(pos, name):
    global folders
    hole = 0
    while (hole in folders):
        hole += 1
    folders[hole] = (pos, _strnorm(name))
    folders = dict(sorted(folders.items()))
    _rawStore()

def rawRemoveFile(fid):
    global files
    del files[fid]
    rawClean()

def rawRemoveFolder(pos):
    global folders
    del folders[pos]
    rawClean()

def rawWriteFolder(pos, pos2, name):
    global folders
    if (not pos in folders): 
        return False
    folders[pos] = (pos2, _strnorm(name))
    _rawStore()

def rawReadFolder(pos):
    global folders
    if (not pos in folders): 
        return False
    return folders[pos]

def rawClean():
    done = False
    while (not done):
        done = True
        todel = []
        for fi in files:
            if not files[fi][0] in folders:
                todel.append(fi)
                done = False
        for fi in todel:
            del files[fi]
        todel = []
        for fo in folders:
            if not folders[fo][0] in folders:
                todel.append(fo)
                done = False
        for fo in todel:
            del folders[fo]
    _rawStore()

def _strnorm(s):
    if s == None:
        return ''
    return str(s)

def _rawLoad():
    global files
    global folders
    files = {}
    folders = {}
    tree = _ET.parse('data.xml')
    root = tree.getroot()
    for file in root[0]:
        files[int(file.attrib['id'])] = (int(file.attrib['pos']), _strnorm(file.attrib['name']), _strnorm(file.text))
    for folder in root[1]:
        folders[int(folder.attrib['id'])] = (int(folder.attrib['pos']), _strnorm(folder.text))
    files = dict(sorted(files.items()))
    folders = dict(sorted(folders.items()))

def _rawStore():
    from shutil import copyfile
    import datetime
    import time
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H.%M.%S')
    copyfile("data.xml", "backup" + st + ".xml")
    global files
    global folders
    ETdata = _ET.Element('data')  
    ETfi = _ET.SubElement(ETdata, 'files')
    ETfo = _ET.SubElement(ETdata, 'folders')
    ETfiles = []
    for i in files:
        ETfiles.append(_ET.SubElement(ETfi, 'file'))
        ETfiles[-1].set('id', _strnorm(i))
        ETfiles[-1].set('pos', _strnorm(files[i][0]))
        ETfiles[-1].set('name', files[i][1])
        ETfiles[-1].text = _strnorm(files[i][2])

    ETfolders = []
    for i in folders:
        ETfolders.append(_ET.SubElement(ETfo, 'folder'))
        ETfolders[-1].set('id', _strnorm(i))
        ETfolders[-1].set('pos', _strnorm(folders[i][0]))
        ETfolders[-1].text = _strnorm(folders[i][1])

    mydata = _ET.tostring(ETdata)
    myfile = open("data.xml", "w")
    myfile.write(mydata.decode('UTF-8'))
    myfile.close()

def rawRun(s, inp1="", inp2="", inp3="", inp4=""):
    output = ""
    s = "\n" + s
    s = s.replace('\n', '\n\t')
    ##print(s)
    exec("def ran_function(inp1 = '', inp2 = '', inp3 = '', inp4 = ''):" + s + "\n\noutput = ran_function(\"" + inp1 + "\", \"" + inp2 + "\", \"" + inp3 + "\", \"" + inp4 + "\")")
    return output

while (boot):
    boot = False
    _rawLoad()
    rawRun(rawRead(0)[2])
    print('SHELL EXITED\nPRESS ENTER TO CONTINUE...')
    input()
