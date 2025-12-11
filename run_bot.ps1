$here = Split-Path -Parent $MyInvocation.MyCommand.Path

$python = Join-Path $here 'venv\Scripts\python.exe'
$bot    = Join-Path $here 'bot.py'

Start-Process -FilePath $python `
              -ArgumentList @("$bot") `
              -WorkingDirectory $here `
              -WindowStyle Hidden

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent(
    [Windows.UI.Notifications.ToastTemplateType]::ToastText02
)

$textNodes = $template.GetElementsByTagName('text')
[void]$textNodes.Item(0).AppendChild($template.CreateTextNode('Casa Squire'))
[void]$textNodes.Item(1).AppendChild($template.CreateTextNode('Agent Running...'))

$toast    = [Windows.UI.Notifications.ToastNotification]::new($template)

$notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Windows PowerShell')

$notifier.Show($toast)
