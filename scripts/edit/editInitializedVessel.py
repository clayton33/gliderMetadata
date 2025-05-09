# modify the capitialization of boat names
ic = models.Vessel.objects.get(vessel_name='Eastcom')
ic.vessel_name = 'EastCom'
ic.save()
