# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['face_lock.py'],
    pathex=[],
    binaries=[],
    datas=[('/home/vihaan/.local/lib/python3.13/site-packages/face_recognition_models/models/shape_predictor_68_face_landmarks.dat', 'face_recognition_models/models'), ('/home/vihaan/.local/lib/python3.13/site-packages/face_recognition_models/models/shape_predictor_5_face_landmarks.dat', 'face_recognition_models/models'), ('/home/vihaan/.local/lib/python3.13/site-packages/face_recognition_models/models/mmod_human_face_detector.dat', 'face_recognition_models/models'), ('/home/vihaan/.local/lib/python3.13/site-packages/face_recognition_models/models/dlib_face_recognition_resnet_model_v1.dat', 'face_recognition_models/models')],
    hiddenimports=['cv2', 'numpy', 'PIL', 'face_recognition', 'face_recognition_models', 'dlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='face_lock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
