Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- 1. ฐานข้อมูลคลังปั๊ม Nuosai ---
$NuosaiPumps = @(
    [PSCustomObject]@{Series="PMPA"; Model="100PMPA64-1"; PumpKey="booster_set"; MotorHP=5.5; MinFlow=30.0; MaxFlow=85.0; MinHead=10.0; MaxHead=30.0},
    [PSCustomObject]@{Series="PMPA"; Model="100PMPA64-2"; PumpKey="booster_set"; MotorHP=10.0; MinFlow=30.0; MaxFlow=85.0; MinHead=25.0; MaxHead=58.0},
    [PSCustomObject]@{Series="PMPA"; Model="100PMPA64-3"; PumpKey="booster_set"; MotorHP=15.0; MinFlow=30.0; MaxFlow=85.0; MinHead=40.0; MaxHead=88.0},
    [PSCustomObject]@{Series="PMPA"; Model="100PMPA64-4"; PumpKey="booster_set"; MotorHP=20.0; MinFlow=30.0; MaxFlow=85.0; MinHead=60.0; MaxHead=118.0},
    [PSCustomObject]@{Series="PMPA"; Model="100PMPA90-2"; PumpKey="booster_set"; MotorHP=25.0; MinFlow=50.0; MaxFlow=120.0; MinHead=30.0; MaxHead=70.0},
    [PSCustomObject]@{Series="PMPA"; Model="125PMPA120-3"; PumpKey="booster_set"; MotorHP=40.0; MinFlow=60.0; MaxFlow=160.0; MinHead=45.0; MaxHead=95.0},
    [PSCustomObject]@{Series="PWPC"; Model="PWPC2-4"; PumpKey="transfer_pump"; MotorHP=1.0; MinFlow=0.5; MaxFlow=4.0; MinHead=10.0; MaxHead=32.0},
    [PSCustomObject]@{Series="PWPC"; Model="PWPC4-3"; PumpKey="transfer_pump"; MotorHP=1.5; MinFlow=1.0; MaxFlow=6.5; MinHead=12.0; MaxHead=38.0},
    [PSCustomObject]@{Series="PWPC"; Model="PWPC8-3"; PumpKey="transfer_pump"; MotorHP=2.0; MinFlow=2.0; MaxFlow=11.5; MinHead=15.0; MaxHead=42.0},
    [PSCustomObject]@{Series="PWPC"; Model="PWPC12-3"; PumpKey="transfer_pump"; MotorHP=3.0; MinFlow=4.0; MaxFlow=17.0; MinHead=15.0; MaxHead=46.0},
    [PSCustomObject]@{Series="NSLA"; Model="NSLA32-25-2"; PumpKey="industrial_pump"; MotorHP=3.0; MinFlow=3.0; MaxFlow=16.0; MinHead=12.0; MaxHead=32.0},
    [PSCustomObject]@{Series="NSLA"; Model="NSLA40-25-2"; PumpKey="industrial_pump"; MotorHP=5.5; MinFlow=5.0; MaxFlow=28.0; MinHead=15.0; MaxHead=40.0},
    [PSCustomObject]@{Series="NSLA"; Model="NSLA50-32-2"; PumpKey="industrial_pump"; MotorHP=7.5; MinFlow=10.0; MaxFlow=50.0; MinHead=15.0; MaxHead=48.0},
    [PSCustomObject]@{Series="NSLA"; Model="NSLA65-40-2"; PumpKey="industrial_pump"; MotorHP=15.0; MinFlow=15.0; MaxFlow=75.0; MinHead=20.0; MaxHead=58.0},
    [PSCustomObject]@{Series="NSLA"; Model="NSLA80-40-2"; PumpKey="industrial_pump"; MotorHP=25.0; MinFlow=20.0; MaxFlow=120.0; MinHead=20.0; MaxHead=52.0},
    [PSCustomObject]@{Series="NSWA"; Model="NSWA40-25-2"; PumpKey="industrial_pump"; MotorHP=5.5; MinFlow=5.0; MaxFlow=28.0; MinHead=15.0; MaxHead=42.0},
    [PSCustomObject]@{Series="NSWA"; Model="NSWA50-32-2"; PumpKey="industrial_pump"; MotorHP=7.5; MinFlow=10.0; MaxFlow=52.0; MinHead=18.0; MaxHead=52.0},
    [PSCustomObject]@{Series="NSWA"; Model="NSWA65-40-2"; PumpKey="industrial_pump"; MotorHP=15.0; MinFlow=15.0; MaxFlow=80.0; MinHead=22.0; MaxHead=62.0},
    [PSCustomObject]@{Series="NSQW"; Model="50NSQW15-15-1.5"; PumpKey="submersible"; MotorHP=2.0; MinFlow=5.0; MaxFlow=22.0; MinHead=5.0; MaxHead=18.0},
    [PSCustomObject]@{Series="NSQW"; Model="50NSQW25-28-4"; PumpKey="submersible"; MotorHP=5.5; MinFlow=10.0; MaxFlow=35.0; MinHead=12.0; MaxHead=32.0},
    [PSCustomObject]@{Series="NSQW"; Model="65NSQW25-28-4"; PumpKey="submersible"; MotorHP=5.5; MinFlow=12.0; MaxFlow=40.0; MinHead=10.0; MaxHead=30.0},
    [PSCustomObject]@{Series="NSQW"; Model="100NSQW40-15-4"; PumpKey="submersible"; MotorHP=5.5; MinFlow=15.0; MaxFlow=65.0; MinHead=8.0; MaxHead=18.0},
    [PSCustomObject]@{Series="NSQW"; Model="100NSQW50-17-5.5"; PumpKey="submersible"; MotorHP=7.5; MinFlow=20.0; MaxFlow=75.0; MinHead=10.0; MaxHead=22.0},
    [PSCustomObject]@{Series="NSQW"; Model="150NSQW140-23-15"; PumpKey="submersible"; MotorHP=20.0; MinFlow=50.0; MaxFlow=200.0; MinHead=12.0; MaxHead=28.0}
)

# --- 2. หน้าต่างหลักโปรแกรม (GUI Form) ---
$MainForm = New-Object System.Windows.Forms.Form
$MainForm.Text = "NUOSAI PUMP SELECTION SYSTEM"
$MainForm.Size = New-Object System.Drawing.Size(1100, 750)
$MainForm.StartPosition = "CenterScreen"
$MainForm.BackColor = [System.Drawing.Color]::FromArgb(245, 247, 250)

# หัวแบนเนอร์
$Header = New-Object System.Windows.Forms.Label
$Header.Text = "NUOSAI PUMP SELECTION ENGINE"
$Header.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
$Header.ForeColor = [System.Drawing.Color]::White
$Header.BackColor = [System.Drawing.Color]::FromArgb(15, 76, 129)
$Header.TextAlign = "MiddleCenter"
$Header.Size = New-Object System.Drawing.Size(1080, 50)
$Header.Location = New-Object System.Drawing.Point(0, 0)
$MainForm.Controls.Add($Header)

# โหลดโลโก้บริษัท (ถ้ามีไฟล์อยู่จริง)
$LogoPath = "C:/nuosai-pump-selector/images/logo.png"
if (Test-Path $LogoPath) {
    $LogoBox = New-Object System.Windows.Forms.PictureBox
    $LogoBox.Image = [System.Drawing.Image]::FromFile($LogoPath)
    $LogoBox.SizeMode = "Zoom"
    $LogoBox.Size = New-Object System.Drawing.Size(90, 46)
    $LogoBox.Location = New-Object System.Drawing.Point(10, 2)
    $LogoBox.BackColor = [System.Drawing.Color]::FromArgb(15, 76, 129)
    $MainForm.Controls.Add($LogoBox)
    $LogoBox.BringToFront()
}

# --- 3. ส่วนรับข้อมูลฝั่งซ้าย (Inputs Group) ---
$GroupInput = New-Object System.Windows.Forms.GroupBox
$GroupInput.Text = " 📥 กรอกข้อมูลการออกแบบหน้างาน (Inputs) "
$GroupInput.Size = New-Object System.Drawing.Size(420, 630)
$GroupInput.Location = New-Object System.Drawing.Point(15, 65)
$GroupInput.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$MainForm.Controls.Add($GroupInput)

# ฟังก์ชันสร้าง Label + Input แบบเร็ว
function Add-InputLabel($Text, $Y, $Parent) {
    $Label = New-Object System.Windows.Forms.Label
    $Label.Text = $Text
    $Label.Location = New-Object System.Drawing.Point(20, $Y)
    $Label.Size = New-Object System.Drawing.Size(380, 23)
    $Parent.Controls.Add($Label)
}

# 1. กลุ่มลักษณะงาน
Add-InputLabel "ประเภทกลุ่มงานที่ต้องการใช้งาน:" 25 $GroupInput
$ComboCat = New-Object System.Windows.Forms.ComboBox
$ComboCat.Location = New-Object System.Drawing.Point(20, 50)
$ComboCat.Size = New-Object System.Drawing.Size(360, 28)
$ComboCat.Items.AddRange(@("1. งานบ้านพักอาศัยขนาด 1-3 ชั้น", "2. ชุดปั๊มเสริมแรงดันอัตโนมัติ", "3. ระบบสูบส่งน้ำขึ้นดาดฟ้า", "4. งานการเกษตรและชลประทาน", "5. งานระบบป้องกันอัคคีภัย", "6. งานระบบในโรงงานอุตสาหกรรม", "7. งานระบบบำบัดน้ำเสีย"))
$ComboCat.SelectedIndex = 1
$GroupInput.Controls.Add($ComboCat)

# 2. ซีรีส์ปั๊ม
Add-InputLabel "เลือกซีรีส์รุ่นชนิดปั๊มที่ต้องการ (Pump Series):" 85 $GroupInput
$ComboSeries = New-Object System.Windows.Forms.ComboBox
$ComboSeries.Location = New-Object System.Drawing.Point(20, 110)
$ComboSeries.Size = New-Object System.Drawing.Size(360, 28)
$ComboSeries.Items.AddRange(@("แสดงทุกซีรีส์ปั๊มน้ำ (All Series)", "PMPA", "PWPC", "NSLA", "NSWA", "NSQW"))
$ComboSeries.SelectedIndex = 0
$GroupInput.Controls.Add($ComboSeries)

# 3. Flow
Add-InputLabel "อัตราการไหลที่ต้องการ / Flow Rate (m³/hr):" 150 $GroupInput
$TxtFlow = New-Object System.Windows.Forms.TextBox
$TxtFlow.Location = New-Object System.Drawing.Point(20, 175)
$TxtFlow.Text = "35.0"
$GroupInput.Controls.Add($TxtFlow)

# 4. Vertical Head
Add-InputLabel "ระยะส่งสูงแนวดิ่งจริง / Vertical Static Head (m):" 210 $GroupInput
$TxtVHead = New-Object System.Windows.Forms.TextBox
$TxtVHead.Location = New-Object System.Drawing.Point(20, 235)
$TxtVHead.Text = "45.0"
$GroupInput.Controls.Add($TxtVHead)

# 5. Horizontal Pipe
Add-InputLabel "ระยะทางเดินท่อนอนรวม / Horizontal Pipe Length (m):" 270 $GroupInput
$TxtHPipe = New-Object System.Windows.Forms.TextBox
$TxtHPipe.Location = New-Object System.Drawing.Point(20, 295)
$TxtHPipe.Text = "20.0"
$GroupInput.Controls.Add($TxtHPipe)

# 6. ขนาดท่อ
Add-InputLabel "ขนาดท่อส่งหลัก / Main Pipe Diameter (Inch):" 330 $GroupInput
$ComboDia = New-Object System.Windows.Forms.ComboBox
$ComboDia.Location = New-Object System.Drawing.Point(20, 355)
$ComboDia.Size = New-Object System.Drawing.Size(150, 28)
$ComboDia.Items.AddRange(@("1.0", "1.5", "2.0", "2.5", "3.0", "4.0"))
$ComboDia.SelectedIndex = 3
$GroupInput.Controls.Add($ComboDia)

# 7. วัสดุท่อ
Add-InputLabel "ชนิดวัสดุของท่อส่ง / Pipe Material:" 395 $GroupInput
$ComboMat = New-Object System.Windows.Forms.ComboBox
$ComboMat.Location = New-Object System.Drawing.Point(20, 420)
$ComboMat.Size = New-Object System.Drawing.Size(360, 28)
$ComboMat.Items.AddRange(@("ท่อ PVC / PE (ผิวเรียบ แรงเสียดทานต่ำ)", "ท่อสแตนเลส (Stainless Steel)", "ท่อเหล็กชุบสังกะสี", "ท่อเหล็กดำ / เหล็กหล่อ"))
$ComboMat.SelectedIndex = 0
$GroupInput.Controls.Add($ComboMat)

# 8. สิ่งเจือปน
Add-InputLabel "ลักษณะของเหลวและสารแขวนลอย:" 460 $GroupInput
$ComboPart = New-Object System.Windows.Forms.ComboBox
$ComboPart.Location = New-Object System.Drawing.Point(20, 485)
$ComboPart.Size = New-Object System.Drawing.Size(360, 28)
$ComboPart.Items.AddRange(@("💧 น้ำสะอาดบริสุทธิ์", "🍃 น้ำปนเศษตะกอนอ่อน (< 5mm)", "🪵 น้ำโคลนหนาแน่น / น้ำเสียเข้มข้น"))
$ComboPart.SelectedIndex = 0
$GroupInput.Controls.Add($ComboPart)

# ปุ่มกดคำนวณ
$BtnCalc = New-Object System.Windows.Forms.Button
$BtnCalc.Text = "🚀 คำนวณสเปกและค้นหารุ่นปั๊มน้ำ"
$BtnCalc.Location = New-Object System.Drawing.Point(20, 550)
$BtnCalc.Size = New-Object System.Drawing.Size(360, 45)
$BtnCalc.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
$BtnCalc.BackColor = [System.Drawing.Color]::FromArgb(29, 112, 184)
$BtnCalc.ForeColor = [System.Drawing.Color]::White
$BtnCalc.FlatStyle = "Flat"
$GroupInput.Controls.Add($BtnCalc)


# --- 4. ส่วนแสดงผลลัพธ์ฝั่งขวา (Outputs & Panels) ---
$GroupOutput = New-Object System.Windows.Forms.GroupBox
$GroupOutput.Text = " 📊 ผลการคำนวณและการจับคู่ผลิตภัณฑ์ (Outputs) "
$GroupOutput.Size = New-Object System.Drawing.Size(625, 630)
$GroupOutput.Location = New-Object System.Drawing.Point(450, 65)
$GroupOutput.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$MainForm.Controls.Add($GroupOutput)

# ส่วนแสดงตัวเลขชลศาสตร์ (Hydraulic Results)
$LblResultHydraulic = New-Object System.Windows.Forms.Label
$LblResultHydraulic.Text = "ผลลัพธ์คำนวณ: อัตราไหล: - m³/h | TDH: - m | มอเตอร์แนะนำ: - HP"
$LblResultHydraulic.Location = New-Object System.Drawing.Point(15, 30)
$LblResultHydraulic.Size = New-Object System.Drawing.Size(590, 30)
$LblResultHydraulic.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$LblResultHydraulic.ForeColor = [System.Drawing.Color]::FromArgb(15, 76, 129)
$GroupOutput.Controls.Add($LblResultHydraulic)

# ดรอปดาวน์เลือกรุ่นที่ผ่านเกณฑ์
$LblSelectPump = New-Object System.Windows.Forms.Label
$LblSelectPump.Text = "🔍 รุ่นที่รองรับสเปกคำนวณ (คลิกเพื่อเปลี่ยนโมเดล):"
$LblSelectPump.Location = New-Object System.Drawing.Point(15, 70)
$LblSelectPump.Size = New-Object System.Drawing.Size(590, 20)
$GroupOutput.Controls.Add($LblSelectPump)

$ComboMatchedModels = New-Object System.Windows.Forms.ComboBox
$ComboMatchedModels.Location = New-Object System.Drawing.Point(15, 95)
$ComboMatchedModels.Size = New-Object System.Drawing.Size(590, 28)
$ComboMatchedModels.Enabled = $false
$GroupOutput.Controls.Add($ComboMatchedModels)

# ส่วนแสดงข้อมูลสเปกตัวเลขแคตตาล็อก
$TxtSpecDetails = New-Object System.Windows.Forms.RichTextBox
$TxtSpecDetails.Location = New-Object System.Drawing.Point(15, 140)
$TxtSpecDetails.Size = New-Object System.Drawing.Size(590, 110)
$TxtSpecDetails.ReadOnly = $true
$TxtSpecDetails.BackColor = [System.Drawing.Color]::White
$GroupOutput.Controls.Add($TxtSpecDetails)

# ส่วนแสดงรูปภาพ (Tab Control แยกระหว่าง Dimension และ Curve)
$TabImages = New-Object System.Windows.Forms.TabControl
$TabImages.Location = New-Object System.Drawing.Point(15, 265)
$TabImages.Size = New-Object System.Drawing.Size(590, 350)
$GroupOutput.Controls.Add($TabImages)

$TabDim = New-Object System.Windows.Forms.TabPage
$TabDim.Text = "📐 ขนาดและมิติตัวปั๊ม (Dimension Sheet)"
$TabDim.BackColor = [System.Drawing.Color]::White
$TabImages.Controls.Add($TabDim)

$PicBoxDim = New-Object System.Windows.Forms.PictureBox
$PicBoxDim.Size = New-Object System.Drawing.Size(570, 310)
$PicBoxDim.Location = New-Object System.Drawing.Point(8, 8)
$PicBoxDim.SizeMode = "Zoom"
$TabDim.Controls.Add($PicBoxDim)

$TabCurve = New-Object System.Windows.Forms.TabPage
$TabCurve.Text = "降低 กราฟแคตตาล็อกโรงงาน (Performance Curve)"
$TabCurve.BackColor = [System.Drawing.Color]::White
$TabImages.Controls.Add($TabCurve)

$PicBoxCurve = New-Object System.Windows.Forms.PictureBox
$PicBoxCurve.Size = New-Object System.Drawing.Size(570, 310)
$PicBoxCurve.Location = New-Object System.Drawing.Point(8, 8)
$PicBoxCurve.SizeMode = "Zoom"
$TabCurve.Controls.Add($PicBoxCurve)


# --- 5. ฟังก์ชันช่วยเหลือสำหรับดึงภาพ ---
function Get-ExactPumpImage($Prefix, $ModelCode) {
    $ImgDir = "C:/nuosai-pump-selector/images/"
    if (-not (Test-Path $ImgDir)) { return $null }
    
    $Extensions = @(".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
    $SearchToken = "$($Prefix.ToLower())_$($ModelCode.ToLower())".Replace(" ", "").Replace("-", "")
    $AltToken = "curev_$($ModelCode.ToLower())".Replace(" ", "").Replace("-", "")
    
    # วิ่งไล่เช็กชื่อไฟล์แบบยืดหยุ่น
    foreach ($File in Get-ChildItem $ImgDir) {
        $CleanName = $File.Name.ToLower().Replace(" ", "").Replace("-", "")
        if ($CleanName.Contains($SearchToken) -or ($Prefix -eq "Curve" -and $CleanName.Contains($AltToken))) {
            return $File.FullName
        }
    }
    return $null
}

# --- 6. ตรรกะเหตุการณ์เมื่อคลิกเลือกโมเดล (Dropdown Change Event) ---
$Global:CurrentMatchedList = @()

$ComboMatchedModels.Add_SelectedIndexChanged({
    if ($ComboMatchedModels.SelectedIndex -lt 0) { return }
    $SelectedName = $ComboMatchedModels.SelectedItem.ToString()
    
    $Pump = $Global:CurrentMatchedList | Where-Object { $_.Model -eq $SelectedName } | Select-Object -First 1
    if ($null -eq $Pump) { return }
    
    # อัปเดตตารางข้อมูลตัวเลข
    $TxtSpecDetails.Clear()
    $TxtSpecDetails.SelectionFont = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $TxtSpecDetails.AppendText("📦 โมเดลผลิตภัณฑ์ที่เลือก: $($Pump.Model) (ซีรีส์ $($Pump.Series))\n")
    $TxtSpecDetails.SelectionFont = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Regular)
    $TxtSpecDetails.AppendText("• มอเตอร์ติดตั้งประจำรุ่น: $($Pump.MotorHP) HP (แรงม้า)\n")
    $TxtSpecDetails.AppendText("• ช่วงอัตราไหลทำงานโรงงาน: $($Pump.MinFlow) ถึง $($Pump.MaxFlow) m³/hr\n")
    $TxtSpecDetails.AppendText("• ช่วงระยะส่งสูงทำงานโรงงาน: $($Pump.MinHead) ถึง $($Pump.MaxHead) เมตร\n")
    $TxtSpecDetails.AppendText("✅ รหัสผลิตภัณฑ์ตรงตามขอบเขตความปลอดภัยวิศวกรรมชลศาสตร์หน้างาน")

    # อัปเดตรูปภาพ Dimension Sheet
    $DimPath = Get-ExactPumpImage "Dimension" $Pump.Model
    if ($DimPath -and (Test-Path $DimPath)) {
        $PicBoxDim.Image = [System.Drawing.Image]::FromFile($DimPath)
    } else {
        $PicBoxDim.Image = $null
    }

    # อัปเดตรูปภาพ Performance Curve
    $CurvePath = Get-ExactPumpImage "Curve" $Pump.Model
    if ($CurvePath -and (Test-Path $CurvePath)) {
        $PicBoxCurve.Image = [System.Drawing.Image]::FromFile($CurvePath)
    } else {
        $PicBoxCurve.Image = $null
    }
})

# --- 7. ตรรกะเมื่อกดปุ่มคำนวณ (Click Button Event) ---
$BtnCalc.Add_Click({
    # ดึงค่าตัวเลขจากฟอร์มอย่างปลอดภัย
    [double]$Flow = 0; [double]::TryParse($TxtFlow.Text, [ref]$Flow)
    [double]$StaticHead = 0; [double]::TryParse($TxtVHead.Text, [ref]$StaticHead)
    [double]$HorizPipe = 0; [double]::TryParse($TxtHPipe.Text, [ref]$HorizPipe)
    
    $SelectedCat = $ComboCat.SelectedItem.ToString()
    $SelectedSeries = $ComboSeries.SelectedItem.ToString()
    $PipeDiameter = [double]$ComboDia.SelectedItem.ToString()
    
    # กำหนดกลุ่มซีรีส์ที่อนุญาตตามประเภทงาน
    $AllowedSeries = @()
    $ResidualHead = 2.0
    $SelectedCatKey = ""
    
    if ($SelectedCat.Contains("1.")) { $AllowedSeries = @("PWPC", "NSLA"); $ResidualHead = 10.0; $SelectedCatKey = "building" }
    elseif ($SelectedCat.Contains("2.")) { $AllowedSeries = @("PMPA", "PWPC"); $ResidualHead = 25.0; $SelectedCatKey = "booster" }
    elseif ($SelectedCat.Contains("3.")) { $AllowedSeries = @("NSLA", "NSWA", "PMPA"); $ResidualHead = 4.0; $SelectedCatKey = "watersupply" }
    elseif ($SelectedCat.Contains("4.")) { $AllowedSeries = @("NSLA", "NSWA"); $ResidualHead = 15.0; $SelectedCatKey = "agriculture" }
    elseif ($SelectedCat.Contains("5.")) { $AllowedSeries = @("PMPA", "NSWA", "NSLA"); $ResidualHead = 45.0; $SelectedCatKey = "fire" }
    elseif ($SelectedCat.Contains("6.")) { $AllowedSeries = @("PMPA", "PWPC", "NSLA", "NSWA", "NSQW"); $ResidualHead = 20.0; $SelectedCatKey = "industrial" }
    else { $AllowedSeries = @("NSLA", "NSQW"); $ResidualHead = 2.0; $SelectedCatKey = "wastewater" }

    # คำนวณ Friction Loss
    $MatFactor = 1.0
    if ($ComboMat.SelectedIndex -eq 0) { $MatFactor = 0.85 }
    elseif ($ComboMat.SelectedIndex -eq 1) { $MatFactor = 0.95 }
    else { $MatFactor = 1.10 }
    
    $SolidFactor = 1.0
    if ($ComboPart.SelectedIndex -eq 1) { $SolidFactor = 1.05 }
    elseif ($ComboPart.SelectedIndex -eq 2) { $SolidFactor = 1.25 }
    
    $TotalPipeLength = ($StaticHead + $HorizPipe) * 1.25
    $FLossPer100m = 4.5 * ($Flow / ($PipeDiameter * $PipeDiameter * 8))
    $FrictionLoss = ($FLossPer100m * $TotalPipeLength / 100) * $MatFactor
    
    # ผลลัพธ์ทางชลศาสตร์ที่แท้จริง
    $TDH = $StaticHead + $FrictionLoss + $ResidualHead
    $SuggestedHP = (($Flow * $TDH * $SolidFactor) / (367 * 0.60) * 1.341) * 1.20
    
    # แสดงตัวเลขการคำนวณบนหัวตาราง
    $LblResultHydraulic.Text = "ผลคำนวณจริง: อัตราไหล: {0:N1} m³/h | TDH: {1:N1} เมตร | มอเตอร์ดีไซน์: {2:N1} HP" -f $Flow, $TDH, $SuggestedHP
    
    # วิ่งกรอกโมเดลปั๊มน้ำกรองเงื่อนไข
    $Matched = $NuosaiPumps | Where-Object {
        ($_.Series -in $AllowedSeries) -and
        ($_.MinFlow -le $Flow) -and ($_.MaxFlow -ge $Flow) -and
        ($_.MinHead -le $TDH) -and ($_.MaxHead -ge $TDH)
    }
    
    # หากผู้ใช้งานเจาะจงซีรีส์เพิ่มเติมใน Dropdown ซ้าย
    if ($SelectedSeries -ne "แสดงทุกซีรีส์ปั๊มน้ำ (All Series)") {
        $Matched = $Matched | Where-Object { $_.Series -eq $SelectedSeries }
    }
    
    # อัปเดตรายการลง Dropdown ขวา
    $ComboMatchedModels.Items.Clear()
    if ($Matched.Count -gt 0) {
        $Global:CurrentMatchedList = $Matched
        foreach ($P in $Matched) {
            [void]$ComboMatchedModels.Items.Add($P.Model)
        }
        $ComboMatchedModels.Enabled = $true
        
        # ล็อกหาตัวที่ใกล้ที่สุดอัตโนมัติก่อนในทีแรก (Best Match Index)
        $BestIndex = 0
        $MinDist = [double]::MaxValue
        for ($i=0; $i -lt $Matched.Count; $i++) {
            $MidHead = ($Matched[$i].MinHead + $Matched[$i].MaxHead) / 2
            $Dist = [Math]::Abs($MidHead - $TDH)
            if ($Dist -lt $MinDist) {
                $MinDist = $Dist
                $BestIndex = $i
            }
        }
        $ComboMatchedModels.SelectedIndex = $BestIndex
    } else {
        $ComboMatchedModels.Enabled = $false
        $TxtSpecDetails.Text = "⚠️ ไม่พบรุ่นผลิตภัณฑ์ Nuosai ที่รองรับช่วงการคำนวณสเปกตัวเลขชุดนี้ได้หน้างาน (เกิน Operating Window) กรุณาขยายขนาดท่อหลักหรือปรับลดสเปกตัวแปรดีไซน์"
        $PicBoxDim.Image = $null
        $PicBoxCurve.Image = $null
    }
})

# รันฟอร์ม
[void]$MainForm.ShowDialog()
