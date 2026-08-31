; Pywix - custom Inno Setup installer
; Build the app first (see CLAUDE.md's PyInstaller command -> produces out/Pywix/),
; then compile this script with Inno Setup (iscc PywixSetup.iss).

#define MyAppName "Pywix"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Robin Gupta"
#define MyAppExeName "Pywix.exe"
#define MyAppSourceDir "..\out\Pywix"

[Setup]
AppId={{B7B1D9B0-7D2E-4A9F-9C1E-7B2B7B1D9B01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=PywixSetup
Compression=lzma2
SolidCompression=yes
SetupIconFile=..\Assets\APP_BUILDER_ICON.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
LicenseFile=LICENSE_AGREEMENT.txt
WizardStyle=modern
WizardSizePercent=100
DisableWelcomePage=no
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "{#MyAppSourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Launch with a flag the app checks on startup to show the 6-second
; "Thank you" fireworks celebration exactly once, right after install.
Filename: "{app}\{#MyAppExeName}"; Parameters: "--post-install"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent runasoriginaluser

[Code]
var
  IntroPage: TWizardPage;

procedure InitializeWizard;
var
  IntroLabel: TNewStaticText;
begin
  { Custom "skeleton" welcome page shown before Setup's own welcome page,
    giving a branded intro message specific to this installer. }
  IntroPage := CreateCustomPage(wpWelcome, 'Welcome', '');

  IntroLabel := TNewStaticText.Create(IntroPage);
  IntroLabel.Parent := IntroPage.Surface;
  IntroLabel.Left := 0;
  IntroLabel.Top := 16;
  IntroLabel.Width := IntroPage.SurfaceWidth;
  IntroLabel.AutoSize := False;
  IntroLabel.WordWrap := True;
  IntroLabel.Caption :=
    'Welcome to the ' + '{#MyAppName}' + ' installer!' + #13#10 + #13#10 +
    'This wizard will install ' + '{#MyAppName}' + ' on your computer, so you can ' +
    'turn your Python scripts into standalone Windows .exe files without ' +
    'touching a single PyInstaller command.' + #13#10 + #13#10 +
    'Click Next to continue.';
  IntroLabel.Height := 140;

  { Personalize Setup's own built-in welcome page text too. }
  WizardForm.WelcomeLabel1.Caption := 'Setting up ' + '{#MyAppName}';
  WizardForm.WelcomeLabel2.Caption :=
    'This will install ' + '{#MyAppName}' + ' version ' + '{#MyAppVersion}' +
    ' on your computer.' + #13#10 + #13#10 +
    'It is recommended that you close all other applications before continuing.';
end;
