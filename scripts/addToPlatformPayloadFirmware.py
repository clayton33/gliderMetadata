def initiate_PlatformPayloadFirmware():
    file = io.FileIO(file=r".\initializationData\platform\platformPayloadFirmware02.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        ppf = models.PlatformPayloadFirmware(platform_payloadFirmwareVersion=getattr(row, "platformPayloadFirmware"),
                                             platform_payloadFirmwareVersionComments=getattr(row, "platformPayloadFirmwareComments"))
        ppf.save()


initiate_PlatformPayloadFirmware()