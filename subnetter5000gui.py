from PyQt5.QtWidgets import *

# Initialization
app = QApplication([])
form = QDialog()
form.setFixedHeight(400)
form.setFixedWidth(700)
form.setWindowTitle('Subnet Calculator 5000')

# Network Information
NetAddrLineEdit = QLineEdit()
NetAddrLabel = QLabel("Network Address:")
HostsPerSubnetLineEdit = QLineEdit()
HostsPerSubnetLabel = QLabel("# of Hosts Per Subnet:")
CalculatedSizeLineEdit = QLineEdit()
CalculatedSizeLabel = QLabel("Calculated Subnet Size:")

NetworkInfo_layout = QGridLayout()
NetworkInfo_layout.addWidget(NetAddrLabel, 0, 0)
NetworkInfo_layout.addWidget(NetAddrLineEdit, 0, 1)
NetworkInfo_layout.addWidget(HostsPerSubnetLabel, 1, 0)
NetworkInfo_layout.addWidget(HostsPerSubnetLineEdit, 1, 1)
NetworkInfo_layout.addWidget(CalculatedSizeLabel, 2, 0)
NetworkInfo_layout.addWidget(CalculatedSizeLineEdit, 2, 1)
NetworkInfo_groupbox = QGroupBox('Network Information')
NetworkInfo_groupbox.setLayout(NetworkInfo_layout)

# List of IP Ranges

IPRangeList = QListWidget()
LoIPR_layout = QVBoxLayout()
LoIPR_layout.addWidget(IPRangeList)
LoIPR_groupbox = QGroupBox('List of IP Ranges')
LoIPR_groupbox.setLayout(LoIPR_layout)

# Address Information
DecOctetLineEdit = QLineEdit()
DecOctetLabel = QLabel("Decimal Octets:")
DecAddrLineEdit = QLineEdit()
DecAddrLabel = QLabel("Decimal Address:")
BinOctetLineEdit = QLineEdit()
BinOctetLabel = QLabel("Binary Octets:")
HexOctetLineEdit = QLineEdit()
HexOctetLabel = QLabel("Hex Octets:")

AddrInfo_layout = QGridLayout()
AddrInfo_layout.addWidget(DecOctetLabel, 0, 0)
AddrInfo_layout.addWidget(DecOctetLineEdit, 0, 1)
AddrInfo_layout.addWidget(DecAddrLabel, 1, 0)
AddrInfo_layout.addWidget(DecAddrLineEdit, 1, 1)
AddrInfo_layout.addWidget(BinOctetLabel, 2, 0)
AddrInfo_layout.addWidget(BinOctetLineEdit, 2, 1)
AddrInfo_layout.addWidget(HexOctetLabel, 3, 0)
AddrInfo_layout.addWidget(HexOctetLineEdit, 3, 1)

AddrInfo_groupbox = QGroupBox('Address Information')
AddrInfo_groupbox.setLayout(AddrInfo_layout)

# Netmask Information
NetworkClassLineEdit = QLineEdit()
NetworkClassLineEdit.setFixedWidth(30)
NetworkClassLabel = QLabel("Network Class:")
NumIPAddrLineEdit = QLineEdit()
NumIPAddrLineEdit.setFixedWidth(30)
NumIPAddrLabel = QLabel("# of IP Addresses:")
SubnetMaskLineEdit = QLineEdit()
SubnetMaskLabel = QLabel("Subnet Mask:")
BinaryMaskLineEdit = QLineEdit()
BinaryMaskLabel = QLabel("Binary Mask:")
NumSubnetLineEdit = QLineEdit()
NumSubnetLineEdit.setFixedWidth(30)
NumSubnetLabel = QLabel("# of Subnets:")

NetMaskInfo_layout = QGridLayout()
NetMaskInfo_layout.addWidget(NetworkClassLabel, 0, 0)
NetMaskInfo_layout.addWidget(NetworkClassLineEdit, 0, 1)
NetMaskInfo_layout.addWidget(NumIPAddrLabel, 1, 0)
NetMaskInfo_layout.addWidget(NumIPAddrLineEdit, 1, 1)
NetMaskInfo_layout.addWidget(SubnetMaskLabel, 2, 0)
NetMaskInfo_layout.addWidget(SubnetMaskLineEdit, 2, 1)
NetMaskInfo_layout.addWidget(BinaryMaskLabel, 3, 0)
NetMaskInfo_layout.addWidget(BinaryMaskLineEdit, 3, 1)
NetMaskInfo_layout.addWidget(NumSubnetLabel, 4, 0)
NetMaskInfo_layout.addWidget(NumSubnetLineEdit, 4, 1)

NetMaskInfo_groupbox = QGroupBox('Netmask Information')
NetMaskInfo_groupbox.setLayout(NetMaskInfo_layout)


def addressinformation_tab():
    # Binary Octets
    binoctet = ''  # initialize variables
    binarynumber = ''
    address = NetAddrLineEdit.text().split('.')  # grab address from network address and split into list by '.'
    for octet in address:  # for each octet in the address
        if octet == "0":  # if the octet is 0, add 8 0's followed by a '.'
            binoctet += '00000000.'
        else:  # else the octet is not === 0
            temp = str(bin(int(octet))).lstrip('0b')  # tempstring = binary version of the octet stripping off the '0b'
            remaining = 8 - len(temp)  # remaining characters = 8 minus the binary numbers added
            temp = '0' * remaining + temp  # add remaining 8's to make string full binary length (32)
            binoctet += temp + '.'  # add '.' at end to seperate octets as they're added
    binarynumber = binoctet.replace('.', '')  # make stripped version of string without '.'s
    BinOctetLineEdit.setText(binoctet.rstrip('.'))

    # Decimal Address
    DecAddrLineEdit.setText(str(int(binarynumber, 2)))  # take binary number without '.'s, convert to decimal by base 2

    # Hex Octets
    hexoctet = ''  # initialize empty string to fill then setText()
    binaryoctetsraw = binoctet.rstrip('.').split('.')  # get raw binary octets split by '.''s removing trailing '.'
    for octet in binaryoctetsraw:  # for each octet in binary number
        if octet == '00000000':  # if the octet is empty
            hexoctet += '00.'  # add two 0's to hexoctet
        else:  # else octet is <= 1
            temp = hex(int(octet, 2)).lstrip('0x').upper()  # tempstring = hex number of the octet by base 2.
            if len(temp) == 1:  # if the hex number is only once character
                hexoctet += '0' + temp + '.'  # add 0 before the hex, with a '.' to seperate next duo
            else:  # else octet is normal format, ex: 'A8'
                hexoctet += temp + '.'  # add temp to hexoctet string with a '.' to seperate next duo
    HexOctetLineEdit.setText(hexoctet.rstrip('.'))  # settext to hexoctet and strip trailing '.'


def networkinformation_tab():
    DecOctetLineEdit.setText(NetAddrLineEdit.text())  # get network address
    addressnumber = 4294967296  # set maximum possible number of hosts
    while addressnumber >= 4:  # loop per lowest possible host (looping backwards through cidr sizes)
        if int(HostsPerSubnetLineEdit.text()) < int(addressnumber - 1):  # if #hosts can fit in the cirrent host size
            CalculatedSizeLineEdit.setText(str(int(addressnumber)))  # settext to current max #hosts size
        addressnumber /= 2  # divide by two for next loop down the cidr host size range


def netmaskinformation_tab():
    # Network Class
    octetlar = NetAddrLineEdit.text().split('.')  # grab network string, split into list by '.'
    firstoctet = int(octetlar[0])  # grab first octet in network string ex: '192.' or '16.'
    if 1 <= firstoctet <= 127:  # if the first octet is between class A ranges
        NetworkClassLineEdit.setText('A')  # set text to class A
    elif 128 <= firstoctet <= 191:  # if between class B ranges
        NetworkClassLineEdit.setText('B')  # set class B
    elif 192 <= firstoctet <= 223:  # if between class C ranges
        NetworkClassLineEdit.setText('C')  # set class C
    elif 224 <= firstoctet <= 239:  # if between class D ranges
        NetworkClassLineEdit.setText('D')  # set class D
    elif 240 <= firstoctet <= 255:  # if between class E ranges
        NetworkClassLineEdit.setText('E')  # set class E
    else:  # class D and E networks have no ip ranges, but are still available in this program
        print('error')  # else range is not recognized, print error to console because something is definetly wrong

    # Binary Mask
    size = CalculatedSizeLineEdit.text()  # get calculated subnet size
    max = 4294967296  # initialize maximum number of hosts size
    cidr = 0  # initialize cidr starting at 0
    length = 0  # initialize length at 0
    while max >= 4:  # loop per lowest cidr range, 4294967296 to 4, diving each time to get all cidr ranges
        if int(size) == max:  # if current # hosts at loop is equal to the number we calculated earlier
            break  # exit loop
        cidr += 1  # add one to cidr each loop, because are looping down the host range max to smallest
        max /= 2  # cut total # addresses in half to hit next host size and cidr range, ex: /0 to /1 to /2 to /3
    binarymaskstring = ''  # initialize empty string
    remaining = 32 - cidr  # set max size for binary number equal to 32 minus how many 1's we are going to have in it
    for i in range(cidr):  # for each in range of our cidr
        length += 1  # increase length of binary number
        binarymaskstring += '1'  # add 1 to string (for each in range(cidr)
        if length == 8:  # if the length is at 8
            binarymaskstring += '.'  # add '.' to seperate octets
            length = 0  # reset current length (to prevent 4 if statements of 8, 16, 24, 32)
    for i in range(remaining):  # after added all the 1's, remaining must be 0's
        length += 1  # increase length
        binarymaskstring += '0'  # add '0'
        if length == 8:
            binarymaskstring += '.'
            length = 0
    BinaryMaskLineEdit.setText(binarymaskstring.rstrip('.'))  # settext to binary string stripping trailing '.'

    # Subnet Mask
    subnetmaskstring = ''  # initialize empty subnetmask string
    binaryoctets = binarymaskstring.rstrip('.').split('.')  # binary octets equal to binary string split at each '.'
    for octet in binaryoctets:  # for each octet in the binary number
        decoctet = str(int(octet, 2))  # decimaloctet = decimal version of binary octet by base 2
        subnetmaskstring += decoctet + '.'  # add to subnetmask string with '.' to seperate next octet
    SubnetMaskLineEdit.setText(subnetmaskstring.rstrip('.') + ' or /' + str(cidr))  # set entire string, Rstripping '.'

    # Number of IP Addresses
    if NetworkClassLineEdit.text() == 'A':  # if class A network
        NumIPAddrLineEdit.setText('16777216')  # number of ip addresses is 16777216
    elif NetworkClassLineEdit.text() == 'B':  # if class B network
        NumIPAddrLineEdit.setText('65536')  # number of ip addresses is 65536
    elif NetworkClassLineEdit.text() == 'C':  # if class C network
        NumIPAddrLineEdit.setText('256')  # number of ip addresses is 256

    # Number of Subnets
    NumSubnetLineEdit.setText(str(int(int(NumIPAddrLineEdit.text()) / int(CalculatedSizeLineEdit.text()))))
    # set text of number of subnets equal to number of ip addresses divided by calculated subnet size


def listofipranges_tab():
    CalculatedSubnetSize = int(CalculatedSizeLineEdit.text())  # initialize Calculated subnet size
    solidsize = CalculatedSubnetSize  # set variable to what the initial size is
    startingsize = 0  # starting fourth octet is 0
    addr = NetAddrLineEdit.text().split('.')
    interval = int(addr[2])  # initialize third octet to 0
    for i in range(int(NumSubnetLineEdit.text())):  # loop per number of subnets
        primary = f'{addr[0]}.{addr[1]}.{str(interval)}.'  # primary string is 192.168 + interval + . <to be added>
        strong = primary + str(startingsize)  # first address = primary plus starting size number
        weak = primary + str(CalculatedSubnetSize - 1)  # second ip address equal to the calculated subnet size minus 1
        if CalculatedSubnetSize - 1 < 255:  # while the last octet is less than 255
            startingsize += solidsize  # starting size plus the initial size
            CalculatedSubnetSize += solidsize  # calculated size plus the initial size
            IPRangeList.addItem(strong + ' - ' + weak)  # add string to ip ranges list
        else:  # else the last octet hits 225
            interval += 1  # increase interval (for third octet)
            startingsize = 0  # reset starting size
            CalculatedSubnetSize = solidsize  # calculated size = initialize size
            IPRangeList.addItem(strong + ' - ' + weak)  # add string to ip ranges list


def addvalues():  # on button click
    IPRangeList.clear()  # clear the ip ranges list (to prevent the user continually adding ranges with each run
    networkinformation_tab()  # calculate network information
    addressinformation_tab()  # calculate address information
    netmaskinformation_tab()  # calculate netmask information
    listofipranges_tab()  # calculate list of ip ranges


# Calculate Button
calcbutton = QPushButton('Calculate')  # initialize button
calcbutton.setFixedWidth(60)  # set button size
calcbutton.clicked.connect(addvalues)  # connect button to addvalues() function

# Final Layout
layout = QGridLayout()
layout.addWidget(NetworkInfo_groupbox, 0, 0)
layout.addWidget(LoIPR_groupbox, 1, 0, 2, 1)
layout.addWidget(AddrInfo_groupbox, 0, 1)
layout.addWidget(NetMaskInfo_groupbox, 1, 1)
layout.addWidget(calcbutton, 2, 1)

form.setLayout(layout)
form.show()
app.exec_()
