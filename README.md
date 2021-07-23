# OtusNetDesign

## Network Topology and IP Addresses Allocation
<img width="735" alt="Screen Shot 2021-05-22 at 00 27 16" src="https://user-images.githubusercontent.com/39993377/119200051-d831ca80-ba94-11eb-9fbc-e60ae5dfabfb.png">

Underlay IP address Block:

| IP Block          | Description                 |
| ----------------- | --------------------------- |
| 172.17.11.x/24    | Spine1 IP block             |
| 172.17.12.x/24    | Spine2 IP block             |
| 172.17.21.x/24    | Spine3 IP block             |
| 172.17.123.x/24   | Multiaccess between Spines  |
| 172.17.255.x/24   | Loopbck interfaces          |

Each first interface on a leaf switch is connected to the first spine, the second - to the second leaf and so on.
Network block is devided into subnets with /31 prefix for peer to peer connection between switches.
Odd addresses are allocated to leafs switches and even to spines.

- E.g. link between Leaf_1-1 E1/1: 172.17.11.1/31 and Spine_1-1 E1/1: 172.17.11.0/31.
- link between Leaf_1-1 E1/2: 172.17.12.1/31 and Spine_1-2 E1/1: 172.17.12.0/31.
- E1/7 on SPINE_1-1, SPINE_1-2 and SPINE_2-1 has the last octet of the subnet - .1, .2 and .3 respectively.

NOTE: This ip address plan with /31 prefix for p-2-p connection is used when devices are not suuposed to use **UNNUMBERED** configuration
Full IP address allocation for the scheme is displayed in the table below.
<table>
  <tr align="center">
    <th>&nbsp;</th>
    <th>SPINE_1-1</th>
    <th>SPINE_1-2</th>
    <th>SPINE_2-1</th>
  </tr>
  <tr>
    <td align="left">LEAF_1-1</td>
    <td align="left">172.17.11.0/31</td>
    <td align="left">172.17.12.0/31</td>
    <td align="center"> - </td>
  </tr>
    <td align="left">LEAF_1-2</td>
    <td align="left">172.17.11.2/31</td>
    <td align="left">172.17.12.2/31</td>
    <td align="center"> - </td>
  </tr>
    <td align="left">LEAF_1-3</td>
    <td align="left">172.17.11.4/31</td>
    <td align="left">172.17.12.4/31</td>
    <td align="center"> - </td>
  </tr>
   <tr>
    <td align="left">LEAF_2-1</td>
    <td align="center"> - </td>
    <td align="center"> - </td>
    <td align="left">172.17.21.0/31</td>
  </tr>
</table>
<br />
IP address on loppback interfaces:
<table>
  <tr align="left">
    <th>Device Name</th>
    <th>IP Address</th>
  </tr>
  <tr>
    <th align="left">LEAF_1-1</th>
    <th align="left">172.17.255.11/32</th>
  </tr>
    <tr>
    <th align="left">LEAF_1-2</th>
    <th align="left">172.17.255.12/32</th>
  </tr>
  <tr>
    <th align="left">LEAF_1-3</th>
    <th align="left">172.17.255.13/32</th>
  </tr>
  <tr>
    <th align="left">LEAF_2-1</th>
    <th align="left">172.17.255.21/32</th>
  </tr>
  <tr>
    <th align="left">SPINE_1-1</th>
    <th align="left">172.17.255.111/32</th>
  </tr>
  <tr>
    <th align="left">SPINE_1-2</th>
    <th align="left">172.17.255.112/32</th>
  </tr>
  <tr>
    <th align="left">SPINE_2-1</th>
    <th align="left">172.17.255.121/32</th>
  </tr>
</table>
<p align="left">Incterconnections between Leaf_1-1 and Leaf_1-2 is used to create redundancy (VPC):<br />
<ul>
<li align="left">E1/3: keepalive link.</li>
<li align="left">E1/4: Member of Portchanell 45 as a peer link.</li>
<li align="left">E1/5: member of Portchanell 45 as a peer link.</li>
</ul>
<br />

---

## Underlay. OSPF

To achive full reachability between all network devices we are going to use IGP protocol OSPF
We will follow the best practice reccomendations to be on the safe site:

- ip unnumbered for p-2-p between Spine and Leaf switches if devices support (in our case)
- p-2-p connection between Spine and Leaf switches with /31 mask
- passive interface on leaf switches
- use default timers for routing protocol messages
- use BFD protocol to detect failurs between switches
- launch OSPF process on all switches within backbone area (area 0)
- use point-to-point network type on interfaces
- avoide usnig redistribution in a OSPF process
- use authentication in OSPF

In this scenario Switch device is used as L2 switch to provide broadcast domain for Spines connection.
All switches will be part of OSPF Area0 becouse we have to take into considiration the fact that all Areas in OSPF have to connect to the backbone area - Area0. So we can not assign separate spine into Area0 and connect leafs to two different Area0. We can use Area division in a scenario with multi Pods design using Super-Spine switches. In this scenario we assign Super-Spine and Spine switches into Area 0 and each Pod will be associated with its own non-backbone area.
A network type between Spines and Leafs is Point-to-Point so there is no DR/BDR election process and between Spines - multiaccess. Point-to-point interfaces are also configured as `ip unnumbered` to avoid using additional ip address allocation.
Role Spine devices in OSPF:
- SPINE_1-1 is DR
- SPINE_1-2 is BDR
- SPINE_2-1 is DR/OTHER


---

## Underlay. IS-IS
IS-IS is the alternative IGP protocol which also can used as an Underlay Layer to provide full connectivity between network devices.
This protocol satisfies requirements for a protocol on clos topology:
- ECMP
- Opportunity to increase bandwidth for East-West traffic
- Reliability and resiliency because of using redundancy and ECMP
- Scalability
- Manageability 

Compare to OSPF IS-IS has got following advantages:
- Stability (ISIS is based on CLNS, that is, it runs at the link layer. In this way, even if the IP layer is faulty, the Layer 2 communication is not interrupted)
- Scalability (All routing information is transmitted using TLVs (TYPE/LENGTH/VALUE), ensuring simple structure and providing easy scalability.)
- Convergence (When the network scale is large, the convergence speed of ISIS is much faster than that of OSPF. When changes occur on the network segment where a node in an area resides, PRC algorithm is triggered, ensuring fast route convergence and low route calculation cost.)
- Complexity (ISIS areas are classified into level1 and level2, the backbone area of ISIS is relatively flexible.)

All Spines switches can be L2/L1 type and all Leafs swithces can be L1-type in their own Area.
L1 type for Leafs allows us to avoid an overwhelming number of routes in a routing table. In this case Leafs will receive only defoult routes from Spines.
As far as Spine switches are connected with each other in a single broadcast domain through Switch it allows exchange routing information between all L2-type devices. A network infrastructure can be easily scaled up.

If we consider to use IS-IS in spine/leaf two-layer architecture implementation within one POD without using interconnection between Spines switches we have to apply L2-type to all Clos devices. This is step also provides us opportubity to recieve more specific prefixes from all devices to use routing domain more flexible. All Spine/Leafe switches will be in the different Areas to control size of the IS-IS topological database. The topological information is not shared between administrative domains, only reachability information is shared. Following this design allows us to avoid escaping a big impact in the overall network stabilityan because of unstable link or failure.

> IS-IS by default pads the Hellos to the **full interface MTU size** to detect MTU mismatches

If we are sure of the MTU on the link, the padding of the Hellos can be turned off:
- Avoid using bandwidth unnecessary 
- Reduced Buffer Usage 
- Reduced processing overhead when using authentication 

Under router isis CLI ` [no] hello padding [multi-point|point-to-point] `

Under interface CLI ` [no] isis hello padding `

- Even if padding is disabled, at the beginning, the router still sends a few hellos at full MTU. `always` option which is hidden can be used to prevent it.

> We also have to take into consideration that BFD protol is not supported by EVE-NG, so BFD must disable from configuration to create adjacency between ISIS peers.

---

## Underlay. BGP
ISIS Versus OSPF as from the perspective of DC underlay network it will not make a big difference. So for the sake simplicity an IGP in DC is either ISIS or OSPF for underlay network (OSPF may more popular).

###### iBGP
In this case there is a point which devices we are going to use as Route Reflectors (RR).
For example in case we use as RR Spine Switches it will cause configuration complexity (proper design RR cluster to prevent loops in a topology) and prevention increase scalability as well.
Therefore if we had like to choose iBGP protocol as an IGP it would be better deploying VMs with routing module as RR function.
In this scenario BFD must be enabled between all VMs connections as far as interfaces on Virtual Switch of a Hypervisor are always up.
Such implementation allows us to avoid drowbacks which were discribed in scenario with RR on Spines.
Overall we are not going to use iBGP as an IGP for underlay network due to its complexity.
We have also take into considiration the fact that we are using eBGP protocol for Underlay.
So using eBGP as a IGP will give preference to the selection of a single routing protocol to reduce complexity and interdependencies.

###### eBGP
This part is reffering to IETF of P. Lapukhov [Use of BGP for Routing in Large-Scale Data Centers](https://datatracker.ietf.org/doc/html/rfc7938#section-3.2)

Pros of using eBGP:
- one protocol on Underlay and Overlay (no IGP)
- flexible management
- template configuration
- scalability and maintenance (`as-path multipath-relax`)
- ECMP load balancing (`maximum-path <number-paths>`)

**Fault Detection Timing**
The proposed routing design does not use an IGP, so the remaining mechanisms that could be used for fault detection are BGP keep-alive time-out (or any other type of keep-alive mechanism) and link-failure triggers.

Relying solely on BGP keep-alive packets may result in high convergence delays, on the order of multiple seconds (on many BGP implementations the minimum configurable BGP hold timer value is three seconds).  However, many BGP implementations can shut down local EBGP peering sessions in response to the "link down" event for the outgoing interface used for BGP peering.

Alternatively, some platforms may support BFD to allow for sub-second failure detection and fault signaling to the BGP process.

Each leaf has got their own AS number. Spine switches is going to be configured in one AS.
BGP AS allocation:
| Device  | AS number                                      |
| ------- | ---------------------------------------------- |
| Leaf    | 65{{ data_center }}{{ row }}{{ device number }}|
| Spine   | 6460{{ pod number }}                           |

Here is the result of `show ip route bgp` command which was executed on LEAF_1-1.
It depictes full connectivity between devices:
```
LEAF_1-1# show ip route bgp-65111
172.17.255.12/32, ubest/mbest: 2/0
    *via 172.17.11.0, [20/0], 1d13h, bgp-65111, external, tag 64601
    *via 172.17.12.0, [20/0], 1d13h, bgp-65111, external, tag 64601
172.17.255.13/32, ubest/mbest: 2/0
    *via 172.17.11.0, [20/0], 1d13h, bgp-65111, external, tag 64601
    *via 172.17.12.0, [20/0], 1d13h, bgp-65111, external, tag 64601
172.17.255.21/32, ubest/mbest: 2/0
    *via 172.17.11.0, [20/0], 1d13h, bgp-65111, external, tag 64601
    *via 172.17.12.0, [20/0], 1d13h, bgp-65111, external, tag 64601
172.17.255.111/32, ubest/mbest: 2/0
    *via 172.17.11.0, [20/0], 1d13h, bgp-65111, external, tag 64601
    *via 172.17.12.0, [20/0], 1d13h, bgp-65111, external, tag 64601
172.17.255.112/32, ubest/mbest: 2/0
    *via 172.17.11.0, [20/0], 1d13h, bgp-65111, external, tag 64601
    *via 172.17.12.0, [20/0], 1d13h, bgp-65111, external, tag 64601
172.17.255.121/32, ubest/mbest: 2/0
    *via 172.17.11.0, [20/0], 1d13h, bgp-65111, external, tag 64601
    *via 172.17.12.0, [20/0], 1d13h, bgp-65111, external, tag 64601
```

---

## VxLAN. BUM traffic learning
VxLAN terminology:
- VNI / VNID – VXLAN Network Identifier, or VXLAN ID. This replaces VLAN ID.
- VTEP – VXLAN Tunnel End Point, the end point where the box performs VXLAN encap / decap. This could be physical HW(Nexus9k) or virtual (Nexus 1000v, Nexus 9000v). 
- VXLAN Segmenet -  The resulting layer 2 overlay network 
- VXLAN Gateway – Device that forwards traffic between VXLANS. The VXLAN Gateway can be both L2 and L3 forwarding. 
- NVE – Network Virtualization Edge, is the tunnel interface, and represents VTEP
- BUM traffic - Broadcast Unknown Unicast

There are multiple ways to build the VXLAN mapping database, which is VTEP IP address-to-MAC address mapping. It is essential to be able to forward traffic.
Address learning aproaches:
- Data Plane Learning - traditional method to learning addresses
- Controll Plne Learing - method uses BGP to share MAC address information

**VXLAN Data Plane Learning**
VXLAN data plane learning utilizes flood-and learn mechanisms to build its VTEP-to-MAC address information. It requires multicast to be running in the underlying network to reduce flooding scope. Each VNI is mapped to a multicast group, so only the hosts participating in a specific VXLAN segment will receive the traffic. The multicast group is mapped to the VNI. It is also used to transport broadcast, unknown unicast, and multicast traffic (BUM traffic: ARP, ND, DHCP and other).

**VXLAN Unicast-Only Mode**
This scenario is also known as unicast-only mode (Ingress Replication). VTEPs can be statically configured, or a control plane can announce to each VTEP the list of VTEPs and associated VNIs. The VTEP receiving the BUM traffic is responsible for creating multiple copies of the traffic and sending it to the remote VTEPs, which are mapped to a specific VNI (each packet is replicated to all other VTEPS belonging to the same vni). In smaller installations this is valid solutions because of its simplicity, there is no need for the Multicast protocol in Underlay network.

**VXLAN Using Control Plane Protocol**
Multiprotocol Border Gateway Protocol (MP-BGP) Ethernet virtual private network (EVPN) can be used as the control plane protocol. It can provide peer VTEP discovery and end-host reachability information, establish BGP peering between VTEPs, advertise MAC-to-VNI mapping and MAC-to-IP mapping, and advertise using BGP EVPN. EVPN uses the L2VPN EVPN address family to advertise this information.


###### Multicast
IP multicast is used to reduce the flooding scope of the set of hosts that are participating in the VXLAN segment.
Each VXLAN segment, or VNID, is mapped to an IP multicast group in the transport IP network.
Each VTEP device is independently configured and joins this multicast
group as an IP host through the Internet Group Management Protocol (IGMP). The IGMP joins trigger PIM joins and signaling through the transport network for the particular multicast group. The multicast distribution tree for this group is
built through the transport network based on the locations of participating VTEPs.
BUM traffic in the VNI will be encapsulated into multicast packets using this multicast group as the outer destination IP address and then sent to the remote VTEPs using the underlay network multicast replication and forwarding
Configuration example:
```
vlan 200
    vn-segment 1200
interface nve 1
    member vni 1200
        mcast-group 225.2.2.2
```
2 Multicast Mode can be used in Clos topology:

- PIM-ASM (Anycast-RP)
We should use different source loopback address from loopback which is partisipating in routing process.
If interface nve1 down the interface beloning to its source will be also in down state that can be cause an routing process issue.
On Leaf Switches we have to configure RP as a anycast RP of Spine Switches e.g.
```
ip pim rp-address 10.10.10.254 group-list 224.0.0.0/4
```
On Spines we need to configure additional loopback interface for Anycast-RP and also unique address for Anycast-RP.
```
ip pim rp-address 10.10.10.254 group-list 224.0.0.0/4
ip pim anycast-rp 10.10.10.254 10.10.10.11
```
Each interface of switches that is partisipating in PIM process configure the following command `(config-if)# ip pim sparse-mode`.
- PIM-SSM
It requires source information only. There is no Randevous Point in Source Specific Multicast, no RP Engineering , no Anycast RP. It is designed for One to Many applications. Source address information should be known by the receivers though. In PIM SSM all the routers every source-group address state. Thus it requires more memory and cpu on the devices, there is no (*,G) state in PIM SSM, only (S,G). We also must ensure that IGMPv3 is enabled on interfaces which connect to SSM clients.
Once you have PIM-SM running, PIM-SSM is trivial to enable: `(config)# ip pim ssm default` (default group range (232.0.0.0/8)).
We also must ensure that IGMPv3 is enabled on interfaces which connect to SSM clients: `(config-if)# ip igmp version 3`
Now any requests to join a multicast group within the specified SSM range must specify a source address, and no shared trees will be built for these SSM channels.

- PIM BiDir (Phantom RP)
PIM Bidir enabled routers only keep (*,G) states. Only shared tree is used in Bidirectional PIM for sources and destinations.
Not optimal traffic flow since all the traffic always have to pass through Randevous Point.
PIM BiDir at a glance — One shared tree per multicast group.
Use different length mask (e.g. /29 and /28) in Spine Switches on Loopback interfaces for multicast.
The bidirectional Multicast Tree, where Spine with the longest preffix (/29) is working as a routing vector, is now ready. Spine with /28 is not participating the Shared Tree at this moment. In case of active Spine failure, backup Spine still advertises RPA network with mask /28.
Protocol is not well compatible with all kind off devices and vendors.
`ip pim rp-address 10.10.10.254 group-list 238.0.0.0/24 bidir`

From the complexity point of view, the Ingress Replication model is the most simple but it has its scalability limitations. If we compare PIM-ASM and PIM-BiDir we have to make a decision which is a more sutable and compatable during design.
We have to take into account protocol specifications before making desision which is used.

The foolowing address blok we are going to use for Loopback interfaces for PIM-ASM:
| Device Name       | Loopback1 IP address  | RP Anycast IP     |
| ----------------- | --------------------- | ----------------- |
| SPINE_1-1         |   172.17.254.111/32   | 172.17.254.254/32 |
| SPINE_1-2         |   172.17.254.112/32   | 172.17.254.254/32 |
| SPINE_2-1         |   172.17.254.121/32   | 172.17.254.254/32 |
| LEAF_1-1          |   172.17.254.11/32    |         -         |
| LEAF_1-2          |   172.17.254.12/32    |         -         |
| LEAF_1-3          |   172.17.254.13/32    |         -         |
| LEAF_2-1          |   172.17.254.21/32    |         -         |

We are using eBGP routing protocol and configuration template to distribute source ip addresses for multicast BUM traffic in underlay network.

###### VXLAN EVPN type-2
There are 2 method to handle BUM traffic: Multicast and Head-end (avaliable with BGP EVPN) replication.
As it was mentioned before MP-BGP EVPN can be used as the control plane protocol.
Control Plane learning is much more functional and efficient. Control Plane lerning means that switches learn MAC addresses before they are needed. A L2VNI is used for bridging.
It works in the same way as a routing protocol. Switches peer with each other using BGP and share the addresses that they know about.
This uses the EVPN address family. Each switch runs BGP and peers with other switches over the ip network. The normal BGP ruls still apply here: need full mesh or route reflector.
Some or all of these swithes will contain VTEPs. This means that each switch automatically learns where all the other VTEPs are in the network.

With extensions to the BGP EVPN address family, it is now possible to distribute endpoint (IP, MAC)-to-VTEP bindings within a VXLAN network. In this way, the moment an endpoint is learned locally at a VTEP, using BGP EVPN, this reachability information can be distributed to all the interested VTEPs. Any traffic to this endpoint can then be optimally forwarded from any other VTEP without the need for any flood traffic.

The distribution of reachability information with BGP EVPN allows the realization of a distributed IP anycast gateway:

`Leaf_N(config)# fabric forwarding anycast-gateway-mac 0000.2222.3333`

`Leaf_N(config-if)# fabric forwarding mode anycast-gateway`

The same default gateway can be simultaneously configured at any and all leaf switches as needed. In this way, when a workload moves between various leaf switches, it still finds its default gateway directly attached to it. This helps with virtual machine mobility.

As eBGP design is taken into consideration we have to pay attantion to the following recomendations:
| command                         | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| `retain route-target all`       | Required for eBGP. Allows the SPINE to retain and advertise  
                                    all EVPN routes when there are no local VNI configured with 
                                    matching import route targets.                               |


```
route-map permitall permit 10
  set ip next-hop unchanged
!
router bgp 100
  router-id 10.1.1.1
  address-family l2vpn evpn
    nexthop route-map permitall
```
The route-map keeps the next-hop unchanged for EVPN routes. It is implemented on Spines.


###### Leaf Redundancy - VPC
The bundling of multiple physical interfaces into a single logical interface between two chassis is referred to as a port channel, which is also known as a link aggregation group (LAG).
Virtual PortChannel (vPC) is a technology that provides Layer 2 redundancy across two or more physical chassis.
Specifically, a single chassis is connected to two other chassis that are configured as a vPC pair. The industry term for this is Multi-Chassis Link Aggregation Group (MC-LAG).
Any device that supports layer-2 port-channels can connect by a vPC. The device does not need to be vPC aware. Devices include physical servers, firewalls, other switches, and load balancers.

**Benefits of Using vPC:**
- Enables a single device to use a port channel across two upstream switches
- Eliminates STP blocked ports
- Provides a loop-free topology
- Uses all available uplink bandwidth
- Provides fast convergence in the case of link or device failure
- Provides link-level resiliency
- Helps ensure high availability

**vPC Limitations**
It is important to know the limitations of vPC technology. Some of the key points about vPC limitations are outlined next:
- Only two switches per vPC domain: A vPC domain by definition consists of a pair of switches identified by a shared vPC domain ID. It is not possible to add more than two switches or virtual device contexts (VDCs) to a vPC domain.
- Only one vPC domain ID per switch: Only one vPC domain ID can be configured on a single switch or VDC. It is not possible for a switch or VDC to participate in more than one vPC domain.
- Each VDC is a separate switch: vPC is a per-VDC function on the Cisco Nexus 7000 Series switches. vPCs can be configured in multiple VDCs, but the configuration is entirely independent. A separate vPC peer link and vPC peer keepalive link is required for each of the VDCs. vPC domains cannot be stretched across multiple VDCs on the same switch, and all ports for a given vPC must be in the same VDC.
- Peer-link is always 10 Gbps or more: Only 10 Gigabit Ethernet ports can be used for the vPC peer link. It is recommended that you use at least two 10 Gigabit Ethernet ports in dedicated mode on two different I/O modules.
- vPC is a Layer 2 port channel: A vPC is a Layer 2 port channel. The vPC technology does not support the configuration of Layer 3 port channels. Dynamic routing from the vPC peers to routers connected on a vPC is not supported. It is recommended that routing adjacencies be established on separate routed links.

**Configuration for our case**
We need allocate the same IP address to loopback interface which is configured as source-interface for VTEP (`interface nve1`) e.g. LEAF_1-1 and LEAF_1-2 Lo1: `ip address 172.17.254.100/32 secondary`
If a Leaf in a VPC domain `id` key has to be the same on both switches, e.g. LEAF_1-1 and LEAF_1-2 - `id: 1`. In spines_params.yaml file `leaf_id` must be the same for switches in a VPC route domain as well.