<div>
  <h1>Server Groups</h1>
    <div>

	<?php if (isset($groupID)): ?>
	<div class="category" id="category-0">
	<?php else: ?>
	<div class="category selected" id="category-0">
	<?php endif ?>
		<?php echo link_to("All servers", 'server/index') ?>
	</div>

	<?php foreach($groups as $group): ?>
	<?php if ($group->getId() == $sf_request->getParameter("group")): ?>
	<div class="category selected" id="category-<?php echo $group->getId() ?>"><?php echo link_to($group->getName(),'server/index?group='.$group->getId()) ?></div>
	<?php else: ?>
	<div class="category" id="category-<?php echo $group->getId() ?>"><?php echo link_to($group->getName(),'server/index?group='.$group->getId()) ?></div>
	<?php endif ?>
	<?php if ($group->getId() == $sf_request->getParameter("id")): ?>
		<div class="category-contents" style="display: block" id="category-contents-<?php echo $group->getId() ?>">
	<?php else: ?>
		<div class="category-contents" id="category-contents-<?php echo $group->getId() ?>">
	<?php endif ?>
		<ul>
			<?php foreach($group->getServers() as $server): ?>
			<li class="category-contents-item">
				<?php echo $server->getHostname() ?>
				<div class="right">
					<a class="button" href="/frontend_dev.php/server/new">Edit</a>
				</div>
			</li>
			<?php endforeach ?>
		</ul>
	</div>
	<?php endforeach ?>
    <div>
</div>
<script>
	$("[id*=category-]").click(function(event) {

		var id = event.target.id.split('-');
		id = id[id.length-1];

		if ($("#category-contents-"+id).is(":visible"))
			$("#category-contents-"+id).slideUp();
		else
			$("#category-contents-"+id).slideDown();
		

	});
</script>
