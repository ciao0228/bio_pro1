# -*- mode: python -*-

block_cipher = None


a = Analysis(['manage.py'],
             pathex=['F:\\Ecust\\DAISO\\bio_pro',
	'D:\Mysystem\Python\Lib\site-packages\pymysql',
	'D:\Mysystem\Python\Lib\site-packages\apscheduler'],
             binaries=[],
             datas=[(r'F:\Ecust\DAISO\bio_pro\static',r'.\static'),(r'F:\Ecust\DAISO\bio_pro\templates',r'.\templates')],
              hiddenimports=[
       	'django.contrib.admin',
        	'django.contrib.auth',
       	'django.contrib.contenttypes',
       	'django.contrib.sessions',
      	'django.contrib.messages',
       	'django.contrib.staticfiles',
        	'django_apscheduler',
       	'showproject',
        	'django_apscheduler.apps',
	'django_windows_tools',
	'pymysql'
	],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib','MySQLdb','IPython','tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='manage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='manage')
