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
<p align="left">Full IP address allocation for the scheme is displayed in the table below.
<br />
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
<p align="left">IP address on loppback interfaces:
<br />
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
| Device  | AS number                |
| ------- | ------------------------ |
| Leaf    | 6500{{ device number }}  |
| Spine   | 6460{{ pod number }}      |