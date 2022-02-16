# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['on_cue.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += [('OnCueIcon.png', '/home/madeline/Dropbox/Files/Git_projects/OnCue/OnCueIcon.png', 'DATA')]
exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='OnCue',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon = '/home/madeline/Dropbox/Files/Git_projects/OnCue/OnCueIcon.png' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='OnCue')
