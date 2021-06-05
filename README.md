# OtusNetDesign

## Network Topology and IP Addresses Allocation
<img width="735" alt="Screen Shot 2021-05-22 at 00 27 16" src="https://user-images.githubusercontent.com/39993377/119200051-d831ca80-ba94-11eb-9fbc-e60ae5dfabfb.png">
<p align="left"> Underlay IP address Block: </p>
<table>
  <tr align="center">
    <th>IP Block</th>
    <th>Description</th>
  </tr>
  <tr>
    <td align="left">172.17.11.x/24</td>
    <td align="left">Spine1 IP block</td>
  </tr>
    <tr>
    <td align="left">172.17.12.x/24</td>
    <td align="left">Spine2 IP block</td>
  </tr>
    <tr>
    <td align="left">172.17.21.x/24</td>
    <td align="left">Spine3 IP block</td>
  </tr>
  </tr>
    <tr>
    <td align="left">172.17.123.x/24</td>
    <td align="left">Multiaccess between Spines</td>
  </tr>
  <tr>
    <td align="left">172.17.255.x/24</td>
    <td align="left">Loopbck interfaces</td>
  </tr>
</table><br />
<p align="left">Each first interface on a leaf switch is connected to the first spine, the second - to the second leaf and so on.<br />
<p align="left">Network block is devided into subnets with /31 prefix for peer to peer connection between switches.<br />
<p align="left">Odd addresses are allocated to leafs switches and even to spines.<br />
<ul>
  <li align="left">E.g. link between Leaf_1-1 E1/1: 172.17.11.1/31 and Spine_1-1 E1/1: 172.17.11.0/31.</li>
  <li align="left">link between Leaf_1-1 E1/2: 172.17.12.1/31 and Spine_1-2 E1/1: 172.17.12.0/31.</li>
  <li align="left">E1/7 on SPINE_1-1, SPINE_1-2 and SPINE_2-1 has the last octet of the subnet - .1, .2 and .3 respectively.</li>
</ul>
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
<ul>
<li align="left">ip unnumbered for p-2-p between Spine and Leaf switches if devices support (in our case)</li>
<li align="left">p-2-p connection between Spine and Leaf switches with /31 mask</li>
<li align="left">passive interface on leaf switches</li>
<li align="left">use default timers for routing protocol messages</li>
<li align="left">use BFD protocol to detect failurs between switches</li>
<li align="left">launch OSPF process on all switches within backbone area (area 0)</li>
<li align="left">use point-to-point network type on interfaces</li>
<li align="left">avoide usnig redistribution in a OSPF process</li>
<li align="left">use authentication in OSPF</li>
</ul>
In this scenario Switch device is used as L2 switch to provide broadcast domain for Spines connection.
All switches will be part of OSPF Area0 becouse we have to take into considiration the fact that all Areas in OSPF have to connect to the backbone area - Area0. So we can not assign separate spine into Area0 and connect leafs to two different Area0. We can use Area division in a scenario with multi Pods design using Super-Spine switches. In this scenario we assign Super-Spine and Spine switches into Area 0 and each Pod will be associated with its own non-backbone area.
A network type between Spines and Leafs is Point-to-Point so there is no DR/BDR election process and between Spines - multiaccess. Point-to-point interfaces are also configured as `ip unnumbered` to avoid using additional ip address allocation.
Role Spine devices in OSPF:
<ul>
<li align="left">SPINE_1-1 is DR</li>
<li align="left">SPINE_1-2 is BDR</li>
<li align="left">SPINE_2-1 is DR/OTHER</li>
</ul>

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

---

## Underlay. BGP
###### iBGP
###### eBGP
