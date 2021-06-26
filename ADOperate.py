# coding=utf-8
from ini import *

#解锁账号
def user_unlock(account):
  try:
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #先检查用户是否存在(无实际性能提升)
    #if user_check(account) == 1 :
    #    raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = ' Unlock-ADAccount {0} '.format(account)

    #解锁账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = "{0}\n{1} 账号解锁成功".format(optime,account) 
        #print(log)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0}\n{1} 账号解锁失败\n{2}".format(optime,account,result)
    cmd = "{0} | Out-File -Append {1}".format(log.replace("\n"," "),unlock_log_path)
    s.run_ps(cmd)
    return log

  except Exception as e:
    #print(traceback.format_exc())
    #添加optime,避免内容重复导致无法推送
    return "{0}\n{1}".format(optime,str(e))

#重置密码
def user_resetpw(account):
  try:
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #先检查所申请的账号是否已经存在
    if user_check(account) == 1 :
        raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = 'Set-ADAccountPassword -Reset {0} -NewPassword (ConvertTo-SecureString -AsPlainText "{1}" -Force) ; \
            Unlock-ADAccount {0} '.format(account,passwd)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ) :

        log = "{0}\n{1} 密码已重置为{2}".format(optime,account,passwd) 
    else :
        result = r.std_err.decode().splitlines()[0]
        log = "{0}\n{1} 重置密码失败\n{2}".format(optime,account,result)
    cmd = "{0} | Out-File -Append {1}".format(log.replace("\n"," "),pwchange_log_path)
    s.run_ps(cmd)
    return log

  except Exception as e:
    #print(traceback.format_exc())
    #添加optime,避免内容重复导致无法推送
    return "{0}\n{1}".format(optime,str(e))

#创建账户
def user_create(account,dept,title):
  try:
      optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
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
      if user_check(account) == 0 :
          raise ValueError("邮箱账号已存在,请联系IT处理")
      #构建powershell命令,此处同时设定了密码永不过期
      cmd = ' New-ADUser -Name {0} -SamAccountName {0} -DisplayName {0} \
              -EmailAddress "{0}@makrochina.com" -UserPrincipalName "{0}@makrochina.com" \
              -Surname {1} -GivenName {2} \
              -Department {3} -Office {4} -Title {5} \
              -Company "Makro - China" -Country "CN" \
              -Path "{6},OU=Users,OU=MakroChinaGZ,DC=makrochina,DC=com" \
              -AccountPassword (ConvertTo-SecureString -AsPlainText "{7}" -Force) \
              -PasswordNeverExpires 1 -Enabled 1 ' \
              .format(account,surname,givenname,dept,office,title,OU,passwd)
      group_addmember_result = ""
      passwd_result = ""

      #创建账号
      s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
      r = s.run_ps(cmd)
      #账号创建成功后添加对应的用户组
      if ( r.status_code == 0 ):
          log = "{0}\n{1} 账号创建成功".format(optime,account)
          group = "MKCN {0}".format(dept).strip()
          group_addmember_result = group_addmember(account,group)
          passwd_result = "初始密码 : {0}".format(passwd)
      else :
          result = r.std_err.decode().splitlines()[0]
          log = "{0}\n{1} 账号创建失败\n{2}".format(optime,account,result)
      cmd = "{0} | Out-File -Append {1}".format(log.replace("\n"," "),user_log_path)
      s.run_ps(cmd)
      return log+"\n"+passwd_result+"\n"+group_addmember_result

  except Exception as e:
    print(traceback.format_exc())
    #添加optime,避免内容重复导致无法推送
    return "{0}\n{1}".format(optime,str(e))

#删除用户
def user_remove(account):
  try:
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #生成powershell命令以及获取当前时间
    cmd = 'Remove-ADUser {0} -Confirm:0'.format(account)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = "{0}\n{1} 用户已删除".format(optime,account)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0}\n{1} 用户删除失败\n{2}".format(optime,account,result)
    cmd = "{0} | Out-File -Append {1}".format(log.replace("\n"," "),user_log_path)
    s.run_ps(cmd) 
    return log

  except Exception as e:
    #print(traceback.format_exc())
    #添加optime,避免内容重复导致无法推送
    return "{0}\n{1}".format(optime,str(e))

#检查用户是否存在
def user_check(account):
    try:
        optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #构建ps命令
        cmd = ' Get-ADUser {0} '.format(account)
        s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
        r = s.run_ps(cmd)
        if ( r.status_code == 0 ):
            #print("已存在的用户")
            return 0
        else :
            result=r.std_err.decode().splitlines()[0]
            #print(result)
            return 1
    except Exception as e:
        #print(traceback.format_exc())
        #添加optime,避免内容重复导致无法推送
        return "{0}\n{1}".format(optime,str(e))

#添加用户组
def group_addmember(account,group):
  try:
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if user_check(account) == 1 :
        raise ValueError('未找到该账号,请检查输入')
    #生成powershell命令以及获取当前时间
    cmd = ' Add-ADGroupMember -Members {0} -Identity "{1}" '.format(account,group)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
 
    if ( r.status_code == 0 ):
        log = "{0}\n{1} 已添加到用户组 {2}".format(optime,account,group)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0}\n{1} 无法添加到用户组 {2}\n{3}".format(optime,account,group,result)
    cmd = "{0} | Out-File -Append {1}".format(log.replace("\n"," "),group_log_path)
    s.run_ps(cmd)
    return log

  except Exception as e:
    #print(traceback.format_exc())
    #添加optime,避免内容重复导致无法推送
    return "{0}\n{1}".format(optime,str(e))

#移除用户组
def group_removemember(account,group):
  try:
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #生成powershell命令以及获取当前时间
    cmd = ' Remove-ADGroupMember -Members {0} -Identity "{1}" -Confirm:0 '.format(account,group)
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = "{0}\n{1} 已移除用户组 {2}".format(optime,account,group)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = "{0}\n{1} 无法移除用户组 {2}\n{3}".format(optime,account,group,result)
    cmd = "{0} | Out-File -Append {1}".format(log.replace("\n"," "),group_log_path)
    s.run_ps(cmd)
    return log

  except Exception as e:
    #print(traceback.format_exc())
    #添加optime,避免内容重复导致无法推送
    return "{0}\n{1}".format(optime,str(e))

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

