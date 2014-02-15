# Tries to transform real-world language to ticker symbols

def parse(rawTicker):
	rawTicker = rawTicker.upper();
	if 'EQUITY' in rawTicker:
		print 'Contains us equity'
		return rawTicker
	if 'COMDTY' in rawTicker:
		print 'contains comdty'
		return rawTicker
	if rawTicker.__len__() <= 4:
		print 'short letter assuming es equity'
		return rawTicker + ' Equity';
	if rawTicker == 'COFFEE':
		print 'coffe assuming KCH4'
		return 'KCH4 Comdty';
	if rawTicker == 'COCOA':
		return 'CCH4 Comdty'
	if rawTicker == 'ORANGE':
		return 'OJH4 Comdty'
	if rawTicker == 'ORANGE JUICE':
		return 'OJH4 Comdty'
	if rawTicker == 'CORN':
		return 'CH4 Comdty'
	if rawTicker == 'WHEAT':
		return 'ZWH4 Comdty'
	if rawTicker == 'GOOGLE':
		return 'GOOG US equity'
	if rawTicker == 'FACEBOOK':
		return 'FB US equity'
	if rawTicker == 'MICROSOFT':
		return 'MSFT US equity'
	return rawTicker
