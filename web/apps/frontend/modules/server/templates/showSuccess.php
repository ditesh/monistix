<table>
  <tbody>
    <tr>
      <th>Id:</th>
      <td><?php echo $server->getId() ?></td>
    </tr>
    <tr>
      <th>Hostname:</th>
      <td><?php echo $server->getHostname() ?></td>
    </tr>
    <tr>
      <th>Group:</th>
      <td><?php echo $server->getGroupId() ?></td>
    </tr>
    <tr>
      <th>Enabled:</th>
      <td><?php echo $server->getEnabled() ?></td>
    </tr>
    <tr>
      <th>Created at:</th>
      <td><?php echo $server->getCreatedAt() ?></td>
    </tr>
    <tr>
      <th>Updated at:</th>
      <td><?php echo $server->getUpdatedAt() ?></td>
    </tr>
  </tbody>
</table>

<hr />

<a href="<?php echo url_for('server/edit?id='.$server->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('server/index') ?>">List</a>
