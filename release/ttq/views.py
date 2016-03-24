from django.shortcuts import render
import os, time, paramiko, multiprocessing
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from multiprocessing import Pool, Process, Queue
from django.http import JsonResponse


rmuploads = 'rm -rf /buddy/release/uploads/*'         #清空上传目录
uploadpath = '/buddy/release/uploads/'                #发布服务器上传路径
remoteserverpath = '/data/yunwei/update'              #应用服务器更新包暂存路径
# releaseshell = 'sh /data/yunwei/shell/njw_update.sh'  #发布脚本


#single ssh函数(循环备份用)

def single_sshd(ip,port,commd):
        ssh = paramiko.SSHClient()
        pkey='/root/.ssh/id_rsa'
        key = paramiko.RSAKey.from_private_key_file(pkey)
        ssh.load_system_host_keys()
        ssh.connect(ip,port,'root',pkey=key)
        stdin, stdout, stderr = ssh.exec_command(commd)  
        results = stdout.readlines() + stderr.readlines()
        stdstr =ip + '\n' + ' ' + ' '.join(results)
        return stdstr



#ssh连接函数
def sshd(q,ip,port,commd):
	ssh = paramiko.SSHClient()
	pkey='/root/.ssh/id_rsa'
	key = paramiko.RSAKey.from_private_key_file(pkey)
	ssh.load_system_host_keys()
	ssh.connect(ip,port,'root',pkey=key)
	stdin, stdout, stderr = ssh.exec_command(commd)  
	results = stdout.readlines() + stderr.readlines()
	stdstr =ip + '\n' + ' ' + ' '.join(results)	
	q.put(stdstr)

# 多线程队列读取
def readresult(q):
	while True:
		if not q.empty():
			value = q.get(True)
			return value
		else:
			value = 'time out'
			return value
			break

# 多线程执行命令
def multiconn(form):
	ipaddr = form.cleaned_data['ipaddr']
	commd = form.cleaned_data['commd']
	port = form.cleaned_data['port']
	pool = Pool(6)
	manager = multiprocessing.Manager()
	q = manager.Queue()

	for cleanip in ipaddr:		
		ip =str(cleanip)
		#调用ssh连接
		pool.apply_async(sshd, args=(q,ip,port,commd,))
	time.sleep(3)
	pool.close()
	pool.join()
	value =''
	for cleanip in ipaddr:
		value += readresult(q) + '\n'
	return value

#命令执行视图
@login_required
def commexec(request):
	if request.method == 'POST':
		form = CommForm(request.POST)
		if form.is_valid():
			#获取表单数据
			value = multiconn(form)
			# # #保存命令结果到数据库
			post = form.save(commit=False)
			post.results = value
			post.exec_date = timezone.now()
			post.user = request.user
			post.save()			
			return redirect('ttq.views.ret_results',pk=post.pk)
			# return HttpResponse(value)
	else:
		form = CommForm()
		return render(request,'ttq/index.html',{'form':form})


#结果展示视图
@login_required
def ret_results(request,pk):
	if request.method == "POST":
		form = CommForm(request.POST)
		if form.is_valid():
			#获取表单数据
			value = multiconn(form)
			# #保存命令结果到数据库
			post = form.save(commit=False)
			post.results = value
			post.exec_date = timezone.now()
			post.user = request.user
			post.save()			
			#重定向到结果展示视图
			return redirect('ttq.views.ret_results',pk=post.pk)
	else:
		#从数据库获取命令执行结果并传给表单实例进行展示
		results = Hostname.objects.get(pk=pk)
		form = CommForm(instance=results)
	return render(request,'ttq/index.html',{'form':form})


#上传表单处理视图
def uploads_form_del(form,uf):
	filename = form.cleaned_data['filename']
	remoteIP = form.cleaned_data['remoteIP']
	remoteDir = form.cleaned_data['remoteDir']
	ip = ''
	for rip in remoteIP:
		ip += str(rip) + ' '
	#保存文件title及路径到数据库
	uf.destIPs = ip
	uf.filename = filename
	uf.upload_time = timezone.now()
	uf.remoteDir = remoteDir
	uf.save()

#多进程上传
def ftp(localpath,remotefile,lips,port):
	t = paramiko.Transport((lips,port))
	pkey='/root/.ssh/id_rsa'
	key = paramiko.RSAKey.from_private_key_file(pkey)
	t.connect(username='root',pkey=key)
	sftp = paramiko.SFTPClient.from_transport(t)
	#传到远程服务器
	sftp.put(localpath,remotefile,confirm=True)	

#文件上传视图
@login_required
def uploads_file(request):
	if request.method == "POST":
		form = UploadsForm(request.POST,request.FILES)
		if form.is_valid():
			os.system(rmuploads)  #删除服务器上传目录下的文件，避免文件重复造成的重命名
			uf = Uploads()
			uf.user = request.user		
			uploads_form_del(form,uf)
			# return HttpResponse(filename)
			return redirect ('ttq.views.send_to_server',pk=uf.pk)
	else:
		form = UploadsForm()
		h_list = Hostlist.objects.all()
	return render(request,'ttq/uploads.html',{'form':form,'h_list':h_list})		

#结果显示 及 继续上传
@login_required
def send_to_server(request,pk):
	if request.method == "POST":
		form = UploadsForm(request.POST,request.FILES)
		if form.is_valid():
			os.system(rmuploads)
			uf = Uploads()
			uf.user = request.user		
			uploads_form_del(form,uf)			
			return redirect ('ttq.views.send_to_server',pk=uf.pk)
	else:
		results = Uploads.objects.get(pk=pk)
		#远程文件完整路径
		localpath=str(results.filename)
		remotepath=str(results.remoteDir)
		localfile_list = localpath.split('/')
		remotefile_name = localfile_list[-1]
		remotefile = remotepath+'/'+remotefile_name
		#远程文件完整路径保存到数据库
		results.remotefile = remotefile
		results.save()
		dips = str(results.destIPs)
		ips = dips.split(' ')
		pool = Pool(6)
		#上传文件传到指定远程服务器
		port = 22
		for ip in range(len(ips)-1):
			lips = ips[ip]
			pool.apply_async(ftp, args=(localpath,remotefile,lips,port,))
		pool.close()
		pool.join()						
		form = UploadsForm()
	return render(request,'ttq/uploads.html',{'form':form,'results':results})	
	# return HttpResponse(lips)

#版本发布、备份
@login_required
def publish(request):
	if request.method == 'POST':
		form = ReleaseForm(request.POST,request.FILES)
		if form.is_valid():
			os.system(rmuploads)  #删除服务器上传目录下的文件，避免文件重复造成的重命名
			uf = Release()
			user = request.user
			filename = form.cleaned_data['zipname']
			project_name = form.cleaned_data['project_name']

			dbpname = ''
			for pname in project_name:
				dbpname += str(pname) + ' '
			#保存到数据库,上传到发布服务器
			uf.user = user
			uf.filename = filename
			uf.release_time = timezone.now()
			uf.project_name = dbpname
			uf.save()


			#多进程上传更新包到应用服务器
			localpath = uploadpath+str(filename)   #发布服务器路径
			remotepath = remoteserverpath					#应用服务器路径
			remotefile = remotepath+'/'+str(filename)

			pool = Pool(6)
			ips = ''
			value =''
			for pname in project_name:
				value = str(pname)
				pro = Projects.objects.get(name=value)
				port = pro.port
				ip = str(pro.ip)
				pool.apply_async(ftp, args=(localpath,remotefile,ip,port,))
			pool.close()
			pool.join()

			zippack = str(filename)
			full_name_list = zippack.split('.')
			first_name = full_name_list[0]

			#发布命令执行
			# commd = releaseshell + ' ' + first_name
			pool = Pool(6)
			manager = multiprocessing.Manager()
			q = manager.Queue()

			for pname in project_name:
				value = str(pname)
				pro = Projects.objects.get(name=value)
				port = pro.port
				ip = str(pro.ip)
				commd = 'sh' + ' ' + str(pro.script) + ' ' + first_name
				#调用ssh连接
				pool.apply_async(sshd, args=(q,ip,port,commd,))
			time.sleep(3)
			pool.close()
			pool.join()
			value =''
			for pname in project_name:
				value += readresult(q) + '\n'
			#结果保存到数据库
			pk = uf.pk
			rel = Release.objects.get(pk=pk)			
			rel.results = value
			rel.filename = str(filename)
			rel.save()

			###### 循环记录备份到数据库
			for pname in project_name:
				value = str(pname)
				pro = Projects.objects.get(name=value)
				port = pro.port
				ip = str(pro.ip)
				backpath = str(pro.back_path)
				commd = 'ls'+' '+ backpath + '/`date +%Y%m%d`|grep zip'
				#调用ssh连接
				value = single_sshd(ip,port,commd)
				time.sleep(1)
				needback = value.split(' ')[-2]

				#结果保存到数据库
				bp = Backup()
				bp.project_name = pname
				bp.backfile = needback
				bp.save()

			# form = ReleaseForm()
			# return HttpResponse(needback)
			# resu = Release.objects.get(pk=pk)
			# form = CommForm(instance=resu)
			return redirect ('ttq.views.publish_result',pk=uf.pk)

	else:
		form = ReleaseForm()
		return render(request,'ttq/release.html',{'form':form})

@login_required
def publish_result(request,pk):
	if request.method == "POST":
		pass
	else:
		resu = Release.objects.get(pk=pk)
		form = CommForm(instance=resu)
		return render(request,'ttq/release_results.html',{'form':form})

@login_required
def release_hist(request):
	re_list = Release.objects.order_by('-id')[:16]
	return render(request,'ttq/release_history.html',{'re_list':re_list})

#测试
def host_list(request):
	h_list = Hostlist.objects.all()

	return render(request,'ttq/host_list.html',{'h_list':h_list})


#回滚
@login_required
def rollback_form(request):
	if request.method == 'POST':
		project = request.POST.get('project')
		backfile = request.POST.get('backfile')
		if project.strip() and backfile != "---------":
			pro = Projects.objects.get(name=project)
			port = pro.port
			ip = str(pro.ip)
			rollback_shell= pro.rollback_shell
			first_name = backfile.split('.')[0]
			back_time =	 backfile.split('.')[3]
			roll_commd = 'sh' + ' ' + rollback_shell + ' ' + first_name + ' ' + back_time
			roll_result = single_sshd(ip,port,roll_commd)
			time.sleep(1)

			#保存Rollback结果到数据库
			rb = Rollback()
			rb.user = request.user
			rb.project_name = project
			rb.backtofile = backfile
			rb.rollback_time = timezone.now()
			rb.results = roll_result
			rb.save()

			return redirect ('ttq.views.rollback_result',pk=rb.pk)
			# return HttpResponse(roll_result)
			# return HttpResponse(project + backfile)
		else:
			return HttpResponse("please selected correctly")
	else:
		form = RollbackForm()
		return render(request,'ttq/rollback.html',{'form':form})
		
#回滚结果
@login_required
def rollback_result(request,pk):
	if request.method == "POST":
		pass
	else:
		resu = Rollback.objects.get(pk=pk)
		form = CommForm(instance=resu)
		return render(request,'ttq/rollback_results.html',{'form':form})

#备份列表
def backfile_list(request):
	rtn = []
	pro_name = request.GET.get('cid')
	backfiles = Backup.objects.filter(project_name=pro_name).order_by('-id')[:6]
	for backfile in backfiles:
		rtn.append(str(backfile))
		# print(rtn)
	return JsonResponse(rtn,safe=False)

