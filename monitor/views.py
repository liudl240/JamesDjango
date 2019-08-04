from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response,HttpResponsePermanentRedirect
from Users.models import UserInfo
from monitor.models import company
from Users.views import login_require
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage

# Create your views here.
@login_require
def listinfo(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    companyinfo = company.objects.all()
    
    
    input_search_field = "title"
    input_keyword = ""
    if request.method == "POST":
        input_search_field = request.POST.get("search_field")
        input_keyword = request.POST.get("keyword",None)
        """标题检索"""
        if input_search_field == "company":
            companyinfo = companyinfo.filter(company__icontains=input_keyword)
        """作者检索"""
        if input_search_field == "application":
            companyinfo = companyinfo.filter(application__icontains=input_keyword)
        """作者检索"""
        if input_search_field == "product":
            companyinfo = companyinfo.filter(product__icontains=input_keyword)
    """"分页"""
    # 值1：所有的数据
    # 值2：每一页的数据
    # 值3：当最后一页数据少于n条，将数据并入上一页
    paginator = Paginator(companyinfo,10,3)
    try:
        # GET请求方式，get()获取指定Key值所对应的value值
        # 获取index的值，如果没有，则设置使用默认值1
        num = request.GET.get('index','1')
        # 获取第几页
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是整数，那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)


    context = {"userinfo":userinfo[0],'page':number,'paginator':paginator}
    return render(request,'monitor/company/listinfo.html',context)

def addinfo(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    context = {"userinfo":userinfo[0]}#,"tasklist_json":tasklist_json,"input_search_field":input_search_field,"input_keyword":input_keyword, 'page':number,'paginator':paginator}
    if request.method == "POST":
        input_company=request.POST.get('company',None)
        input_product=request.POST.get('product',None)
        input_buy_time=request.POST.get('buy_time',None)
        input_price=request.POST.get('price',None)
        input_exprie_time=request.POST.get('exprie_time',None)
        input_application=request.POST.get('application',None)
        input_num=request.POST.get('num',None)
        input_urladdress=request.POST.get('urladdress',None)
        newinfo = company(
            company=input_company,
            product=input_product,
            price=input_price,
            buy_time=input_buy_time,
            exprie_time=input_exprie_time,
            application=input_application,
            num=input_num,
            urladdress=input_urladdress,
        ) 
        newinfo.save()
        return HttpResponseRedirect('monitor/company/listinfo.html',context)
    
    return render(request,'monitor/company/addinfo.html',context)

def editinfo(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    input_id = request.GET.get('edit_id',None)
    companyinfo = company.objects.all().filter(id=input_id)
    context = {"userinfo":userinfo[0]}
    
    if request.method == "POST":
        input_company=request.POST.get('company',None)
        input_product=request.POST.get('product',None)
        input_buy_time=request.POST.get('buy_time',None)
        input_price=request.POST.get('price',None)
        input_exprie_time=request.POST.get('exprie_time',None)
        input_application=request.POST.get('application',None)
        input_num=request.POST.get('num',None)
        input_urladdress=request.POST.get('urladdress',None)
        companyinfo.update(company=input_company, product=input_product, price=input_price, buy_time=input_buy_time, exprie_time=input_exprie_time, application=input_application, num=input_num, urladdress=input_urladdress)
        return HttpResponseRedirect('monitor/company/listinfo.html',context)
    context = {"userinfo":userinfo[0],"companyinfo":companyinfo}
    return render(request,'monitor/company/editinfo.html',context)

def delinfo(request):
    username = request.session.get("username", None)
    userinfo = UserInfo.objects.filter(username=username)
    infolist = company.objects.all()
    """获取复选框内容"""
    check_box_list = request.GET.getlist('ids[]')
    print(check_box_list)
    """获取id对象"""
    for input_id in check_box_list:
        """获取id的对象"""
        companyinfo = company.objects.filter(id=input_id)
        companyinfo.delete()
    context = {"userinfo":userinfo[0],"companyinfo":companyinfo}
    return HttpResponseRedirect('/monitor/company/listinfo',context)
