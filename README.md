# OtusNetDesign
<h3> Network Topology and IP Addresses Allocation </h3>
<img width="735" alt="Screen Shot 2021-05-11 at 11 48 52" src="https://user-images.githubusercontent.com/39993377/117787227-ee4aba00-b24e-11eb-9f17-d102ffd2a4ce.png">
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
</ul>
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
<h3>Underlay. OSPF</h3>
<p>To achive full reachability between all network devices we are going to use IGP protocol OSPF.</p>
<p>We will follow the best practice reccomendations to be on the safe site:<p/>
<ul>
<li align="left">p-2-p connection between Spine and Leaf switches with /31 mask</li>
<li align="left">passive interface on leaf switches</li>
<li align="left">use default timers for routing protocol messages</li>
<li align="left">use BFD protocol to detect failurs between switches</li>
<li align="left">launch OSPF process on all switches within backbone area (area 0)</li>
<li align="left">use point-to-point network type on interfaces</li>
<li align="left">avoide usnig redistribution in a OSPF process</li>
<li align="left">use authentication in OSPF</li>
</ul>
