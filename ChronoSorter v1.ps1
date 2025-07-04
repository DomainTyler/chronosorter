# Define the URL of the executable
$exeUrl = "https://github.com/DomainTyler/chronosorter/raw/main/chronosorter.exe"

# Define the local path where the exe will be saved (in the temp folder)
$localPath = "$env:TEMP\chronosorter.exe"

try {
    # Download the exe file
    Invoke-WebRequest -Uri $exeUrl -OutFile $localPath -ErrorAction Stop

    # Run the exe
    Start-Process -FilePath $localPath -Wait
} catch {
    Write-Error "Failed to download or run the executable: $_"
}