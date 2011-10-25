<?php slot(
  'title',
  sprintf('Monistix - Plugins'))
?>

<?php if (isset($plugin)): ?>
<h1 class="left"><?php echo $plugin->getName() ?></h1>
<?php else: ?>
<h1 class="left">All Plugins</h1>
<?php endif ?>
<div class="right">
	<a class="button" href="<?php echo url_for('plugin/new') ?>">New</a>
</div>
<table>
  <thead>
    <tr>
      <th>Plugin</th>
      <th>Enabled</th>
      <th class="right">Actions</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($plugins as $plugin): ?>
    <tr>
      <td><a href="<?php echo url_for('plugin/show?id='.$server->getId()) ?>"><?php echo $plugin->getName() ?></a></td>
      <td><?php echo $server->getEnabled() ? "Yes" : "No" ?></td>
      <td class="right">
	<a href="" class="minibutton">Reports</a>
	<a href="<?php echo url_for('plugin/edit?id='.$plugin->getId()) ?>" class="minibutton">Edit</a>
      </td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
