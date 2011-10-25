<table>
  <tbody>
    <tr>
      <th>Id:</th>
      <td><?php echo $server_group->getId() ?></td>
    </tr>
    <tr>
      <th>Name:</th>
      <td><?php echo $server_group->getName() ?></td>
    </tr>
    <tr>
      <th>Enabled:</th>
      <td><?php echo $server_group->getEnabled() ?></td>
    </tr>
    <tr>
      <th>Created at:</th>
      <td><?php echo $server_group->getCreatedAt() ?></td>
    </tr>
    <tr>
      <th>Updated at:</th>
      <td><?php echo $server_group->getUpdatedAt() ?></td>
    </tr>
  </tbody>
</table>

<hr />

<a href="<?php echo url_for('servergroup/edit?id='.$server_group->getId()) ?>">Edit</a>
&nbsp;
<a href="<?php echo url_for('servergroup/index') ?>">List</a>
