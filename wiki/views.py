from django.shortcuts import render,HttpResponseRedirect, HttpResponse
from JamesDjango.settings import MEDIA_ROOT
import markdown

# Create your views here.

"""文章列表"""
def wikilist(request):
    doc_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname="abc.html")
    #return  HttpResponse(html)
    return render(request, "abc.html")

"""添加文章"""
def adddoc(request):
    if request.method == "POST":
        
        #print(request.POST.get("test-editormd-markdown-doc",None))
        #print(request.POST.get("test-editormd-html-code",None))
        doc_markdown = request.POST.get("test-editormd-markdown-doc",None)
        doc_html = request.POST.get("test-editormd-html-code",None)
        doc_markdown_name = "{_dir}/wiki/doc/{_docname}".format(_dir=MEDIA_ROOT,_docname="abc")
        #doc_html_name = "{_dir}/temp/templates/{_docname}".format(_dir=MEDIA_ROOT,_docname="abc")
        with open("{}.md".format(doc_markdown_name), 'w') as f :
            f.write(doc_markdown)  
            f.close()
        with open("{}.html".format("./templates/abc"),'w') as f:
            f.write(doc_html)  
            f.close()
        return HttpResponseRedirect('/wiki/adddoc.html')
    return render(request, "wiki/adddoc.html")



"""删除文章"""
def deldoc(request):
    pass






"""编辑文档"""
def editdoc(request):
    pass
