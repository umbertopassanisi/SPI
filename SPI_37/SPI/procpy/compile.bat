rem --------------------------------------------------------------------
rem compilateur script PYTHON, mettre le nom du fichier SANS extension PY
rem --------------------------------------------------------------------&&exit
path=c:\python26;%path%
set fileinput=%1.py
set repIn=source\
set repLog=log\
type nul>%fileinput%c && python compilateur.pyc %repIn%%fileinput% 2>%repLog%%1.err&& xcopy %repIn%%fileinput%c . /F /Y && del %repIn%%fileinput%c&& exit 