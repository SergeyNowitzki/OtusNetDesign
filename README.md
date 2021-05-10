# OtusNetDesign
<h3>Underlay IP address Block:</h3>
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
<p align="left">E.g. link between Leaf_1-1 E1/1: 172.17.11.1/31 and Spine_1-1 E1/1: 172.17.11.0/31.<br />
<p align="left">     link between Leaf_1-1 E1/2: 172.17.12.1/31 and Spine_1-2 E1/1: 172.17.12.0/31.<br />
<p align="left">Full IP address allocation for the scheme is displayed in the table below.<br />
<br />
<img width="729" alt="Clos_Scheme" src="https://user-images.githubusercontent.com/39993377/117587840-8bf79980-b128-11eb-96c9-f2199b558861.png">
