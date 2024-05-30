from ij import IJ, ImagePlus
from ij.plugin.filter import ParticleAnalyzer
from ij.measure import ResultsTable
from ij.process import ImageStatistics as IS
import ij.gui.GenericDialog as GenericDialog

# 閾値をユーザーに入力させる
gd = GenericDialog("Threshold Input")
gd.addNumericField("Enter threshold value:", 0, 0)
gd.showDialog()
if gd.wasCanceled():
    IJ.log("User canceled dialog!")
    exit()
threshold = gd.getNextNumber()

# ハイパースタックを取得
imp = IJ.getImage()
width, height, numChannels, numSlices, numFrames = imp.getDimensions()

# 新しいスタックを作成（16ビット）
newStack = IJ.createImage("Extracted Z-Slices", "16-bit black", width, height, 1, 1, numFrames)

# 各時間点での処理
for t in range(1, numFrames + 1):
    maxRawIntDen = 0
    bestSlice = 1

    # 各Zスライスの閾値を超えた領域のRawIntDenを計算
    for z in range(1, numSlices + 1):
        imp.setPosition(1, z, t)
        ip = imp.getProcessor()
        ip.setThreshold(threshold, ip.getMax(), ip.NO_LUT_UPDATE)
        imp.updateAndDraw()

        # ParticleAnalyzerの設定 最小サイズ=16, 最大サイズ=5000
        rt = ResultsTable()
        pa = ParticleAnalyzer(ParticleAnalyzer.SHOW_NONE, ParticleAnalyzer.INTEGRATED_DENSITY, rt, 16, 5000)
        pa.setHideOutputImage(True)
        pa.analyze(imp)

        # 閾値を超えた領域のRawIntDenの総和を計算
        rawIntDenColumn = rt.getColumn(rt.INTEGRATED_DENSITY)
        if rawIntDenColumn is not None:
            currentRawIntDen = sum(rawIntDenColumn)
        else:
            currentRawIntDen = 0

        if currentRawIntDen > maxRawIntDen:
            maxRawIntDen = currentRawIntDen
            bestSlice = z

    # 最もRawIntDenが高いスライスを新しいスタックに追加
    imp.setPosition(1, bestSlice, t)
    ip = imp.getProcessor()
    newStack.setSlice(t)
    newStack.getProcessor().copyBits(ip, 0, 0, 0)

# 新しいスタックを表示
newImp = ImagePlus("Extracted Z-Slices", newStack.getStack())
newImp.show()
