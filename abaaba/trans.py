import json,pypandoc

class Translate:
    def __init__(self,translate=None,fl="zh",tl="en"):
        self.bot=Translate
        self._sl=fl
        self._tl=tl
        self.doc=None
        if not translate:
            try:
                from abaaba.AlibabaTrans import AliTrans
                self.bot=AliTrans
            except ImportError:
                raise NotImplementedError("找不到翻译器！！")

    def translate(self,src):
        self.doc = json.loads(pypandoc.convert_file(src, "json", format="markdown",
                                                    extra_args=["--from=markdown-markdown_in_html_blocks+raw_html"]))
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
        data=json.dumps(self.doc)
        data=pypandoc.convert_text(data,format="json",to="markdown_strict",extra_args=["--wrap=none"])
        with open(dst,mode="w",encoding="utf-8") as file:
            file.write(data)