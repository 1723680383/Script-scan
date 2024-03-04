import json
import re
import requests
import sys
import os

def scan_findinfo() -> list[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}

    fileurl = "/findinfo/JS"

    filemkdir = fileurl.split('_')[0]
    if not os.path.exists(filemkdir):
        os.makedirs(filemkdir)

    #get path + 路径名称
    paths = []
    for dirpath, dirnames, filenames in os.walk('./' + filemkdir):
        for file in filenames:
            try:
                with open("./" + filemkdir + "/" + file, "r", encoding='gb18030', errors='ignore') as f2:
                    lines = f2.readlines()
                for line in lines:
                    line = line.strip('\n').strip('\t')
                    matches = re.findall(r'(?i)((access_key|username|user|jwtkey|jwt_key|AESKEY|AES_KEY|appsecret|app_secret|access_token|password|admin_pass|admin_user|algolia_admin_key|algolia_api_key|alias_pass|alicloud_access_key|amazon_secret_access_key|amazonaws|ansible_vault_password|aos_key|api_key|api_key_secret|api_key_sid|api_secret|api\.googlemaps\s+AIza|apidocs|apikey|apiSecret|app_debug|app_id|app_key|app_log_level|app_secret|appkey|appkeysecret|application_key|appspot|auth_token|authorizationToken|authsecret|aws_access|aws_access_key_id|aws_bucket|aws_key|aws_secret|aws_secret_key|aws_token|AWSSecretKey|b2_app_key|bashrc\ password|bintray_apikey|bintray_gpg_password|bintray_key|bintraykey|bluemix_api_key|bluemix_pass|browserstack_access_key|bucket_password|bucketeer_aws_access_key_id|bucketeer_aws_secret_access_key|built_branch_deploy_key|bx_password|cache_driver|cache_s3_secret_key|cattle_access_key|cattle_secret_key|certificate_password|ci_deploy_password|client_secret|client_zpk_secret_key|clojars_password|cloud_api_key|cloud_watch_aws_access_key|cloudant_password|cloudflare_api_key|cloudflare_auth_key|cloudinary_api_secret|cloudinary_name|codecov_token|config|conn\.login|connectionstring|consumer_key|consumer_secret|credentials|cypress_record_key|database_password|database_schema_test|datadog_api_key|datadog_app_key|db_password|db_server|db_username|dbpasswd|dbpassword|dbuser|deploy_password|digitalocean_ssh_key_body|digitalocean_ssh_key_ids|docker_hub_password|docker_key|docker_pass|docker_passwd|docker_password|dockerhub_password|dockerhubpassword|dot-files|dotfiles|droplet_travis_password|dynamoaccesskeyid|dynamosecretaccesskey|elastica_host|elastica_port|elasticsearch_password|encryption_key|encryption_password|env\.heroku_api_key|env\.sonatype_password|eureka\.awssecretkey)\s*[:=><]{1,2}\s*[\"\']{0,1}([0-9a-zA-Z\-_=+/]{8,64})[\"\']{0,1})', line)
                    for match in matches:
                        paths.append(file + "---" + str(match[0]))

                    matches = re.findall(r'''(['"]\s*(?:GOOG[\w\W]{10,30}|AZ[A-Za-z0-9]{34,40}|AKID[A-Za-z0-9]{13,20}|AKIA[A-Za-z0-9]{16}|IBM[A-Za-z0-9]{10,40}|OCID[A-Za-z0-9]{10,40}|LTAI[A-Za-z0-9]{12,20}|AK[\w\W]{10,62}|AK[A-Za-z0-9]{10,40}|AK[A-Za-z0-9]{10,40}|UC[A-Za-z0-9]{10,40}|QY[A-Za-z0-9]{10,40}|KS3[A-Za-z0-9]{10,40}|LTC[A-Za-z0-9]{10,60}|YD[A-Za-z0-9]{10,60}|CTC[A-Za-z0-9]{10,60}|YYT[A-Za-z0-9]{10,60}|YY[A-Za-z0-9]{10,40}|CI[A-Za-z0-9]{10,40}|gcore[A-Za-z0-9]{10,30})\s*['"])''', line)
                    for match in matches:
                        paths.append(file + "---" + str(match))

                    matches = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', line)
                    for match in matches:
                        paths.append(file + "---" + str(match))

                    matches = re.findall(r'(?<!\d)(13\d{9}|14[579]\d{8}|15[^4\D]\d{8}|166\d{8}|17[^49\D]\d{8}|18\d{9}|19[189]\d{8})(?!\d)', line)
                    for match in matches:
                        paths.append(file + "---" + str(match))

                    matches = re.findall(r'\b\d{17}[\dXx]|\b\d{14}\d{1}|\b\d{17}[\dXx]', line)
                    for match in matches:
                        paths.append(file + "---" + str(match))

                    matches = re.findall(r'\d+\.\d+\.\d+\.\d+', line)
                    for match in matches:
                        paths.append(file + "---" + str(match))
            except Exception as e:
                print("发生错误")


    for var in (vars := sorted(set(paths))):
        with open(fileurl + '_path.txt', "a+", encoding='gb18030', errors='ignore') as paths_file:
            paths_file.write(var + '\n')
            # 打印当前路径到终端并设置颜色为黄色
            print('\033[33m' + var + '\033[0m')
    return vars