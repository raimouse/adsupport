from Conf import *

#解锁账号
def user_unlock(account):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Unlock-ADAccount {0} '.format(account)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    #解锁账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
    if ( r.status_code == 0 ):
        log = ' "{0} {1} 账号解锁成功" | Out-File -Append {2} '.format(optime,account,unlock_log_path)
        s.run_ps(log)
        return "{0} {1} 账号解锁成功".format(optime,account)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 账号解锁失败:{2}" | Out-File -Append {3} '.format(optime,account,result,unlock_log_path)
        s.run_ps(log)
        return " {0} {1} 账号解锁失败:{2}".format(optime,account,result)
  except Exception as e:
    return traceback.format_exc()

#重置密码
def user_resetpw(account):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Set-ADAccountPassword -Reset {0} -NewPassword (ConvertTo-SecureString -AsPlainText "{1}" -Force) ' \
         .format(account,passwd)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #连接AD并执行命令
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
    if ( r.status_code == 0 ) :
        #生成日志以及审批流
        log = ' "{0} {1} 密码已重置为:{2}" | Out-File -Append {3} '.format(optime,account,passwd,pwchange_log_path)
        s.run_ps(log)
        return "{0} {1} 密码已重置为:{2}".format(optime,account,passwd)
    else :
        #只生成日志
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 重置密码失败:{2}" | Out-File -Append {3} '.format(optime,account,result,pwchange_log_path)
        s.run_ps(log)
        #输出错误信息
        return "{0} {1} 重置密码失败:{2}".format(optime,account,result)
  except Exception as e:
    return traceback.format_exc()

#创建账户
def user_create(account,dept,office,jobtitle):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' New-ADUser -Name {0} -SamAccountName {0} -DisplayName {0} \
            -EmailAddress "{0}@makrochina.com" -UserPrincipalName "{0}@makrochina.com" \
            -Surname {1} -GivenName {2} \
            -Department {3} -Office {4} -Title {5} \
            -Company "Makro - China" -Country "CN" \
            -Path "OU={3},OU={4},OU=Users,OU=MakroChinaGZ,DC=makrochina,DC=com" \
            -AccountPassword (ConvertTo-SecureString -AsPlainText "{6}" -Force) \
            -PasswordNeverExpires 1 -Enabled 1 ' \
            .format(account,account.split('.')[0],account.split('.')[1],dept,office,jobtitle,passwd)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    #创建账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
    if ( r.status_code == 0 ):
        log = ' "{0} {1} 账号创建成功" | Out-File -Append {2} '.format(optime,account,user_log_path)
        s.run_ps(log)
        return "{0} {1} 账号创建成功".format(optime,account)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 账号创建失败:{2}" | Out-File -Append {3} '.format(optime,account,result,user_log_path)
        s.run_ps(log)
        return " {0} {1} 账号创建失败:{2} ".format(optime,account,result)
  except Exception as e:
    return traceback.format_exc()

#删除用户
def user_delete(account):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Remove-ADUser {0} -Confirm:0 '.format(account)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    #创建账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
    if ( r.status_code == 0 ):
        log = ' "{0} {1} 用户已删除 " | Out-File -Append {2} '.format(optime,account,user_log_path)
        s.run_ps(log)
        return " {0} {1} 用户已删除 ".format(optime,account)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 无法删除用户:{2} " | Out-File -Append {3} '.format(optime,account,result,user_log_path)
        s.run_ps(log)
        return " {0} {1} 无法删除用户:{2} ".format(optime,account,result)
  except Exception as e:
    return traceback.format_exc()


#添加用户组
def group_add(account,group):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Add-ADGroupMember -Members {0} -Identity "{1}" '.format(account,group)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
 
    #创建账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
    if ( r.status_code == 0 ):
        log = ' "{0} {1} 已添加到用户组 {2}" | Out-File -Append {3} '.format(optime,account,group,group_log_path)
        s.run_ps(log)
        return "{0} {1} 已添加到用户组 {2}".format(optime,account,group)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 无法添加到用户组 {2}:{3}" | Out-File -Append {4} '.format(optime,account,group,result,group_log_path)
        s.run_ps(log)
        return "{0} {1} 无法添加到用户组 {2}:{3}".format(optime,account,group,result)
  except Exception as e:
    return traceback.format_exc()
