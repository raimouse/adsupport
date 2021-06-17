from ini import *

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
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 账号解锁失败:{2}" | Out-File -Append {3} '.format(optime,account,result,unlock_log_path)
    s.run_ps(log)
    return log.split("|")[0]

  except Exception as e:
    return traceback.format_exc()

#重置密码
def user_resetpw(account):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Set-ADAccountPassword -Reset {0} -NewPassword (ConvertTo-SecureString -AsPlainText "{1}" -Force) ' \
         .format(account,passwd)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ) :
        log = ' "{0} {1} 密码已重置为:{2}" | Out-File -Append {3} '.format(optime,account,passwd,pwchange_log_path)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 重置密码失败:{2}" | Out-File -Append {3} '.format(optime,account,result,pwchange_log_path)
    s.run_ps(log)
    return log.split("|")[0]

  except Exception as e:
    return traceback.format_exc()

#创建账户
def user_create(account,dept,title):
  try:
    #将钉钉的dept转换为ad对应的dept
    dept_info = get_ou(dept)
    dept = dept_info["dept"]
    office = dept_infoou["office"]
    OU = dept_info["OU"]
    #构建powershell命令
    cmd = ' New-ADUser -Name {0} -SamAccountName {0} -DisplayName {0} \
            -EmailAddress "{0}@makrochina.com" -UserPrincipalName "{0}@makrochina.com" \
            -Surname {1} -GivenName {2} \
            -Department {3} -Office {4} -Title {5} \
            -Company "Makro - China" -Country "CN" \
            -Path "{6},OU=Users,OU=MakroChinaGZ,DC=makrochina,DC=com" \
            -AccountPassword (ConvertTo-SecureString -AsPlainText "{7}" -Force) \
            -PasswordNeverExpires 1 -Enabled 1 ' \
            .format(account,account.split('.')[1],account.split('.')[0],dept,office,title,OU,passwd)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    group_add__result = ""
    
    #创建账号
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
    #账号创建成功后添加对应的用户组
    if ( r.status_code == 0 ):
        log = ' "{0} {1} 账号创建成功" | Out-File -Append {2} '.format(optime,account,user_log_path)
        group = "MKCN {0}".format(dept)
        group_add_result = group_add(account,group)
    else :
        result = r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 账号创建失败:{2}" | Out-File -Append {3} '.format(optime,account,result,user_log_path)
    s.run_ps(log)
    return log.split("|")[0]+"\n"+group_add_result

  except Exception as e:
    return traceback.format_exc()

#删除用户
def user_remove(account):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Remove-ADUser {0} -Confirm:0 '.format(account)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = ' "{0} {1} 用户已删除 " | Out-File -Append {2} '.format(optime,account,user_log_path)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 无法删除用户:{2} " | Out-File -Append {3} '.format(optime,account,result,user_log_path)
    s.run_ps(log) 
    return log.split("|")[0]

  except Exception as e:
    return traceback.format_exc()


#添加用户组
def group_add(account,group):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Add-ADGroupMember -Members {0} -Identity "{1}" '.format(account,group)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)
 
    if ( r.status_code == 0 ):
        log = ' "{0} {1} 已添加到用户组 {2}" | Out-File -Append {3} '.format(optime,account,group,group_log_path)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 无法添加到用户组 {2}:{3}" | Out-File -Append {4} '.format(optime,account,group,result,group_log_path)
    s.run_ps(log)
    return log.split("|")[0]

  except Exception as e:
    return traceback.format_exc()

#移除用户组
def group_remove(account,group):
  try:
    #生成powershell命令以及获取当前时间
    cmd = ' Remove-ADGroupMember -Members {0} -Identity "{1}" -Confirm:0 '.format(account,group)
    optime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    s = winrm.Session(ad_server,auth=(ad_admin,ad_admin_pw))
    r = s.run_ps(cmd)

    if ( r.status_code == 0 ):
        log = ' "{0} {1} 已移除用户组 {2}" | Out-File -Append {3} '.format(optime,account,group,group_log_path)
    else :
        result=r.std_err.decode().splitlines()[0]
        log = ' "{0} {1} 无法移除用户组 {2}:{3}" | Out-File -Append {4} '.format(optime,account,group,result,group_log_path)
    s.run_ps(log)
    return log.split("|")[0]

  except Exception as e:
    return traceback.format_exc()

#构建ou
def get_ou(dept):
    #部门列表
    #dept_it = ["IT","IT-Infrastructure","IT-ERP","IT-Digital"]
    #dept_hr = ["HR"]
    #dept_fa = ["FA"]
    #dept_cm = ["CM","CM-Fresh","CM-Dry & Non Food"]
    #dept_mk = ["MKCD","MKCD-MK（MM","MKCD-MK2","MKCD-MK3（电商）"]
    #dept_md = ["MD","MD-BD"]
    #dept_op = ["OP"]
    #默认office为HQ
    office = "HQ"
    if   "IT" in dept :
        dept = "IT"
        ou = "OU=IT,OU=HQ"
    elif "HR" in dept :
        dept = "HR"
        ou = "OU=HR,OU=HQ"
    elif "FA" in dept :
        dept = "FA"
        ou = "OU=FA,OU=HQ"
    elif "CM" in dept :
        dept = "CM"
        ou = "OU=CM,OU=HQ"
    elif "MK" in dept :
        dept = "MKT"
        ou = "OU=MKT,OU=HQ"
    elif "MD" in dept :
        dept = "MD"
        ou = "OU=MD,OU=HQ"
    elif "KA" in dept :
        dept = "OPTN"
        ou = "OU=OPTN,OU=HQ"
    elif "OP" == dept :
        dept = "OPTN"
        ou = "OU=OPTN,OU=HQ"
    elif "1001" in dept :
        dept = "ST01"
        ou = "OU=ST01"
        office = "ST01"

    return { "OU" : ou , "office" : office , "dept" : dept }

