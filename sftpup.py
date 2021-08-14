import pysftp

with pysftp.Connection('218.97.11.20', username='chenwang', password='ok@6Ra!P2MKKEjg#') as sftp:
    with sftp.cd('/chenwang'):            
        sftp.put('./dummy.bin') 
        sftp.get('./dummy.bin')         
