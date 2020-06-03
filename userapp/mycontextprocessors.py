#encoding=utf-8
# 全局上下文的特点是，参数是request，返回值是dict,无论哪个页面，templates页面都能共享这部分信息
def getUserInfo(request):
    return {'suser':request.session.get('user',None)}