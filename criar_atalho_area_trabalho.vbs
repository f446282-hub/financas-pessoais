Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\Iniciar Financas Pessoais.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = WScript.Arguments(0) & "Iniciar_Sistema.bat"
oLink.WorkingDirectory = WScript.Arguments(0)
oLink.IconLocation = "shell32.dll,21"
oLink.Description = "Inicia o sistema Financas Pessoais (Backend + Frontend)"
oLink.Save
WScript.Echo "Atalho criado na area de trabalho!"

