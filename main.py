import argparse
from abaaba import Translate
import os
import shutil
from pathlib import Path
from multiprocessing import Pool
pth = []
def t_process(p:tuple):
    o,d,t=p
    if Path(o).suffix in (".md",".rst"):
        t.translate(o)
        t.save(d)
    else:
        shutil.copyfile(o, d)
def main_trans(src,dst,t:Translate=None):
    if not (os.path.exists(dst) and os.path.isdir(dst)):
        os.makedirs(dst,exist_ok=True)
    for obj in os.listdir(src):
        o=os.path.join(src,obj)
        if os.path.isdir(o):
            d=os.path.join(dst, obj)
            os.makedirs(d,exist_ok=True)
            main_trans(o,d)
        else:
            o = os.path.join(src, obj)
            d = os.path.join(dst, obj)
            pth.append((o, d,t))
            # print(f"translate {o} to {d}")
            # if Path(o).suffix==".md":
            #     t.translate(o)
            #     t.save(d)
            # else:
            #     shutil.copyfile(o,d)

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ak", required=(not "AK_ABA" in os.environ.keys()), help="API KEY")
    parser.add_argument("--sk", required=(not "SK_ABA" in os.environ.keys()), help="API SECRET")
    parser.add_argument("-s", "--source", help="source directory", required=True)
    parser.add_argument("-d", "--dest", help="destination directory", required=False)
    parser.add_argument("-T", "--translator", help="destination directory", default="ali")
    parser.add_argument("-f", "--from_lang", help="from language", default="zh")
    parser.add_argument("-t", "--to_lang", help="to language", default="en")
    parser.add_argument("-b", "--build", help="build to html", action="store_true")
    # parser.add_argument("-i", "--interactive", help="interactive Tool", action="store_true")
    args = parser.parse_args()
    os.environ['AK_ABA'] = args.ak
    os.environ['SK_ABA'] = args.sk
    # if args.interactive:
    #     import inquirer
    #     questions = [
    #         inquirer.Text('src', message="请黏贴你的文档路径")]
    #     answers = inquirer.prompt(questions)
    #     print(answers)
    #     exit()
    src = args.source
    dest = args.dest
    if dest is None:
        dest = args.source + "_" + args.to_lang
    t = Translate(fl=args.from_lang, tl=args.to_lang)
    main_trans(src, dest, t)
    for p in pth:
        t_process(p)
    if args.build:
        try:
            from sphinx.cmd.build import main as sphinx_build
        except ImportError:
            if os.system("pip install sphinx_markdown_tables recommonmark sphinx_rtd_theme") == 0:
                from sphinx.cmd.build import main as sphinx_build
            else:
                print("No sphinx libaray found")
                exit(-1)
        sphinx_build((src, src + "_html"))
        sphinx_build((dest, dest + "_html"))

if __name__ == '__main__':
    run()


