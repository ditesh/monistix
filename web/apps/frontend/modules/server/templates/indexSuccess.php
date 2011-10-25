<?php slot(
  'title',
  sprintf('Monistix - Servers'))
?>

<?php if (isset($group)): ?>
<h1 class="left"><?php echo $group->getName() ?></h1>
<?php else: ?>
<h1 class="left">All Servers</h1>
<?php endif ?>
<div class="right">
	<a class="button" href="<?php echo url_for('server/new') ?>">New</a>
</div>
<table>
  <thead>
    <tr>
      <th>Hostname</th>
      <th>Group</th>
      <th>Enabled</th>
      <th class="right">Actions</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($servers as $server): ?>
    <tr>
      <td><a href="<?php echo url_for('server/show?id='.$server->getId()) ?>"><?php echo $server->getHostname() ?></a></td>
      <td><?php echo $server->getServerGroup()->getName() ?></td>
      <td><?php echo $server->getEnabled() ? "Yes" : "No" ?></td>
      <td class="right">
	<a href="" class="minibutton">Reports</a>
	<a href="" class="minibutton">Notifications</a>
	<a href="<?php echo url_for('server/edit?id='.$server->getId()) ?>" class="minibutton">Edit</a>
      </td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
