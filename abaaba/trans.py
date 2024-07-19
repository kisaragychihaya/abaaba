import json,pypandoc
from pathlib import Path
class Translate:
    def __init__(self,translate=None,fl="zh",tl="en"):
        self.bot=None
        self._sl=fl
        self._tl=tl
        self.doc=None
        if not translate:
            try:
                from abaaba.AlibabaTrans import AliTrans
                self.bot=AliTrans()
            except ImportError:
                raise NotImplementedError("找不到翻译器！！")
        else:
            self.bot=translate()

    def translate(self,src):
        self.suffix=Path(src).suffix
        if self.suffix==".md":
            self.doc = json.loads(pypandoc.convert_file(src, "json", format="markdown",
                                                    extra_args=["--from=markdown-markdown_in_html_blocks+raw_html"]))
        elif self.suffix==".rst":
            self.doc=""
            with open(src,"r",encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if len(line)and (not line[0].isascii()):
                        self.doc+=str(self.bot.main(line, self._sl, self._tl)).strip("\n")+"\n"
                    else:
                        self.doc+=line
                return
        for blk in self.doc["blocks"]:
            if blk["t"]=="RawBlock":
                continue
            self._p(blk)

    def _p(self,blk):
        if isinstance(blk,dict):
            if blk["t"] == "Str":
                q=f"{blk['c']}"
                if not q.isascii():
                    blk["c"]=str(self.bot.main(q,self._sl,self._tl)).strip("\n")
                    print(blk["c"])
            elif "c" in blk.keys():
                self._p(blk["c"])
        elif isinstance(blk,list):
            for content in blk:
                self._p(content)
    def save(self,dst):
        data=self.doc
        if self.suffix==".md":
            data = json.dumps(self.doc)
            data=pypandoc.convert_text(data,format="json",to="markdown_strict",extra_args=["--wrap=none"])
        elif self.suffix==".rst":
            pass
        else:
            raise NameError("Unsupported format {}".format(self.suffix))
        with open(dst, mode="w", encoding="utf-8") as file:
            file.write(data)



