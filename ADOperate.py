# coding=utf-8
from ini import *


#解锁账号
def user_unlock(account):
  try:
    error_code = 1
    #先检查用户是否存在(无实际性能提升)
    if user_check(account) == "False" :
        raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = ' Unlock-ADAccount {0} '.format(account)

    #解锁账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = "{0} 账号解锁成功".format(account) 
        error_code = 0
        #print(log)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0} 账号解锁失败\n{1}".format(account,result)
    adsupport_logger.info(log)
    return { 'log':log,
             'error_code':error_code }

  except Exception as e:
    log = "内部系统错误:{0}".format(str(e))
    adsupport_logger.error(log)
    return { 'log':log,
             'error_code':error_code }

#重置密码
def user_resetpw(account):
  try:
    error_code = 1
    #先检查所申请的账号是否已经存在
    if user_check(account) == "False" :
        raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = 'Set-ADAccountPassword -Reset {0} -NewPassword (ConvertTo-SecureString -AsPlainText "{1}" -Force) ; \
            Unlock-ADAccount {0} '.format(account,passwd)
    
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ) :

        log = "{0} 密码已重置为{1}".format(account,passwd) 
        error_code = 0
    else :
        result = r.std_err.decode().splitlines()[0]
        log = "{0} 重置密码失败\n{1}".format(account,result)
    adsupport_logger.info(log)
    return { 'log':log,
             'error_code':error_code }
  except Exception as e:
    log = "内部系统错误:{0}".format(str(e))
    print(error_code)
    adsupport_logger.error(log)
    return { "log" : log,
             "error_code" : error_code }
    print("kl")

#创建账户
def user_create(account,dept,title):
  try:
      #获取部门信息
      dept_info = get_ou(dept)
      dept = dept_info["dept"]
      office = dept_info["office"]
      OU = dept_info["OU"]
      #门店员工不会创建AD账号
      if dept == "ST01" :
          raise ValueError("门店员工不创建个人邮箱账号\n新建门店邮箱账号请联系IT处理")
      #检查账号格式是否正确
      if ("." in account) :
          surname = account.split('.')[1].strip()
          givenname = account.split('.')[0].strip()
      else :
          raise ValueError("账号格式有误,请检查输入")
      #检查账号是否已经存在
      if user_check(account) == "True" :
          raise ValueError("邮箱账号已存在,请联系IT处理")
      #构建powershell命令,此处同时设定了密码永不过期
      cmd = ' New-ADUser -Name {0} -SamAccountName {0} -DisplayName {0} \
              -EmailAddress "{0}@makrochina.com" -UserPrincipalName "{0}@makrochina.com" \
              -Surname {1} -GivenName {2} \
              -Department {3} -Office {4} -Title "{5}" \
              -Company "Makro - China" -Country "CN" \
              -Path "{6},OU=Users,OU=MakroChinaGZ,DC=makrochina,DC=com" \
              -AccountPassword (ConvertTo-SecureString -AsPlainText "{7}" -Force) \
              -PasswordNeverExpires 1 -Enabled 1 ' \
              .format(account,surname,givenname,dept,office,title,OU,passwd)
      group_addmember_result = ""
      group_addmember_result2 = ""
      passwd_result = ""

      #创建账号
      s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
      r = s.run_ps(cmd)
      #账号创建成功后添加对应的用户组
      if ( r.status_code == 0 ):
          log = "{0} 账号创建成功".format(account)
          group = "MKCN {0}".format(dept).strip()
          group_addmember_result = group_addmember(account,group)
          group_addmember_result2 = group_addmember(account,"MKCN")
          passwd_result = "初始密码 : {0}".format(passwd)
      else :
          result = r.std_err.decode().splitlines()[0]
          log = "{0} 账号创建失败\n{1}".format(account,result)
      adsupport_logger.info(log)
      return log+"\n"+passwd_result+"\n"+group_addmember_result+"\n"+group_addmember_result2

  except Exception as e:
    log = "内部系统错误:{0}".format(str(e))
    adsupport_logger.error(log)
    return log

#删除用户
def user_remove(account):
  try:
    if user_check(account) == "False" :
        raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = 'Remove-ADUser {0} -Confirm:0'.format(account)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = "{0} 用户删除成功".format(account)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0} 用户删除失败\n{1}".format(account,result)
    adsupport_logger.info(log)
    return log

  except Exception as e:
    log = "内部系统错误:{0}".format(str(e))
    adsupport_logger.error(log)
    return log

#检查用户是否存在
def user_check(account):
    try:
        #构建ps命令
        cmd = ' Get-ADUser {0} '.format(account)
        s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
        r = s.run_ps(cmd)
        if ( r.status_code == 0 ):
            return "True"
        else :
            result=r.std_err.decode().splitlines()[0]
            return "False"
    except Exception as e:
    	log = "内部系统错误:{0}".format(str(e))
    	adsupport_logger.error(log)
    	return log

#添加用户组
def group_addmember(account,group):
  try:
    if user_check(account) == "False" :
        raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = ' Add-ADGroupMember -Members {0} -Identity "{1}" '.format(account,group)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
 
    if ( r.status_code == 0 ):
        log = "{0} 已添加到用户组 {1}".format(account,group)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0} 无法添加到用户组 {1}\n{2}".format(account,group,result)
    adsupport_logger.info(log)
    return log

  except Exception as e:
    log = "内部系统错误:{0}".format(str(e))
    adsupport_logger.error(log)
    return log

#移除用户组
def group_removemember(account,group):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Remove-ADGroupMember -Members {0} -Identity "{1}" -Confirm:0 '.format(account,group)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = "{0} 已移除用户组 {1}".format(account,group)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0} 无法移除用户组 {1}\n{2}".format(account,group,result)
    adsupport_logger.info(log)
    return log

  except Exception as e:
    log = "内部系统错误:{0}".format(str(e))
    adsupport_logger.error(log)
    return log

#添加Admins组
def group_addAdmins(account,scheduler):
    '''
    :param string account : ad账号
    :param scheduler      : flask_scheduler实例
    '''
    try:
        error_code = 1
        if user_check(account) == "False" :
            raise ValueError('未找到该账号,请检查输入')
        #生成powershell命令以及获取当前时间
        cmd = ' Add-ADGroupMember -Identity "Domain Admins" -Members {0} ; \
                Set-ADUser -Identity {0} -Replace @{{primarygroupid=512}} '.format(account)

        s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
        r = s.run_ps(cmd)
        if ( r.status_code == 0 ):
            error_code = 0
            log = "{0} 权限处理成功\n请注销或重启电脑\n权限有效期30分钟\n注:可能需要注销多次".format(account)
            #添加定时任务回收权限
            job_id = "removeAdmins:{0}".format(account)
            start_time=(datetime.datetime.now()+datetime.timedelta(minutes=30))
            scheduler.add_job(job_id,group_removeAdmins,args=[account],trigger='date',run_date=start_time)
        else :
            result=r.std_err.decode().splitlines()[0]
            log = "{0} 权限处理失败,请联系IT处理\n{1}".format(account,result)
        adsupport_logger.info(log)
        return { "log" : log,
                 "error_code" : error_code}
    except Exception as e:
        log = "内部系统错误:{0}".format(str(e))
        adsupport_logger.error(log)
        return { "log" : log,
                 "error_code" : error_code}

#移除Admins组
def group_removeAdmins(account):
    try:
        if user_check(account) == "False" :
            raise ValueError('未找到该账号,请检查输入')
        cmd = 'Set-ADUser -Identity {0} -Replace @{{primarygroupid=513}} ; \
               Remove-ADGroupMember -Identity "Domain Admins" -Members {0} -Confirm:0 '.format(account)
        
        s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
        r = s.run_ps(cmd)
        if ( r.status_code == 0 ):
            log = "{0} 移除Admins组成功".format(account)
        else :
            result=r.std_err.decode().splitlines()[0]
            log = "{0} 移除Admins组失败\n{1}".format(account,result)
        adsupport_logger.info(log)
        return log
    except Exception as e:
        log = "内部系统错误:{0}".format(str(e))
        adsupport_logger.error(log)
        return log

#解锁usb权限
def enableusb(account,scheduler):
    '''
    :param string account : ad账号
    :param scheduler      : flask_scheduler实例
    '''
    try:
        error_code = 1
        if user_check(account) == "False" :
            raise ValueError('未找到该账号,请检查输入')
        #生成powershell命令以及获取当前时间
        cmd = ' Add-ADGroupMember -Identity "EnableUSB" -Members {0} '.format(account)

        s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
        r = s.run_ps(cmd)
        if ( r.status_code == 0 ):
            error_code = 0
            log = "{0} 权限处理成功\n请注销或重启电脑\n权限有效期120分钟\n注:可能需要注销多次".format(account)
            #添加定时任务回收权限
            job_id = "disableUSB:{0}".format(account)
            start_time=(datetime.datetime.now()+datetime.timedelta(minutes=120))
            scheduler.add_job(job_id,disableusb,args=[account],trigger='date',run_date=start_time)
        else :
            result=r.std_err.decode().splitlines()[0]
            log = "{0} 权限处理失败,请联系IT处理\n{1}".format(account,result)
        adsupport_logger.info(log)
        return { "log" : log,
                 "error_code" : error_code}
    except Exception as e:
        log = "内部系统错误:{0}".format(str(e))
        adsupport_logger.error(log)
        return { "log" : log,
                 "error_code" : error_code}

#移除USB权限
def disableusb(account):
    try:
        if user_check(account) == "False" :
            raise ValueError('未找到该账号,请检查输入')
        cmd = ' Remove-ADGroupMember -Identity "EnableUSB" -Members {0} -Confirm:0 '.format(account)
        
        s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
        r = s.run_ps(cmd)
        if ( r.status_code == 0 ):
            log = "{0} 移除USB权限成功".format(account)
        else :
            result=r.std_err.decode().splitlines()[0]
            log = "{0} 移除USB权限失败\n{1}".format(account,result)
        adsupport_logger.info(log)
        return log
    except Exception as e:
        log = "内部系统错误:{0}".format(str(e))
        adsupport_logger.error(log)
        return log

#构建ou
def get_ou(dept):
    #部门列表
    dept_it = ["IT","Infrastructure","ERP","Digital"]
    dept_hr = ["HR"]
    dept_fa = ["FA"]
    dept_cm = ["CM","Fresh","Dry & Non Food"]
    dept_mk = ["MKCD","MK（MM）","MK2","MK3（电商）"]
    dept_md = ["MD","BD"]
    dept_op = ["OP","KA"]
    dept_ST01 = ["1001 花都迎宾店","CD","ALC","水产","冷冻冷藏","果蔬","肉类","收银部","收货","干货","配送","GA"]

    office = "HQ"

    if  dept in dept_it :
        dept = "IT"
        ou = "OU=IT,OU=HQ"
    elif dept in dept_hr :
        dept = "HR"
        ou = "OU=HR,OU=HQ"
    elif dept in dept_fa :
        dept = "FA"
        ou = "OU=FA,OU=HQ"
    elif dept in dept_cm :
        dept = "CM"
        ou = "OU=CM,OU=HQ"
    elif dept in dept_mk :
        dept = "MK"
        ou = "OU=MKT,OU=HQ"
    elif dept in dept_md :
        dept = "MD"
        ou = "OU=MD,OU=HQ"
    elif dept in dept_op :
        dept = "OP"
        ou = "OU=OPTN,OU=HQ"
    elif dept in dept_ST01 :
        dept = "ST01"
        ou = "OU=ST01"
        office = "ST01"
    else :
        #默认OU为HQ,默认部门为IT
        ou = "OU=HQ"
        dept = "IT"

    return { "OU" : ou , "office" : office , "dept" : dept }

