import argparse
from abaaba import Translate
import os
def main(src,dst,t:Translate=None):
    if not (os.path.exists(dst) and os.path.isdir(dst)):
        os.makedirs(dst,exist_ok=True)
    for obj in os.listdir(src):
        o=os.path.join(src,obj)
        if os.path.isdir(o):
            d=os.path.join(dst, obj)
            os.makedirs(d,exist_ok=True)
            main(o,d)
        else:
            o = os.path.join(src, obj)
            d = os.path.join(dst, obj)
            print(f"translate {o} to {d}")
            t.translate(o)
            t.save(d)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ak",required=(not "AK_ABA" in os.environ.keys()),help="API KEY")
    parser.add_argument("--sk",required=(not "SK_ABA" in os.environ.keys()),help="API SECRET")
    parser.add_argument("-s","--source",help="source directory",required=True)
    parser.add_argument("-d","--dest",help="destination directory",required=True)
    parser.add_argument("-T", "--translator", help="destination directory", default="ali")
    parser.add_argument("-f", "--from_lang", help="from language", default="zh")
    parser.add_argument("-t", "--to_lang", help="to language", default="en")
    args=parser.parse_args()
    os.environ['AK_ABA']=args.ak
    os.environ['SK_ABA']=args.sk
    t=Translate(fl=args.from_lang,tl=args.to_lang)
    main(args.source, args.dest,t)

