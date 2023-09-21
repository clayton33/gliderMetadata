import pandas as pd
import yaml
import re
from gliderMetadataApp import models

# for testing/debug
platform_company = 'Alseamar'
platform_model = 'SeaExplorer'
platform_serial = '"032"'
mission_number = 51
timebase_sourceVariable = 'GPCTD_TEMPERATURE'
interpolate = True

def createPygliderIOOSyaml(platform_company, platform_model, platform_serial,
                           mission_number,
                           timebase_sourceVariable,
                           interpolate=True,
                           filename="deployment.yml"):
    """
    :param platform_company: a string indicating the name of the company associated with the
           platform_serial (e.g. Alseamar)
    :param platform_model: a string indicating the model of the platform (e.g. SeaExplorer, Slocum)
    :param platform_serial: a string indicating the serial number of the glider for the mission
    :param mission_number: a string indicating the mission number
    :param timebase_sourceVariable: a string indicating which source variable to interpolate over,
           see pyglider fn blank for additional details
    :param interpolate: a logical value indicating if interpolation should be completed
    :param filename: a string indicating the filename for the yml file that is output
    :return:
    """
    # 1. Get the primary key of the company/model
    #    do this in the event that some gliders have the same serial number, but they're
    #    different companies/models.
    pcQ = models.PlatformCompany.objects.filter(platform_company=platform_company,
                                                platform_model=platform_model)
    #   a. check that the pcQ Query set is not empty, if it is, give message on options for next steps for user
    if not(pcQ.exists()):
        # check the platform_company provided, does it exist in the database ?
        pcCheckQ = models.PlatformCompany.objects.filter(platform_company=platform_company)
        if not(pcCheckQ.exists()):
            print(f"Unable to find match in database for platform_company: {platform_company}")
            print(f"These are the current instances in the database: {models.PlatformCompany.objects.values('platform_company')}")
            print(f"If the desired platform_company is not in the database, please contact the developer.")
        else:
            print(f"Valid platform_company provided.")
        # check the platform_model provided, does it exists in the database ?
        pmCheckQ = models.PlatformCompany.objects.filter(platform_model=platform_model)
        if not(pmCheckQ.exists()):
            print(f"Unable to find match in database for platform_model: {platform_model}")
            print(f"These are the current instances in the database: {models.PlatformCompany.objects.values('platform_model')}")
            print(f"If the desired platform_model is not in the database, please contact the developer.")
        else:
            print(f"Valid platform_model provided.")
        # give error and exit out of function
        print(f"Unable to find Query match for the platform_company and platform_model provided, see"
              f"debug print statements for help.")
        return

    # 2. Get primary key of the glider
    psQ = models.PlatformName.objects.filter(platform_companyId=pcQ.first().pk,
                                             platform_serial=platform_serial)
    #    a. check that psQ Query set is not empty, if it is, give message on options for next steps for user
    if not(psQ.exists()):
        # print out options of the serialNumbers for the given platform_companyId already found.
        pcmCheckQ = models.PlatformName.objects.filter(platform_companyId=pcQ.first().pk)
        print(f"Unable to find Query match for platform_serial {platform_serial}"
              f"for the provided platform_company {platform_company} and platform_model {platform_model}")
        print(f"Valid platform_serial are {pcmCheckQ.values('platform_serial')}")
        return

    # 3. Get mission information
    mQ = models.Mission.objects.filter(mission_platformName=psQ.first().pk,
                                       mission_number=mission_number)
    #    a. check that mQ Query set is not empty, if it is, print a message
    if not(mQ.exists()):
        print(f"No mission entry for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        pnQ = models.Mission.object.filter(mission_platformName=psQ.first().pk)
        print(f"The most recent mission entered into the database for platform_serial is {pnQ.values().last()}")
        return

    # 4. Get contributor information
    cQ = models.ContributorMission.objects.filter(contributor_mission = mQ.first().pk)
    if not(cQ.exists()):
        print(f"No contributor entries for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        return
    # get all the contributors out of the query
    allContributorNames = []
    allContributorRoles = []
    for item in cQ.iterator():
        allContributorNames.append(item.contributor_missionPerson.contributor_firstName +
                               ' ' +
                               item.contributor_missionPerson.contributor_lastName)
        allContributorRoles.append(item.contributor_missionRole.contributor_role)

    # 5. Define variables dict, and add timebase and interpolate options
    netcdfVariablesDict = {}
    netcdfVariablesDict['timebase'] = dict(source=timebase_sourceVariable)
    netcdfVariablesDict['interpolate'] = interpolate
    # 5. Get variable information based on the platform
    ipQ = models.PlatformVariable.objects.filter(platform_variablePlatformCompany = pcQ.first().pk)
    # select platform variables are used as the axis variables
    # make a separate dict for those
    # identify them based on platform company
    # in the future I might have to treat them even more special than what is done below

    if(pcQ.first().platform_company == 'Alseamar'):
        coordinateSourceVariables = ['Timestamp',
                                     'NAV_LONGITUDE',
                                     'NAV_LATITUDE']
        coordinateAxisVariables = ['T',
                                   'X',
                                   'Y']
        coordinatedf = pd.DataFrame(list(zip(coordinateSourceVariables,
                                             coordinateAxisVariables)),
                                    columns=['sourceVariable',
                                             'axisVariable'])
        for row in coordinatedf.itertuples():
            ipcvQ = models.PlatformVariable.objects.get(platform_variablePlatformCompany=pcQ.first().pk,
                                                        platform_variableSourceName=getattr(row, 'sourceVariable'))
            # special treatment for time, i'll have to think about this
            # this is an OK hack for now, i'm not really sure if the units are correct though
            if getattr(row, 'sourceVariable') == 'Timestamp':
                long_name = 'time'
                standard_name = 'time'
                units = 'seconds since 1970-01-01T00:00:00Z'
            else:
                long_name = ipcvQ.platform_variableStandardName.variable_longName
                standard_name = ipcvQ.platform_variableStandardName.variable_cfName.variable_standardName
                units = ipcvQ.platform_variableStandardName.variable_cfUnit.variable_unit
            netcdfVariablesDict[standard_name] = dict(
                source=ipcvQ.platform_variableSourceName,
                axis=getattr(row, 'axisVariable'),
                long_name=long_name,
                standard_name=standard_name,
                units=units
            )

    skipVars = ['NAV_MISSIONID', 'NAV_NUMBEROFYO', 'PLD_REALTIMECLOCK', 'Temperature']
    # some variables did not exist for certain navigation firmware versions
    navFirmware = mQ.first().mission_platformNavFirmware.platform_navFirmwareVersion
    print(f"{navFirmware}")
    # remove the 'v' and '-r'
    navFirmware = navFirmware.replace('v', '')
    navFirmware = navFirmware.replace('-r', '')
    navFirmware = navFirmware.replace('-cr', '')
    deadReckFirmware = '2.8.1'
    # compare navFirmware to deadReckFirmware
    navFirmware = [int(v) for v in navFirmware.split(".")]
    deadReckFirmware = [int(v) for v in deadReckFirmware.split(".")]
    for i in range(max(len(navFirmware), len(deadReckFirmware))):
        nf = navFirmware[i] if i < len(navFirmware) else 0
        drf = deadReckFirmware[i] if i < len(deadReckFirmware) else 0
        if nf == drf and i == (max(len(navFirmware), len(deadReckFirmware))-1):
            skipDeadReck = False # all three digits the same
        elif nf == drf:
            continue # go to next index
        elif nf > drf:
            skipDeadReck = False
            break # once a number is greater than deadReckoning, exit
        elif nf < drf:
            skipDeadReck = True
            break # once a number is less than deadReckoning, exit


    if skipDeadReck:
        print(f"skipping DeadReckoning")
        skipVars.append('DeadReckoning')

    for platformVariable in ipQ:
        platformVariableDictName = platformVariable.platform_variableSourceName
        if platformVariableDictName in coordinateSourceVariables:
            print(f"{platformVariableDictName}, is a coordinate variable, continuing to next variable")
            continue
        # some variables aren't actual variables (I don't think)
        if platformVariableDictName in skipVars:
            print(f"{platformVariableDictName} isn't an actual variable in the files, continuing to next variable")
            continue
        if platformVariable.platform_variableStandardName is None:
            long_name = ''
            standard_name = ''
            units = platformVariable.platform_variableSourceUnits
        else:
            long_name = platformVariable.platform_variableStandardName.variable_longName
            standard_name = platformVariable.platform_variableStandardName.variable_cfName.variable_standardName
            units = platformVariable.platform_variableStandardName.variable_cfUnit.variable_unit
        netcdfVariablesDict[platformVariableDictName] = dict(
            source=platformVariable.platform_variableSourceName,
            coordinates='time depth latitude longitude',
            long_name=long_name,
            standard_name=standard_name,
            units=units)

    # 6. Get mission instrument information
    iQ = models.InstrumentMission.objects.filter(instrument_mission=mQ.first().pk)
    #    a. check that iQ Query set is not empty, if it is, print a message
    if not(iQ.exists()):
        print(f"No instrument entries for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        return

    # 7. Get variable information based on instruments
    # add to netcdfVariablesDict
    for instrument in iQ.iterator():
        instrumentModel = instrument.instrument_calibration.instrument_calibrationSerial.instrument_serialNumberModel.pk
        ivQ = models.InstrumentVariable.objects.filter(instrument_variablePlatformCompany=pcQ.first().pk,
                                                       instrument_variableInstrumentModel=instrumentModel)
        for instrumentVariable in ivQ.iterator():
            # there are some variables that might be None, so define those if the are
            if instrumentVariable.instrument_variableStandardName is None:
                instrumentVariableDictName = instrumentVariable.instrument_variableSourceName
                long_name = ''
                standard_name = ''
                units = instrumentVariable.instrument_variableSourceUnits
            else:
                instrumentVariableDictName = instrumentVariable.instrument_variableStandardName.variable_parameterName
                # if there are more than 1 of the same parameter name (e.g. when 2 CTD's are on glider),
                # add number to the dict name
                if instrumentVariableDictName in list(netcdfVariablesDict.keys()):
                    # find how many are in there
                    nreps = [bool(re.search(instrumentVariableDictName, x)) for x in list(netcdfVariablesDict.keys())].count(
                        True)
                    # add number to the device name
                    instrumentVariableDictName = instrumentVariableDictName + str((nreps + 1))
                long_name = instrumentVariable.instrument_variableStandardName.variable_longName
                # now have to go through each variable separately
                if instrumentVariable.instrument_variableStandardName.variable_cfName is None:
                    standard_name = ''
                else:
                    standard_name = instrumentVariable.instrument_variableStandardName.variable_cfName.variable_standardName
                if instrumentVariable.instrument_variableStandardName.variable_cfUnit is None:
                    units = ''
                else:
                    units = instrumentVariable.instrument_variableStandardName.variable_cfUnit.variable_unit
                if instrumentVariableDictName == 'conductivity':
                    units = 'mS cm-1' # same for both GPCTD and LEGATO, so OK for now
            netcdfVariablesDict[instrumentVariableDictName] = dict(source=instrumentVariable.instrument_variableSourceName,
                                                                       coordinates='time depth latitude longitude',
                                                                       long_name=long_name,
                                                                       standard_name=standard_name,
                                                                       units=units)
    # 8. get 'glider_devices', this is specific to pyglider and not any file standard
    #    it's essentially just information on the instruments
    gliderDeviceDict = {}
    profileVariablesDict = {} # need to add glider devices to profileVariableDict as well
    for instrument in iQ.iterator():
        i = instrument.instrument_calibration # this is just to make the below a bit easier
        # gliderDeviceName (this is the type)
        gliderDeviceDictName = i.instrument_calibrationSerial.instrument_serialNumberModel.instrument_modelType.instrument_type
        # if there are more than 1 type of instrument, add number to the dict name
        if gliderDeviceDictName in list(gliderDeviceDict.keys()):
            # find how many are in there
            nreps = [bool(re.search(gliderDeviceDictName, x)) for x in list(gliderDeviceDict.keys())].count(True)
            # add number to the device name
            gliderDeviceDictName = gliderDeviceDictName + str((nreps + 1))
        profileVariablesDictName = 'instrument_' + gliderDeviceDictName
        # make
        make = i.instrument_calibrationSerial.instrument_serialNumberModel.instrument_modelMake.instrument_make
        if make is None:
            make = ''
        # model
        model = i.instrument_calibrationSerial.instrument_serialNumberModel.instrument_model
        if model is None:
            model = ''
        # serial
        serial = i.instrument_calibrationSerial.instrument_serialNumber
        if serial is None:
            serial = ''
        # long_name
        long_name = ''
        # make_model
        make_model = ''
        # factory_calibrated
        factory_calibrated = 'yes'
        # calibration_date
        calibration_date = i.instrument_calibrationDate
        if calibration_date is None:
            calibration_date = ''
        else:
            calibration_date=calibration_date.isoformat()
        # calibration_report
        calibration_report = i.instrument_calibrationReport
        if calibration_report is None:
            calibration_report = ''
        # set dict
        gliderDeviceDict[gliderDeviceDictName] = dict(make=make,
                                                      model=model,
                                                      serial=serial,
                                                      long_name=long_name,
                                                      make_model=make_model,
                                                      factory_calibrated=factory_calibrated,
                                                      calibration_date=calibration_date,
                                                      calibration_report=calibration_report)
        profileVariablesDict[profileVariablesDictName] = dict(make=make,
                                                      model=model,
                                                      serial=serial,
                                                      long_name=long_name,
                                                      make_model=make_model,
                                                      factory_calibrated=factory_calibrated,
                                                      calibration_date=calibration_date,
                                                      calibration_report=calibration_report)

    # fake 'pressure' sensor for now
    gliderDeviceDict['pressure'] = dict(make='Micron',
                                        model='Pressure',
                                        serial='',
                                        long_name='',
                                        make_model='',
                                        factory_calibrated='',
                                        calibration_date='',
                                        calibration_report='')

    # 9. get profile variables for IOOS
    # note that initiation of the dict done before gliderDevices
    pvQ = models.Variable.objects.filter(variable_parameterNameComment='ioosProfile')
    for profileVar in pvQ.iterator():
        profileVarDictName = profileVar.variable_parameterName
        # only have long_name, standard_name (for some) and units for (for some) now
        long_name = profileVar.variable_longName
        if profileVar.variable_cfName is None:
            standard_name = ''
        else:
            standard_name = profileVar.variable_cfName.variable_standardName
        if profileVar.variable_cfUnit is None:
            units = ''
        else:
            units = profileVar.variable_cfUnit.variable_unit
        if profileVarDictName == 'profile_time': # no units for profile_time
            profileVariablesDict[profileVarDictName] = dict(long_name=long_name,
                                                            standard_name=standard_name)
        else:
            profileVariablesDict[profileVarDictName] = dict(long_name=long_name,
                                                            standard_name=standard_name,
                                                            units=units)

    # 10. start creating yaml for use in pyglider
    #    there are 4 components
    #       metadata
    #       glider_devices
    #       netcdf_variables
    #       profile_variables
    metadataDict = dict(acknowledgement='',
                        comment='',
                        contributor_name=', '.join(allContributorNames),
                        contributor_role=', '.join(allContributorRoles),
                        creator_email='',
                        creator_name='',
                        creator_url='',
                        data_mode='P',
                        deployment_id=mQ.first().mission_number,
                        deployment_name='dfo' + '-' + psQ.first().platform_name + psQ.first().platform_serial.replace('"', '') + '-' + mQ.first().mission_deploymentDate.strftime('%Y%m%d'),  # institute (dfo) - gliderName + gliderSerial - deploymentDate
                        deployment_start=mQ.first().mission_deploymentDate,
                        deployment_end=mQ.first().mission_recoveryDate,
                        format_version='',
                        glider_name=psQ.first().platform_name,
                        glider_serial=psQ.first().platform_serial.replace('"', ''),
                        glider_model=pcQ.first().platform_model,
                        glider_instrument_name=pcQ.first().platform_model,  # check this
                        glider_wmo=psQ.first().platform_wmo,
                        wmo_id=psQ.first().platform_wmo,   # pyglider specific
                        institution='',
                        keywords='',
                        keywords_vocabulary='',
                        license='',
                        metadata_link='',
                        Metadata_Conventions='',
                        naming_authority='',
                        network='',
                        platform_type=pcQ.first().platform_model + ' Glider',
                        processing_level='',
                        project='',
                        project_url='',
                        publisher_email='',
                        publisher_name='',
                        publisher_url='',
                        references='',
                        sea_name='',
                        source='',
                        standard_name_vocabulary='',
                        summary=mQ.first().mission_summary,
                        transmission_system='')
    # for now i'm going to skip 'glider_devices', I think it's a C-PROOF thing
    # the information there will be summarized in the
    # 'instrument_[instrumentType]' variable that is seen in the IOOS format
    # netcdf_variables
    # profile_variables
    outDict = {}
    outDict['metadata'] = metadataDict
    outDict['glider_devices'] = gliderDeviceDict
    outDict['netcdf_variables'] = netcdfVariablesDict
    outDict['profile_variables'] = profileVariablesDict

    with open(filename, 'w') as yaml_file:
        yaml.dump(outDict, yaml_file, default_flow_style=False)