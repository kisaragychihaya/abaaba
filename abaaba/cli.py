import argparse
import json

from abaaba import Translate
import os
import shutil
from pathlib import Path
from multiprocessing import Pool
import hashlib
def t_process(p:tuple):
    o,d,t,sum_target=p
    with open(o,'rb') as f:
        data=f.read()
        sum_real=hashlib.sha256(data).hexdigest()
    if Path(o).suffix in (".md",".rst"):
        if not (sum_real==sum_target and Path(d).is_file()):
            t.translate(o)
            t.save(d)
    else:
        shutil.copyfile(o, d)
    return sum_real
def main_trans(src,dst,t:Translate,sums:dict):
    if not (os.path.exists(dst) and os.path.isdir(dst)):
        os.makedirs(dst,exist_ok=True)
    for obj in os.listdir(src):
        o=os.path.join(src,obj)
        if os.path.isdir(o):
            d=os.path.join(dst, obj)
            os.makedirs(d,exist_ok=True)
            main_trans(o,d,t,sums)
        else:
            o = os.path.join(src, obj)
            d = os.path.join(dst, obj)
            pths.append((o, d,t,sums.get(str(o),"")))
            # print(f"translate {o} to {d}")
            # if Path(o).suffix==".md":
            #     t.translate(o)
            #     t.save(d)
            # else:
            #     shutil.copyfile(o,d)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ak",required=(not "AK_ABA" in os.environ.keys()),help="API KEY")
    parser.add_argument("--sk",required=(not "SK_ABA" in os.environ.keys()),help="API SECRET")
    parser.add_argument("-s","--source",help="source directory",required=True)
    parser.add_argument("-d","--dest",help="destination directory",required=False)
    parser.add_argument("-T", "--translator", help="destination directory", default="ali")
    parser.add_argument("-f", "--from_lang", help="from language", default="zh")
    parser.add_argument("-t", "--to_lang", help="to language", default="en")
    parser.add_argument("-b", "--build", help="build to html", action="store_true")
    # parser.add_argument("-i", "--interactive", help="interactive Tool", action="store_true")
    args=parser.parse_args()
    if args.build:
        try:
            from sphinx.cmd.build import main as sphinx_build
        except ImportError:
            if os.system("pip install sphinx_markdown_tables recommonmark sphinx_rtd_theme")==0:
                from sphinx.cmd.build import main as sphinx_build
            else:
                print("No sphinx libaray found,Pls run 'pip install sphinx_markdown_tables recommonmark sphinx_rtd_theme' manually")
                exit(-1)
    os.environ['AK_ABA']=args.ak
    os.environ['SK_ABA']=args.sk
    pths=[]
    # if args.interactive:
    #     import inquirer
    #     questions = [
    #         inquirer.Text('src', message="请黏贴你的文档路径")]
    #     answers = inquirer.prompt(questions)
    #     print(answers)
    #     exit()
    src=args.source
    dest=args.dest
    if dest is None:
        dest=args.source+"_"+args.to_lang
    t=Translate(fl=args.from_lang,tl=args.to_lang)
    if (Path(src)/".statue.json").is_file():
        with open(Path(src)/".statue.json",mode="r",encoding="utf-8")as f:
            d_statue=json.load(f)
    else:
        d_statue={}
    main_trans(src, dest,t,d_statue)
    with Pool(4) as p:
        sr=p.map(t_process, pths)
        d_new={}
        for i,t_args in enumerate(pths):
            f=t_args[0]
            d_new[f]=sr[i]
            with open(Path(src)/".statue.json",mode="w",encoding="utf-8")as f:
                json.dump(d_new,f,indent=4)
    if args.build:
        sphinx_build((src,src+"_html"))
        sphinx_build(( dest, dest + "_html"))


