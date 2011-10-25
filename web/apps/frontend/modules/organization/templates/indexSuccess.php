<?php slot(
  'title',
  sprintf('Monistix - Organizations'))
?>

<h1 style="float: left">Organizations</h1>
<div style="float: right">
	<a class="button" href="<?php echo url_for('organization/new') ?>">New</a>
</div>

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Enabled</th>
      <th class="right">Actions</th>
    </tr>
  </thead>
  <tbody>
    <?php foreach ($organizations as $organization): ?>
    <tr>
      <td><a href="<?php echo url_for('organization/show?id='.$organization->getId()) ?>"><?php echo $organization->getName() ?></a></td>
      <td><?php echo $organization->getEnabled() ? "Yes" : "No" ?></td>
      <td class="right">
	<a href="" class="minibutton">Reports</a>
	<a href="" class="minibutton">Plugins</a>
	<a href="<?php echo url_for('organization/edit?id='.$organization->getId()) ?>" class="minibutton">Edit</a>
      </td>
    </tr>
    <?php endforeach; ?>
  </tbody>
</table>
