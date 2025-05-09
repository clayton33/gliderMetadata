import io
# the PTT's were out of order in the original initialization file
# only two were out of order. Fixing this automatically fixes
# ArgosTagSerialNumber

ic = models.ArgosTagPTT.objects.get(pk=1)
ic.argosTag_PTT = 162640
ic.save()

ic = models.ArgosTagPTT.objects.get(pk=3)
ic.argosTag_PTT = 162642
ic.save()


