def getMaskByIpRange(ipBegin, ipEnd):
    """
    get ip range mask
    :param ipBegin:
    :param ipEnd:
    :return:
    """
    ipBeginList = ipBegin.strip().split('.')
    ipEndList = ipEnd.strip().split('.')
    for i in range(4):
        ipRange = str(ipBeginList[i])
        fullRange = ''
        length = len(ipRange)
        if length < 3:
            rest = 3 - length
            for j in xrange(rest):
                fullRange = fullRange + '0'
        fullRange = fullRange + ipRange
        ipBeginList[i] = fullRange
    for i in xrange(4):
        ipRange = str(ipEndList[i])
        fullRange = ''
        length = len(ipRange)
        if length < 3:
            rest = 3 - length
            for j in xrange(rest):
                fullRange = fullRange + '0'
        fullRange =  fullRange + ipRange
        ipEndList[i] = fullRange

    ipBinBegin = ''
    for i in ipBeginList:
        ipBin = str(bin(int(i))).replace('0b', '')
        length = len(ipBin)
        if length < 8:
            rest = 8 - length
            for j in xrange(rest):
                ipBin = '0' + ipBin
        ipBinBegin = ipBinBegin + ipBin
    ipBinEnd = ''
    for i in ipEndList:
        ipBin = str(bin(int(i))).replace('0b', '')
        length = len(ipBin)
        if length < 8:
            rest = 8 - length
            for j in xrange(rest):
                ipBin = '0' + ipBin
        ipBinEnd = ipBinEnd + ipBin
    if len(ipBinBegin) != len(ipBinEnd):
        return False
    sameTimes = 0
    for i in xrange(32):
        if ipBinBegin[i] == ipBinEnd[i]:
            sameTimes = sameTimes + 1
        else:
            break
    restTimes = 32 - sameTimes
    maskBinStr = ''
    for i in xrange(sameTimes):
        maskBinStr = maskBinStr + '1'
    for i in xrange(restTimes):
        maskBinStr = maskBinStr + '0'
    range1 = ''
    range2 = ''
    range3 = ''
    range4 = ''
    for i in [0, 1, 2, 3, 4, 5, 6, 7]:
        range1 = range1 + maskBinStr[i]
    for i in [8, 9, 10, 11, 12, 13, 14, 15]:
        range2 = range2 + maskBinStr[i]
    for i in [16, 17, 18, 19, 20, 21, 22, 23]:
        range3 = range3 + maskBinStr[i]
    for i in [24, 25, 26, 27, 28, 29, 30, 31]:
        range4 = range4 + maskBinStr[i]
    intRange1 = int(range1, 2)
    intRange2 = int(range2, 2)
    intRange3 = int(range3, 2)
    intRange4 = int(range4, 2)
    maskStr = "%s.%s.%s.%s" % (intRange1, intRange2, intRange3, intRange4)
    return maskStr

def getHostNo(ipBegin, ipEnd):
    ipBeginList = ipBegin.strip().split('.')
    ipEndList = ipEnd.strip().split('.')
    for i in range(4):
        ipRange = str(ipBeginList[i])
        fullRange = ''
        length = len(ipRange)
        if length < 3:
            rest = 3 - length
            for j in xrange(rest):
                fullRange = fullRange + '0'
        fullRange = fullRange + ipRange
        ipBeginList[i] = fullRange
    for i in xrange(4):
        ipRange = str(ipEndList[i])
        fullRange = ''
        length = len(ipRange)
        if length < 3:
            rest = 3 - length
            for j in xrange(rest):
                fullRange = fullRange + '0'
        fullRange =  fullRange + ipRange
        ipEndList[i] = fullRange

    ipBinBegin = ''
    for i in ipBeginList:
        ipBin = str(bin(int(i))).replace('0b', '')
        length = len(ipBin)
        if length < 8:
            rest = 8 - length
            for j in xrange(rest):
                ipBin = '0' + ipBin
        ipBinBegin = ipBinBegin + ipBin
    ipBinEnd = ''
    for i in ipEndList:
        ipBin = str(bin(int(i))).replace('0b', '')
        length = len(ipBin)
        if length < 8:
            rest = 8 - length
            for j in xrange(rest):
                ipBin = '0' + ipBin
        ipBinEnd = ipBinEnd + ipBin
    if len(ipBinBegin) != len(ipBinEnd):
        return False
    sameTimes = 0
    for i in xrange(32):
        if ipBinBegin[i] == ipBinEnd[i]:
            sameTimes = sameTimes + 1
        else:
            break
    return sameTimes

def ipRangeToCIDR(ipBegin, ipEnd):
    ipBeginList = ipBegin.strip().split('.')
    ipEndList = ipEnd.strip().split('.')
    ipBeginStr = ''.join(ipBeginList)
    ipEndStr = ''.join(ipEndList)
    if len(ipBeginStr) != len(ipEndStr):
        return False
    length = len(ipBeginStr)
    sameTimes = 0
    for i in xrange(length):
        if ipBeginStr[i] == ipEndStr[i]:
            sameTimes = sameTimes + 1
        else:
            break

def removeZero(ip):
    ipList = ip.strip().split('.')
    for i in xrange(4):
        partStr = str(int(ipList[i]))
        ipList[i] = partStr
    ip = '.'.join(ipList)
    return  ip

def compressCidrListByPl(cidrList):
    pass

def compressCidrList(cidrList):
    """
    return cidr list after compressed and ipCount
    """
    cidrHash = {}
    compressedCidrList = []
    ipCount = 0
    for cidr in cidrList:
        ip, prefix = cidr.strip().split('/')
        if not cidrHash.has_key(prefix):
            cidrHash[prefix] = []
        cidrHash[prefix].append(cidr)
    from IPy import IP, IPSet
    for prefix, cidrList in cidrHash.items():
        ipSetList = []
        for cidr in cidrList:
            ipSetList.append(IP(cidr, make_net = 1))
        ipSet = IPSet(ipSetList)
        for compressdCidr in ipSet:
            compressedCidrList.append(str(compressdCidr))
            ipCount = ipCount + compressdCidr.len()
    return compressedCidrList, ipCount
    """
    from IPy import IP, IPSet
    ipSetList = []
    for cidr in cidrList:
        try:
            ipSetList.append(IP(cidr, make_net=1))
            #print cidr
        except Exception, ex:
            #print 'except:' + cidr
            print str(ex)
    ipSet = IPSet(ipSetList)
    """