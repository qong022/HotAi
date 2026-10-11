[Setup]
AppName=Hot Ai
AppVersion=3.1.0
AppPublisher=Hot Ai Team
AppPublisherURL=https://github.com/qong022/HotAi
DefaultDirName={autopf}\HotAi
DefaultGroupName=Hot Ai
OutputDir=Output
OutputBaseFilename=HotAi_Setup
SetupIconFile=icon.ico
LicenseFile=terms.txt
Compression=lzma2/max
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "installollama"; Description: "Download and launch Ollama setup (recommended for offline mode)"; GroupDescription: "Offline Engine:"

[Files]
; The compiled executable
Source: "dist\HotAi.exe"; DestDir: "{app}"; Flags: ignoreversion
; Pre-configured template for API keys
Source: ".env"; DestDir: "{app}"; DestName: ".env"; Flags: onlyifdoesntexist
; Icon resource
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Hot Ai"; Filename: "{app}\HotAi.exe"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\Hot Ai"; Filename: "{app}\HotAi.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
; Optional task: open Ollama download page if selected
Filename: "https://ollama.com/download/OllamaSetup.exe"; Description: "Download Ollama installer"; Flags: shellexec runhidden postinstall nowait skipifsilent; Tasks: installollama
; Launch Hot Ai at the end of installation
Filename: "{app}\HotAi.exe"; Description: "{cm:LaunchProgram,Hot Ai}"; Flags: nowait postinstall skipifsilent