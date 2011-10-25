<?php slot(
  'title',
  sprintf('Monistix - Server Groups'))
?>

<h1 style="float: left">Server Groups</h1>
<div style="float: right">
	<a class="button" href="<?php echo url_for('servergroup/new') ?>">New</a>
</div>

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Enabled</th>
      <th># servers</th>
      <th class="right">Actions</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($server_groups as $server_group): ?>
    <tr>
      <td><a href="<?php echo url_for('servergroup/show?id='.$server_group->getId()) ?>"><?php echo $server_group->getName() ?></a></td>
      <td><?php echo $server_group->getEnabled() ? "Yes" : "No" ?></td>
      <td><?php echo 10 ?></td>
      <td class="right">
	<a href="" class="minibutton">Reports</a>
	<a href="" class="minibutton">Plugins</a>
	<a href="<?php echo url_for('servergroup/edit?id='.$server_group->getId()) ?>" class="minibutton">Edit</a>
      </td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>

