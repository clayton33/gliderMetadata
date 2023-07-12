def initiate_PlatformNavigationFirmware():
    file = io.FileIO(file=r".\initializationData\platform\platformNavigationFirmware02.csv", mode="r")
    df = pd.read_csv(file)
    for row in df.itertuples():
        pnf = models.PlatformNavigationFirmware(platform_navFirmwareVersion=getattr(row, "platformNavigationFirmware"),
                                                platform_navFirmwareComments=getattr(row, "platformNavigationFirmwareNotes"))
        pnf.save()


initiate_PlatformNavigationFirmware()