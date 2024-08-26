import pandas as pd
import yaml
import re
from gliderMetadataApp import models

# for testing/debug
platform_company = 'Alseamar'
platform_model = 'SeaExplorer'
platform_serial = '"022"'
mission_number = 66
timebase_sourceVariable = 'GPCTD_TEMPERATURE'
interpolate = True
add_keep_variables=True

# to reduce anchors/aliases in yaml output file
# found on https://ttl255.com/yaml-anchors-and-aliases-and-how-to-disable-them/
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True

def createPygliderIOOSyaml(platform_company, platform_model, platform_serial,
                           mission_number,
                           timebase_sourceVariable,
                           interpolate=True,
                           add_keep_variables=True,
                           subset_navigationVariables=True,
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
    :param add_keep_variables: a logical value indicating if keep_variables should be added. Right now,
           it will see which instruments are on the glider, and pull one from each.
    :param subset_navigationVariables: a boolean value indicating if a subset of the ancillary navigation variables
           should only be included in the output. These variables include pitch, roll, and heading. Default is True.
    :param filename: a string indicating the filename for the yml file that is output
    :return:
    """
    # 1. Get the primary key of the company/model
    #    do this in the event that some gliders have the same serial number, but they're
    #    different companies/models.
    pcQ = models.PlatformCompany.objects.filter(platform_company=platform_company,
                                                platform_model=platform_model)
    #   a. check that the pcQ Query set is not empty, if it is, give message on options for next steps for user
    if not (pcQ.exists()):
        # check the platform_company provided, does it exist in the database ?
        pcCheckQ = models.PlatformCompany.objects.filter(platform_company=platform_company)
        if not (pcCheckQ.exists()):
            print(f"Unable to find match in database for platform_company: {platform_company}")
            print(
                f"These are the current instances in the database: {models.PlatformCompany.objects.values('platform_company')}")
            print(f"If the desired platform_company is not in the database, please contact the developer.")
        else:
            print(f"Valid platform_company provided.")
        # check the platform_model provided, does it exists in the database ?
        pmCheckQ = models.PlatformCompany.objects.filter(platform_model=platform_model)
        if not (pmCheckQ.exists()):
            print(f"Unable to find match in database for platform_model: {platform_model}")
            print(
                f"These are the current instances in the database: {models.PlatformCompany.objects.values('platform_model')}")
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
    if not (psQ.exists()):
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
    if not (mQ.exists()):
        print(f"No mission entry for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        pnQ = models.Mission.object.filter(mission_platformName=psQ.first().pk)
        print(f"The most recent mission entered into the database for platform_serial is {pnQ.values().last()}")
        return
    # 4. Get contributor information
    cQ = models.ContributorMission.objects.filter(contributor_mission=mQ.first().pk)
    if not (cQ.exists()):
        print(f"No contributor entries for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        return
    # get all the contributors out of the query
    allContributorNames = []
    allContributorRoles = []
    allContributorVocabulary = []
    for item in cQ.iterator():
        allContributorNames.append(item.contributor_missionPerson.contributor_firstName +
                                   ' ' +
                                   item.contributor_missionPerson.contributor_lastName)
        allContributorRoles.append(item.contributor_missionRole.role_name)
        allContributorVocabulary.append(item.contributor_missionRole.role_vocabulary)
    # get contributingInstitution information (very similar pull to contributors)
    ciQ = models.ContributingInstitutionMission.objects.filter(contributingInstitution_mission=mQ.first().pk)
    if not (ciQ.exists()):
        print(f"No contributing institution entries for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        return
    # get all the contributors out of the query
    allContributingInstitution = []
    allContributingInstitutionRole = []
    allContributingInstitutionVocabulary = []
    allContributingInstitutionRoleVocabulary = []
    for item in ciQ.iterator():
        allContributingInstitution.append(item.contributingInstitution_missionInstitute.institute_name)
        allContributingInstitutionVocabulary.append(item.contributingInstitution_missionInstitute.institute_vocabulary)
        allContributingInstitutionRole.append(item.contributingInstitution_missionRole.role_name)
        allContributingInstitutionRoleVocabulary.append(item.contributingInstitution_missionRole.role_vocabulary)
    # 5. Define variables dict, and add timebase and interpolate options
    netcdfVariablesDict = {}
    netcdfVariablesDict['timebase'] = dict(source=timebase_sourceVariable)
    netcdfVariablesDict['interpolate'] = interpolate  # boolean values will appear as true/false, so not capitalized
    # 5. Get variable information based on the platform
    ipQ = models.PlatformVariable.objects.filter(platform_variablePlatformCompany=pcQ.first().pk)
    # select platform variables are used as the axis variables
    # make a separate dict for those
    # identify them based on platform company
    # in the future I might have to treat them even more special than what is done below
    if (pcQ.first().platform_company == 'Alseamar'):
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
                long_name = ipcvQ.platform_nercVariable.variable_nerc_variableLongName
                standard_name = ipcvQ.platform_cfVariable.variable_standardName
                units = ipcvQ.platform_nercVariable.variable_nerc_unit
            netcdfVariablesDict[standard_name] = dict(
                source=ipcvQ.platform_variableSourceName,
                axis=getattr(row, 'axisVariable'),
                long_name=long_name,
                standard_name=standard_name,
                units=units,
                observation_type='measured' # everything that is output by the glider is considered measured
            )
            if getattr(row, 'sourceVariable') in ['NAV_LATITUDE', 'NAV_LONGITUDE']:
                netcdfVariablesDict[standard_name].update(
                    conversion='nmea2deg', # required for SX
                    reference='WGS84',
                    coordinate_reference_frame='urn: ogc:crs: EPSG::4326'
                )
            # add valid_[max,min] for latitude and longitude
            if getattr(row, 'sourceVariable') in ['NAV_LONGITUDE']:
                netcdfVariablesDict[standard_name].update(valid_max="180.00",
                                                          valid_min="-180.00")
            if getattr(row, 'sourceVariable') in ['NAV_LATITUDE']:
                netcdfVariablesDict[standard_name].update(valid_max="90.00",
                                                          valid_min="-90.00")
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
        if nf == drf and i == (max(len(navFirmware), len(deadReckFirmware)) - 1):
            skipDeadReck = False  # all three digits the same
        elif nf == drf:
            continue  # go to next index
        elif nf > drf:
            skipDeadReck = False
            break  # once a number is greater than deadReckoning, exit
        elif nf < drf:
            skipDeadReck = True
            break  # once a number is less than deadReckoning, exit

    if skipDeadReck:
        print(f"skipping DeadReckoning")
        skipVars.append('DeadReckoning')
    keepNavVars = ['Pitch', 'Roll', 'Heading'] # fragile ?
    for platformVariable in ipQ.iterator():
        platformVariableSource = platformVariable.platform_variableSourceName
        if platformVariableSource in coordinateSourceVariables:
            print(f"{platformVariableSource}, is a coordinate variable, continuing to next variable")
            continue
        # some variables aren't actual variables (I don't think)
        if platformVariableSource in skipVars:
            print(f"{platformVariableSource} isn't an actual variable in the files, continuing to next variable")
            continue
        # check subset_navigationVariables
        if subset_navigationVariables:
            if platformVariableSource not in keepNavVars:
                print(f"subset_navigationVariables is True, {platformVariableSource} is not one of the retained "
                      f"variables, continuing to next variable.")
                continue
        # need to set things for variables,
        #   dict name, which will be the variable name in the netCDF file, NERC primary, CF secondary, sourceName third
        #   standard_name, which comes from the cf_convention
        #   long_name, primary will be from NERC
        #   units, primary will be from NERC, secondary will be default glider units
        #   vocabulary, primary will be from NERC, secondary will be from CF, third will be None (glider defined)
        #
        # initialize all vars to reduce amount of elif statements
        long_name = standard_name = vocabulary = units = unitsvocabulary = ''
        # minimum case
        if platformVariable.platform_nercVariable is None and platformVariable.platform_cfVariable is None:
            platformVariableDictName = platformVariable.platform_variableSourceName
            units = platformVariable.platform_variableSourceUnits
        elif not(platformVariable.platform_nercVariable is None) and platformVariable.platform_cfVariable is None:
            platformVariableDictName = platformVariable.platform_nercVariable.variable_nerc_variableName
            long_name = platformVariable.platform_nercVariable.variable_nerc_variableLongName
            vocabulary = platformVariable.platform_nercVariable.variable_nerc_variableVocabulary
            units = platformVariable.platform_nercVariable.variable_nerc_unit
            unitsvocabulary = platformVariable.platform_nercVariable.variable_nerc_unitVocabulary
        elif platformVariable.platform_nercVariable is None and not(platformVariable.platform_cfVariable is None):
            platformVariableDictName = platformVariable.platform_cfVariable.variable_standardName
            vocabulary = platformVariable.platform_cfVariable.variable_nameVocabulary
            units = platformVariable.platform_variableSourceUnits
        else : # both are true, then we'll do the same as not(nerc is None) and cf is None
            platformVariableDictName = platformVariable.platform_nercVariable.variable_nerc_variableName
            long_name = platformVariable.platform_nercVariable.variable_nerc_variableLongName
            vocabulary = platformVariable.platform_nercVariable.variable_nerc_variableVocabulary
            units = platformVariable.platform_nercVariable.variable_nerc_unit
            unitsvocabulary = platformVariable.platform_nercVariable.variable_nerc_unitVocabulary
        # standard_name only comes from CF so set it here
        if not(platformVariable.platform_cfVariable is None):
            standard_name = platformVariable.platform_cfVariable.variable_standardName
        netcdfVariablesDict[platformVariableDictName] = dict(
            source=platformVariable.platform_variableSourceName,
            coordinates='time depth latitude longitude',
            long_name=long_name,
            standard_name=standard_name,
            vocabulary=vocabulary,
            units=units,
            unitsVocabulary=unitsvocabulary,
            observation_type='measured' # everything that is output by the glider is considered measured
            )

    # 6. Get mission instrument information
    iQ = models.InstrumentMission.objects.filter(instrument_mission=mQ.first().pk)
    #    a. check that iQ Query set is not empty, if it is, print a message
    if not (iQ.exists()):
        print(f"No instrument entries for glider with serial number {platform_serial} and"
              f"mission {mission_number} in database. Please contact developer or enter information"
              f"into database.")
        return

    # 7. Do multiple things in this loop
    #   a. Get variable information based on instruments
    #   b. get 'glider_devices', this is specific to pyglider and not any file standard
    #   c. get instrument information for 'profile_variables'
    # things will not be extracted in that order, comments will be included below to make everything clear
    # add to netcdfVariablesDict
    # pull out one variable from each instrument for keepVariables
    gliderDeviceDict = {}
    profileVariablesDict = {}  # need to add glider devices to profileVariableDict as well
    keepVariables = []
    gcmdKeywords = []
    for instrument in iQ.iterator():
        # get glider_devices and instrument types for profile_variables
        i = instrument.instrument_calibration  # this is just to make the below a bit easier
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
        long_name = i.instrument_calibrationSerial.instrument_serialNumberModel.instrument_longname
        # make_model, assuming it's just make + model
        make_model = make + ' ' + model
        # factory_calibrated
        factory_calibrated = 'yes'
        # calibration_date
        calibration_date = i.instrument_calibrationDate
        if calibration_date is None:
            calibration_date = ''
        else:
            calibration_date = calibration_date.isoformat()
        # calibration_report
        calibration_report = i.instrument_calibrationReport
        if calibration_report is None:
            calibration_report = ''

        # set dict for glider devices and instrument variables for profile variables
        gliderDeviceDict[gliderDeviceDictName] = dict(make=make,
                                                      model=model,
                                                      serial_number=serial,
                                                      long_name=long_name,
                                                      make_model=make_model,
                                                      factory_calibrated=factory_calibrated,
                                                      calibration_date=calibration_date,
                                                      calibration_report=calibration_report)
        profileVariablesDict[profileVariablesDictName] = dict(make=make,
                                                              model=model,
                                                              serial_number=serial,
                                                              long_name=long_name,
                                                              make_model=make_model,
                                                              factory_calibrated=factory_calibrated,
                                                              calibration_date=calibration_date,
                                                              calibration_report=calibration_report)
        # calibration coefficients (if applicable) 20240730, only Sea-Bird 43F
        if make == 'Sea-Bird' and model == '43F':
            # use calibration pk
            ccQ = models.InstrumentSeabird43FOxygenCalibrationCoefficients.objects.get(
                calibrationSeaBird43F_calibration=i.pk)
            calibration_coefficients = dict(Soc=float(ccQ.calibrationSeaBird43F_Soc),
                                            Foffset=float(ccQ.calibrationSeaBird43F_Foffset),
                                            Tau20=float(ccQ.calibrationSeaBird43F_Tau20),
                                            A=float(ccQ.calibrationSeaBird43F_A),
                                            B=float(ccQ.calibrationSeaBird43F_B),
                                            C=float(ccQ.calibrationSeaBird43F_C),
                                            Enom=float(ccQ.calibrationSeaBird43F_Enom))
            calibration_sourceVars = dict(temperature='GPCTD_TEMP',
                                          conductivity='GPCTD_CONDUCTIVITY',
                                          pressure='GPCTD_PRESSURE')
            # add to gliderDevice and profileVariable dict
            gliderDeviceDict[gliderDeviceDictName].update(calibration_coefficients=calibration_coefficients,
                                                          calibration_sourceVars=calibration_sourceVars)
            profileVariablesDict[profileVariablesDictName].update(calibration_coefficients=calibration_coefficients,
                                                                  calibration_sourceVars=calibration_sourceVars)


        # get instrument variables
        instrumentModel = instrument.instrument_calibration.instrument_calibrationSerial.instrument_serialNumberModel.pk
        ivQ = models.InstrumentVariable.objects.filter(instrument_variablePlatformCompany=pcQ.first().pk,
                                                       instrument_variableInstrumentModel=instrumentModel)
        for instrumentVariable in ivQ.iterator():
            # if it is a '_COUNT' variable, omit for now, continue to next
            if bool(re.search('_COUNT', instrumentVariable.instrument_variableSourceName)):
                print(f"Variable is {instrumentVariable.instrument_variableSourceName}, omitting COUNT variable.")
                continue
            # add gcmdKeywords
            gcmdKeywords.append(instrumentVariable.instrument_gcmdKeyword)
            # same logic as parameterVariable, follow the same statements
            # need to set things for variables,
            #   dict name, which will be the variable name in the netCDF file, NERC primary, CF secondary, sourceName third
            #   standard_name, which comes from the cf_convention
            #   long_name, primary will be from NERC
            #   units, primary will be from NERC, secondary will be default glider units
            #   vocabulary, primary will be from NERC, secondary will be from CF, third will be None (glider defined)
            #
            # initialize all vars to reduce amount of elif statements
            long_name = standard_name = vocabulary = units = unitsvocabulary = ''
            # minimum case
            if instrumentVariable.instrument_nercVariable is None and instrumentVariable.instrument_cfVariable is None:
                instrumentVariableDictName = instrumentVariable.instrument_variableSourceName
                units = instrumentVariable.instrument_variableSourceUnits
            elif not(instrumentVariable.instrument_nercVariable is None) and instrumentVariable.instrument_cfVariable is None:
                instrumentVariableDictName = instrumentVariable.instrument_nercVariable.variable_nerc_variableName
                long_name = instrumentVariable.instrument_nercVariable.variable_nerc_variableLongName
                vocabulary = instrumentVariable.instrument_nercVariable.variable_nerc_variableVocabulary
                units = instrumentVariable.instrument_nercVariable.variable_nerc_unit
                unitsvocabulary = instrumentVariable.instrument_nercVariable.variable_nerc_unitVocabulary
            elif instrumentVariable.instrument_nercVariable is None and not(instrumentVariable.instrument_cfVariable is None):
                instrumentVariableDictName = instrumentVariable.instrument_cfVariable.variable_standardName
                vocabulary = instrumentVariable.instrument_cfVariable.variable_nameVocabulary
                units = instrumentVariable.instrument_variableSourceUnits
            else : # both are true, then we'll do the same as not(nerc is None) and cf is None
                instrumentVariableDictName = instrumentVariable.instrument_nercVariable.variable_nerc_variableName
                long_name = instrumentVariable.instrument_nercVariable.variable_nerc_variableLongName
                vocabulary = instrumentVariable.instrument_nercVariable.variable_nerc_variableVocabulary
                units = instrumentVariable.instrument_nercVariable.variable_nerc_unit
                unitsvocabulary = instrumentVariable.instrument_nercVariable.variable_nerc_unitVocabulary
            # standard_name only comes from CF so set it here
            if not (instrumentVariable.instrument_cfVariable is None):
                standard_name = instrumentVariable.instrument_cfVariable.variable_standardName
            # some variables need to be hard coded (for pyglider)
            # they include: temperature, conductivity, and pressure
            # (longitude, latitude, and time are as well, but they're coordinate vars)
            # brute force it for now (if need be, i'll have to add slocum vars once I get there)
            replaceName = None  # this is for hardcoding some names
            if instrumentVariable.instrument_variableSourceName in ['GPCTD_TEMPERATURE', 'LEGATO_TEMPERATURE']:
                replaceName = instrumentVariableDictName
                instrumentVariableDictName = 'temperature'
            if instrumentVariable.instrument_variableSourceName in ['GPCTD_CONDUCTIVITY', 'LEGATO_CONDUCTIVITY']:
                replaceName = instrumentVariableDictName
                instrumentVariableDictName = 'conductivity'
            if instrumentVariable.instrument_variableSourceName in ['GPCTD_PRESSURE', 'LEGATO_PRESSURE']:
                replaceName = instrumentVariableDictName
                instrumentVariableDictName = 'pressure'
            # check if the dict name exists, if so, add a number to it.
            if instrumentVariableDictName in list(netcdfVariablesDict.keys()):
                # find how many are in there
                nreps = [bool(re.search(instrumentVariableDictName, x)) for x in
                         list(netcdfVariablesDict.keys())].count(
                    True)
                # add number to the device name
                instrumentVariableDictName = instrumentVariableDictName + str((nreps + 1))
            if instrumentVariableDictName == 'conductivity':
                units = 'S m-1'  # GPCTD, is LEGATO 'mS cm-1' ?
            netcdfVariablesDict[instrumentVariableDictName] = dict(
                source=instrumentVariable.instrument_variableSourceName,
                coordinates='time depth latitude longitude',
                long_name=long_name,
                standard_name=standard_name,
                units=units,
                vocabulary=vocabulary,
                unitsvocabulary=unitsvocabulary,
                instrument=profileVariablesDictName,
                observation_type='measured'  # everything that is output by the glider is considered measured
            )
            if not(replaceName is None):
                netcdfVariablesDict[instrumentVariableDictName].update(replaceName=replaceName)
            # save one variable from each instrument, but the trick here is I need to save the instrumentVariableDictName
            if instrumentVariable.instrument_variableSourceName == ivQ.first().instrument_variableSourceName:
                print(f"Saving {instrumentVariableDictName} to keepVariables")
                keepVariables.append(instrumentVariableDictName)
            # add conversion to GPCTD_DOF
            if instrumentVariable.instrument_variableSourceName == 'GPCTD_DOF':
                netcdfVariablesDict[instrumentVariableDictName].update(calculate_oxygenConcentration = 'sbe43Fhz2conc')
    # convert the gcmdKeywords to a set (to get unique set), make it a list, then add the platform keyword
    print(f"length of gcmdKeywords is {len(gcmdKeywords)}")
    # remove 'None' in gcmdKeywords
    gcmdKeywords = [x for x in gcmdKeywords if x is not None]
    gcmdKeywords = list(set(gcmdKeywords))
    gcmdKeywords.append("AUVS > Autonomous Underwater Vehicles")
    # put keepVariables in netcdf_variables
    if add_keep_variables:
        # netcdfVariablesDict['keep_variables']='[' + ', '.join(keepVariables) + ']'
        netcdfVariablesDict['keep_variables'] = keepVariables
    # fake 'pressure' sensor for now
    # don't actually need this
    # gliderDeviceDict['pressure'] = dict(make='Micron',
    #                                     model='Pressure',
    #                                     serial='',
    #                                     long_name='',
    #                                     make_model='',
    #                                     factory_calibrated='',
    #                                     calibration_date='',
    #                                     calibration_report='')

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
        profileVariablesDict[profileVarDictName] = dict(long_name=long_name,
                                                        standard_name=standard_name,
                                                        comment='',
                                                        platform='platform', # to make IOOS DAC happy (should pyglider do this?)
                                                        observation_type='calculated')
        if profileVarDictName != 'profile_time': # no units for profile_time, pyglider will fill it in
            profileVariablesDict[profileVarDictName].update(units=units)
        if profileVarDictName == 'profile_id': # valid_min and valid_max
            profileVariablesDict[profileVarDictName].update(valid_min=1, # copied from a cproof slocum yaml
                                                            valid_max=2147483647 # copied from a cproof slocum yaml
                                                            )
        if bool(re.search('lon', profileVarDictName)):
            profileVariablesDict[profileVarDictName].update(valid_min="-180.00",
                                                           valid_max="180.00")
        if bool(re.search('lat', profileVarDictName)):
            profileVariablesDict[profileVarDictName].update(valid_min="-90.00",
                                                           valid_max="90.00")
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
                        contributor_role_vocabulary=', '.join(allContributorVocabulary),
                        contributing_institutions=', '.join(allContributingInstitution),
                        contributing_institutions_vocabulary=', '.join(allContributingInstitutionVocabulary),
                        contributing_institutions_role=', '.join(allContributingInstitutionRole),
                        contributing_institutions_role_vocabulary=', '.join(allContributingInstitutionRoleVocabulary),
                        Conventions='CF-1.6', # fixed value
                        creator_email='',
                        creator_name='',
                        creator_url='',
                        data_mode='P',
                        deployment_id=mQ.first().mission_number,
                        deployment_name='dfo' + '-' + psQ.first().platform_name + psQ.first().platform_serial.replace(
                            '"', '') + '-' + mQ.first().mission_deploymentDate.strftime('%Y%m%d'),
                        # institute (dfo) - gliderName + gliderSerial - deploymentDate
                        deployment_start=mQ.first().mission_deploymentDate,
                        deployment_end=mQ.first().mission_recoveryDate,
                        featureType='trajectory',  # fixed value
                        format_version='IOOS_Glider_NetCDF_v2.0.nc', # fixed value
                        glider_name=psQ.first().platform_name,
                        glider_serial=psQ.first().platform_serial.replace('"', ''),
                        glider_model=pcQ.first().platform_model,
                        glider_instrument_name=pcQ.first().platform_model,  # check this
                        glider_wmo=psQ.first().platform_wmo,
                        wmo_id=psQ.first().platform_wmo,  # IOOS
                        institution='Bedford Institute of Oceanography',
                        institution_vocabulary='https://edmo.seadatanet.org/report/1811',
                        internal_mission_identifier=mQ.first().mission_cruiseNumber,
                        keywords=', '.join(gcmdKeywords),
                        keywords_vocabulary='GCMD Science Keywords',
                        license='',
                        metadata_link='',
                        Metadata_Conventions='CF-1.6, Unidata Dataset Discovery v1.0',
                        naming_authority='',
                        network=mQ.first().mission_network,
                        platform="sub-surface gliders", # this is always going to be the case
                        platform_vocabulary="https://vocab.nerc.ac.uk/collection/L06/current/27/",
                        platform_type=pcQ.first().platform_model + ' Glider',
                        processing_level='',
                        project='',
                        project_url='',
                        publisher_email='',
                        publisher_name='',
                        publisher_url='',
                        references='',
                        sea_name='North Atlantic Ocean, East Coast - US/Canada',
                        source='',
                        standard_name_vocabulary='',
                        summary=mQ.first().mission_summary,
                        transmission_system=''
                        )
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
        yaml.dump(outDict, yaml_file, default_flow_style=False, Dumper=NoAliasDumper)
